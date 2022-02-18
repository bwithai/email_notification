from fastapi import FastAPI, BackgroundTasks
from pydantic import ValidationError

from database import session
from models import EmailSchedule
from schemas import SendingEmailSchema
from send_email import send_email_background

app = FastAPI()


@app.get('/')
def index():
    return 'Wellcome to Home'


@app.get('/send-email/backgroundtasks')
def send_email_backgroundtasks(background_tasks: BackgroundTasks):
    emails: EmailSchedule = session.query(EmailSchedule).all()
    for email in emails:
        try:
            send_email_background(background_tasks, email.title, email.email_to, email.message)
        except ValidationError as error:
            email.status = str(error)
            session.commit()
            return str(error)

        email.status = "Email send Successfully"
        session.commit()
        return {
            "message": "Email send Successfully"
        }


@app.post('/subscribe')
def send_email_queue(data: SendingEmailSchema):
    with session as db_session:
        new_entry = EmailSchedule(title=data.title, email_to=data.email, message=data.message, status="")
        db_session.add(new_entry)
        db_session.commit()
        return {
            "message": "Added successfully"
        }
