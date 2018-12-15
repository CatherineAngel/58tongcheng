import requests

from lxml import etree

import time

import base64_parse
from pymongo import MongoClient
import dbmongo

headers={
'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'zh-CN,zh;q=0.9',
'Connection':'keep-alive',
'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
'Cookie': 'BAIDUID=7F4150868CEDE1C9F481485C24D7E581:FG=1; BIDUPSID=7F4150868CEDE1C9F481485C24D7E581; PSTM=1544004887; CPROID=7F4150868CEDE1C9F481485C24D7E581:FG=1; BDUSS=g3amhHUFJ0OXRVbHpidzdvfkMzOWsyZTVMWDRmMnlKS001ZTdJRnRicUhtakZjQVFBQUFBJCQAAAAAAAAAAAEAAABx3N3Qxa7J8bnUudS1xGEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIcNClyHDQpcQ0; ZD_ENTRY=baidu; delPer=0; PSINO=2; H_PS_PSSID=1422_21080_28019_27751_27245_22157; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598',

}
def url_parse(url):
    res = requests.get(url)
    html=etree.HTML(res.text)
    list=html.xpath("//div[@class='img_list']/a/@href")
    return list

def parse(html):
    data={}
    #宣传语
    try:
        data['tagline'] = html.xpath("//div[@class='house-title']/h1/text()")
        #房价
        data['price'] = base64_parse.parse_price(html) #调用反扒base64中的解析函数
        #议价方式
        data['议价方式']=html.xpath("//div[@class='house-pay-way f16']/span[@class='c_333']/text()")
        # 租赁方式：
        # 房屋类型：
        # 朝向楼层：
        # 所在小区：
        # 所属区域：
        # 详细地址：
        data['lease'] = ''.join(html.xpath("//div[@class='house-desc-item fl c_333']/ul/li[1]/span[2]/text()")[0].split())
        data['Type'] = base64_parse.parse_type(html)
        data['toward'] = base64_parse.parse_toward(html)
        data['plot'] = ''.join(html.xpath("//div[@class='house-desc-item fl c_333']/ul/li[4]/span[2]/a/text()")[0].split())
        data['area'] = (''.join(html.xpath("string(//div[@class='house-desc-item fl c_333']/ul/li[5])").split())).replace('所属区域：','')
        data['address']=''.join(html.xpath("//div[@class='house-desc-item fl c_333']/ul/li[6]/span[2]/text()")[0].split())
        # list_value=html.xpath("//div[@class='house-desc-item fl c_333']/ul/li[1]/span[2]/text()")

        data['phonenumber'] =html.xpath("//div[@class='house-chat-phone']/span/text()")
        #详细介绍
        data["introduct"] = ''.join(
            html.xpath("//div[@class='house-word-introduce f16 c_555']/ul/li[2]/span[2]//strong/text()")).split()

        #在租和在售
        data['inrent'] = ''.join(html.xpath("//div[@class='house-desc-item fl c_333']/ul/li[4]/em/a[@class='c_0091d7 ah']/text()")[0]).split()
        data['onsale'] = ''.join(html.xpath("//div[@class='house-desc-item fl c_333']/ul/li[4]/em/a[@class='c_0091d7 ah']/text()")[1]).split()
    except IndexError:
        print("出现异常")
    return data




if __name__=='__main__':
    #start_url = 'https://xa.58.com/chuzu/?PGTID=0d100000-001e-3005-fc0e-fc1b243fa56e&ClickID=2'
    # 实例化mongodb并连接
    # db=dbmongo.mongo()
    for count in range(1,70):
        start_url = 'https://xa.58.com/chuzu/pn' + str(count) + '/?PGTID=0d100000-001e-3005-fc0e-fc1b243fa56e&ClickID=2'
        url_list = url_parse(start_url)
        print("第"+str(count)+"页的数据")
        print("*"*40)
        for url in url_list:
            url = 'https:' + url
            print(url)
            response = requests.get(url, headers=headers)
            html = etree.HTML(response.text)
            data = parse(html)
            data['url']=url
            # db.insert(data)
            with open('data2.txt', 'a')  as f:
                f.write(str(data) + '\n')
            print(data)
            time.sleep(2.5)

# for i in datas:
    #     print(i)
    #
    #



