import requests
from bs4 import BeautifulSoup


class Base:
    BASE_URL = 'https://www.avito.ru/'

    def city(self, city):
        self.city = city
        return self

    def min_price(self, min_price):
        self.min_price = min_price
        return self

    def max_price(self, max_price):
        self.max_price = max_price
        return self

    def search_object(self, search_object):
        self.search_object = search_object
        return self


class Avito(Base):
    def get(self):
        headers = {
            'User-Agent': (
                'Mozilla/5.0 '
                '(Windows NT 10.0; Win64; x64) '
                'AppleWebKit/537.36'
                ' (KHTML, like Gecko) '
                'Chrome/89.0.4389.82 Safari/537.36'
            )
        }
        response = requests.get(
            f'{self.BASE_URL}'
            f'{self.city + "?"}'
            f'{"pmin=" + str(self.min_price)}'
            f'{"&pmax=" + str(self.max_price)}'
            f'{"&q=" + str(self.search_object)}',
            headers=headers
        )
        soup = BeautifulSoup(response.text, 'lxml')
        price = soup.find_all(
            'span', class_='price-text-1HrJ_ text-text-1PdBw text-size-s-1PUdo'
        )
        text = soup.find_all(
            'div', class_='iva-item-text-2xkfp iva-item-description-2pXGm text-text-1PdBw text-size-s-1PUdo'
        )
        link = soup.find_all(
            'a', href=True, class_='link-link-39EVK link-design-default-2sPEv title-root-395AQ iva-item-title-1Rmmj title-listRedesign-3RaU2 title-root_maxHeight-3obWc'
        )
        result = []
        [result.append([text[i].text, price[i].text.replace(u'\xa0', ' ').replace(u'\u2009', ''),
                        'https://www.avito.ru/' + link[i]['href']]) for i in range(0, len(text))]
        return result

parse = Avito()
print(parse.city('moskva').min_price('2033200').max_price('333333333').search_object('tayota').get())
