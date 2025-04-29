import os
import sys
import time
import webbrowser
from fyers_apiv3 import fyersModel
from .token_manager import TokenManager
from .callback_server import start_callback_server

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import redirect_uri,client_id, secret_key, grant_type, response_type, state


def generateAuthCode(tk_mgn, appSession):
    
    generateTokenUrl = appSession.generate_authcode()
    # print((generateTokenUrl))
    webbrowser.open(generateTokenUrl, new=1)

    auth_code = start_callback_server()

    # print(f'Auth Code received: {auth_code}')

    # Send this auth_code to saveToken
    appSession.set_token(auth_code)
    response = appSession.generate_token()

    try:
        if response['code'] == 200:
            tk_mgn.save_token(response)
            time.sleep(3)

            access_token = tk_mgn.get_access_token()
            return access_token
        else:
            raise Exception

    except Exception as e:
        print(e, response)
        return False



def initiate_auth():

    tk_mgn = TokenManager()
    appSession = fyersModel.SessionModel(client_id=client_id, redirect_uri=redirect_uri, response_type=response_type, state=state, secret_key=secret_key, grant_type=grant_type)

    
    if not os.path.exists('api/token_data.json'):
        print("No tokens found, generating token url ...")
        access_token = generateAuthCode(tk_mgn, appSession)

    else:
        print("Token file found, retrieving access token ...")
        access_token = tk_mgn.get_access_token()


    if not access_token:
        print("couldn't get access token.")


    fyers = fyersModel.FyersModel(client_id=client_id, is_async=False, token=access_token, log_path="")

    return fyers, access_token

