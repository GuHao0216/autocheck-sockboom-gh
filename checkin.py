import requests
import json
import argparse
import os
import time
from bs4 import BeautifulSoup
from requests.packages.urllib3.exceptions import InsecureRequestWarning
# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
}


# 设置一个全局参数存储打印信息，最后好推送
contents = ''

checkUrl = 'https://sockboom.best'

def output(content):
    global contents
    contents += '\n'+content
    print(content)


def sign(header,email,passwd):
    url = checkUrl+'/auth/login?email='+email+'&passwd='+passwd+''
    response = requests.post(url=url, headers=header, verify=False)
    sign_message = json.loads(response.text)['msg']
    user = json.loads(response.text)['user']
    output('  [+]'+sign_message+'，用户：'+user)
    cookie = response.headers
    cookie_uid = cookie['Set-Cookie'].split('/')[0].split(';')[0]
    cookie_email = email
    cookie_key = cookie['Set-Cookie'].split('/')[2].split(';')[0].split(',')[1]
    cookie_ip = cookie['Set-Cookie'].split('/')[3].split(';')[0].split(',')[1]
    cookie_expire_in = cookie['Set-Cookie'].split('/')[4].split(';')[
        0].split(',')[1]
    Cookie = cookie_uid+';'+cookie_email+';' + \
        cookie_key+';'+cookie_ip+';'+cookie_expire_in
    return Cookie


def user_centre(cookie):  # 用户中心
    url = checkUrl+'/user'
    headers = {
        'Cookie': cookie
    }
    response = requests.get(url=url, headers=headers, verify=False)
    soup = BeautifulSoup(response.text, 'html.parser')  # 解析html页面
    # 获取流量信息
    flows = soup.select('span[class="pull-right strong"]')
    flow = [flow.string for flow in flows]
    output('  [+]总流量:'+flow[0])
    output('  [+]使用流量:'+flow[1])
    output('  [+]剩余流量:'+flow[2])
    output('  [+]可用天数:'+flow[3])
    return headers


def checkin(headers):
    url = checkUrl+'/user/checkin'
    response = requests.post(url=url, headers=headers, verify=False)
    msg = json.loads(response.text)['msg']
    output('  [+]签到信息:'+msg)


def main(email,passwd):
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    cookie = sign(header,email,passwd)
    headers = user_centre(cookie)
    checkin(headers)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--email", dest="email")
    parser.add_argument("--p", dest="p")
    args = parser.parse_args()
    main(args.email,args.p)