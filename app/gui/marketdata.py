import sys

from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QTableView, QMainWindow, QVBoxLayout, QHBoxLayout, QComboBox
from PyQt5.QtCore import Qt, QAbstractTableModel

from app.database import mongo_manager
import pandas as pd


class TableModel(QAbstractTableModel):
    def __init__(self, data) -> None:
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)
    
    def rowCount(self, index):
        # The length of the outer list.
        return self._data.shape[0]

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return self._data.shape[1]
    
    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return str(self._data.columns[section])


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        
        mainLayout = QVBoxLayout()
        menuLayout = QHBoxLayout()
        self.combobox = QComboBox()
        self.table = QTableView()

        collection_names = mongo_manager.get_all_market_data_collections()

        self.comboBoxUI(collection_names)
        self.tableUI(collection_names[0])

        menuLayout.addWidget(self.combobox)
        mainLayout.addLayout(menuLayout)
        mainLayout.addWidget(self.table)

        window = QWidget() 
        window.setLayout(mainLayout)
        self.setCentralWidget(window)
        self.setWindowTitle("MongoDB - marketdata")
        self.setGeometry(600, 600, 680, 600)
    
    def activated(self, index):
        collection_name = self.combobox.currentText()
        self.tableUI(collection_name)

    def comboBoxUI(self, collection_names: list[str]):
        collection_names.sort()
        self.combobox.addItems(collection_names)
        self.combobox.activated.connect(self.activated)

    def tableUI(self, collection_name: str):
        
        res = mongo_manager.get_all(collection_name)
        tmp = list(res)

        df = pd.DataFrame(tmp, columns=["_id", "Date", "Bid", "Ask", "Opening price", "High price", "Low price", "Closing price", "Average price", "Total volume", "Turnover", "Trades"])
        df["_id"] = df["_id"].astype(str)
        df["Total volume"] = df["Total volume"]
        df["Date"] = df["Date"].astype(str)

        model = TableModel(df)
        self.table.setModel(model)
        

def main():
    app = QApplication([])
    
    # Create your application's GUI
    window = MainWindow()

    # Show your application's GUI
    window.show()
    # Run your application's event loop
    sys.exit(app.exec())

if __name__ == '__main__':
    main()