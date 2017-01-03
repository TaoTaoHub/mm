import urllib.request
import urllib.error
import os
from bs4 import BeautifulSoup

class Spider:
    mainPage = ''
    root = ''
    maxPage = ''
    tree = {}

    def __init__(self, mainPage, maxPage, root):
        self.mainPage = mainPage
        self.maxPage = maxPage
        self.root = root

    #解析html
    def __getHtmlContent(self, url):
        try:
            res = urllib.request.urlopen(url, timeout=5)
            html = res.read().decode('utf-8')
            return BeautifulSoup(html)
        except urllib.error.HTTPError:
            print('timeout')
            return ''
        except Exception:
            return ''

    #保存图片
    def __saveImage(self, url, path, filename):
        try:
            if not os.path.exists(path):
                os.makedirs(path)
            if os.path.exists(path+filename):
                return ''
            img = urllib.request.urlopen(url, timeout=5)
            img = img.read()
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


    #得到一个女孩的图片地址列表
    def __getOneGirlImageUrls(self, url):
        list = []
        try:
            #得到每个人的总页数
            totalPage = self.__getHtmlContent(url).find(id = 'opic').previous_sibling.string
            for page in range(1, int(totalPage)):
                page = str(page)
                html = self.__getHtmlContent(url + '/' + page)
                res = html.find(id='content')
                src = res.a.img['src']
                list.append(src)
        except Exception:
            print('wrong')
        return list


    #得到网站图片url树形结构
    def __getNodeTree(self):
        for page in range(1, self.maxPage):
            page = str(page)
            self.tree[page] = {}
            mainHtml = self.__getHtmlContent(self.mainPage+'/'+page)
            try:
                images = mainHtml.find_all('li')
                for li in images:
                    coverImg = li.a.img['src']
                    coverName = li.a.img['alt']
                    coverUrl = li.a['href']
                    self.tree[page][coverImg] = {}
                    temp = {'name':'', 'img':'', 'list':[]}
                    temp['name'] = coverName
                    temp['img'] = coverImg
                    temp['list'] = self.__getOneGirlImageUrls(coverUrl)
                    self.tree[page][coverImg] = temp
                    print(temp)
            except Exception:
                print('wrong')
        print(self.tree)


    def __parserTree(self):
        for page in self.tree:
            for coverImg in self.tree[page]:
                coverImg = self.tree[page][coverImg]['img']
                coverName = self.tree[page][coverImg]['name']
                coverList = self.tree[page][coverImg]['list']
                path = self.root+'/'+str(page)+'/'+coverName+'/'
                filename = 'cover.jpg'
                self.__saveImage(coverImg, path, filename)
                print(path + filename)
                i = 1
                for list in coverList:
                    filename = str(i)+'.jpg'
                    self.__saveImage(list, path, filename)
                    i += 1
                    print(path + filename)


    def run(self):
        print('生成网站图片结构树....')
        self.__getNodeTree()
        print('网站结构树生成完毕，开始爬取图片....')
        self.__parserTree()
        print('爬取完毕！')

if __name__ == "__main__":
    spider = Spider('http://www.mmjpg.com/home', 2, 'image')
    print('进程开始....')
    spider.run()



























