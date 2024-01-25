import gspread
from gspread import Spreadsheet

class SheetsTransition:
    def __init__(self, key_path, url_path):
        self.key_path = key_path
        self.url_path = url_path
        self.column_to_read = None
        self.column_to_modify = None

    def getSheetData(self):
        gc = gspread.service_account(self.key_path)
        sh: Spreadsheet = gc.open_by_url(self.url_path)
        self.ws = sh.sheet1
        self.column_a_values = []
        self.column_a_values = self.ws.col_values(self.column_to_read)
        self.column_a_values = [value.lower() for value in self.column_a_values]

    def CheckSheetData(self, names: list):
        for i, value in enumerate(self.column_a_values, start=1):
            if value in names:
                cell_format = {"backgroundColor": {"red": 0, "green": 1, "blue": 0}}
                self.ws.format(f"{self.column_to_modify}{i}", cell_format)
            else:
                cell_format = {"backgroundColor": {"red": 1, "green": 0, "blue": 0}}
                self.ws.format(f"{self.column_to_modify}{i}", cell_format)

        print(self.column_a_values)