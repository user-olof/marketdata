from app.database import mongo_manager, mongo_calculator as mc
from datetime import datetime


def main():
    print("Start")
    from_date = datetime(1999, 6, 22)
    to_date = datetime(2024, 4, 30)
    stock_price_return = mc.stock_price_return("ABB-1999-06-22-2024-04-30.csv", from_date, to_date)
    str_return = "{:.0%}".format(stock_price_return)
    print("Stock price return is " + str_return)
    td = mc.get_time_difference(from_date, to_date)
    print(f"In {td.years} years, {td.months} months and {td.days} days, the stock price return is {str_return}")
    annual_return = mc.annualized_stock_price_return(stock_price_return, from_date, to_date)
    str_annual_return = f"{annual_return:.2%}"
    print(f"Annual stock price return is {str_annual_return}")
    print("Finished!")

if __name__ == "__main__":
    main()


