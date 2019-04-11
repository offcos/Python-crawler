import requests
import bs4


def get_html(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status
        r.encoding = ('utf-8')
        return r.text
    except:
        return "Someting Wrong！"


def get_content(url):
    '''
    爬取每一类型小说排行榜，
    按顺序写入文件，
    文件内容为 小说名字+小说链接
    将内容保存到列表
    并且返回一个装满url链接的列表
    '''
    url_list = []
    html = get_html(url)
    soup = bs4.BeautifulSoup(html, 'lxml')

    category_list = soup.find_all('div', class_='index_toplist')

    for cate in category_list:
        name = cate.find('div', class_='toptab').span.string
        with open('novel_list.csv', 'a+', encoding='utf-8') as f:
            f.write("\n小说种类：{} \n".format(name))

        general_list = cate.find(style='display: block;')

        book_list = general_list.find_all('li')
        for book in book_list:
            link = 'http://www.qu.la/' + book.a['href']
            title = book.a['title']
            url_list.append(link)
            with open('novel_list.csv', 'a', encoding='utf-8') as f:
                f.write("小说名：{:<} \t 小说地址：{:<} \n".format(title, link))

    return url_list


def get_txt_url(url):
    '''
    获取该小说每个章节的url地址：
    并创建小说文件
    '''
    url_list = []
    html = get_html(url)
    soup = bs4.BeautifulSoup(html, 'lxml')
    lista = soup.find_all('dd')
    txt_name = soup.find('h1').string
    with open('D:/Django/python-crawler/小说/{}.txt'.format(txt_name), "a+", encoding='utf-8') as f:
        f.write('小说标题：{} \n'.format(txt_name))
    for url in lista:
        u = url.a['href']
        if u.startswith('/book'):
            url_list.append('http://www.qu.la/' + u)

    return url_list, txt_name


def get_one_txt(url, txt_name):
    '''
    获取小说每个章节的文本
    并写入到本地
    '''
    html = get_html(url).replace('<br />', '\n')
    soup = bs4.BeautifulSoup(html, 'lxml')
    try:
        txt = soup.find('div', id='content').get_text().replace('chaptererror();', '')
        title = soup.find('h1').string

        with open('D:/Django/python-crawler/小说/{}.txt'.format(txt_name), "a", encoding='utf-8') as f:
            f.write(title)
            f.write(txt)
            print('当前小说：{} 当前章节{} 已经下载完毕'.format(txt_name, title))
    except (OSError, TypeError, ValueError, AttributeError, NameError, SyntaxError) as reason:
        print(reason)


def get_all_txt(url_list):
    '''
    下载排行榜里所有的小说
    并保存为txt格式
    '''
    for url in url_list:
        page_list, txt_name = get_txt_url(url)
        
        for page_url in page_list:
            get_one_txt(page_url, txt_name)
            #print('当前进度 {}% '.format(url_list.index(url) / len(url_list) * 100))
        

def main():
    base_url = 'http://www.qu.la/paihangbang/'
    url_list = get_content(base_url)
    url_list = list(set(url_list))
    get_all_txt(url_list)


if __name__ == '__main__':
    main()
