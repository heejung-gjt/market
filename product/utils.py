
# product sale percentage function
def calculate_price(origin_price, sale_price):
  try:
    price = sale_price
    price_gap = int(origin_price) - int(price)
    real_sale = int(price_gap)/int(origin_price)*100
    discount_rate = round(real_sale, 1)
    return discount_rate
  except:
    discount_rate = -1
    return discount_rate

