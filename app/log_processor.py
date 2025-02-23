from sqlalchemy.orm import Session
from .services import parse_log_line, save_message_entry, save_log_entry

def process_log_file(db: Session, log_file_path: str):
    with open(log_file_path) as file:
        for line in file:
            created, int_id, flag, address, str_content = parse_log_line(line)
            if flag == "<=":
                try:
                    id = str_content.split("id=")[1].split()[0]
                except IndexError:
                    id = int_id
                save_message_entry(db, created, id, int_id, str_content)
            else:
                save_log_entry(db, created, int_id, str_content, address)
