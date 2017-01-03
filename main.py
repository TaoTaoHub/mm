import urllib.request
import urllib.error
import os
from bs4 import BeautifulSoup


def getHtmlContent(url):
    try:
        res = urllib.request.urlopen(url, timeout=5)
        html = res.read().decode('utf-8')
        return BeautifulSoup(html)
    except urllib.error.HTTPError:
        print('timeout')
        return ''
    except Exception:
        return ''

def saveImage(url, path, filename):
    try:
        img = urllib.request.urlopen(url, timeout=5)
        img = img.read()
        if not os.path.exists(path):
            os.makedirs(path)
        if(os.path.exists(path+filename)):
            return ''
        file = open(path+filename, 'wb')
        file.write(img)
        file.close()
        return ''
    except urllib.error.HTTPError:
        print('timeout')
        return ''
    except Exception:
        print('wrong')
        return ''



def getOneGirlImageUrl(url, page):
    page = str(page)
    html = getHtmlContent(url+'/'+page)
    try:
        res = html.find(id='content')
        src = res.a.img['src']
        return src
    except Exception:
        print('wrong')


def getMainPage(url, mainPage):
    mainPage = str(mainPage)
    mainHtml = getHtmlContent(url+'/home/'+mainPage)
    images = mainHtml.find_all('li')
    for x in images:
        path = 'image/'+mainPage+'/'+x.a.img['alt']+'/'
        filename = 'cover.jpg'
        url = x.a.img['src']
        #保存封面
        saveImage(url, path, filename)

        #保存大图
        oneGirlUrl = x.a['href']
        #得到每个人的总页数
        page = getHtmlContent(oneGirlUrl).find(id = 'opic').previous_sibling.string
        page = int(page)
        while page >= 1:
            filename = str(page)+'.jpg'
            url = getOneGirlImageUrl(oneGirlUrl, page)
            saveImage(url, path, filename)
            page -= 1
            print(path+filename+'\n')


if __name__ == "__main__":
    getMainPage('http://www.mmjpg.com/', 1)