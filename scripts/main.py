
from app.database import mongodb


def main():
    print('Start.. ')
    path = input("Path: ")
    # mongodb.load_market_data_csv(file)
    mongodb.load_all_new_csv(path)
    # stock_price_return = mongodb.stock_price_return("ALFA-2002-05-17-2024-04-30.csv")
    # print("Stock price return is {:.0%}".format(stock_price_return))

    # mongodb.drop_all_market_data_collections()
    print("Finished!")

if __name__ == '__main__':
    main()