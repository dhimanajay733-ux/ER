from fastapi import FastAPI
from src.schemas.user_schema import UserCreate
from src.core.config import settings
from src.routers.user_routes import router


app=FastAPI()
app.include_router(router)
@app.get('/Info')
def fun():
    return('This is a True Statement')

@app.post('/User')
def User(user:UserCreate):
    return 'Successfully created'           
            

