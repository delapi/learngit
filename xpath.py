import re
import requests
import os


if __name__ == "__main__":
    if not os.path.exists('imglibs'):
        os.mkdir('imglibs')
    url = 'https://www.douban.com/'
    headers = {
        'user-agent':'Mozilla/5.0(Windows NT 10.0; Win64; x64)\
        AppleWebKit/537.36(KHTML, like Gecko)\
        Chorme/104.0.0.0 Safari/537.36'      
    }
    page_text = requests.get(url, headers=headers).text
    extract = '<div class="pic">.*?<img src=.*? data-origin="(.*?)" alt=.*?</div>'
    img_src_list = re.findall(extract, page_text, re.S)
    #print(img_src_list)
    for src in img_src_list:
        img_data = requests.get(src, headers=headers).content
        img_name = src.split('/')[-1]
        img_path = 'imglibs/' + img_name
        with open(img_path, 'wb') as fp:
            fp.write(img_data)
            print(img_name, '成功下载')