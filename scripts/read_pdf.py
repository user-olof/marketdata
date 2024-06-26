from app.pdf.reader import reader, number_of_pages
from dotenv import load_dotenv

load_dotenv()




def main():
    print("Start")
    #convert the pdf to XML
    # pdf.tree.write('/home/olof/data/marketdata/xml/ABB-2023-Q1.xml', pretty_print = True)
    print(number_of_pages)
    print("Finished!")

if __name__ == "__main__":
    main()