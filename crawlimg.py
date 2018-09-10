from urllib.request import urlopen
from urllib.request import urlretrieve
from bs4 import BeautifulSoup

def crawlimg(url):
    soup = BeautifulSoup(urlopen(url), 'html.parser')
    orgMainInfo = soup.select("ul[class='p-list']")
    orgImgLinks = soup.select("div[class='img']")

    imgLinks = []
    carNames = []

    for imgLink in orgImgLinks:
        imgLinks.append(imgLink.img.get("src"))

    for mInfo in orgMainInfo:
        carNames.append(mInfo.li.a.get_text())

    for (x, y) in zip(imgLinks, carNames):
        imgPath = "E:/img3/" + y + ".png"
        urlretrieve(x, imgPath)

hUrl = "http://koubei.bitauto.com/tree/xuanche/?page="
tUrl = "&s=6&order=1"
links = []
for i in range(1, 92):
    links.append(hUrl + str(i) + tUrl)

for l in links:
    crawlimg(l)
