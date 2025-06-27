from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import PlainTextResponse
import json
import logging
from dotenv import load_dotenv
from pydantic import BaseModel
import os
import requests
from client_supabase import fetch_records, update_record


app = FastAPI()
load_dotenv()

base_url = os.getenv("BASE_URL", "http://localhost:8000")

@app.get("/initiate")
def call_api():
    url = f"{base_url}/initiate-call"

    user_records = fetch_records()
    phoneNumber = user_records[0]['phnumber'] if user_records else None
    print(f"Phone number fetched: {phoneNumber}")
    payload = json.dumps({
        "customer_phone": f"{phoneNumber}"
    })

    try:
        response = requests.post(url, data=payload, headers={"Content-Type": "application/json"},verify="C:\\Users\\sdubey\\Downloads\\genaiplatform.ajbpoc.co.uk.crt")
        response.raise_for_status()
        return response.json()
        print("END")
    except requests.RequestException as e:
        logging.error(f"Error calling API: {e}")
        return PlainTextResponse("Error calling API", status_code=500)
    
class Record(BaseModel):
    cust_id: int
    phnumber: str
    email: str = None


@app.put("/update-record")
def update_api(record: Record):
    try:
        updated_record = update_record(record.dict())
        if updated_record: 
            return PlainTextResponse("Record updated successfully", status_code=200)
    except requests.RequestException as e:
        logging.error(f"Error updating record: {e}")
        return PlainTextResponse("Error updating record", status_code=500)