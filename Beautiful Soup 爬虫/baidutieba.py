
import requests
from bs4 import BeautifulSoup

def get_html(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = 'utf-8'
        return r.text
    except:
        return " ERROR "

def get_content(url):

    comments = []

    html = get_html(url)

    soup = BeautifulSoup(html, 'lxml')

    liTags = soup.find_all('li', attrs={'class': 'j_thread_list'})

    for li in liTags:

        comment = {}
        comment['title'] = li.find('a', class_='j_th_tit').string
        comment['link'] = 'http://tieba.baidu.com' + li.find('a', class_='j_th_tit').get('href')
        comment['name'] = li.find('a', class_='frs-author-name').string
        comment['time'] = li.find('span', class_='is_show_create_time').string
        comment['replyNum'] = li.find('span', class_='threadlist_rep_num').string
        comments.append(comment)

    return comments

def Out2File(dict):
    with open('TTBT.txt', 'a+', encoding='utf-8') as f:
        for comment in dict:
            f.write('标题： {} \t 链接：{} \t 发帖人：{} \t 发帖时间：{} \t 回复数量： {} \n'.format(
                comment['title'], comment['link'], comment['name'], comment['time'], comment['replyNum']))

        print('当前页面爬取完成')

def main(base_url, deep):
    url_list = []
    for i in range(0, deep):
        url_list.append(base_url + '&pn=' + str(50 * i))
    print('所有的网页已经下载到本地！ 开始筛选信息。。。。')

    for url in url_list:
        content = get_content(url)
        Out2File(content)
    print('所有的信息都已经保存完毕！')

base_url = 'http://tieba.baidu.com/f?kw=%E7%94%9F%E6%B4%BB%E5%A4%A7%E7%88%86%E7%82%B8'
deep = 3

if __name__ == '__main__':
    main(base_url, deep)
