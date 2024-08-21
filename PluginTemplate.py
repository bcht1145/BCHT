import requests #你在安装时就已经安装上了
flora_api = {}  # 顾名思义,FloraBot的API,载入(若插件已设为禁用则不载入)后会赋值上

def occupying_function(*values):  # 该函数仅用于占位,并没有任何意义
    pass

send_msg = occupying_function

def init():  # 插件初始化函数,在载入(若插件已设为禁用则不载入)或启用插件时会调用一次,API可能没有那么快更新,可等待,无传入参数
    global send_msg
    print(flora_api)
    send_msg = flora_api.get("SendMsg")
    print("main_消息处理 加载成功")

def api_update_event():  # 在API更新时会调用一次(若插件已设为禁用则不调用),可及时获得最新的API内容,无传入参数
    pass

def qq_wjid(uidd): #违禁次数判断模块
    nn = 1
    uidd = str(uidd)
    try:
        with open('wjqq.txt','r')as fileu:
            line = fileu.readline()
            while line != "":
                if not line:
                    break
                if line.find(uidd) != -1:
                    nn = int(line[0])
                line = fileu.readline()
    except FileNotFoundError:
        with open('wjqq.txt','w')as fileu:#为了防止文件缺失而导致错误
            pass
    with open('wjqq.txt','a+')as fileu:
        if nn == 5:#把5是触发违禁词几次后禁言
            fileu.write(str(1)+"/"+uidd+'\n')
            return True
        else:
            fileu.write(str(nn+1)+"/"+uidd+'\n')
            return False

wj = [""] #填入你想要屏蔽的词

def event(data: dict):  # 事件函数,FloraBot每收到一个事件都会调用这个函数(若插件已设为禁用则不调用),传入原消息JSON参数
    uid = data.get("user_id")  # 事件对象QQ号
    gid = data.get("group_id")  # 事件对象群号
    mid = data.get("message_id")  # 消息ID
    msg = data.get("raw_message")  # 消息内容
    if msg is not None:
        msg = msg.replace("&#91;", "[").replace("&#93;", "]").replace("&amp;", "&").replace("&#44;", ",")  # 消息需要将URL编码替换到正确内容
        if uid in flora_api.get('Administrator'):
            pass
        if msg[3:9].find("image")==-1 and msg[3:9].find("video")==-1: #判断消息是否为图片或视频
            for i in wj: #判断消息是否包含屏蔽词
                if msg.find(i) != -1:
                    url = "http://127.0.0.1:3000/delete_msg"#撤回消息
                    data = {
                        "message_id":int(mid)
                    }
                    urlj = "http://127.0.0.1:3000/set_group_ban"#禁言
                    dataj = {
                        "group_id":int(gid),
                        "user_id":int(uid),
                        "duration":300
                    }
                    if qq_wjid(uid):
                        requests.post(url,json=data)
                        send_msg("你的消息多次违反了管理员的设定，已禁言",uid,gid,mid)
                        requests.post(urlj,json=dataj)
                        break
                    else:
                        send_msg("你的消息违反了管理员的设定，警告一次",uid,gid,mid)
                        requests.post(url,json=data)
                        break
                    # send_msg("你的消息违反了管理员的设定，警告一次",uid,gid,mid)
                    # requests.post(url,json=data)
                    # break
        else:
            pass

"""
制作人：不出胡桃
这是我做的第5个插件

是个检测违禁词，然后消息撤回模块

如果不想禁言只想撤回，
那就把75~67行的代码注释掉
然后取消76~78行的注释即可
"""
