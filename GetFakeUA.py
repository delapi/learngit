import requests
from lxml import etree

headers = {
        'user-agent':'Mozilla/5.0(Windows NT 10.0; Win64; x64)\
        AppleWebKit/537.36(KHTML, like Gecko)\
        Chorme/104.0.0.0 Safari/537.36'      
    }
url = 'https://useragentstring.com/pages/useragentstring.php?name=Chrome'

response = requests.get(url, headers=headers).text


tree = etree.HTML(response)


ul_list = tree.xpath("//*[@id='liste']/ul")


with open('./fake_UA.txt','a', encoding='utf-8') as fp:
    for ul in ul_list:
        UA = ul.xpath('./li/a/text()')
        for i in range(0,len(UA)):
            ua = '"' + UA[i] + '",\n'
            print(ua)
            fp.write(ua)