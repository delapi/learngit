import re
import requests
import os

if __name__ == "__main__":
    if not os.path.exists('liyitong'):
        os.mkdir('liyitong')
    url = 'https://web.6parkbbs.com/index.php?app=forum&act=view&tid=4452671'
    headers = {
        'user-agent':'Mozilla/5.0(Windows NT 10.0)\
        AppleWebKit/537.36(KHTML, like Gecko)\
        Chorme/104.0.0.0 Safari/537.36'      
    }
    page_text = requests.get(url, headers=headers).text
    extract = '<img myDataSrc=".*?"  src="(.*?)">'
    img_src_list =re.findall(extract, page_text, re.S)
    print(img_src_list)
    for src in img_src_list:
        img_data = requests.get(src, headers=headers).content
        img_name = src.split('/')[-1]
        img_path = 'liyitong/' + img_name
        with open(img_path, 'wb') as fp:
            fp.write(img_data)
            print(img_name, '下载成功')