import tkinter as tk
import random as rd
import time
import secrets  # 用于更安全的随机数生成
import os

import _tkinter

from tkinter.filedialog import askdirectory,askopenfilename
import cv2
from PIL import Image, ImageTk

import sys

script_path = sys.argv[0] # 获取当前脚本的路径
absolute_path = os.path.abspath(script_path) # 将可能的相对路径转换为绝对路径
directory = os.path.dirname(absolute_path) # 获取脚本所在的目录

f_path = "D:\\存档\\抽卡存档\\抽卡存档__"#通用路径
Account_path=""#用户登录后路径
denglu_if=False
Account=""#用户登录后用户名
cundang_path=""#存档路径
bag=[]
video_once=["D:\\存档\\动画素材\\单抽出金.mp4","D:\\存档\\动画素材\\单抽出紫.mp4",
            "D:\\存档动画素材\\单抽出蓝.mp4",]
video_ten=["D:\\存档\\动画素材\\十连出金.mp4","D:\\存档\\动画素材\\十连出紫.mp4"]
juese=["D:\\存档\\动画素材\\迪卢克.mp4","D:\\存档\\动画素材\\钟离.mp4"]

#for i in range(0,3):
#    video_once[i]=directory+video_once[i]
#for i in range(0,2):
#    video_ten[i]=directory+video_ten[i]
#for i in range(0,2):
#    juese[i]=directory+juese[i]
#print(video_once)

# 定义抽卡物品列表
kachi = ["迪卢克*五星（歪）", "钟离*五星", "香菱*四星", "鹿野院平藏*四星", "瑶瑶*四星", "菲谢尔*四星", "飞天御剑*三星", "黎明神剑*三星", "冷刃*三星", "以理服人*三星",
         "沐浴龙血的剑*三星", "铁影阔剑*三星", "黑缨枪*三星", "翡玉法球*三星", "讨龙英杰谭*三星", "魔导绪*三星",
         "弹弓*三星", "神射手之誓*三星", "鸦羽弓*三星"]

# 初始化成年列表和重试次数
adult = []
retry = 0

# 获取更稳定的随机数种子（使用secrets模块）
seed_value = secrets.token_hex(16) #生成一个 16 字节（128 位）的随机十六进制字符串
rd.seed(seed_value)

def mkdir(path):
    folder = os.path.exists(path)
    if not folder:                   #判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)            #makedirs 创建文件时如果路径不存在会创建这个路径
        print("账户创建成功！")
        return 1


# 定义颜色对应的Tkinter中的颜色表示
class Colors:
    RED = "red"
    GREEN = "green"
    YELLOW = "yellow"
    BLUE = "blue"
    MAGENTA = "magenta"
    CYAN = "cyan"
    WHITE = "white"

# 定义保底相关常量
FIVE_STAR_DABAODI=180
FIVE_STAR_PITY = 90  # 五星保底抽数
FOUR_STAR_PITY = 10  # 四星保底抽数
five_star_path = 0
four_star_path = 0
dabaodi=False

def read_bag(n):
    global bag
    def read(cundang_path):
        bag=[]
        bag_check=[]
        check=""
        f=open(cundang_path,'r')
        for i in range(0,len(kachi)):
            check=""
            bag_c=f.readline()
            bag_check.append(bag_c)
            for j in bag_check[i]:
                if j.isdigit():
                    check=str(check)+str(j)
                    check=int(check)
            bag.append(check) 
        return bag
    bag_window = tk.Toplevel()
    bag_window.title("背包")
    if denglu_if==False:
        bag_window.title("警告")
        bag_window.geometry("400x200")
        tip = tk.Label(bag_window,text="请先登录！")
        tip.pack()
    else:
        label_text=[]
        bag=read(cundang_path)
        bag_window.geometry("800x500")
        for i in range(0,len(kachi)):
            label_text.append("label_"+str(i))
            context=kachi[i]+"*"+str(bag[i])
            label_text[i]=tk.Label(bag_window,text=context)
            #label_text[i].pack()
            label_text[i].grid(row=i, column=0, sticky=tk.W)
    
def save(jieguo,choushu):#保存抽卡数据
    for i in range(0,choushu):
        bag[jieguo[i]]+=1
    with open(cundang_path,'w') as file:
        text=str(bag[0])+"\n"
        file.write(text)
    with open(cundang_path,'a') as file:
        for i in range(0,len(bag)-1):
            text=str(bag[i+1])+"\n"
            file.write(text)

# 登录验证/注册
def pri(name,IF):
    if IF==True:
        A=destroy_denglu_label(0)
    def login():#登录
        global g_path
        global Account_path
        global denglu_if
        global Account
        global cundang_path
        g_path=f_path
        def read_password(f,account):
            f=f+"\\password.txt"
            f=open(f,'r')
            firstline=f.readline()
            return firstline
        myAccount = a_entry.get()
        myPassword = p_entry.get()
        g_path=g_path+myAccount
        folder = os.path.exists(g_path)
        if not folder:
            tip_label.config(text="此账户不存在！")
        else:
            password=read_password(g_path,myAccount)
            if myPassword != password:
                tip_label.config(text="密码错误！")
            else:
                tip_label.config(text="登录成功！")
                py.destroy()
                Account_path=g_path
                Account=myAccount
                a="当前账户："+Account
                account_menu.add_command(label=a)
                cundang_path=g_path+"\\cundang.txt"
                denglu_if=True
                p=read_bag(0)
        print(Account_path,denglu_if,Account,cundang_path)
    def sign_up():
        g_path=f_path
        myAccount = a_entry.get()
        myPassword = p_entry.get()
        g_path=g_path+myAccount
        cundang_path=g_path+"\\cundang.txt"
        def sign(path):
            os.makedirs(path)
            password_path=path+"\\password.txt"
            with open(password_path, 'a') as file:
                file.write(myPassword)
            with open(cundang_path, 'a') as cundang:
                for i in range(0,len(kachi)):
                    cundang.write("0\n")
        if myAccount=="" or myPassword=="":
            tip_label.config(text="请不要输入空字符！")
        else:
            folder = os.path.exists(g_path)
            if folder:
                tip_label.config(text="该用户已存在！")
            else:
                a=sign(g_path)
                tip_label.config(text="注册成功！")
            
        
    py = tk.Toplevel()
    py.geometry("300x150+800+400")
    if name == "登录":
        py.title("登录")
    else:
        py.title("注册")

    a_label = tk.Label(py, text="用户名：")
    a_label.grid(row=0, column=0, sticky=tk.W)
    a_entry = tk.Entry(py)
    a_entry.grid(row=0, column=1, sticky=tk.E)

    # 密码
    p_label = tk.Label(py, text="密码：")
    p_label.grid(row=1, column=0, sticky=tk.W)
    p_entry = tk.Entry(py)
    p_entry["show"] = "*"

    p_entry.grid(row=1, column=1, sticky=tk.E)
    
    # 登录按钮点击事件处理函数       
    if name == "登录":
        denglu = tk.Button(py, text="登录",command=login)
        denglu.grid(row=3, column=2, sticky=tk.E)
        tip_label=tk.Label(py,text="请登录")
        tip_label.grid(row=3,column=0,sticky=tk.E)
        warning_button=tk.Button(py,text="    没有账号？去注册    ",command=lambda n="注册",F=False:pri(n,F))
        warning_button.grid(row=4,column=1,sticky=tk.W)
    elif name == "注册":
        zhuce = tk.Button(py, text="注册",command=sign_up)
        zhuce.grid(row=3, column=2, sticky=tk.E)
        tip_label=tk.Label(py,text="请输入用户名和密码！")
        tip_label.grid(row=3,column=0,sticky=tk.E)

def play_video(v_path):#播放视频
    video_window=tk.Toplevel()
    video_window.title("抽卡动画")
    movieLabel = tk.Label(video_window)  # 创建一个用于播放视频的label容器
    movieLabel.grid(row = 1, column = 0,padx=10, pady=10)
    for i in v_path:
        video_path=i
        if video_path[-3:] == "mp4":
            video = cv2.VideoCapture(video_path)
            while video.isOpened():
                ret, frame = video.read()
                if ret == True:
                    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
                    current_image = Image.fromarray(img).resize((192*6,108*6))
                    imgtk = ImageTk.PhotoImage(image=current_image)
                    movieLabel.imgtk = imgtk
                    movieLabel.config(image=imgtk)
                    movieLabel.update()
                else:
                    break
    video_window.destroy()
# 抽卡函数
def chouka1(choushu, five_star_pity_count, four_star_pity_count):
    global dabaodi
    jieguo = []
    yet=-1
    for i in range(0,choushu):
        yet=yet+1
        result = rd.randint(0, 10001)
        #print(result,end=" ")
        if result in range(0, 101):
            wai = rd.randint(1, 3)
            if wai == 1:  # 歪
                if dabaodi==False:
                    jieguo.append(0)
                    dabaodi=True
                    #print("0",jieguo[i])
                else:
                    jieguo.append(1)
                    dabaodi=False
                    #print("1",jieguo[i])
            else:
                jieguo.append(1)
                dabaodi=False
                #print("2",jieguo[i])
        elif result in range(101,1001):
            wai = rd.randint(1, 5)
            if wai == 1:  # 香菱
                jieguo.append(2)
            elif wai == 2:  # 鹿野院平藏
                jieguo.append(3)
            elif wai == 3:  # 瑶瑶
                jieguo.append(4)
            elif wai == 4:
                jieguo.append(5)
        else:
            # 修正这里，确保随机数不会超出列表范围
            random_item_index = rd.randint(6, len(kachi) - 1)
            jieguo.append(random_item_index)

        while len(jieguo)<i+1:
            result = rd.randint(0, 10001)
            if result in range(0, 101):
                wai = rd.randint(1, 3)
                if wai == 1:  # 歪
                    if dabaodi==False:
                        jieguo.append(0)
                        dabaodi=True
                        #print("0")
                    else:
                        jieguo.append(1)
                        dabaodi=False
                        #print("1")
                else:
                    jieguo.append(1)
                    dabaodi=False
                    #print("2")
            elif result in range(101, 1001):
                wai = rd.randint(1, 5)
                if wai == 1:  # 香菱
                    jieguo.append(2)
                elif wai == 2:  # 鹿野院平藏
                    jieguo.append(3)
                elif wai == 3:  # 瑶瑶
                    jieguo.append(4)
                elif wai == 4:
                    jieguo.append(5)
            else:
                # 修正这里，确保随机数不会超出列表范围
                random_item_index = rd.randint(6, len(kachi) - 1)

                jieguo.append(random_item_index)

        if jieguo[i] in range(2,6):
            four_star_path=0
        elif four_star_pity_count>=FOUR_STAR_PITY-1:
            jieguo.remove(jieguo[yet])
            jieguo.insert(i,rd.randint(2,5))
            four_star_pity_count=0
        else:
            four_star_pity_count=four_star_pity_count+1


        if jieguo[i] == 0:
            five_star_pity_count=0
            dabaodi=True
        elif jieguo[i]== 1:
            five_star_pity_count=0
            dabaodi=False
        elif five_star_pity_count>=FIVE_STAR_PITY-1:
            jieguo.remove(jieguo[yet])
            jieguo.insert(i,rd.randint(0,2))
            if jieguo[i]==0:
                dabaodi=True
            else:
                dabaodi=False
            five_star_pity_count=0
        else:
            five_star_pity_count=five_star_pity_count+1
    if denglu_if==True:
        x=save(jieguo,choushu)
    try:
        if choushu==1:
            vid_path=[]
            if jieguo[0] in range(2,6):
                vid_path.append(video_once[1])
                a=play_video(vid_path)
            elif jieguo[0] in range(0,2):
                vid_path.append(video_once[0])
                if jieguo[0]==0:
                    vid_path.append(juese[0])
                else:
                    vid_path.append(juese[1])
                a=play_video(vid_path)
            else:
                vid_path.append(video_once[2])
                a=play_video(vid_path)
        elif choushu==10:
            vid_path=[]
            if any(num in jieguo for num in range(0,2)):
                vid_path.append(video_ten[0])
                if any(num in jieguo for num in range(0,1)):
                    vid_path.append(juese[0])
                else:
                    vid_path.append(juese[1])
                a=play_video(vid_path)
            else:
                vid_path.append(video_ten[1])
                a=play_video(vid_path)
    except _tkinter.TclError:
        pass
    #print(jieguo)
    #print(five_star_pity_count,four_star_pity_count)
    return jieguo,five_star_pity_count, four_star_pity_count

# 显示抽卡结果（提取公共部分到函数中）
def show_result(result_text, choushu, five_star_pity_count, four_star_pity_count):
    global five_star_path
    global four_star_path
    jieguo, five_star_pity_count, four_star_pity_count = chouka1(choushu, five_star_pity_count, four_star_pity_count)
    label = tk.Label(result_text, text="抽卡结果为：")
    result_text.window_create(tk.END, window=label)
    result_text.insert(tk.END, "\n")
    for index in range(choushu):
        if jieguo[index] == 0:
            label = tk.Label(result_text, text=kachi[0], fg=Colors.RED)
            result_text.window_create(tk.END, window=label)
            result_text.insert(tk.END, "  ")
        elif jieguo[index] == 1:
            label = tk.Label(result_text, text=kachi[1], fg=Colors.YELLOW)
            result_text.window_create(tk.END, window=label)
            result_text.insert(tk.END, "  ")
        elif jieguo[index] in [2, 3, 5, 4]:
            label = tk.Label(result_text, text=kachi[jieguo[index]], fg=Colors.MAGENTA)
            result_text.window_create(tk.END, window=label)
            result_text.insert(tk.END, "  ")
        else:
            result_text.insert(tk.END, kachi[jieguo[index]] + "  ")
    five_star_path=five_star_pity_count
    four_star_path=four_star_pity_count
    #print("hou:",five_star_path,four_star_path)
    result_text.insert(tk.END, f"\n五星保底剩余抽数：{FIVE_STAR_PITY - five_star_pity_count}")
    result_text.insert(tk.END, f"\n四星保底剩余抽数：{FOUR_STAR_PITY - four_star_pity_count}")
    result_text.insert(tk.END, f"\n是否为大保底：{dabaodi}")
    result_text.insert(tk.END, "\n")

def destroy_denglu_label(n):
    denglu_label.destroy()

def gailv_show(n):
    gailv=tk.Toplevel()
    gailv.title("概率公示")
    gailv.geometry("400x450+800+300")
    for i in range(0,2):
        text=kachi[i]+"：1%"
        gai_lv_1=tk.Label(gailv,text=text)
        gai_lv_1.pack()
    for i in range(2,6):
        text=kachi[i]+"：9%"
        gai_lv_1=tk.Label(gailv,text=text)
        gai_lv_1.pack()
    for i in range(6,len(kachi)):
        text=kachi[i]+"：90%"
        gai_lv_1=tk.Label(gailv,text=text)
        gai_lv_1.pack()

def banquan_show(n):
    banquan=tk.Toplevel()
    banquan.title("版权信息")
    banquan.geometry("400x250+800+300")
    banquan_1=tk.Label(banquan,text="\n\n\n\n\n作者：宇的事\n动画素材：MiHoYo")
    banquan_1.pack()


    
# 创建主窗口
root = tk.Tk()
root.title("抽卡模拟器")
root.geometry('800x400+500+300')

denglu_label=tk.Toplevel()
denglu_label.title("登录?")
denglu_label.geometry('200x100+800+400')
label_dl=tk.Label(denglu_label,text="是否登录?")
label_dl.grid(row=0,column=0,sticky=tk.W)
button_dl_yes=tk.Button(denglu_label,text="  是  ",command=lambda n="登录",F=True:pri(n,F))
button_dl_yes.grid(row=1,column=1,sticky=tk.E)
button_dl_no=tk.Button(denglu_label,text="  否  ", command=lambda n=0:destroy_denglu_label(n))
button_dl_no.grid(row=1,column=0,sticky=tk.E)
denglu_label.attributes('-topmost', True)

#一级菜单
menuBar = tk.Menu(root)
account_menu = tk.Menu(menuBar)#账户
bag_menu = tk.Menu(menuBar)#背包
gailv = tk.Menu(menuBar)#概率公示
banquan = tk.Menu(menuBar)
#二级菜单及对应函数
for i in ["登录", "注册"]:
    account_menu.add_command(label=i, command=lambda n=i,F=False:pri(n,F))
bag_menu.add_command(label="背包", command=lambda n="":read_bag(n))
gailv.add_command(label="概率公示",command=lambda n="":gailv_show(n))
banquan.add_command(label="版权信息",command=lambda n="":banquan_show(n))
#将二级菜单加入一级菜单
menuBar.add_cascade(label="账户", menu=account_menu)
menuBar.add_cascade(label="背包", menu=bag_menu)
menuBar.add_cascade(label="其他",menu=gailv)
menuBar.add_cascade(label="版权信息",menu=banquan)
root["menu"] = menuBar

# 抽卡按钮
button_draw_10 = tk.Button(root, text="十连", command=lambda: show_result(result_text, 10, five_star_path, four_star_path))
button_draw_10.pack()
button_draw = tk.Button(root, text="单抽", command=lambda: show_result(result_text, 1, five_star_path, four_star_path))
button_draw.pack()

# 用于显示结果的文本框
result_text = tk.Text(root)
result_text.pack()

root.mainloop()
