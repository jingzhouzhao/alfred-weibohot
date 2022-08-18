import json
import os
import requests
import random


def get_headers():
    ag_list = [
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Mozilla/5.0 (Windows NT 6.1; rv2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
        "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11"
    ]
    return random.choice(ag_list)


def urldownload(url, filename=None):
    """
    下载文件到指定目录
    :param url: 文件下载的url
    :param filename: 要存放的目录及文件名，例如：./test.xls
    :return:
    """
    down_res = requests.get(url)
    with open(filename, 'wb') as file:
        file.write(down_res.content)


def get_weibo():
    session = requests.Session()
    headers = {'User-Agent': get_headers()}
    url = "https://m.weibo.cn/api/container/getIndex?containerid=106003type%3D25%26t%3D3%26disable_hot%3D1%26filter_type%3Drealtimehot&title=%E5%BE%AE%E5%8D%9A%E7%83%AD%E6%90%9C&extparam=seat%3D1%26cate%3D10103%26region_relas_conf%3D0%26dgr%3D0%26pos%3D0_0%26mi_cid%3D100103%26filter_type%3Drealtimehot%26c_type%3D30%26recommend_tab%3D0%26lcate%3D1001%26display_time%3D1660804469%26pre_seqid%3D672158790&luicode=10000011&lfid=231583"
    # 向url发送对应请求
    json_str = session.get(url, headers=headers).text
    jsonData = json.loads(json_str)
    group = jsonData['data']['cards'][0]['card_group']
    data = []
    for card in group:
        icon_url = card.get('pic', '')
        icon_path = ''
        if icon_url != '':
            icon_name = str(icon_url).removeprefix('https://simg.s.weibo.com')
            icon_path = "./icons" + icon_name
            if not os.path.exists(icon_path):
                urldownload(icon_url, icon_path)
        data.append({
            "title": card['desc'],
            "subtitle": card.get('desc_extr', '置顶'),
            "arg": card['scheme'],
            "icon": {
                # "type": "fileicon",
                "path": icon_path
            }
        })
    return data


def main():
    results = get_weibo()
    data = {"items": []}
    for res in results:
        data['items'].append(res)
    print(json.dumps(data))


if __name__ == '__main__':
    main()
