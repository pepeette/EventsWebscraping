import requests
from bs4 import BeautifulSoup
import re
import csv
from time import sleep
from random import randint
import pandas as pd
import nbconvert
import typer

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
pages = ['', 'xbox-one', 'ps4', '3ds', 'pc', 'nintendo-switch']

class Process:

    def __init__(self):
        pass
    def run(self):
        pass
    
def search_event(pages, headers):
    event = []
    date = []

    for page in pages: 
        url = f"https://www.gamespot.com/gamespot-50/{page}"
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        titles = soup.find_all("h3")
        for t in titles:
            try:
                event.append(t.a.text.strip())
            except Exception:
                event.append('n/a')
        dates = soup.find_all(class_="media-release-date")
        for d in dates:
            date.append(d.findChild().text)
        sleep(randint(2,10))

    return event, date

        
def create_dataframe(event, date):
    pd.set_option('display.max_rows', 500)
    df = pd.DataFrame(list(zip(event,date)),
            columns =['event', 'date'])
    df = df.drop_duplicates(subset=['event'])
    df = df[df['event']!= "n/a"]

    df['paged'] = df['event'].astype(str)
    df['paged'] = df['paged'].str.lower()
    df['paged'] = df['paged'].str.replace(":","").str.replace("'","").str.replace(".","").str.replace("&","and").str.replace("- ","")
    df['paged'] = df['paged'].str.replace(" ","-")
    return df

def search_game(df, headers):
    platform = []
    des = []

    for page in df.paged: 
        url = f"https://www.gamespot.com/games/{page}"
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        res = soup.find('ul', attrs={'class' : 'game-module__platform'}).get_text()
        platform.append(res)
        desc = soup.find('p', attrs={'class' : 'game-module__description'}).get_text()
        des.append(desc)
        sleep(randint(2,10))

    return platform, des


def compile(df, platform, des):
    df['platform'] = platform
    df['des'] = des

    df.to_csv('eventsTest.csv')


def main(param: str):
    process = Process()
    process.run()
    search = search_event(pages, headers)
    result = create_dataframe(event, date)
    result = search_game(df, headers)
    compile(df, platform, des)


if __name__ == "__main__":
    typer.run(main)



