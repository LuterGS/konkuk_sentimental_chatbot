from pydantic import BaseModel


class Message(BaseModel):
    userInput: str
