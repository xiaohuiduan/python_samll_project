import requests
from bs4 import BeautifulSoup
import os

title= '王者'
os.mkdir(title)
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
for i in range(2, 50):
    list_url = 'http://www.netbian.com/s/wangzherongyao/index_'+str(i)+'.htm'
    list_source = requests.get(list_url, headers=headers).text
    list_soup = BeautifulSoup(list_source, 'lxml')
    page_urls = list_soup.find('div', {'class': 'list'}).find_all('li')
    for j in page_urls:
        second_url = 'http://www.netbian.com'+j.find('a')['href']
        try:
            second_source = requests.get(second_url, headers=headers).text
        except:
            print(' ')
        second_soup = BeautifulSoup(second_source, 'lxml')
        second_page_urls = second_soup.find('div', {'class': 'pic'}).find_all('p')
        for each in second_page_urls:
            third_url = 'http://www.netbian.com'+each.find('a')['href']
            # print(third_url)
            third_request = requests.get(third_url,headers = headers)
            third_pagesource = third_request.text
            third_soup = BeautifulSoup(third_pagesource,'lxml')
            img_name = third_soup.find('title').text
            # print(img_name)
            try:
              img_source = third_soup.find('table', {'id': 'endimg'}).find_all('img')#找到图片标签
            except:
                print(' ')
            # print(img_source)
            for img in img_source:
                url = img['src']
                print(url)
                img = requests.get(url, headers=headers).content
                f = open(title+'\\'+img_name + '.jpg', 'wb')
                f.write(img)
                f.close()




