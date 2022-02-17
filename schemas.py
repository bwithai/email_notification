from pydantic import BaseModel


class SendingEmailSchema(BaseModel):
    title: str
    email: str
    message:str