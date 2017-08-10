#coding=UTF-8

import requests
import urllib.request
import os
import bs4
from urllib import parse    #汉字转换gb2312格式
# 这是Python的一个非常有名的图片库，这里我们用它来显示验证码
from PIL import Image


def get_data(url, url_check):

    webpage=requests.get(url )
    Cookie = webpage.cookies    #获取访问教务处的cookie
    print(Cookie)
    for c in Cookie:
        cookie=c.name+'='+c.value 
    print(cookie)
    # 由于教务处Headers的Cookie格式问题，我们将其进行格式化保存，等会再解释哈
    #print(cookie)
    soup = bs4.BeautifulSoup(webpage.text, 'lxml')
    # 熬汤
    # 找到form的验证参数，教务处网站存在着验证---"__VIEWSTATE"
    __VIEWSTATE = soup.find('input', attrs={'name': '__VIEWSTATE'})['value']
    
    #验证码
    pic=requests.get(url_check,cookies=Cookie,headers=headers)
    
    with open(r'ver_pic.png','wb')as f:
        f.write(pic.content)

    ID=input("输入用户名: ")
    password=input("输入密码 ")
    
    # 打开验证码图片
    image = Image.open('{}/ver_pic.png'.format(os.getcwd()))
    image.show()
    ycode=input("输入弹出的验证码: ")
    
    student = "学生"
    res=student.encode('GBK')
    student = parse.quote(student)
    data={
             '__VIEWSTATE':__VIEWSTATE,
             'txtUserName':ID,
             'TextBox2':password,
             'txtSecretCode':ycode,
             'RadioButtonList1':student, #学生按钮的GB2312编码
             'Button1':"",
             'lbLanguage':'',
             'hidPdrs':'',
             'hidsc':'',
            }

    Log_url=r"http://222.24.19.201/default2.aspx"
                         
    r=requests.post(url=Log_url,data=data,headers=headers,cookies=Cookie)

    # 测试看看是否能找到登陆后的信息
    #print(r.headers)

    soup = bs4.BeautifulSoup(r.text, 'lxml')
    #print(soup.headers)
    try:
        name = soup.find('span', attrs={'id': 'xhxm'}).text
    except:
        name = '登录失败 '
    print(name)
    return name,cookie,ID


def get_request(name,cookie,ID):

    name = name[:-2]
    res=name.encode('GBK')
    name = parse.quote(res)

    #name.encoding='gb2312'


    print('http://222.24.19.201/xs_main.aspx?xh='+ID+'&xm='+name+'&gnmkdm=N121605')

    latest_headers={  
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',  
    'Referer':'http://222.24.19.201/xscjcx.aspx?xh='+ID+'&xm='+name+'&gnmkdm=N121605',
    'Cookie': cookie,
    #扩大适用性
    } 


    html = requests.get('http://222.24.19.201/xscjcx.aspx?xh='+ID+'&xm='+name+'&gnmkdm=N121605',headers=latest_headers) 
    soup = bs4.BeautifulSoup(html.text, 'lxml')
    #print(soup.text)

    # 找到form的验证参数
    __VIEWSTATE_1 = soup.find('input', attrs={'name': '__VIEWSTATE'})['value']
    name_1 = "历年成绩"
    res = name_1.encode('GBK')
    name_1 = parse.quote(res)

    data_1 = {
        '__VIEWSTATE':__VIEWSTATE_1,
        'btn_zcj': name_1,
    }

    html = requests.post('http://222.24.19.201/xscjcx.aspx?xh='+ID+'&xm='+name+'&gnmkdm=N121605',data = data_1, headers=latest_headers) 
    soup = bs4.BeautifulSoup(html.text, 'lxml')

    #print(soup.text)
    Score_lists = soup.find('table',attrs={'class': 'datelist'} )

    Score_subjects = Score_lists.find_all('tr')

    for trs in Score_subjects:
        #print(trs.text)
        for te in trs:
            try:
                te = te.string.lstrip() # 清除字符串左边的空格
            except:
                te = '无'
            print(te,end = '   ')
        print()
            
    #print(html.text)

headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}
def main():
    # data---post的信息
    # cookie_str---网页申请时的data cookie
    # username---学号
    # cookie---登录网页所需的
    url = 'http://222.24.19.201/default2.aspx'
    url_check='http://222.24.19.201/CheckCode.aspx'
    name,cookie,ID = get_data(url, url_check)
    get_request(name,cookie,ID)
if __name__ == '__main__':
    main()
