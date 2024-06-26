from app.database import mongo_manager

def main():
    print('Start.. ')
    file = input("File: ")
    mongo_manager.load_market_data_csv(file)
    print("Finished!")

if __name__ == '__main__':
    main()