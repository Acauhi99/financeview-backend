import requests
from bs4 import BeautifulSoup

class BrazillianStocksController:

    def get_stocks(self) -> dict:
        url = "https://www.infomoney.com.br/cotacoes/empresas-b3/"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        sectors = {}
        for sector in soup.find_all('div', {'class': 'list-companies'}):
            sector_name = sector.find('h2').text.strip()
            companies = []
            for company in sector.find_all('tr')[1:]:
                company_name = company.find('td', {'class': 'higher'}).text.strip()
                ticker = company.find('td', {'class': 'strong'}).find('a').text.strip()
                companies.append({'nome': company_name, 'ticker': ticker})
            sectors[sector_name] = companies

        return sectors