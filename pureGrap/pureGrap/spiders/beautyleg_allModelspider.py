import scrapy, os


class beautylegAllModelspider(scrapy.Spider):
    name = "beautylegallmodel"

    def __init__(self, mcookie=None, mdir=None, *args, **kwargs):
        super(beautylegAllModelspider, self).__init__(*args, **kwargs)
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
        self.modelList = []

    def start_requests(self):
        yield scrapy.Request(url="http://www.beautyleg.com/model_list.php", headers=self.myheaders,
                             cookies={"PHPSESSID": self.myCookie}, callback=self.parse)

    def parse(self, response):
        for aLink in response.xpath('//td/a'):
            modelUrl = aLink.xpath('@href').extract_first().strip()
            if "model_list_result" in modelUrl:
                modelName = aLink.xpath('../br/following-sibling::text()').extract_first().strip()
                self.modelList.append({"modelUrl": modelUrl, "modelName": modelName})

    def spider_closed(self):
        with open(self.topDir + "/model_list.txt", "wb") as tempWrite:
            for oneModel in self.modelList:
                tempWrite.write("{} {}\n".format(oneModel["modelUrl"], oneModel["modelName"]))
