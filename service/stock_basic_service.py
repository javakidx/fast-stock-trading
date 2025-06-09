from typing import List

import requests
from bs4 import BeautifulSoup

from enums import IssueType
from models import Stock
from repository import database, stock_collection

def get_stock(symbol: str):
    return stock_collection.find(symbol)

def init_stock_basics():
    database.drop_collection("stocks")
    stocks = gather_stock_data(IssueType.TWSE)
    database.insert_many("stocks", stocks)

def gather_stock_data(issue_type: IssueType) -> List[Stock]:
    url = f"https://isin.twse.com.tw/isin/class_main.jsp?market=1&issuetype={issue_type.value}"
    req = requests.get(url, verify=False)
    html = req.text

    soup = BeautifulSoup(html)
    stocks: List[Stock] = []
    rows = soup.find_all("tr")

    for i in range(1, len(rows)):
        tds = rows[i].find_all("td")
        symbol = tds[2].text
        name = tds[3].text
        market_type = tds[4].text #市場別
        industry = tds[6].text  # 產業別

        stock = Stock(
            symbol=symbol,
            name=name,
            market_type=market_type,
            industry=industry,
            issue_date=tds[7].text,
        )
        stocks.append(stock)

    return stocks


