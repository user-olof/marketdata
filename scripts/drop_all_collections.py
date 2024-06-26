from app.database import mongo_manager


def main():
    print("Start...")
    mongo_manager.drop_all_market_data_collections()
    print("Finished!")


if __name__ == "__main__":
    main()


