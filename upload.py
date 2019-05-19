import tkinter as tk
from tkinter.filedialog import askdirectory           #窗口
from tkinter import StringVar            #窗口
import tkinter.messagebox
import json
import base64
import urllib3
import os
import time
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
a_labname=''
log_result=''
log_file=''
l_list=[]
log_upresult=''
a_path=''
suc_file=0
f_file=0
temmm=0
def selectParh():
    path_=askdirectory()
    path_=path_.replace("/","\\")
    path.set(path_)
    global a_path
    a_path=path_

# def LabelsName():
#     labname_=lab.get()
#     labname.set(labname_)
#     a_labname=labname_
# def cheakstring():
    
def LabelList():
    access_token = '24.5bd9d33ad007169c01db493a4b76d7ac.2592000.1560521571.282335-16203984'
    url = 'https://aip.baidubce.com/rpc/2.0/easydl/label/list?access_token='+access_token
    http=urllib3.PoolManager()
    body={
        'type':'IMAGE_CLASSIFICATION',
        'dataset_id':33410
    }
    encoded_date=json.dumps(body).encode('utf-8')
    request=http.request('POST',
                         url,
                         body=encoded_date,
                         headers={'Content-Type':'application/json'})
    result=str(request.data,'utf-8')
    result=eval(result)
    if 'error_code' in result:
        global log_result
        log_result=str(result)
        log()
        lerror=tk.messagebox.askretrycancel('错误','获取标签名发生错误详情请查看日志',parent=window)
        if (lerror):
            LabelList()
        else:
            window.destroy()
    else:
        result=list(result['results'])
        lenoflist=len(result)
        for i in range(lenoflist):
            result2=result[i]
            dictresult=eval(str(result2))
            l_list.append(str(dictresult['label_name']))

def UploadPic():
    global suc_file
    global f_file
    global log_upresult
    global log_file
    blabel.destroy()
    bpath.destroy()
    access_token = '24.5bd9d33ad007169c01db493a4b76d7ac.2592000.1560521571.282335-16203984'
    url = 'https://aip.baidubce.com/rpc/2.0/easydl/dataset/addentity?access_token='+access_token
    http=urllib3.PoolManager()
    filename=os.listdir(a_path)
    for i in filename:
        f=open(a_path+'\\'+i,'rb')
        img=base64.b64encode(f.read())
        params=str(img,'utf-8')
        body={
            'type':'IMAGE_CLASSIFICATION',
            'dataset_id':33410,
            'entity_content':params,
            'entity_name':i,
            'labels':[{
                'label_name':a_labname,
            }]
        }
        encoded_date=json.dumps(body).encode('utf-8')
        request=http.request('POST',
                            url,
                            body=encoded_date,
                            headers={'Content-Type':'application/json'})
        result=str(request.data,'utf-8')
        result=eval(result)
        if 'error_code' in result:
            f_file=f_file+1
            log_upresult=str(result)
            log_file=i
            uplog()
            list2.insert(tk.END,i)
        else:
            log_file=i
            suc_file=suc_file+1
            list1.insert(tk.END,i)
            successlog()
        window.update()
        list1.update()
        list2.update()
    tk.messagebox.showinfo("成功","上传完毕")
    
def tqdmtest():
    lerror=tk.messagebox.askretrycancel('错误','获取标签名发生错误请检查日志',parent=window)
    if (lerror):
        tqdmtest()
    else:
        window.destroy()

def successlog():
    global temmm
    successlog=open("已上传.txt","a")
    if(temmm==7 or temmm==0):
        successlog.write("\n")
        temmm=0
    temmm=temmm+1
    successlog.write(log_file+"     ")
    successlog.close()

def uplog():
    logfile=open("log.txt","a")
    logfile.write(time.strftime('%Y.%m.%d %H:%M:%S',time.localtime(time.time()))+":\n")
    logfile.write("上传失败："+log_file+"     "+log_upresult+"\n")
    logfile.write("\n")
    logfile.close()
    return

def log():
    logfile=open("log.txt","a")
    logfile.write(time.strftime('%Y.%m.%d %H:%M:%S',time.localtime(time.time()))+":\n")
    logfile.write("获取标签名失败："+log_result+"\n")
    logfile.write("\n")
    logfile.close()
    return

def CheakLabel():
    labname_=lab.get()
    labname.set(labname_)
    global a_labname
    a_labname=labname_
    lab1=tk.Label(labelframe,text='当前标签名为:'+str(a_labname))
    lab1.place(x=7,y=30)
    if a_labname in l_list:
        m=0
    else:
        dele=open("已上传.txt","w")
        dele.write("\n")
        dele.close()
    
def on_closing():
    if (tk.messagebox.askokcancel("退出", "是否关闭窗口？")):
        window.destroy()
        
def click_upb():
    if (a_path==''):
        tk.messagebox.askretrycancel('错误','请检查路径是否正确',parent=window)
    elif (a_labname==''):
        tk.messagebox.askretrycancel('错误','请检查标签名是否正确',parent=window)
    else:
        UploadPic()

window=tk.Tk()
window.geometry('520x600')
window.title("上传")
path=StringVar()
labname=StringVar()
filename=StringVar()
LabelList()
window.protocol("WM_DELETE_WINDOW", on_closing)
ver=tk.Label(window,text='版本：1.3.0')
ver.place(x=15,y=500)
acc=tk.Label(window,text="当前access_token'24.5bd9d33ad007169c01db493a4b76d7ac.2592000.1560521571.282335-16203984'")
acc.place(x=15,y=530)
#标签名
labelframe=tk.LabelFrame(window,text='标签名',labelanchor='nw')
labelframe.place(x=5,y=5,width=250,height=80)
lab=tk.Entry(labelframe)
lab.place(x=5,y=5,width=230)
blabel=tk.Button(labelframe,text='  确  认  ',command=CheakLabel)
blabel.place(x=170,y=28)

#目标路径
pathframe=tk.LabelFrame(window,text='目标路径')
pathframe.place(x=5,y=90,width=250,height=80)
entpath=tk.Entry(pathframe,textvariable=path)
entpath.place(x=5,y=5,width=230)
bpath=tk.Button(pathframe,text='选择路径',command=selectParh)
bpath.place(x=170,y=28)

#已有的标签名
haslabelframe=tk.LabelFrame(window,text='已有的标签名',labelanchor='ne')
haslabelframe.place(x=265,y=5,width=250,height=165)
sbhas=tk.Scrollbar(haslabelframe)
sbhas.pack(side='right',fill='y')
labellist=tk.Listbox(haslabelframe,yscrollcommand=sbhas.set)
if l_list != []:
    for listitem in l_list:
        labellist.insert(tk.END,str(listitem))
else:
    tqdmtest()
labellist.place(x=3,y=0,width=227,height=144)
sbhas.config(command=labellist.yview)

#已上传frame1
frame1=tk.LabelFrame(window,text='已上传',labelanchor='nw')
frame1.place(x=5,y=220,width=250,height=200)
sbframe1=tk.Scrollbar(frame1)
sbframe1.pack(side='right',fill='y')
list1=tk.Listbox(frame1,yscrollcommand=sbframe1.set)
list1.place(x=6,y=0,width=224,height=179)
sbframe1.config(command=list1.yview)

#未上传frame2
frame2=tk.LabelFrame(window,text='上传失败',labelanchor='ne')
frame2.place(x=265,y=220,width=250,height=200)
sbframe2=tk.Scrollbar(frame2)
sbframe2.pack(side='right',fill='y')
list2=tk.Listbox(frame2,yscrollcommand=sbframe2.set)
list2.place(x=6,y=0,width=224,height=179)
sbframe2.config(command=list2.yview)

bupload=tk.Button(window,text='  确  认  上  传  ',command=click_upb)
bupload.place(x=160,y=180,width=200,height=35)

# btest=tk.Button(window,text='test',command=test)
# btest.place(x=500,y=450)

window.mainloop()