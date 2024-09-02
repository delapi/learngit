import requests
import json
if __name__ == '__main__':
    url = 'https://www.kfc.com.cn/kfccda/ashx/GetStoreList.ashx?op=keyword'
    headers = {
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
        Applewebkit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
    }
    city = input('请输入您所在的城市')
    position = input('请输入您要查询的位置')
    pageindex = 1
    filename = position + '肯德基餐厅位置信息' + '.json'
    for i in range(20):
        param = {
            'cname': city,
            'pid': '',
            'keyword': position,
            'pageIndex': pageindex,
            'pageSize': '10'
        }
        response = requests.post(url=url, params=param, headers=headers)
        page_text = response.text
        with open(filename, 'a', encoding= 'utf-8') as fp:
            json.dump(page_text, fp=fp, ensure_ascii= False)
            fp.write('\n')
        pageindex += 1
    print('全部查找完成')