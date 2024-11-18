import requests
from bs4 import BeautifulSoup
import urllib3 # 禁用安全请求警告，当目标使用https时使用

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#解决爬取网页时出现中文乱码的情况
def readable_code(url, headers):
    response = requests.get(url=url, headers=headers,verify=False)
    response.encoding = response.apparent_encoding
    return response

if __name__ == '__main__':
    headers = {
        'user-agent':'Mozilla/5.0(Windows NT 10.0; Win64; x64)\
        AppleWebKit/537.36(KHTML, like Gecko)\
        Chorme/104.0.0.0 Safari/537.36'      
    }
    url = 'https://www.shicimingju.com/book/sanguoyanyi.html'
    page_text = readable_code(url,headers).text
    soup = BeautifulSoup(page_text, 'lxml')
    a_list = soup.select('[class~=tabli]')
    fp = open('sanguo.txt', 'w', encoding='utf-8')
    for a in a_list:
        title = a.string
        detail_url = 'https://www.shicimingju.com' + a['href']
        detail_page_text = readable_code(detail_url, headers).text
        detail_soup = BeautifulSoup(detail_page_text, 'lxml')
        div_tag = detail_soup.select('[class~=p_pad]')
        print(div_tag)        
        content = str(div_tag[0])
        fp.write(title + ':' + content + '\n')
        print(title, '本章全文爬取成功')