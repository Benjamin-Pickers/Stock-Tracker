# Stock-Tracker

  This was a project that originally started with a webscraper that grabs stock prices.
Using beautifulSoup4, I wrote a python script that would go to [TMXmoney.com](https://www.tmxmoney.com/en/index.html)
and grab the stock price and daily change. To display this information, I created a basic web application that uses the
micro web frame work, flask and can be found at [flaskstock.ca](https://www.flaskstock.ca/). Flask will handle all requests
for stocks and allows users to create their own accounts to track their own list of stocks. I decided to omit having passwords for
accounts and instead just use usernames to login, as there is no private information stored in accounts and I felt it would be easier to
just sign in with a username. Since not everyone would want to make an account to try out the program, I created a default
account that uses that username "default", that can be used by anyone.

  Once you login to your account, you can add a stock to your list, remove a stock thats already there or refresh the prices
all the stocks you are tracking. The application gets the data from TMXmoney.com, so all queries will be using their formatting.
That is TSX and TSXV stocks can be found using their normal ticker, and NYSE and NASDAQ stocks can be found using the format
<ticker>:us. For example, to find Apple's stock you would search for AAPL:US.

The front-end of the application is quite basic and simple. Just regular html5 and css with bootstrap to make the page responsive.
Since we are using bootstrap, the page does work on mobile devices, but some minor tweaks are needed.
