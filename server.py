from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
import json
import logging
from dotenv import load_dotenv
from pydantic import BaseModel
import os
import requests
from client_supabase import fetch_records, update_record
import datetime as Datetime

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('transcription_test.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or replace * with specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


base_url = os.getenv("BASE_URL", "http://localhost:8000")
agent_url = os.getenv("AGENT_URL", "http://localhost:8000/agent")

@app.get("/initiate")
def call_api():
    url = f"{base_url}/initiate-call"

    user_records = fetch_records()
    phoneNumber = user_records[0]['phnumber'] if user_records else None
    
    try:
        #  send record to agent
        agent_payload = json.dumps({
                    "cust_id": user_records[0]['cust_id'],
                    "name": user_records[0]['name'],
                    "phnumber": user_records[0]['phnumber'],
                    "dob": user_records[0]['dob']
                    })
        response_agent = requests.post(f"{agent_url}/user-info", data=agent_payload, headers={"Content-Type": "application/json"})


        
        #  initiate call
        payload = json.dumps({
            "customer_phone": f"{phoneNumber}"
        })
        response = requests.post(url, data=payload, headers={"Content-Type": "application/json"})
        response.raise_for_status()
        return response.json()
        print("END")
    except requests.RequestException as e:
        logging.error(f"Error calling API: {e}")
        return PlainTextResponse("Error calling API", status_code=500)
    
class Record(BaseModel):
    cust_id: int
    name : str
    phnumber: str
    dob : Datetime.datetime
    email: str
    


@app.put("/update-record")
def update_api(record: Record):
    try:
        updated_record = update_record(record.dict())
        if updated_record: 
            return PlainTextResponse("Record updated successfully", status_code=200)
    except requests.RequestException as e:
        logging.error(f"Error updating record: {e}")
        return PlainTextResponse("Error updating record", status_code=500)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8080)