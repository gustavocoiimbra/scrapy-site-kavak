from scrapy import Request
from scrapy import Spider
from re import findall


class KavakspiderSpider(Spider):
    name = 'KavakSpider'
    allowed_domains = ['www.kavak.com']

    def start_requests(self):
        urls = [
            'https://www.kavak.com/br/carros-usados']

        for x in range(2, 157):
            l = f'https://www.kavak.com/br/page-{x}/carros-usados'
            urls.append(l)

        for url in urls:
            yield Request(
                url,
                callback=self.parse
            )

    def parse(self, response, **kwargs):

        model = response.css(
            'div[class="card-body"] h2::text').getall()
        details = response.css(
            'div[class="card-body"] p::text').getall()
        years = [''.join(findall(r'(\w+)', x)[0])
                 for x in details if findall('•', x)]
        distance = [''.join(findall(r'(\w+)', x)[1:3])
                    for x in details if findall('•', x)]
        state = [' '.join(findall(r'(\w+)', x)[4:])
                 for x in details if findall('•', x)]
        prize = response.css(
            'div[class="payment-tax-wrapper"] span::text').getall()

        for modelo, ano, preco, kil, estado in zip(model, years, prize, distance, state):
            yield {
                "Modelo": modelo,
                "Ano": ano,
                "Preço": preco,
                "KM": kil,
                "Estado": estado
            }
