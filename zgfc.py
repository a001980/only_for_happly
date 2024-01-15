#!/usr/bin/python3
# -- coding: utf-8 --
# -------------------------------
# @Author : github@wd210010 https://github.com/wd210010/only_for_happly
# @Time : 2024/1/15 9:23
# -------------------------------
# cron "0 0 8 * * *" script-path=xxx.py,tag=匹配cron用
# const $ = new Env('福彩抽奖')
import requests,json,os

#活动路径 中国福彩公众号 右下角新年活动
#手机号登录后 抓取https://ssqcx-serv.cwlo.com.cn域名下的请求头的Authorization 放入青龙变量或者放入config.sh 变量名为zgfcau 放在config.sh的话 多账号用&分割 放在青龙变量就多建几个变量

zgfcaulist =os.getenv("zgfcau").split('&')
#推送加 token
plustoken =os.getenv("plustoken")

def Push(contents):
  # plustoken推送
    headers = {'Content-Type': 'application/json'}
    json = {"token": plustoken, 'title': '中国福彩抽奖', 'content': contents.replace('\n', '<br>'), "template": "json"}
    resp = requests.post(f'http://www.pushplus.plus/send', json=json, headers=headers).json()
    print('push+推送成功' if resp['code'] == 200 else 'push+推送失败')


wishidlist =[]
for i in range(len(zgfcaulist)):
    print(f'账号{i+1}')
    headers ={
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.45(0x18002d2a) NetType/WIFI Language/zh_CN',
        'Authorization': zgfcaulist[i],
    }

    print('**开始发送愿望**')
    try:
        for j in range(1):
            resp = requests.post('https://ssqcx-serv.cwlo.com.cn/api/wish/send',headers=headers,data='wish=66666666')
            result = json.loads(resp.text)
            print(result)
            if j == 0:
                wish_id = result['data']['wish_id']
                wishidlist.append(wish_id)
    except:
        print('该Authorization可能无效！')
    print('**开始抽奖**')
    try:
        resp2 = requests.post('https://ssqcx-serv.cwlo.com.cn/api/lottery/start', headers=headers)
        result2 = json.loads(resp2.text)
        # print(result2)
        success = result2['msg']
        if success =='成功' and len(result2['data']['lottery_sn'])>0:
            massage = f'账号{i+1}中奖了！请自行查看'
            print(massage)
            Push(contents=massage)
        elif success =='成功' and len(result2['data']['lottery_sn'])==0:
            print('未中奖')
        else:
            print(success)
    except:
        print('该Authorization可能无效！')
print(wishidlist)
print('**开始点赞**')
for a in range(len(wishidlist)):
    for b in range(len(zgfcaulist)):
        headers2 = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.45(0x18002d2a) NetType/WIFI Language/zh_CN',
            'Authorization': zgfcaulist[b],
        }
        resp3 = requests.post('https://ssqcx-serv.cwlo.com.cn/api/wish/zan',headers=headers2,data=f'wish_id={wishidlist[a]}')
        result3 = json.loads(resp3.text)
        print(result3)