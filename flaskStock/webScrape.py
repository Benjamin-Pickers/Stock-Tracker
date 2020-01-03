from bs4 import BeautifulSoup
import requests
import pandas as pd


class stockScraper:

    def __init__(self, symbol):
        self.symbol = symbol.upper()

    def get_info(self):
        df = pd.read_excel (r'C:\Users\Ben Pickers\Documents\StockScraper\flaskStock\symbols.xlsx')
        ticker_Column = df['Ticker']
        is_valid = False

        for i in ticker_Column:
            if (i == self.symbol):
                is_valid =True

        if(is_valid):
            url = 'https://web.tmxmoney.com/quote.php?qm_symbol=' + self.symbol
            src = requests.get(url).text
            s = BeautifulSoup(src, 'lxml')
            price = s.find('span', class_="price").find('span', recursive = False).text
            c = s.find('div', class_="col-5 col-md-6").find('strong')
            change = '  '.join(c.text.split())
            info_list = [str(self.symbol), str(price), str(change)]
            return info_list
        else:
            info_list = ['0', '0', '0']
            return info_list
