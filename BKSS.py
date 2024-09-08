from urllib.parse import quote
import json
import requests
if __name__ == '__main__':
    storeProvince = input('请输入省级位置')
    storeCity = input('请输入地级市')
    position = input('请输入想要查询的位置')
    filename = position + '的汉堡王.json'
    headers = {
        'user-agent':'Mozilla/5.0(Windows NT 10.0; Win64; x64)\
        AppleWebKit/537.36(KHTML, like Gecko)\
        Chorme/128.0.0.0 Safari/537.36'      
    }
    for i in range(1, 6):
        url = 'https://www.bkchina.cn/restaurant/getMapsListAjax?page='+str(i)+'&storeProvince='\
        +quote(storeProvince,encoding='utf-8')+'&storeCity='\
        +quote(storeCity,encoding='utf-8')+'&localSelect=&search='\
        +quote(position,encoding='utf-8')
        response = requests.get(url=url, headers=headers)
        page_text = response.json()
        data_trim = page_text['data']['data']
        with open(filename, 'a', encoding='utf-8') as fp:
            if data_trim:
                json.dump(data_trim, fp=fp, ensure_ascii=False)
                fp.write('\n')
                for j in range(len(data_trim)):
                    storeAddress = data_trim[j]['storeAddress']
                    storeName = data_trim[j]['storeName']
                    finalMessage = storeName + '店，具体位置位于：' + storeAddress
                    print(finalMessage)
    print('搜索完成')