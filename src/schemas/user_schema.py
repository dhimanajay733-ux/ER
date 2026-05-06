from pydantic import BaseModel

class userInput(BaseModel):
    username=str
    email=str
    password=str
    
    