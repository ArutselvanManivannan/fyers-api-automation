from api.fyers_auth import *
from api.fyers_data import Fyers_Data

from utils.indicators import *
from utils.get_data import *

from_date, to_date = '30', '02' #Hardcode dates
from_month, to_month = '04', '05' #Hardcode month(s)

fyers, access_token = initiate_auth()

fd = Fyers_Data(fyers)
indicators = Indicators()

if not access_token:
    exit()

with open('utils/Nifty50Stocks.txt') as file:
    inside_cam_list = []
    inside_cpr_list = []
    inside_mza_list = []

    file_contents = file.readlines()
    for line in file_contents:
        stock = line.split()[0]

        inside_cam, inside_cpr, inside_mza = get_daily_data(fd, stock, from_month, to_month, from_date, to_date)

        if inside_cam: inside_cam_list.append(stock)
        if inside_cpr: inside_cpr_list.append(stock)
        if inside_mza: inside_mza_list.append(stock)

        time.sleep(0.5)


# print(f"Inside Cam Stocks: {inside_cam_list}")
# print(f"Inside CPR Stocks: {inside_cpr_list}")
# print(f"Inside Money zone area Stocks: {inside_mza_list}")

#Appended only cam and cpr pivot stocks, add mza stocks if needed.
nifty_trending = [*inside_cam_list, *inside_cpr_list]

with open('Output/NiftyTrending_Watchlist.txt', 'w') as file:
    file.write('\n'.join(nifty_trending))
    print('File created successfully! Check Output folder for the watchlist stocks')