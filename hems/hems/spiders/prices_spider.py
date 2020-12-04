import scrapy
import pandas as pd
import numpy
import time


class PricesSpider(scrapy.Spider):
    name = "prices"
    pccom = 'https://www.pccomponentes.com/buscar/?query="'
    phone_prices = []
    last_name = ''
    list_of_names = pd.read_csv('list_of_names').names

    def start_requests(self):

        for i in range(0, self.list_of_names.__len__()):
            composed = self.pccom + self.list_of_names[i] + '"#pg-0&or-search&fm-1116'
            self.last_name = self.list_of_names[i]
            yield scrapy.Request(url=composed, callback=self.prices_listing)

    def prices_listing(self, response):
        phone_card = response.css('div.c-product-card__content')
        price_texts = phone_card.css('span::text').getall()
        price = 'None'

        try:
            for span in range(0, price_texts.__len__()):
                current_span: str = price_texts[span]
                if '€' in current_span:
                    span_formatted = current_span.replace(',', '.').replace('€', '')
                    int_span = float(span_formatted)

                    if int_span > 100:
                        price = int_span
                        break
        except:
            price = 'None'

        self.phone_prices = numpy.append(self.phone_prices, price)
        print(self.phone_prices)
        time.sleep(30.0)
        if self.list_of_names.__len__() == self.phone_prices.__len__():
            self.export_table()

    def export_table(self):
        prices_series = pd.DataFrame({'prices': self.phone_prices})

        final_table = pd.concat([self.list_of_names, prices_series], axis=1)
        final_table.to_csv('Result2')
