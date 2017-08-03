import os, sys

if __name__ == '__main__':
    myCookie = sys.argv[1]
    topdir = sys.argv[2]
    with open("D:/troopar/model_list.txt", "rb") as tempRead:
        for line in tempRead:
            newLine = line.strip("\n|' '").split()
            modelUrl = newLine[0].strip()
            modelName = newLine[1].strip()
            commandCall = 'scrapy crawl beautylegmodelalbumlist -a murl="%s" -a mname="%s" -a mcookie="%s" -a mdir="%s"' % (modelUrl, modelName, myCookie, topdir)
            os.system(commandCall)
