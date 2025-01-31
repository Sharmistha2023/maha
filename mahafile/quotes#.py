# from project1.items import DocumentItem
from scrapy.loader import ItemLoader
# from spiders_dir.items import DocumentItem 
from llama_index.core import Document
import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    # start_urls = [
    #     "https://quotes.toscrape.com/page/1/",
    #     "https://quotes.toscrape.com/page/2/",
    # ]
    # def __init__(self,document):
    #     self.document = document
    def __init__(self, documents=None,start_urls=None, *args, **kwargs):
        super(QuotesSpider, self).__init__(*args, **kwargs)
        self.start_urls = start_urls if start_urls is not None else []
        self.documents = documents if documents is not None else []

    def parse(self, response):
        for quote in response.css("div.quote"):
            self.documents.append(Document(text = quote.css("span.text::text").get(),metadata={"file_name":f"{response.url}"}))
            # yield {
            #     "author": quote.xpath("span/small/text()").get(),
            #     "text": quote.css("span.text::text").get(),
            # }
            # return Document(text = quote.css("span.text::text").get())

        # for quote in response.css("div.quote"):
        #     loader = ItemLoader(item = DocumentItem(),selector=quote)
        #     loader.add_xpath('text',"span.text::text")
        #     yield loader.load_item()

        next_page = response.css('li.next a::attr("href")').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)