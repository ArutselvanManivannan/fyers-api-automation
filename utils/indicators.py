from collections import defaultdict


class Indicators:

    # CPR Pivots
    def get_CPR_pivots(self, high, low, close):

        pivot = (high + low + close) / 3
        bottom_cpr = (high + low) / 2
        top_cpr = (pivot - bottom_cpr) + pivot
        # print(self.top_cpr, self.bottom_cpr)

        if bottom_cpr > top_cpr:
            top_cpr, bottom_cpr = bottom_cpr, top_cpr

        WidthPts = max(top_cpr, bottom_cpr) - pivot
        width = (WidthPts / close) * 100


        return pivot, top_cpr, bottom_cpr, width
    

    #Camarilla Pivots
    def get_Cam_Pivots(self, high, low, close):

        h3 = close + (high - low) * 1.1/4
        h4 = close + (high - low) * 1.1/2

        l3 = close - (high - low) * 1.1/4
        l4 = close - (high - low) * 1.1/2

        width = ((h4 - h3)/close) * 100

        return h3, h4, l3, l4, width


    # MarketProfile:
    def get_value_areas(self, candles, day_high, day_low, tick_size=0.05):
        price_tpo_count = defaultdict(int)
        total_tpos = 0
        tolerance = 0.001

        for candle in candles:
            high = candle[2]
            low = candle[3]

            if high == low:
                price_levels = [round(low, 2)]
            else:
                price_levels = [round(low + i * tick_size, 2) for i in range(int((high - low) / tick_size) + 1)]

            for price in price_levels:
                price_tpo_count[price] += 1
            
            total_tpos += len(price_levels)

        # Find POC
        poc = max(price_tpo_count, key=lambda x: price_tpo_count[x])

        # Sort price levels by TPO count descending
        sorted_prices = sorted(price_tpo_count.items(), key=lambda x: x[1], reverse=True)

        value_area_tpos = 0
        value_area_prices = []

        for price, count in sorted_prices:
            value_area_tpos += count
            value_area_prices.append(price)
            if value_area_tpos >= 0.7 * total_tpos:
                break

        vah = max(value_area_prices)
        val = min(value_area_prices)

        if abs(vah - day_high) <= tolerance * day_high:
            vah = day_high
        if abs(val - day_low) <= tolerance * day_low:
            val = day_low

        return round(val, 2), round(vah, 2), round(poc, 2)
