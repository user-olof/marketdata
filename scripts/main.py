
from app.database import mongodb

def main():
    print('CSV file to read from: ')
    file = input()
    mongodb.load_all_new_csv(file)

if __name__ == '__main__':
    main()