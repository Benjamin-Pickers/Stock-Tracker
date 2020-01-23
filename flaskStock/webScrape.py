from bs4 import BeautifulSoup
import requests
import os
import sys
import pandas as pd


class stockScraper:

    def __init__(self, symbol):
        self.symbol = symbol.upper()

    def get_info(self):
        #loads in excel spreadsheet, that has all tsx stocks information stored in it, as a dataframe
        df = pd.read_excel (os.path.join(sys.path[0], "flaskStock\symbols.xlsx"))
        #Grabs the ticker column from the spreadsheet
        ticker_Column = df['Ticker']
        is_valid = False

        #Check to see if the stock ticker given is a valid tsx stock by comparing it with the spreadsheet
        for i in ticker_Column:
            if (i == self.symbol):
                is_valid =True

        if(is_valid):
            #Website that we will scrape from
            url = 'https://web.tmxmoney.com/quote.php?qm_symbol=' + self.symbol
            src = requests.get(url).text
            s = BeautifulSoup(src, 'lxml')
            #Find the span element with class price, it should hold the price of the stock, if not it'll return None Type
            test = s.find('span', class_="price")
            #If we do find a price, then grab the rest of the information needed and store it into an array and return that array
            if test:
                price = s.find('span', class_="price").find('span', recursive = False).text
                c = s.find('div', class_="col-5 col-md-6").find('strong')
                change = '  '.join(c.text.split())
                info_list = [str(self.symbol), str(price), str(change)]
            else:
                #No price was found so return all zeros, to indicate that the information was not a valid tsx stock
                info_list = ['0', '0', '0']
            return info_list
        else:
            info_list = ['0', '0', '0']
            return info_list
