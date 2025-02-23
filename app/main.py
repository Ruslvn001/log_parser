from fastapi import FastAPI, Request, Depends, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from .models import Message, Log
from .database import SessionLocal, engine, Base
from .log_processor import process_log_file

Base.metadata.create_all(bind=engine)

app = FastAPI()

templates = Jinja2Templates(directory="app/templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    print(request.body)
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/search")
async def search_logs(request: Request, address: str = Form(...), db: Session = Depends(get_db)):
    logs = db.query(Log).filter(Log.address == address).order_by(Log.int_id, Log.created).limit(100).all()
    messages = db.query(Message).filter(Message.str.contains(address)).order_by(Message.int_id, Message.created).limit(100).all()
    results = logs + messages
    return templates.TemplateResponse("index.html", {"request": request, "results": results})

@app.on_event("startup")
async def startup():
    db = SessionLocal()
    try:
        process_log_file(db, "out.log")
    finally:
        db.close()
