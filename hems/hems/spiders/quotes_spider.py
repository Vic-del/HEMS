import scrapy
import pandas as pd
import numpy


class QuotesSpider(scrapy.Spider):
    name = "mobiles"
    antutu = ['https://antutu.com/en/ranking/rank1.htm']
    phone_names = []
    phone_types = []
    phone_scores = []

    def start_requests(self):
        for url in self.antutu:
            yield scrapy.Request(url=url, callback=self.mobile_listing)

    def mobile_listing(self, response):
        cell = response.css('div.nrank-b')

        phone_name = cell.css('li.bfirst::text').getall()
        phone_type = cell.css('span.memory::text').getall()
        phone_score = cell.css('li.blast::text').getall()

        self.phone_names = numpy.append(self.phone_names, phone_name)
        self.phone_types = numpy.append(self.phone_types, phone_type)
        self.phone_scores = numpy.append(self.phone_scores, phone_score)

        mobiles_table = pd.DataFrame(
            {
                'name': self.phone_names,
                'type': self.phone_types,
                'score': self.phone_scores
            }
        )

        all_names = pd.DataFrame({'names': self.phone_names})
        all_names.to_csv('list_of_names')
        mobiles_table.to_csv('mobiles_table')
