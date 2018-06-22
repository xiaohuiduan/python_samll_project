from tkinter import *  # 引用Tk模块
from tkinter import ttk
from tkinter.filedialog import askdirectory
import requests
import json


def go(*args):
    global name_id
    name_id = myCombox.get()


def selectPath():
    path_ = askdirectory()
    path.set(path_)


def find_id_by_name():
    name = name_text.get()
    api = 'http://music.baidu.com/search?key='
    url = api + name
    response = requests.get(url).text  # 网页源代码
    ul = re.findall(r'<ul.*</ul>', response, re.S)[0]  # 找到含有id的部分
    sids = re.findall(r'sid&quot;:(\d+),', ul, re.S)  # 找到
    find_message_by_id(sids)


def find_message_by_id(sids):
    global myComboList
    myComboList = []  # 清空数组
    for id in sids:
        api = 'http://tingapi.ting.baidu.com/v1/restserver/ting?method=baidu.ting.song.play&format=jsonp&callback=jQuery17205500581185420972_1513324047403&songid=%s&_=1513324048127' % id
        respose = requests.get(api).text
        data = json.loads(re.findall(r'\((.*)\)', respose)[0])
        print(data)
        title = data['songinfo']['title']
        try:
            song = data['bitrate']['show_link']
        except:
            continue
        singer = data['songinfo']['author']
        myComboList.append(title + "        " + singer + "," + id)
    myCombox['values'] = myComboList
    myCombox.current(0)


def get_music_by_id():
    global name_id
    music_id = re.findall(r"\d+\.?\d*", name_id)[0]
    api = 'http://tingapi.ting.baidu.com/v1/restserver/ting?method=baidu.ting.song.play&format=jsonp&callback=jQuery17205500581185420972_1513324047403&songid=%s&_=1513324048127' % music_id
    respose = requests.get(api).text
    data = json.loads(re.findall(r'\((.*)\)', respose)[0])
    title = data['songinfo']['title']
    song = data['bitrate']['show_link']
    print(title)
    map3_data = requests.get(song).content
    with open(path.get() + '\\' + title + '.mp3', 'wb')as f:
        f.write(map3_data)


name_id = ""
root = Tk()  # 初始化Tk()
name_text = StringVar()
name = ''
path = StringVar()
myComboList = []

root.title("百度音乐爬虫版")
# root.iconbitmap('F:\\桌面\\bitbug_favicon.ico')
sw = root.winfo_screenwidth()  # 得到屏幕宽度
sh = root.winfo_screenheight()  # 得到屏幕高度
ww = 600
wh = 400
# 窗口宽高为100
x = (sw - ww) / 2
y = (sh - wh) / 2
root.geometry("%dx%d+%d+%d" % (ww, wh, x, y))
root.resizable(width=False, height=False)
start_label = Label(root, text="输入歌名", font=("Red", 12), width=10, height=2).grid(row=0, column=0)  # Label框
start_label = Label(root, text="选择歌曲", font=("Red", 12), width=10, height=2).grid(row=1, column=0)  # 选择Label框
stroe_label = Label(root, text="储存路径", font=("Red", 12), width=10, height=2).grid(row=2, column=0)  # 储存Label
text = Entry(root, textvariable=name_text).grid(row=0, column=1)  # 输入框
button1 = Button(root, text="搜索音乐", command=find_id_by_name).grid(row=0, column=2)  # 按钮
Entry(root, textvariable=path).grid(row=2, column=1)  # 选择储存地址
Button(root, text="路径选择", command=selectPath).grid(row=2, column=2)  # 选择储存按钮
Button(root, text="我要下载", command=get_music_by_id).grid(row=3, column=1)  # 下载按钮
myCombox = ttk.Combobox(root, values=myComboList, width=50, state='readonly', )  # 下拉菜单
myCombox.bind("<<ComboboxSelected>>", go)  # 绑定事件,(下拉列表框被选中时，绑定go()函数)
myCombox.grid(row=1, column=1)
root.mainloop()  # 进入消息循环
