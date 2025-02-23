from sqlalchemy.orm import Session
from .models import Message, Log


def get_mail(parts):
    for part in parts[4:]:
        if '@' in part:
            address = part
            if address[0] == '<':
                return address[1:-1]
            elif address[-1] == ':':
                return address[:-1]
            else:
                return address

def get_message_info(parts):
    created = f"{parts[0]} {parts[1]}"
    int_id = parts[2]
    flag = parts[3]
    address = get_mail(parts)
    return created, int_id, flag, address

def parse_log_line(line: str):
    parts = line.split()
    created, int_id, flag, address = get_message_info(parts)
    str_content = ' '.join(parts[4:]) if len(parts) > 4 else ' '.join(parts[3:])
    return created, int_id, flag, address, str_content

def save_log_entry(db: Session, created: str, int_id: str, str_content: str, address: str):
    db_log = Log(created=created, int_id=int_id, str=str_content, address=address)
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

def save_message_entry(db: Session, created: str, id: str, int_id: str, str_content: str):
    db_message = Message(created=created, id=id, int_id=int_id, str=str_content)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def get_logs_by_address(db: Session, address: str, limit: int = 100):
    logs = db.query(Log).filter(Log.address == address).order_by(Log.int_id, Log.created).limit(limit).all()
    messages = db.query(Message).filter(Message.str.contains(address)).order_by(Message.int_id, Message.created).limit(
        limit).all()
    return logs + messages
