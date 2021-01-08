import requests
from lxml.html import fromstring
import cssselect
import pandas as pd
from tqdm import tqdm
import time

class Parse:
    def __init__(self):
        self.url = 'https://45bwzj1sgc-dsn.algolia.net/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20JavaScript%20(3.35.1)%3B%20Browser%3B%20JS%20Helper%20(3.1.0)&x-algolia-application-id=45BWZJ1SGC&x-algolia-api-key=NDYzYmNmMTRjYzU4MDE0ZWY0MTVmMTNiYzcwYzMyODFlMjQxMWI5YmZkMjEwMDAxMzE0OTZhZGZkNDNkYWZjMHJlc3RyaWN0SW5kaWNlcz0lNUIlMjJZQ0NvbXBhbnlfcHJvZHVjdGlvbiUyMiU1RCZ0YWdGaWx0ZXJzPSU1QiUyMiUyMiU1RCZhbmFseXRpY3NUYWdzPSU1QiUyMnljZGMlMjIlNUQ%3D'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
        }
        self.df = pd.DataFrame()

    def get_html(self, url):
        """
        get html from website
        """
        return fromstring(requests.get(url, headers=self.headers).content)
        
    def get_json(self):
        """
        get json from website
        """
        res = requests.post(self.url, json={
            "requests": [
                {
                    "indexName": "YCCompany_production",
                    "params":"hitsPerPage=1000&query=&page=0&facets=%5B%22name%22%2C%22status%22%2C%22batch%22%2C%20%22website%22%5D"}]}).json()["results"][0]["hits"]
        self.df = pd.DataFrame.from_records(data=res, index='id', columns=['id', 'name', 'website', 'status', 'batch'])


    def get_more(self):
        for i, row in tqdm(self.df.iterrows(), total=self.df.shape[0]):
            html = self.get_html(f"https://www.ycombinator.com/companies/{i}")
            self.df.loc[i, "social"] = ', '.join([link.get('href') for link in html.cssselect('a.social')])
            self.df.loc[i, "founders"] = ', '.join([
                f"{founder.cssselect('.heavy')[0].text.split(',')[0]} {' '.join([a.get('href') for a in founder.cssselect('a.social')])}" 
                    for founder in html.cssselect('div.founder-card')
                ])
            time.sleep(3)
            
        


if __name__ == "__main__":
    parser = Parse()
    parser.get_json()
    parser.get_more()
    parser.df.to_csv('data.csv')
