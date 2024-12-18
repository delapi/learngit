import requests
from lxml import etree
import re
import os

if __name__ == '__main__':
    headers = {
        'user-agent':'Mozilla/5.0(Windows NT 10.0; Win64; x64)\
        AppleWebKit/537.36(KHTML, like Gecko)\
        Chorme/131.0.0.0 Safari/537.36'      
    }
    url0 = 'https://yanjiu.lgmi.com//yj_TTC2_list.htm'
    url = 'https://yanjiu.lgmi.com//yj_TTC2_list%d.htm'

    download_list = []
    download_name_list = []
    if not os.path.exists('langemoron'):
        os.mkdir('langemoron')
    for pageNum in range(1,3):
        if pageNum == 1:
            real_url = url0
        else:
            real_url = url % pageNum
        page_text = requests.get(real_url, headers=headers).text
        tree = etree.HTML(page_text)
        essay_list = tree.xpath('//div[@class="listing-adv top"]/ul/li')
        for essay in essay_list:
            essay_src = essay.xpath('./a/@href')
            if essay_src:
                real_new_url = 'https:%s'
                a = real_new_url % essay_src[0]
                essay_text = requests.get(a, headers=headers).text                
                estree = etree.HTML(essay_text)
                header = estree.xpath('//title/text()')[0].encode('iso-8859-1').decode('GBK')
                banner = '.*?([0-9]+[\u6708]{1}).*'
                name = re.findall(banner, header)
                if name:
                    download_name_list.append(name[0])
                    content = estree.xpath('//div[@class="t3"]/p')[0]
                    patch = content.xpath('string(.)').encode('iso-8859-1').decode('GBK')
                    download_list.append(patch + '\n')
    
    
    
    i = -1
    for name in download_name_list:
        i += 1
        lange_path = 'langemoron/' + download_name_list[i] + '.txt'
        with open(lange_path, 'a') as fp:
            fp.write(download_list[i])
            print('兰格的第'+ str(i+1) + '条废话已收录')
        with open(lange_path, 'r') as fq:
            lines = fq.readlines()
        lines = list(set(lines))
        with open(lange_path, 'w') as fr:
            fr.writelines(lines)
    print('全部完成')