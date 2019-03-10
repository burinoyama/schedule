# -*- coding: UTF-8 -*-
import itchat
import matplotlib.pyplot as plt
import json
import jieba

import wordcount
from echarts import Echart, Legend, Pie
import re

plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False



"""
        pip install echarts-python
        pip install jieba
        pip install wordcloud
"""



def log():
    itchat.login()
    return itchat.get_friends(update=True)


def get_percent(friend):
    male = female = other = 0
    for i in friend[1:]:
        sex = i["Sex"]
        if sex == 1:
            male += 1
        elif sex == 2:
            female += 1
        else:
            other += 1
    return male, female, other


def write_data(friend):
    with open('./friend.txt', 'w') as f:
        json_friend = json.dumps(friend)
        print(json_friend)
        f.write(json_friend)


def draw_pie(lable, size, color, explode):
    plt.figure(figsize=(6, 9))
    plt.pie(size, explode=explode, labels=lable, colors=color, labeldistance=1.1, autopct='%3.1f%%', shadow=False,
            startangle=90, pctdistance=0.6)
    plt.axis('equal')
    plt.legend()
    plt.show()


# def draw_char(friends, lable, size):
#     char=Echart(u'%s的微信好友性别比例' %(friends[0]['NickName']), 'from Wechat')
#     char.use(Pie(
#         'WeChat',
#         [
#             {'value':male, 'name':label[0]}
#         ]
#     ))



def friend_signature(friends):
    sList = []
    for i in friends:
        signature = i["Signature"].replace(" ", "").replace("span", "").replace("class", "").replace("emoji", "")
        reg = re.compile("1f\d.+")
        signature = reg.sub("", signature)
        sList.append(signature)

    text = "".join(sList)
    word_list_jieba = jieba.cut(text, cut_all=True)
    wl_space_split = " ".join(word_list_jieba)

    my_word_count = wordcount().generate(wl_space_split)
    plt.imshow(my_word_count)
    plt.axis('off')
    plt.show()

if '__main__' == __name__:
    label = [u'男性好友', u'女性好友', u'其他']
    friend = log()
    write_data(friend)
    male, female, other = get_percent(friend)
    size = [male, female, other]
    color = ['red', 'yellowgreen', 'lightskyblue']
    explode = (0.05, 0, 0)
    draw_pie(lable=label, size=size, color=color, explode=explode)
