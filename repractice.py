import requests
from lxml import etree
import os

if __name__ == '__main__':
    headers = {
        'user-agent':'Mozilla/5.0(Windows NT 10.0; Win64; x64)\
        AppleWebKit/537.36(KHTML, like Gecko)\
        Chorme/107.0.0.0 Safari/537.36'      
    }
    url0 = 'https://sc.chinaz.com/jianli/free.html'
    url = 'https://sc.chinaz.com/jianli/free_%d.html'
    pageNum = 1

    download_list = []
    download_name_list = []
    if not os.path.exists('./CV_template'):
        os.mkdir('./CV_template')
    for pageNum in range(1,3):
        if pageNum == 1:
            new_url = url0
        else:
            new_url = format(url % pageNum)
        page_text = requests.get(url=new_url, headers=headers).text
        tree = etree.HTML(page_text)
        CV_infor_list = tree.xpath('//div[@class="main_list jl_main"]/div')
        for cv in CV_infor_list:
            CV_src = cv.xpath('./a/@href')[0]
            print(CV_src)
            '''CV_text = requests.get(url=CV_src,headers=headers).text
            ctree = etree.HTML(CV_text)
            download_src = ctree.xpath('//div[@class="down_wrap"]/div[2]/ul/li/a/@href')[0]
            download_list.append(download_src)
            download_name = ctree.xpath('//div[@class="ppt_tit clearfix"]/h1/text()')[0]
            download_name = download_name.encode('iso-8859-1').decode('utf-8') + '.rar'
            download_name_list.append(download_name)


    i = -1
    for cvv in download_list:
        i += 1
        cvv = download_list[i]
        cv_content = requests.get(url=cvv, headers=headers).content
        cv_path = 'CV_template/' + download_name_list[i]
        with open(cv_path, 'wb') as fp:
            fp.write(cv_content)
            print(download_name_list[i] + '下载成功！')'''