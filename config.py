# Update credentials here! This data should match with the data provided while creating Fyers App.

from dotenv import dotenv_values



config = dotenv_values(".env")

redirect_uri= config['redirect_uri']
client_id = config['client_id'] 
secret_key = config['secret_key']  
grant_type = config['grant_type']                 
response_type = config['response_type']                             
state = config['state']
ENCRYPTION_KEY = config['ENCRYPTION_KEY']
appIdHash = config['appIdHash']
pin = config['pin']

