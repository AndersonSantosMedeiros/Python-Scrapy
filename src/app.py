import scrapy

class BricketSetSpider (scrapy.Spider):
    name = 'brickset_spider'
    # Set here the start year which the crawler is getting information
    first_year = 2016
    start_urls = ['http://brickset.com/sets/year-' + str(first_year)]

    def parse(self, response):
        SET_SELECTOR = '.set'
        for brickset in response.css(SET_SELECTOR):
            NAME_SELECTOR = 'h1 a ::text'
            PIECES_SELECTOR = './/dl[dt/text() = "Pieces"]/dd/a/text()'
            RRP_SELECTOR = './/dl[dt/text() = "RRP"]/dd/text()'
            TAGS_SELECTOR = 'div span a ::text'
            MINIFIGS_SELECTOR = './/dl[dt/text() = "Minifigs"]/dd[2]/a/text()'
            IMAGE_SELECTOR = 'img ::attr(src)'
            yield {
                'name': brickset.css(NAME_SELECTOR).extract()[-1],
                'pieces': brickset.xpath(PIECES_SELECTOR).extract_first(),
                'rrp': brickset.xpath(RRP_SELECTOR).extract_first(),
                'tags': brickset.css(TAGS_SELECTOR).extract(),
                'minifigs': brickset.xpath(MINIFIGS_SELECTOR).extract_first(),
                'image': brickset.css(IMAGE_SELECTOR).extract_first(),
            }
        
        NEXT_PAGE_SELECTOR = '.next a ::attr(href)'
        next_page = response.css(NEXT_PAGE_SELECTOR).extract_first()
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse
            )

        else:
            self.first_year += 1
            next_page = 'http://brickset.com/sets/year-' + str(self.first_year)
            try:
                yield scrapy.Request(
                    response.urljoin(next_page),
                    callback=self.parse
                )
            except:
                pass