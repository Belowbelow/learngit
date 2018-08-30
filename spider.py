from urllib import requests
from bs4 import BeautifulSoup
import re
import random
import time


# 爬虫主函数
def mm(url):
    # 设置目标url，使用requests创建请求
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"}
    req0 = requests.get(url=url, headers=header)
    req0.encoding = "gb18030"  # 解决乱码问题
    html0 = req0.text

    # 使用BeautifulSoup创建html代码的BeautifulSoup实例，存为soup0
    soup0 = BeautifulSoup(html0, "html.parser")

    # 获取最后一页数字，对应-122（对照前一小节获取尾页的内容看你就明白了）
    total_page = int(soup0.find("div", class_="pagers").findAll("a")[-2].get_text())
    myfile = open("aika_qc_gn_1_1_1.txt", "a", encoding='gb18030', errors='ignore')  # 解决乱码问题
    print("user", " 来源", " 认为有用人数", " 类型", " comment")
    NAME = "user" + " 来源" + " 认为有用人数" + " 类型" + " comment"
    myfile.write(NAME + "\n")
    for i in list(range(1, total_page + 1)):
        # 设置随机暂停时间
        stop = random.uniform(1, 3)

        url = "http://newcar.xcar.com.cn/257/review/0/0_" + str(i) + ".htm"
        req = requests.get(url=url, headers=header)
        req.encoding = "gb18030"  # 解决乱码问题
        html = req.text

        soup = BeautifulSoup(html, "html.parser")
        contents = soup.find('div', class_="review_comments").findAll("dl")
        l = len(contents)
        for content in contents:
            tiaoshu = contents.index(content)
            try:
                ss = "正在爬取第%d页的第%d的评论，网址为%s" % (i, tiaoshu + 1, url)
                print(ss)  # 正在爬取的条数
                try:

                    # 点评角度
                    comment_jiaodu = content.find("dt").find("em").find("a").get_text().strip().replace("\n",
                                                                                                        "").replace(
                        "\t", "").replace("\r", "")
                except:
                    comment_jiaodu = "sunny"
                try:

                    # 点评类型
                    comment_type0 = content.find("dt").get_text().strip().replace("\n", "").replace("\t", "").replace(
                        "\r",
                        "")
                    comment_type1 = comment_type0.split("【")[1]
                    comment_type = comment_type1.split("】")[0]
                except:
                    comment_type = "sunny"

                # 认为该条评价有用的人数
                try:
                    useful = int(
                        content.find("dd").find("div", class_="useful").find("i").find(
                            "span").get_text().strip().replace(
                            "\n", "").replace("\t", "").replace("\r", ""))
                except:
                    useful = "sunny"

                # 评论来源
                try:
                    comment_region = content.find("dd").find("p").find("a").get_text().strip().replace("\n",
                                                                                                       "").replace(
                        "\t", "").replace("\r", "")
                except:
                    comment_region = "sunny"

                # 评论者名称
                try:
                    user = \
                        content.find("dd").find("p").get_text().strip().replace("\n", "").replace("\t", "").replace(
                            "\r",
                            "").split(
                            "：")[-1]
                except:
                    user = "sunny"

                # 评论内容
                try:
                    comment_url = content.find('dt').findAll('a')[-1]['href']
                    urlc = comment_url
                    headerc = {
                        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"}
                    reqc = requests.get(urlc, headers=headerc)
                    htmlc = reqc.text
                    soupc = BeautifulSoup(htmlc, "html.parser")

                    comment0 = \
                        soupc.find('div', id='mainNew').find('div', class_='maintable').findAll('form')[1].find('table',
                                                                                                                class_='t_msg').findAll(
                            'tr')[1]
                    try:
                        comment = comment0.find('font').get_text().strip().replace("\n", "").replace("\t", "")
                    except:
                        comment = "sunny"
                    try:
                        comment_time = soupc.find('div', id='mainNew').find('div', class_='maintable').findAll('form')[
                                           1].find('table', class_='t_msg').find('div',
                                                                                 style='padding-top: 4px;float:left').get_text().strip().replace(
                            "\n", "").replace(
                            "\t", "")[4:]
                    except:
                        comment_time = "sunny"
                except:
                    try:
                        comment = \
                            content.find("dd").get_text().split("\n")[-1].split('\r')[-1].strip().replace("\n",
                                                                                                          "").replace(
                                "\t", "").replace("\r", "").split("：")[-1]
                    except:
                        comment = "sunny"

                time.sleep(stop)
                print(user, comment_region, useful, comment_type, comment)

                tt = user + " " + comment_region + " " + str(useful) + " " + comment_type + " " + comment
                myfile.write(tt + "\n")
            except Exception as e:
                print(e)
                s = "爬取第%d页的第%d的评论失败，网址为%s" % (i, tiaoshu + 1, url)
                print(s)
                pass
    myfile.close()


# 统计评论分布
def fenxi():
    myfile = open("aika_qc_gn_1_1_1.txt", "r")
    good = 0
    middle = 0
    bad = 0
    nn = 0
    for line in myfile:
        commit = line.split(" ")[3]
        if commit == "好评":
            good = good + 1
        elif commit == "中评":
            middle = middle + 1
        elif commit == "差评":
            bad = bad + 1
        else:
            nn = nn + 1
    count = good + middle + bad + nn
    g = round(good / (count - nn) * 100, 2)
    m = round(middle / (count - nn) * 100, 2)
    b = round(bad / (count - nn) * 100, 2)
    n = round(nn / (count - nn) * 100, 2)
    print("好评占比：", g)
    print("中评占比：", m)
    print("差评占比：", b)
    print ("未评论：", n)


url = "http://newcar.xcar.com.cn/257/review/0.htm"
mm(url)
fenxi()