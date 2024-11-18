import requests
from lxml import etree
import urllib3 # 禁用安全请求警告，当目标使用https时使用
import os

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


if __name__ == '__main__':
    headers = {
        'user-agent':'Mozilla/5.0(Windows NT 10.0; Win64; x64)\
        AppleWebKit/537.36(KHTML, like Gecko)\
        Chorme/104.0.0.0 Safari/537.36'      
    }

    i = -1
    if not os.path.exists('picLibs'):
        os.mkdir('picLibs')
    #设置一个通用的url
    url = 'http://www.eosao.com/photo/4063436803_%d.html'
    pageNum = 1
    src_list = []
    img_name_list = []
    for pageNum in range(1,5):
        new_url = format(url %pageNum)
        page_text = requests.get(url=new_url,headers=headers,verify=False).text
        tree = etree.HTML(page_text)
        li_list = tree.xpath('//div[@class="image_div"]')
        print(li_list)
'''        for li in li_list:
            src = li.xpath('./p/a/img/@src')[0]
            src_list.append(src)
            img_name = li.xpath('./p/a/img/@alt')[0] + str(pageNum) + '.png'
            img_name_list.append(img_name)
    for img_url in src_list:
        i += 1
        img_data = requests.get(img_url,headers=headers).content
        img_path = 'picLibs/' + img_name_list[i]
        with open(img_path, 'wb') as fp:
            fp.write(img_data)
            print(img_name_list[i] + '下载成功！')'''