from urllib.request import urlopen
import urllib.request
import threading
from bs4 import BeautifulSoup
import queue
import time
import re

#爬虫线程
class mThread(threading.Thread):
    def __init__(self, url):
        threading.Thread.__init__(self)
        self.url = url

    def run(self):
        print("crawling " + self.url)
        getMainInfo(self.url)

#保存爬取数据
def save(data):
    fPath = "f:/git/carfinal.txt"
    with open(fPath, 'a', encoding='utf-8') as f:
        f.write(data)

def saveImg(imgLink):
    iPath = "f:/git/carfinalImg.txt"
    with open(iPath, 'a', encoding='utf-8') as f:
        f.write(imgLink)

def getSoup(url):
    try:
        return(BeautifulSoup(urlopen(url, timeout=10), 'html.parser'))
    except Exception as e:
        print(e)

def getMainInfo(url):
    soup = getSoup(url)
    carNames = []
    carPrices = []
    carScores = []
    carLinks = []
    imgLinks = []

    orgMainInfo = soup.select("ul[class='p-list']")
    orgImgLinks = soup.select("div[class='img']")

    for imgLink in orgImgLinks:
        imgLinks.append(imgLink.img.get("src"))

    for mInfo in orgMainInfo:
        carNames.append(mInfo.li.a.get_text())
        carLinks.append(mInfo.li.a.get('href'))

    orgCarPrices = soup.select("li[class='info']")
    orgCarScores = soup.select("span[class='sm_txt']")


    for (x, y) in zip(orgCarPrices, orgCarScores):
        carPrices.append(x.get_text())
        carScores.append(y.get_text())

    for (i, x, y, z, l) in zip(imgLinks, carNames, carPrices, carScores, carLinks):
        print("crawling 2rd page", l)
        print("=================================")
        try:
            field = x + '\t' + y.replace("万", '').split('-')[0] + '\t' + y.replace("万", '').split('-')[1] + \
                '\t' + z.replace("分", '') + '\t'
            getKouBeiInfo(l, field, i)
        except IndexError as e:
            print(e)

def fun1(kb, personKouBeiTitle, personKBlink, personCarType, personCarPrice, personCarBuyTimeAndPlace):
    for pKB in kb:
        orgTitleAndLink = pKB.select("div[class='titbox']")
        title = orgTitleAndLink[0].a.get_text()
        if "微口碑" not in title:
            personKouBeiTitle.append(orgTitleAndLink[0].a.get_text())
            personKBlink.append(orgTitleAndLink[0].a.get("href"))
            headbox = pKB.select("div[class='head-box']")[0]
            personCarType.append(headbox.select("h6")[0].get_text())
            personCarPrice.append(headbox.select("span")[0].em.get_text())
            personCarBuyTimeAndPlace.append(headbox.select("span")[1].get_text())

def getKouBeiInfo(url, field3, imgLink):
    soup = getSoup(url)

    carType = soup.select("h6[class='h6']")[0].a.get_text().replace('关注排行', '')
    carBigType = soup.select("div[class='crumbs-txt']")
    orgBigType = carBigType[0].select("a")
    biggerType = orgBigType[2].get_text()
    bigType = orgBigType[3].get_text()

    moreKbLink = soup.select("a[class='btn-more mt50']")
    kb = soup.select("div[class='kb-list-box']")
    personCarType = []
    personCarPrice = []
    personCarBuyTimeAndPlace = []
    personKouBeiTitle = []
    personKBlink = []


    if moreKbLink != None:
        moreKbUrl = moreKbLink[0].get("href")
        print("crawling moreKbUrl ", moreKbUrl)
        soup = getSoup(moreKbUrl)
        kb = soup.select("div[class='kb-list-box']")

        fun1(kb, personKouBeiTitle, personKBlink, personCarType, personCarPrice, personCarBuyTimeAndPlace)

        if soup.select("div[class='the_pages']"):
            pageNum = soup.select("div[class='the_pages']")[0].select('a')[-2].get_text()
            print(pageNum)
            hKbUrl = (moreKbUrl[:-9])
            tKbUrl = (moreKbUrl[-8:])
            print(hKbUrl, tKbUrl)
            for i in range(2, int(pageNum)+1):
                url = hKbUrl + str(i) + tKbUrl
                print("crawling moreKbUrl", url)
                nSoup = getSoup(url)
                try:
                    nKb = nSoup.select("div[class='kb-list-box']")
                except AttributeError:
                    pass

                fun1(nKb, personKouBeiTitle, personKBlink, personCarType, personCarPrice, personCarBuyTimeAndPlace)

    else:
        fun1(kb, personKouBeiTitle, personKBlink, personCarType, personCarPrice, personCarBuyTimeAndPlace)


    #个人口碑链接， 个人口碑标题
    for (x, y, i, j, k) in zip(personKouBeiTitle, personKBlink, personCarType, personCarPrice, personCarBuyTimeAndPlace):
        #print("crawling 3rd page", y)
        #print("--------------------------------------------")

        # Bug Here, don't use these var together
        buyTime = k.replace(' ', '').split('\n')[1]
        pInfo = k.replace(' ', '').split('\n')[2]
        buyPlace = re.split(r'\s+', pInfo)[0].replace("购于", '')
        factory = re.split(r'\s+', pInfo)[1]
        if(len(factory) == 0):
            factory = "None"
        try:
            rField = parserPersonKB(y)
            if(rField):
                field1 =carType + '\t ' + i + '\t ' + j.replace('万', '') + '\t ' + buyPlace + '\t ' + factory + '\t'
                data = biggerType + '\t ' + bigType + '\t ' +  field3 + field1 + rField + buyTime
                imgPath = 'E:/Img2/' + bigType + '_' + carType + '_' + buyPlace + '.jpg'
                #urllib.request.urlretrieve(imgLink, imgPath)
            saveImg(imgLink)
            save(data)
            print(data)
            print(imgLink)
        except AttributeError as e:
            print(e)

def parserPersonKB(url):
    soup = getSoup(url)

    try:
        orgInfoPart1 = soup.select("div[class='explain']")[0].select("span")
        orgInfoPart2 = soup.select("div[class='item-box']")
        orgInfoPart3 = soup.select("div[class='item-box div_ImgLoadArea']")

        if(len(orgInfoPart1) == 4 and len(orgInfoPart2) == 2 and len(orgInfoPart3) == 10):
            deliverTime = orgInfoPart1[0].get_text()  # 发布时间
            distance = orgInfoPart1[1].get_text()  # 汽车行驶距离
            oilWear = orgInfoPart1[2].get_text()  # 目前油耗
            cost = orgInfoPart1[3].get_text()  # 每月养车费用
            satisfy = orgInfoPart2[0].p.get_text().replace('\n', ' ')  # 最满意的地方
            unsatisfy = orgInfoPart2[1].p.get_text().replace('\n', ' ')  # 最不满意的地方

            # 油耗
            oilCostScore = int(orgInfoPart3[0].select("em")[0].get("style") \
                               .replace("width: ", '').replace('%', '').replace(';', '')) / 20
            oilCostTxt = orgInfoPart3[0].p.get_text().replace('\n', ' ')
            # 操控
            controlScore = int(orgInfoPart3[1].select("em")[0].get("style") \
                               .replace("width: ", '').replace('%', '').replace(';', '')) / 20
            controlTxt = orgInfoPart3[1].p.get_text().replace('\n', ' ')
            # 性价比
            costPerScore = int(orgInfoPart3[2].select("em")[0].get("style") \
                               .replace("width: ", '').replace('%', '').replace(';', '')) / 20
            costPerTxt = orgInfoPart3[2].p.get_text().replace('\n', ' ')
            # 动力
            stimulusScore = int(orgInfoPart3[3].select("em")[0].get("style") \
                                .replace("width: ", '').replace('%', '').replace(';', '')) / 20
            stimulusTxt = orgInfoPart3[3].p.get_text().replace('\n', ' ')
            # 配置
            configScore = int(orgInfoPart3[4].select("em")[0].get("style") \
                              .replace("width: ", '').replace('%', '').replace(';', '')) / 20
            configTxt = orgInfoPart3[4].p.get_text().replace('\n', ' ')
            # 舒适度
            comfortDegreeScore = int(orgInfoPart3[5].select("em")[0].get("style") \
                                     .replace("width: ", '').replace('%', '').replace(';', '')) / 20
            comfortDegreeTxt = orgInfoPart3[5].p.get_text().replace('\n', ' ')
            # 空间
            spaceScore = int(orgInfoPart3[6].select("em")[0].get("style") \
                             .replace("width: ", '').replace('%', '').replace(';', '')) / 20
            spaceTxt = orgInfoPart3[6].p.get_text().replace('\n', ' ')
            # 外观
            apperanceScore = int(orgInfoPart3[7].select("em")[0].get("style") \
                                 .replace("width: ", '').replace('%', '').replace(';', '')) / 20
            apperanceTxt = orgInfoPart3[7].p.get_text().replace('\n', ' ')
            # 内饰
            decorateScore = int(orgInfoPart3[8].select("em")[0].get("style") \
                                .replace("width: ", '').replace('%', '').replace(';', '')) / 20
            decorateTxt = orgInfoPart3[8].p.get_text().replace('\n', ' ')
            # 综合
            colligationScore = int(orgInfoPart3[9].select("em")[0].get("style") \
                                   .replace("width: ", '').replace('%', '').replace(';', '')) / 20
            colligationTxt = orgInfoPart3[9].p.get_text().replace('\n', ' ')

            field = ''
            headInfo = [oilWear[5:].replace('L/100km', ''), cost[5:].replace('元/月', '')]
            scores = [oilCostScore, controlScore, costPerScore, stimulusScore, comfortDegreeScore,
                      configScore, spaceScore, apperanceScore, decorateScore, colligationScore]
            texts = [satisfy.strip(' '), unsatisfy.strip(' '), oilCostTxt.strip(' '), controlTxt.strip(' '),
                     costPerTxt.strip(' '),
                     stimulusTxt.strip(' '), configTxt.strip(' '), comfortDegreeTxt.strip(' '), spaceTxt.strip(' '),
                     apperanceTxt.strip(' '),
                     decorateTxt.strip(' '), colligationTxt.strip(' ')]

            for hInfo in headInfo:
                field = field + hInfo.strip(' ') + '\t '
            for score in scores:
                field = field + str(score).strip(' ') + '\t '
            for text in texts:
                field = field + text.strip(' ') + '\t '
            return(field)
        else:
            pass
    except UnboundLocalError and IndexError as e:
        print(e)
        pass


def main():
    urlQueue = queue.Queue()
    hUrl = "http://koubei.bitauto.com/tree/xuanche/?page="
    tUrl = "&s=6&order=1"
    for i in range(1, 92):
        urlQueue.put(hUrl + str(i) + tUrl)
        
    while urlQueue.empty() != True:
        url = urlQueue.get()
        mThread(url).start()
        time.sleep(10)

main()