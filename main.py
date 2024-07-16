from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic import BaseModel
from typing import Dict
from fastapi.responses import JSONResponse
import uvicorn
import os
from dotenv import load_dotenv

from agente import agent


load_dotenv()

app = FastAPI()

API_KEY_AUTH = os.getenv('API_KEY_AUTH')

if API_KEY_AUTH is None:
    raise Exception("API_KEY_AUTH not configured in .env file")

def get_api_key(api_key_auth: str = Header(...)):
    if api_key_auth != API_KEY_AUTH:
        raise HTTPException(status_code=403, detail="Unauthorized")
    return api_key_auth

# EndPoint Linkedin
class RequestDataLk(BaseModel):
    id_user: str
    sms_user: str

@app.post("/chatboot")
async def analizar_linkedin(request_data: RequestDataLk, api_key_auth: str = Depends(get_api_key)):
    try:
        id_user = request_data.id_user
        sms_user = request_data.sms_user

        sms_asistant = agent(id_user, sms_user)

        return JSONResponse(content={"sms_asistant": sms_asistant}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

#uvicorn main:app --reload