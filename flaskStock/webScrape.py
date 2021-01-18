from bs4 import BeautifulSoup
import requests
from requests_html import AsyncHTMLSession
import asyncio
import pyppdf.patch_pyppeteer
import pyppeteer
import os
import sys
import pandas as pd


class stockScraper:

    def __init__(self, symbol):
        self.symbol = symbol.upper()

    #Work around to render the javascript of the page
    async def get_site(self):
        new_loop=asyncio.new_event_loop()
        asyncio.set_event_loop(new_loop)
        session = AsyncHTMLSession()
        browser = await pyppeteer.launch({
            'ignoreHTTPSErrors':True,
            'headless':True,
            'handleSIGINT':False,
            'handleSIGTERM':False,
            'handleSIGHUP':False
        })
        session._browser = browser
        url = 'https://money.tmx.com/en/quote/' + self.symbol
        resp_page = await session.get(url)
        await resp_page.html.arender()
        return resp_page


    def get_info(self):

        #Create a loop and then request the page
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        src = loop.run_until_complete(self.get_site())

        if(src):
            #Give the source to BeautifulSoup
            s = BeautifulSoup(src.html.raw_html, 'lxml')

            #Find the first two span elements in main, they hold the price and change, if not it'll empty list
            price = s.find('body').find('div', id='root').find('div', id="main").find_all('span', limit=2)
            #If the list isn't empty then return our values
            if price:
                print(price)
                info_list = [str(self.symbol), str(price[0].text), str(price[1].text)]
            else:
                #No price was found so return all zeros, to indicate that the information was not a valid tsx stock
                info_list = ['0', '0', '0']
            return info_list
        else:
            info_list = ['0', '0', '0']
            return info_list
