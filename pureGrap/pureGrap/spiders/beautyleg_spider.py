import scrapy, os


class BeautylegSpider(scrapy.Spider):
    name = "beautyleg"

    def __init__(self, aurl=None, mname=None, mcookie=None, mdir=None, *args, **kwargs):
        super(BeautylegSpider, self).__init__(*args, **kwargs)
        if mdir is None:
            self.topDir = "D:/troopar"
        else:
            self.topDir = mdir
        self.myheaders = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                          'Accept-Encoding': 'gzip, deflate',
                          'Accept-Language': 'en-GB,en-US;q=0.8,en;q=0.6',
                          'Authorization': 'Basic bWFjY2hpY2tlbjpGdFVsNHJlYQ==',
                          'Cache-Control': 'max-age=0',
                          'Connection': 'keep-alive',
                          'Content-Type': 'application/x-www-form-urlencoded',
                          'Host': 'www.beautyleg.com',
                          'Origin': 'http://www.beautyleg.com',
                          'Referer': 'http://www.beautyleg.com/member/index.php',
                          'Upgrade-Insecure-Requests': '1',
                          'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'}
        self.myCookie = mcookie
        self.albumUrl = aurl
        self.modelName = mname
        self.albumNo = self.albumUrl.split("no=")[1]
        self.modelDir = "{}/beautyleg/{}".format(self.topDir, mname)
        self.albumDir = "{}/{}".format(self.modelDir, self.albumNo)
        if not os.path.isdir(self.modelDir): os.mkdir(self.modelDir)
        if not os.path.isdir(self.albumDir): os.mkdir(self.albumDir)

    def start_requests(self):
        yield scrapy.Request(url="http://www.beautyleg.com{}".format(self.albumUrl), headers=self.myheaders,
                             cookies={"PHPSESSID": self.myCookie}, callback=self.parse)

    def parse(self, response):
        for aLink in response.css('a'):
            fileUrl = aLink.xpath('@href').extract()[0]
            fileName = fileUrl.split('/')[-1:][0]
            yield scrapy.Request(url="http://www.beautyleg.com{}".format(fileUrl), headers=self.myheaders,
                                 cookies={"PHPSESSID": self.myCookie},
                                 meta={'fileName': "{}/{}".format(self.albumDir, fileName)},
                                 callback=self.saveFileToDisk)

    def saveFileToDisk(self, response):
        with open(response.meta['fileName'], "wb") as target:
            target.write(response.body)

    def spider_closed(self):
        pass
