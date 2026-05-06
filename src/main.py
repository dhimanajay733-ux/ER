from fastapi import FastAPI
from src.schemas.user_schema import userInput
app=FastAPI()
@app.get('/Info')
def fun():
    return('This is a True Statement')

@app.post('/User')
def User(user:userInput):
    return 'Successfully created'           
            

# except:
#     return {'message':'Unsuccessful'}
# # @app.post('/OTP')
# def OTP('/Enter_Otp'):
