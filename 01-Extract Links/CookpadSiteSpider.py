import scrapy
from time import sleep
 
pageid = 1
old_links = []
is_found_old_link = False
is_oldlinks_file_Exists = True

class BlogSpider(scrapy.Spider):
    name = 'cookpadspider'
    start_urls = ['https://cookpad.com/eg/وصفات?page=1']
    
    
    
    def parse(self, response):
        global old_links, pageid, is_found_old_link, is_oldlinks_file_Exists
        if len(old_links)==0 and is_oldlinks_file_Exists:
            try:
                with open("../02-Extract Recipes/oldlinks.txt", 'r') as oldf:
                    old_links.extend(oldf.readlines(5000))
            except:
                is_oldlinks_file_Exists = False
                pass
                
                                
            
        with open("../02-Extract Recipes/links.txt", 'a') as f:
            for title in response.css('li[class=recipe]> *'):
                new_link = 'https://cookpad.com' + title.css('a ::attr(href)').extract_first()+'\n'
                if new_link not in old_links:
                    f.write(new_link)
                    f.flush()
                else:
                    is_found_old_link = True
            
            f.close()
            
           
        if not is_found_old_link:
            pageid = pageid+1    
            next_page = 'https://cookpad.com/eg/وصفات?page='+str(pageid)
            if next_page:
                yield scrapy.Request(response.urljoin(next_page), callback=self.parse)
