
from app.database import mongo_manager


def main():
    print('Start.. ')
    path = input("Path: ")
    mongo_manager.load_all_new_csv(path)
    print("Finished!")

if __name__ == '__main__':
    main()