from pydantic import BaseModel, EmailStr

class GoogleUser(BaseModel):
    email : EmailStr
    name : str