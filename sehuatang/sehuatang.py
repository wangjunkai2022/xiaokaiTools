import httpx
import bs4
import asyncio
import re

domain = "www.sehuatang.org"
proxy = None
cookie = "cPNj_2132_saltkey=jPh8px1f; _safe=vqd37pjm4p5uodq339yzk6b7jdt6oich"
headers = {
    "cookie": cookie,
}


async def _get_form_hash():
    async with httpx.AsyncClient(proxies=proxy) as client:
        response = await client.get(domain, headers=headers)
        soup = bs4.BeautifulSoup(response.text, "html.parser")
        formhash = soup.find(name="input", attrs={"name": "formhash"})
        print(formhash["value"])
        return formhash['value']


# 更具名字（番号）等关键字搜索sehuatang的磁力连接
# 返回搜到的磁力 这里是个磁力集合
async def SearchNumberToMagnets(text):
    formHash = await _get_form_hash()
    data = "formhash={}&srchtxt={}&searchsubmit=yes".format(formHash, text)
    url = "https://" + domain + "/search.php?mod=forum" + "&" + data
    async with httpx.AsyncClient(proxies=proxy) as client:
        response = await client.post(url, headers=headers)
        if response.status_code == 302 and response.next_request:
            print(response.next_request.url)
            response = await client.get(response.next_request.url, headers=headers)
        soup = bs4.BeautifulSoup(response.text, "html.parser")
        allSearch = soup.find(id="threadlist").find_all("li")
        magnets = []
        for li in allSearch:
            a = li.find("a")
            li_url = a["href"]
            response = await client.post(domain + "/" + li_url, headers=headers)
            soup = bs4.BeautifulSoup(response.text, "html.parser")
            magnet = None
            try:
                magnet = soup.find("div", class_="blockcode").find("li").get_text()
            except:
                magnet = None
            if magnet and magnet.startswith("magnet"):
                magnets.append(magnet)
        magnets = list(set(magnets))
        return magnets


# 爬取对应sehuatang的某板块的的某一页的tid（帖子ID）
# fid:
#    103: 高清中文字幕
#    104: 素人有码系列
#    37: 亚洲有码原创
#    36: 亚洲无码原创
#    39: 动漫原创
#    160: vr
#    151: 4k
#    2: 国产原创
#    38: 欧美无码
#    107: 三级写真
#    152: 韩国主播
# return 所有的tid（可以更具tid获取具体的页面中的数据）
async def ReptileFid(fid, page):
    tids = []
    url = "https://{}/".format(domain)
    # headers
    headers = {
        "cookie": cookie,
    }
    # 参数
    params = {
        "mod": "forumdisplay",
        "fid": fid,
        "page": page,
    }
    async with httpx.AsyncClient(proxies=proxy) as client:
        response = await client.get(url, params=params, headers=headers)
    # 使用bs4解析
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    # print(soup)
    all = soup.find_all(id=re.compile("^normalthread_"))
    try:
        for i in all:
            id = i.find(class_="showcontent y").attrs["id"].split("_")[1]
            tids.append(id)
    except Exception as e:
        print(e)
    return tids


# 更具tid获取磁力连接
# return 磁力
async def GetTidMagent(tid):
    url = "https://{}/?mod=viewthread&tid={}".format(domain, tid)
    # headers
    headers = {
        "cookie": cookie,
    }

    try:
        async with httpx.AsyncClient(proxies=proxy) as client:
            response = await client.get(url, headers=headers)

        soup = bs4.BeautifulSoup(response.text, "html.parser")
        return soup.find("div", class_="blockcode").find("li").get_text()

    except Exception as e:
        print(e)


if __name__ == '__main__':
    # asyncio.run(getMagnets("IPX-567"))
    loop = asyncio.get_event_loop()
    get_future = asyncio.ensure_future(SearchNumberToMagnets("IPZ-299"))  # 相当于开启一个future
    loop.run_until_complete(get_future)  # 事件循环
    magnets = get_future.result()
    print(magnets)  # 获取结果
