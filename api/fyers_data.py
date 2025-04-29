# This file contains the list of functions we can execute once we have valid access_token
# Add functions here to get fyers data

class Fyers_Data:

    def __init__(self, fyers_model):
        self.fyers_model = fyers_model

    def get_profile(self):

        response = self.fyers_model.get_profile()

        return response if response['code'] == 200 else False


    def get_historical_data(self, symbol, resolution, range_from, range_to):

        payload = {
            'symbol': f'NSE:{symbol}-EQ',
            'resolution': resolution,
            'date_format': '1',
            'range_from': range_from,
            'range_to': range_to,
            'cont_flag': '1'
        }

        response = self.fyers_model.history(data=payload)
 
        return response if response['code'] == 200 else False


    def logout(self):

        response = self.fyers_model.logout()

        return response if response['code'] == 200 else False



# if __name__ == '__main':
#     fd = Fyers_Data(fyers_model=fyers)