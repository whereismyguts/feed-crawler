
import threading
import urllib.request
import re
from website.models import Post, Tag, Author
from bs4 import BeautifulSoup
import datetime
import random

class Singleton(type):
    def __init__(cls, name, bases, attrs, **kwargs):
        super(Singleton, cls).__init__(name, bases, attrs)
        cls._instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instance



class MultiThreaded():

    def __init__(self):
        self.threads = []

    def run_thread(self, method):
        method = self.threaded_method(method)
        thread = threading.Thread(target=method, args=[])
        thread.daemon = True          
        thread.stop = False                
        thread.start()        
        self.threads.append(thread)             

    def stop(self):
        for th in self.threads:
            th.stop = True

    def keep_alive(self):
        my_id = threading.current_thread().ident
        for th in self.threads:
                if th.ident == my_id and th.stop:
                    return False
        return True      

    def threaded_method(self, function):
        def result():
            while self.keep_alive():
                try:
                    function()
                except Exception as e:
                    print(e)                    
            print("stop %s\n" % function.__name__ )          
        return result            

class Crawler(MultiThreaded):

    def __init__(self):
        self.post_links = []
        self.source_links = []
        self.exclude_lines = [
            "wp-includes",
            "about",
            "wp-content",
            "xmlrpc",
            "page",
            "feed",
            "tag",
            "category",
            "people",
            "author",
            "comments",
        ]
        self.post_regex = r"href=\"(https://disgustingmen.com/(?!"+"|".join(self.exclude_lines)+r").+?)\""
        self.sources_regex = r"href=\"(https://disgustingmen.com/(category|page).+?)\""    

        MultiThreaded.__init__(self)

    def get_html(self, url):
        with  urllib.request.urlopen(url) as fp:
            mystr = fp.read().decode("utf8")
            return mystr

    def get_links(self, url):
        mystr = self.get_html(url)
        p_links = list(set([link for link in re.findall(self.post_regex, mystr) if "#" not in link]))
        s_links = list(set( m[0] for m in re.findall(self.sources_regex, mystr) ))
        print(url + " crawled")
        return p_links, s_links

    
    def reg_find(self, regex, text):
        return re.findall(regex, text)
    
    def parse(self):
        raw_post = random.choice(Post.objects.filter(is_raw = True))
        page = self.get_html(raw_post.original_url)
        soup = BeautifulSoup(page,"html.parser")
        content =str(soup.find("div", class_="entry-content"))
        if content == "None" or not content:
            raw_post.delete()
            return
        raw_post.html = content
        results = soup.findAll("a", {"rel" : "category tag"})

        tags = [ ( r['href'].split('/')[-2:-1][0], r.contents[0] ) for r in results]
        # for r in results:
        #     tags.append( (r['href'].split('/')[-2:-1][0], r.contents[0]) )

        images = soup.findAll("img")
        raw_post.first_image = images[1]['src']
        raw_post.first_text = str(soup.findAll("p")[0].contents[0])

        raw_post.title = self.reg_find(r"<h1 class=\"entry-title\">(.+?)</h1>", page)[0]
        
        same_post = Post.objects.filter(title = raw_post.title, is_raw = False).first()
        if same_post:
            same_post.delete()

        post_date = self.reg_find(r">.*(\d\d\.\d\d\.\d\d\d\d)</time>", page)[0]
        post_date = post_date.replace('.','')
        #post_date = datetime.datetime.strptime(post_date, "%dd%mm%YYYY").date()
        
        format_str = '%d%m%Y' # The format
        raw_post.post_date = datetime.datetime.strptime(post_date, format_str)

        author = self.reg_find(r"class=\"url fn n\">(.+?)</a>", page)[0]
        a = Author.objects.filter(name = author)
        if a:
            a = a[0]
        else:
            a = Author(name = author)
            a.save()
        raw_post.author = a            

        existed_tags = Tag.objects.filter(name__in = [t[0] for t in tags])
        for t in tags:
            if not t[0] in [et.name for et in  existed_tags]:
                new_tag = Tag(name =t[0], value = t[1])
                new_tag.save()

        post_tags = Tag.objects.filter(name__in = [t[0] for t in tags])
        
        # post = Post(
        #     title = title, 
        #     html = content,  
        #     author =a, 
        #     original_url = url, 
        #     post_date = post_date, 
        #     first_image = first_image, 
        #     first_text=first_p)

        # post.save()
        # post.tags.set(post_tags)
        raw_post.is_raw = False
        raw_post.save()
        raw_post.tags.set(post_tags)

        print("post %s saved" % str(raw_post))

    def seek(self, links=[]):
        if not links: # first iteration:
            self.post_links = [p.original_url for p in Post.objects.filter(is_raw = True)]
            links.append('https://disgustingmen.com/')
            pass

        for sl in links:
            if not(sl in self.source_links):
                p_links, s_links = self.get_links(sl)
                # p_links = list(filter(lambda l: not "#more-" in l, p_links))
                for pl in p_links:
                    if not (pl in self.post_links):
                        Post.objects.create(original_url = pl)
                        self.post_links.append(pl)

                        print("added " + pl)
                #self.post_links+= [l for l in p_links if not (l in self.post_links)  ]
                self.source_links.append(sl)
                self.seek(s_links)


    def start(self):
        #self.run_thread(self.seek) 
        self.run_thread(self.parse)       

class CrawlManager():
    __metaclass__ = Singleton
    def __init__(self):
        self.crawler = Crawler()

    def stop(self):        
        self.crawler.stop()

    def start(self):
        self.crawler.start()
            



