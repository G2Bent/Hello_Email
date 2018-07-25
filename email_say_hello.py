#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import datetime
import smtplib
from email.mime.text import MIMEText
from email.header import Header

import requests
GIRL,BOY = "广州","深圳"
HEADERS = {
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36"
    "(KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
}
MAIL_HOST = os.environ.get('MAIL_HOST')
MAIL_USER = os.environ.get("MAIL_USER")
MAIL_PASS = os.environ.get("MAIL_PASS")

RECEIVER = ['648604875@qq.com']
SENDER = '944921374@qq.com'

#聚合数据天气预报 api
weather_api = 'https://www.sojson.com/open/api/weather/json.shtml?city={}'
#邮件内容
CONTENT_FORMAT = (
    "你好 😄 :\n\n\t"
    "今天是 {_date}，{_week}。\n\t"
    "首先，今天已经是我们认识的第 {_loving_days} 天了喔 💓。然后我就要来播送天气预报了！！\n\n\t"
    "广州明天{_g_weather_high}，{_g_weather_low}，天气 {_g_weather_type}，"
    "需要注意的是{_g_weather_notice}\n\n\t"
    "深圳明天{_b_weather_high}，{_b_weather_low}，天气 {_b_weather_type}，"
    "需要注意的是{_b_weather_notice}"
)

ANGRY_MSG = "😠，这又挂了喔！"


def get_weather_info():
    """
    获取天气信息
    """
    girl = requests.get(weather_api.format(GIRL, headers=HEADERS)).json()
    boy = requests.get(weather_api.format(BOY, headers=HEADERS)).json()

    girl_weather = girl["data"]["forecast"][1]
    boy_weather = boy["data"]["forecast"][1]

    _date, _week = get_today(girl)

    if girl and boy:
        return CONTENT_FORMAT.format(
            _week=_week,
            _date=_date,
            _loving_days=get_loving_days(),
            _g_weather_high=girl_weather["high"],
            _g_weather_low=girl_weather["low"],
            _g_weather_type=girl_weather["type"],
            _g_weather_notice=girl_weather["notice"],
            _b_weather_high=boy_weather["high"],
            _b_weather_low=boy_weather["low"],
            _b_weather_type=boy_weather["type"],
            _b_weather_notice=boy_weather["notice"],
        )


def get_loving_days():
    """
    获取恋爱天数
    """
    today = datetime.datetime.today()
    anniversary = datetime.datetime(2015, 7, 2)
    return (today - anniversary).days


def get_today(today):
    """
    格式化今天日期
    """
    date = today["date"]
    week = today["data"]["forecast"][0]["date"][-3:]
    return "{}-{}-{}".format(date[:4], date[4:6], date[6:]), week


def send_email():
    """
    发送邮件
    """
    try:
        content = get_weather_info()
    except Exception:
        try:
            content = get_weather_info()
        except Exception:
            content = ANGRY_MSG

    message = MIMEText(content, "plain", "utf-8")
    message["From"] = Header("哈哈哈", "utf-8")
    message["To"] = Header("A handsome soul")
    message["Subject"] = Header("😘 日常问候", "utf-8")
    try:
        smtp_obj = smtplib.SMTP_SSL(MAIL_HOST)
        smtp_obj.login(MAIL_USER, MAIL_PASS)
        smtp_obj.sendmail(SENDER, RECEIVER, message.as_string())
        smtp_obj.quit()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    send_email()