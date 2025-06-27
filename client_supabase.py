import os
from supabase import create_client, Client
from dotenv import load_dotenv
from supabase.lib.client_options import SyncClientOptions
import requests

load_dotenv()
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

client = create_client(url, key)

def fetch_records():
    try:
        headers = {
            "apikey": key,
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json"
        }
        # Filter for records where email is null
        params = {
            "email": "is.null",
            "limit": 1
        }
        response = requests.get(
            f"{url}/rest/v1/user_details",
            headers=headers,
            params=params
        )
        response.raise_for_status()
        data = response.json()
        return data
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
    

def update_record(record):
    try:
        headers = {
            "apikey": key,
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json"
        }
        # Filter for records where email is null
        params = {
            "email": f"{record['email']}",
            "updated_by": "system"
        }
        response = requests.patch(
            f"{url}/rest/v1/user_details?cust_id=eq.{record['cust_id']}",
            headers=headers,
            json=params
        )
        response.raise_for_status()
        data = response.json()
        return data
    except Exception as e:
        print(f"An error occurred: {e}")
        return None