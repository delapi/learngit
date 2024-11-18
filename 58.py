import requests
from lxml import etree

if __name__ == '__main__':
    headers = {
        'user-agent':'Mozilla/5.0(Windows NT 10.0; Win64; x64)\
        AppleWebKit/537.36(KHTML, like Gecko)\
        Chorme/104.0.0.0 Safari/537.36'      
    }
    url = 'https://sh.58.com/ershoufang/p%d/?PGTID=0d30000c-0000-2e04-d18a-9af183e2d6a4&ClickID=1'
    with open('58.txt', 'w', encoding='utf-8') as fp:
        for pageNum in range(1,9):
            new_url = format(url %pageNum)
            page_text = requests.get(new_url, headers=headers).text
            tree = etree.HTML(page_text)
            statstical_list = tree.xpath('/html/body//section[@class="list"]/div')
            print(statstical_list)
            for li in statstical_list:
                title = li.xpath('./a//h3/text()')[0]
                print(title)
                fp.write(title + '\n')
    print('over!')
    