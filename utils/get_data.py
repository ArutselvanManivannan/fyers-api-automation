import time
from .indicators import *

indicators = Indicators()

# class GetData:

def get_daily_data(fd, stock, from_month, to_month, from_date, to_date):

    inside_cam = False
    inside_cpr = False
    inside_mza = False

    data = fd.get_historical_data(stock, 'D', f'2025-{from_month}-{from_date}', f'2025-{to_month}-{to_date}')
    data_5m = fd.get_historical_data(stock, '5', f'2025-{from_month}-{from_date}', f'2025-{to_month}-{to_date}')

    day1_5m = data_5m['candles'][:75]
    day2_5m = data_5m['candles'][75:]
    

    day1, day2 = data['candles'][0], data['candles'][1]
    day1_high, day2_high = day1[2], day2[2]
    day1_low, day2_low = day1[3], day2[3]
    day1_close, day2_close = day1[4], day2[4]

    day1_val, day1_vah, day1_poc = indicators.get_value_areas(day1_5m, day1_high, day1_low)
    day2_val, day2_vah, day2_poc = indicators.get_value_areas(day2_5m, day2_high, day2_low)

    day1_cam_h3, day1_cam_h4, day1_cam_l3, day1_cam_l4, day1_cam_width = indicators.get_Cam_Pivots(day1_high, day1_low, day1_close)
    day2_cam_h3, day2_cam_h4, day2_cam_l3, day2_cam_l4, day2_cam_width = indicators.get_Cam_Pivots(day2_high, day2_low, day2_close)

    day1_cpr_pivot, day1_cpr_top, day1_cpr_bottom, day1_width = indicators.get_CPR_pivots(day1_high, day1_low, day1_close)
    day2_cpr_pivot, day2_cpr_top, day2_cpr_bottom, day2_width = indicators.get_CPR_pivots(day2_high, day2_low, day2_close)

    if day1_cam_h3>day2_cam_h3>day1_cam_l3 and day1_cam_h3>day2_cam_l3>day1_cam_l3:
        print(f'{stock} - Inside Camarilla trending!')
        inside_cam = True

    if day1_cpr_top > day2_cpr_top and day1_cpr_bottom<day2_cpr_bottom:
        print(f'{stock} - Inside CPR Trending')
        inside_cpr = True

    if day1_vah > day2_vah and day1_val<day2_val:
        print(f'{stock} - Inside MoneyZone Trending')
        # print(day1_val, day1_vah, day1_poc)
        # print(day2_val, day2_vah, day2_poc)

        inside_mza = True

    # print(day)

    return inside_cam, inside_cpr, inside_mza