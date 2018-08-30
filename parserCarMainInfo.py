from urllib.request import urlopen
from bs4 import BeautifulSoup
import threading
import re

'''
class mThread(threading.Thread):
    def __init__(self, url):
        threading.Thread.__init__()
        self.url = url
'''

def getSoup(url):
    soup = BeautifulSoup(urlopen(url), 'html.parser')
    return soup

def main():
    hUrl = "http://koubei.bitauto.com/tree/xuanche/?page="
    tUrl = "&s=6&order=1"
    for i in range(1, 92):
        url = hUrl + str(i) + tUrl
        #print("crawling " + url)
        #print("+++++++++++++++++++++++++++++++++++++")
        getMainInfo(url)

def getMainInfo(url):
    soup = getSoup(url)
    carNames = []
    carPrices = []
    carScores = []
    carLinks = []

    orgMainInfo = soup.select("ul[class='p-list']")
    for mInfo in orgMainInfo:
        carNames.append(mInfo.li.a.get_text())
        carLinks.append(mInfo.li.a.get('href'))

    orgCarPrices = soup.select("li[class='info']")
    orgCarScores = soup.select("span[class='sm_txt']")


    for (x, y) in zip(orgCarPrices, orgCarScores):
        carPrices.append(x.get_text())
        carScores.append(y.get_text())

    for (x, y, z, l) in zip(carNames, carPrices, carScores, carLinks):
        field = x + '\t' + y.replace("万", '').split('-')[0] + '\t' + y.replace("万", '').split('-')[1] + '\t' + z.replace("分", '') +'\t'
        #print("crawling 2rd page", l)
        #print("=================================")
        try:
            getKouBeiInfo(l, field)
        except IndexError as e:
            pass

def getKouBeiInfo(url, field):
    soup = getSoup(url)

    carType = soup.select("h6[class='h6']")[0].a.get_text().replace('关注排行', '')

    #汽车各项评分

    carScores = []
    draw = soup.select("div[class='draw']")[0]


    #print(scoreString)

    kb = soup.select("div[class='kb-list-box']")
    personCarType = []
    personCarPrice = []
    personCarBuyTimeAndPlace = []
    personKouBeiTitle = []
    personKBlink = []

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

    #个人口碑链接， 个人口碑标题
    for (x, y, i, j, k) in zip(personKouBeiTitle, personKBlink, personCarType, personCarPrice, personCarBuyTimeAndPlace):
        #print("crawling 3rd page", y)
        #print("--------------------------------------------")
        # Bug Here, don't use these var together
        buyTime = k.replace(' ', '').split('\n')[1]
        pInfo = k.replace(' ', '').split('\n')[2]
        buyPlace = re.split(r'\s+', pInfo)[0].replace("购于", '')
        factory = re.split(r'\s+', pInfo)[1]
        #field = field + '\t ' + carType + '\t ' + i + '\t ' + j.replace('万', '') + '\t ' + buyPlace + '\t ' + factory

        #field2 = '{} {} {} {} {} {} {}'.format(field, carType, i, j.replace('万', ''), buyPlace, factory, buyTime)
        field1 = carType + '\t ' + i + '\t ' + j.replace('万', '') + '\t ' + buyPlace + '\t ' + factory + '\t'
        parserPersonKB(y, field, field1)

def parserPersonKB(url, field, field1):
    soup = getSoup(url)

    orgInfoPart1 = soup.select("div[class='explain']")[0].select("span")
    orgInfoPart2 = soup.select("div[class='item-box']")
    orgInfoPart3 = soup.select("div[class='item-box div_ImgLoadArea']")


    deliverTime = orgInfoPart1[0].get_text() #发布时间
    distance = orgInfoPart1[1].get_text() #汽车行驶距离
    oilWear = orgInfoPart1[2].get_text() #目前油耗
    cost = orgInfoPart1[3].get_text() #每月养车费用
    satisfy = orgInfoPart2[0].p.get_text().replace('\n' ,' ') #最满意的地方
    unsatisfy = orgInfoPart2[1].p.get_text().replace('\n' ,' ') #最不满意的地方
    #油耗
    oilCostScore = int(orgInfoPart3[0].select("em")[0].get("style")\
        .replace("width: ", '').replace('%', '').replace(';', ''))/20
    oilCostTxt = orgInfoPart3[0].p.get_text().replace('\n' ,' ')
    #操控
    controlScore = int(orgInfoPart3[1].select("em")[0].get("style")\
        .replace("width: ", '').replace('%', '').replace(';', ''))/20
    controlTxt = orgInfoPart3[1].p.get_text().replace('\n' ,' ')
    #性价比
    costPerScore = int(orgInfoPart3[2].select("em")[0].get("style") \
                       .replace("width: ", '').replace('%', '').replace(';', '')) / 20
    costPerTxt = orgInfoPart3[2].p.get_text().replace('\n' ,' ')
    #动力
    stimulusScore = int(orgInfoPart3[3].select("em")[0].get("style") \
                       .replace("width: ", '').replace('%', '').replace(';', '')) / 20
    stimulusTxt = orgInfoPart3[3].p.get_text().replace('\n' ,' ')
    #配置
    configScore = int(orgInfoPart3[4].select("em")[0].get("style")\
        .replace("width: ", '').replace('%', '').replace(';', ''))/20
    configTxt = orgInfoPart3[4].p.get_text().replace('\n' ,' ')
    #舒适度
    comfortDegreeScore = int(orgInfoPart3[5].select("em")[0].get("style") \
                      .replace("width: ", '').replace('%', '').replace(';', '')) / 20
    comfortDegreeTxt = orgInfoPart3[5].p.get_text().replace('\n' ,' ')
    #空间
    spaceScore = int(orgInfoPart3[6].select("em")[0].get("style") \
                      .replace("width: ", '').replace('%', '').replace(';', '')) / 20
    spaceTxt = orgInfoPart3[6].p.get_text().replace('\n' ,' ')
    #外观
    apperanceScore = int(orgInfoPart3[7].select("em")[0].get("style") \
                      .replace("width: ", '').replace('%', '').replace(';', '')) / 20
    apperanceTxt = orgInfoPart3[7].p.get_text().replace('\n' ,' ')
    #内饰
    decorateScore = int(orgInfoPart3[8].select("em")[0].get("style") \
                      .replace("width: ", '').replace('%', '').replace(';', '')) / 20
    decorateTxt = orgInfoPart3[8].p.get_text().replace('\n' ,' ')
    #综合
    colligationScore = int(orgInfoPart3[9].select("em")[0].get("style") \
                      .replace("width: ", '').replace('%', '').replace(';', '')) / 20
    colligationTxt = orgInfoPart3[9].p.get_text().replace('\n' ,' ')

    '''
    print(deliverTime[2:], distance[5:9], oilWear[5:8], cost[5:8])
    print(satisfy)
    print(unsatisfy)
    print(oilCostScore, oilCostTxt)
    print(controlScore, controlTxt)
    print(costPerScore, costPerTxt)
    print(stimulusScore, stimulusTxt)
    print(configScore, configTxt)
    print(comfortDegreeScore, comfortDegreeTxt)
    print(spaceScore, spaceTxt)
    print(apperanceScore, apperanceTxt)
    print(decorateScore, decorateTxt)
    print(colligationScore, colligationTxt)
    '''

    headInfo = [deliverTime[2:], distance[5:9], oilWear[5:8], cost[5:8]]
    scores = [oilCostScore, controlScore, costPerScore, stimulusScore, comfortDegreeScore,
              configScore, spaceScore, apperanceScore, decorateScore, colligationScore]
    texts = [satisfy.strip(' '), unsatisfy.strip(' '), oilCostTxt.strip(' '), controlTxt.strip(' '), costPerTxt.strip(' '),
             stimulusTxt.strip(' '), configTxt.strip(' '), comfortDegreeTxt.strip(' '), spaceTxt.strip(' '),apperanceTxt.strip(' '),
             decorateTxt.strip(' '), colligationTxt.strip(' ')]

    for hInfo in headInfo:
        field = field + hInfo.strip(' ') + '\t '

    for score in scores:
        field = field + str(score).strip(' ') + '\t '
    for text in texts:
        field = field + text.strip(' ') + '\t '

    '''field3 = '{} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}'.format(
        field, carType, pCarType, pCarPrice, buyPlace, factory,
        deliverTime[2:], distance[5:9], oilWear[5:8], cost[5:8], oilCostScore, controlScore,
        costPerScore, stimulusScore, comfortDegreeScore, configScore, spaceScore, apperanceScore, satisfy, unsatisfy,
        oilCostTxt,decorateScore, controlTxt, costPerTxt, stimulusTxt, configTxt,comfortDegreeTxt, spaceTxt, apperanceTxt,
        decorateTxt,colligationScore, colligationTxt, buyTime)'''
    print(field1, field)

main()