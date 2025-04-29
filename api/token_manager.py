import os
import sys
import pytz
import json
import requests
from datetime import datetime, timedelta
from cryptography.fernet import Fernet

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import ENCRYPTION_KEY, appIdHash, pin


# ENCRYPTION_KEY = '5bKQxqN9tRQfRf7QmBC9uQn8HkGHw-1YJ44N3lq5p8k='
# appIdHash = '0ee126cab551557e28a3af3749e2611079f5d982c545d88a1b8f7d879ece15b8'
# pin = '5248'

# fernet = Fernet(ENCRYPTION_KEY.encode())
# TOKEN_FILE = "api/token_data.json"

# IST = pytz.timezone("Asia/Kolkata")

class TokenManager:
    def __init__(self):
        self.fernet = Fernet(ENCRYPTION_KEY.encode())
        self.TOKEN_FILE = "api/token_data.json"

        self.IST = pytz.timezone("Asia/Kolkata")

    def get_next_6am(self, now):
        today_6am = now.replace(hour=6, minute=0, second=0, microsecond=0)
        return today_6am if now < today_6am else today_6am + timedelta(days=1)

    
    def save_token(self, data: dict):
        
        now = datetime.now(self.IST)

        access_expiry = self.get_next_6am(now)
        refresh_expiry = access_expiry + timedelta(days=14)

        data['access_token_expiry'] = access_expiry.isoformat()
        data['refresh_token_expiry'] = refresh_expiry.isoformat()

        encrypted = self.fernet.encrypt(json.dumps(data).encode())
        with open(self.TOKEN_FILE, 'wb') as file:
            file.write(encrypted)
            print("File created successfully")

    
    def load_token_data(self):
        with open(self.TOKEN_FILE, 'rb') as file:
            encrypted = file.read()

        decrypted_data = self.fernet.decrypt(encrypted).decode()

        return json.loads(decrypted_data)
    
    
    def isExpired(self, token='refresh_token_expiry'):
        
        data = self.load_token_data()

        token_expiry = datetime.fromisoformat(data[token])
        now = datetime.now(self.IST)
        
        # print(f'Checking expiry for {token}: {data[token]} - {now < token_expiry}')
        return now > token_expiry
        
    
    def activate_refresh_token(self, refresh_token):
        headers = {'Content-Type': 'application/json'}

        json_data = {
            'grant_type': 'refresh_token',
            'appIdHash': appIdHash,
            'refresh_token': refresh_token,
            'pin': pin
        }

        try:
            response = requests.post('https://api-t1.fyers.in/api/v3/validate-refresh-token', headers=headers, json=json_data)
            if response.json()['code'] != 200:
                raise Exception
            
            access_token = response.json()['access_token']

            data = self.load_token_data()
            data['access_token'] = access_token

            self.save_token(data)

            return access_token

        except Exception as e:
            print(e)
            return False
    

    def get_access_token(self):
        
        data = self.load_token_data()

        if not self.isExpired('access_token_expiry'):
            print(f"Access token not expired. Expiry Date: {data['access_token_expiry']}")
            # print(data)
            return data['access_token']
        
        if not self.isExpired():
            print(f"Refresh token not expired. Expiry Date: {data['refresh_token_expiry']}")
            return self.activate_refresh_token(data['refresh_token'])
        
        print('Both the access token and refresh token are expired. Please initiate new tokens!!')
        if os.path.exists('token_data.json'):
            os.remove('token_data.json')

        return False
        

    

if __name__ == '__main__':
    print(ENCRYPTION_KEY, appIdHash, pin)

