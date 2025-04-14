import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from typing import List
import re
import logging

# 链家基础地址
BASE_URL = 'https://sz.lianjia.com'
CHENGJIAO_URL = f'{BASE_URL}/chengjiao/'
# 登录后从浏览器接口中获取
COOKIE = 'SECKEY_ABVK=IgUop9LRUyQZmxW/HREC5c8OZbVYTPZC/z44HQNVFp8%3D; BMAP_SECKEY=_ywz9lThlRaTr9LiMxerbhBscV4uB9R2g3YxI3zuXe8JDZ3qZPuP5-1-4KCjFPFaFiGtHH8qg5h2GGhxbtZqlVRKTOemBPELqMD9VggBxvmYVNwblAnocaosDlSlsxUF-rNQFCsfKjRZOXlEW7C_li3axdLeVsNTO6gejdq4h5hVKIILxQyOUzgqPD9L3lve; lianjia_uuid=03957efd-b052-49a0-aa93-ef37973cdd7e; crosSdkDT2019DeviceId=-w3922v-iyxcy5-97ut3olr53ydoh9-4hwrwxxg1; lfrc_=ca088554-12b8-46c5-80c4-a83f63b357fc; _ga=GA1.2.50611551.1741189542; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2219566fbc4a44fe-0a59fd2e2ee45c-26001051-1024000-19566fbc4a51455%22%2C%22%24device_id%22%3A%2219566fbc4a44fe-0a59fd2e2ee45c-26001051-1024000-19566fbc4a51455%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; ftkrc_=2ab1a6e1-7332-4f25-87d3-06b0f2449800; mp_8b1215dbcc852955566c4df66e547374_mixpanel=%7B%22distinct_id%22%3A%20%2219566fb402be7e-0a8036db9059bc-26001051-fa000-19566fb402c1395%22%2C%22%24device_id%22%3A%20%2219566fb402be7e-0a8036db9059bc-26001051-fa000-19566fb402c1395%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%2C%22__mps%22%3A%20%7B%7D%2C%22__mpso%22%3A%20%7B%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%7D%2C%22__mpus%22%3A%20%7B%7D%2C%22__mpa%22%3A%20%7B%7D%2C%22__mpu%22%3A%20%7B%7D%2C%22__mpr%22%3A%20%5B%5D%2C%22__mpap%22%3A%20%5B%5D%2C%22%24search_engine%22%3A%20%22bing%22%7D; select_city=440300; lianjia_ssid=ee172019-4054-463b-b3c3-8383edf5c6e0; login_ucid=2000000470822752; lianjia_token=2.001045f11e46ceb39201e8d82f9708fb03; lianjia_token_secure=2.001045f11e46ceb39201e8d82f9708fb03; security_ticket=dqoz9fn/oNeVo38AYAjeXeKCYgl8Tuj6d7F4VutT9ujIusbG25i3P0RL+Syn9gsTexh0w5plm1eODwhgyhpEN/9ORsQsEEkQ+R13Z8RW3SzqlgQ6e4Rhv3hfrzh+elgoYkCLdsIRPT+JHcpg1m8zjwtjKbJ6gY3+m40TcYWtEBs=; _jzqa=1.1154581109497148700.1741189531.1743000207.1744642681.9; _jzqc=1; _jzqx=1.1741189531.1744642681.5.jzqsr=clogin%2Elianjia%2Ecom|jzqct=/.jzqsr=clogin%2Elianjia%2Ecom|jzqct=/; _jzqckmp=1; _qzjc=1; Hm_lvt_46bf127ac9b856df503ec2dbf942b67e=1743000207,1744642689; HMACCOUNT=7825B90E2E271E43; _gid=GA1.2.418670882.1744642692; _qzja=1.2073338545.1741189530617.1743000207024.1744642681349.1744642716605.1744642749301.0.0.0.48.9; _qzjb=1.1744642681349.6.0.0.0; _qzjto=6.1.0; _jzqb=1.6.10.1744642681.1; Hm_lpvt_46bf127ac9b856df503ec2dbf942b67e=1744642749; srcid=eyJ0Ijoie1wiZGF0YVwiOlwiODRhZmRmZDUwNWQ5MjNlNmIyZjM0ZWNkNjhhOGI1Yzg5YTkwYjY4OGExMzJiOTBkZGVkMGVkMTc4NDgyOTg3ZDA1N2Q0ZTkxNjM3MTFjOGEzYTlhNTIxNmY2MDk5OTMzOGFhYjQ3NjEzMzA0YmQwYWU2NDQ5YTg1ZjZlZDVmZTU5NGMwM2Y3MTEwZGFjNDVkYjg3YzA0MzMxMzJhYTc2YjY5MjZjZTExZTQxNDEzZGZhNTJjOWNmOTE1OTY2ZTM3NTA3YmUyMTA2NWRkNmVlMzUwYmEyYjE1OGQ1NTcxZDdhN2UxZTlkMmU1Y2Q5Yzc2YTE1NDc4MTEzOTU4YTNhOFwiLFwia2V5X2lkXCI6XCIxXCIsXCJzaWduXCI6XCI2MjI1MGI5NVwifSIsInIiOiJodHRwczovL3N6LmxpYW5qaWEuY29tL2NoZW5namlhby8iLCJvcyI6IndlYiIsInYiOiIwLjEifQ==; _gat=1; _gat_global=1; _gat_new_global=1; _gat_dianpu_agent=1; _ga_C4R21H79WC=GS1.2.1744642692.9.1.1744642762.0.0.0'
# 结果储存位置
OUT_DIR = './output'


"""
获得页面html解析后的soup对象
"""
def get_html_soup(url:str) -> BeautifulSoup:
    # 设置请求头，模拟浏览器访问
    headers = {
        "Cookie": COOKIE,
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
    }
    # 发送GET请求
    response = requests.get(url=url, headers=headers)
    if response.status_code != 200:
        print(f"页面 {url} 请求失败，状态码：{response.status_code}")
        return None
    return BeautifulSoup(response.text, "html.parser")


"""
获得成交页面所有列表页信息[[xxx,xxx],[xxx,xxx],...]
"""
def get_chengjiao_info_by_page(start_page:int, end_page:int) -> List[List[str]]:
    all_data = []
    # 遍历每一页得到
    for page in range(start_page, end_page+1):
        url = ''
        if page == 1:
            url = CHENGJIAO_URL
        else:
            url = f"{CHENGJIAO_URL}pg{page}/"
        print(f"正在爬取：{url}")
        page_data = get_chengjiao_info(url)
        all_data += page_data
        # 阻塞5秒模拟人类分页访问
        time.sleep(5)
    return all_data


"""
获得单个成交页面的信息[[xxx,xxx],[xxx,xxx],...]
"""
def get_chengjiao_info(url:str) -> List[List[str]]:
    soup = get_html_soup(url)
    if soup == None:
        return []
    house_list:List[BeautifulSoup] = soup.find_all('div', class_='info')
    # 遍历house_list找到你需要的信息
    data = [] # 二维数组
    for house in house_list:
        try:
            ############# TODO:根据标签找到你所需要的信息 #############
            title_div = house.find('div', class_='title')
            title = title_div.text.strip()
            link = title_div.find('a').get('href')
            id = parse_house_id(link)
            dealDate = house.find("div", class_="dealDate").text.strip()
            # TODO:把上面所有的变量都按字段顺序放进来
            row = [id, title, dealDate, link] 
            #########################################################
            data.append(row)
        except Exception as e:
            print(f"爬取 {url} 失败")
            logging.exception(e)
            
    return data



def get_chengjiao_details(url_list:List[str]) -> List[List[str]]:
    details = []
    for url in url_list:
        print(f"正在爬取：{url}")
        detail = get_chengjiao_detail(url)
        details.append(detail)
        # 阻塞5秒模拟人类分页访问
        time.sleep(5)
    return details


"""获得单个成交页面的详情信息"""
def get_chengjiao_detail(url:str) -> List[str]:
    soup = get_html_soup(url)
    if soup == None:
        return []
    # 返回结果为一维数组
    data = []
    try:
        # 从url中解析单个成交的id
        id = parse_house_id(url)
        data.append(id)

        # 解析线上信息
        msg = soup.find('div', class_='msg')
        span_tags:List[BeautifulSoup] = msg.find_all('span')
        msg_labels = ['挂牌价格（万）', '成交周期（天）', '调价（次）', '带看（次）', '关注（人）', '浏览（次）']
        msg_data = [''] * len(msg_labels)
        for span in span_tags:
            # 获得标签值
            value = span.find('label').get_text(strip=True)
            # 获得标签名
            name = span.get_text(strip=True).replace(value, '')
            if name in msg_labels:
                # 保证返回结果和标签一致
                index = msg_labels.index(name)
                msg_data[index] = value
        data += msg_data

        # 解析基本属性
        base = soup.find('div', class_='base')
        li_tags:List[BeautifulSoup] = base.find_all('li')
        base_labels = ['房屋户型', '建成年代', '装修情况', '梯户比例', '配备电梯']
        base_data = [''] * len(base_labels)
        for li in li_tags:
            # 获得标签名
            name = li.find('span').get_text(strip=True)
            # 获得标签值
            value = li.get_text(strip=True).replace(name, '')
            if name in base_labels:
                # 保证返回结果和标签一致
                index = base_labels.index(name)
                base_data[index] = value
        data += base_data

        # TODO: 添加交易属性信息
    except Exception as e:
        print(f"爬取 {url} 失败")
        logging.exception(e)
    return data
   

"""保存文件到csv"""
def save_as_csv(data:List[List[str]], columns:List[str], file_name:str) -> None:
    df = pd.DataFrame(data, columns=columns)
    file_path = f'{OUT_DIR}/{file_name}.csv'
    df.to_csv(file_path, index=False, encoding="utf-8-sig")
    print(f"爬取完成，数据已保存到{file_path}")



"""从链接中解析house的id"""
def parse_house_id(url:str) -> str:
    # 定义更通用的正则表达式模式
    pattern = r'https?://[^/]+/chengjiao/(\d+)\.html'
    # 使用re.search匹配URL
    match = re.search(pattern, url)
    
    # 如果匹配成功，返回ID
    if match:
        return match.group(1)
    else:
        return None


"""获取二级区域的链接"""
def get_sub_area_links() -> None:
    print(f'正在爬取{CHENGJIAO_URL}')
    soup = get_html_soup(CHENGJIAO_URL)
    if soup == None:
        return
    # 获得一级地址
    ershoufang_div = soup.find('div', attrs={'data-role': 'ershoufang'})
    a_tags:List[BeautifulSoup] = ershoufang_div.find_all("a")
    area_urls = [f'{BASE_URL}{a.get("href")}' for a in a_tags]
    # 阻塞5秒模拟人类分页访问
    time.sleep(5)
    # 获得二级地址
    sub_area_urls = []
    for area_url in area_urls:
        print(f'正在爬取{area_url}')
        sub_soup = get_html_soup(area_url)
        if soup == None:
            continue
        ershoufang_div = sub_soup.find('div', attrs={'data-role': 'ershoufang'})
        divs:List[BeautifulSoup] = ershoufang_div.find_all('div', recursive=False)
        second_div = divs[1]
        a_tags = second_div.find_all('a')
        sub_area_urls += [f'{BASE_URL}{a.get("href")}' for a in a_tags]
        # 阻塞5秒模拟人类分页访问
        time.sleep(5)
    # 导出为csv
    save_as_csv(sub_area_urls, ['二级地址链接'], '二级地址链接')
    


# 程序主入口
if __name__ == "__main__":
    house_info = get_chengjiao_info_by_page(1, 1)
    # TODO: 把字段对应的表头顺序一一对应补充到这里
    info_columns = ['id', '标题', '成交日期', '链接']
    save_as_csv(house_info, info_columns, '成交列表信息_P1')
    # 拿到所有详情url
    detail_urls = [row[-1] for row in house_info]
    house_details = get_chengjiao_details(detail_urls)
    detail_columns = ['id', '挂牌价格（万）', '成交周期（天）', '调价（次）', '带看（次）', '关注（人）', '浏览（次）','房屋户型', '建成年代', '装修情况', '梯户比例', '配备电梯']
    save_as_csv(house_details, detail_columns, '成交房屋详情_P1')
    # get_sub_area_links()