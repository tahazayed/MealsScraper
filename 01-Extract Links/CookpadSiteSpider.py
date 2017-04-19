import scrapy
from time import sleep
 
pageid = 1

class BlogSpider(scrapy.Spider):
    name = 'cookpadspider'
    start_urls = ['https://cookpad.com/eg/وصفات?page=1']
    
    
    def parse(self, response):
        with open("../02-Extract Recipes/links.txt", 'a') as f:
            for title in response.css('li[class=recipe]> *'):
                f.write('https://cookpad.com' + title.css('a ::attr(href)').extract_first()+"\n")
            f.flush()
            f.close()
            
           

        global pageid
        pageid = pageid+1    
        next_page = 'https://cookpad.com/eg/وصفات?page='+str(pageid)
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)
