
import json
import requests
import os
import random
# from PIL import Image

class sharephoto():

    def __init__(self):
        #在微信公众平台取得appID和appsecret
        self.appID = 'xxx' #填写自己公众号的appid
        self.appsecret = 'xxx'  # appsecret 同上
        self.photo_dir = '/photo_dir' #填写自己存储的照片根目录
        self.access_token = self.get_access_token()  # 获取 access token
        self.opend_ids = self.get_openid()  # 获取关注用户的openid
        self.media = self.push_media()

    def get_openid(self):
        """
        获取所有用户的openid
        微信公众号开发文档中可以查阅获取openid的方法
        """
        next_openid = ''
        url_openid = 'https://api.weixin.qq.com/cgi-bin/user/get?access_token=%s&next_openid=%s' % (
        self.access_token, next_openid)
        ans = requests.get(url_openid)
        open_ids = json.loads(ans.content)['data']['openid']
        return open_ids

    def get_random_image_path(self):
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif']  # 可以根据需要添加其他图片格式的扩展名
        # 遍历指定目录及其子目录下的所有文件
        image_files = [os.path.join(root, file) for root, dirs, files in os.walk(self.photo_dir) for file in files
                        if any(file.lower().endswith(ext) for ext in image_extensions)]
        if not image_files:
            return None  # 如果没有找到图片文件，返回None
        # 随机选择一张图片的路径
        random_image_path = random.choice(image_files)
        return random_image_path

    def get_access_token(self):
        """
        获取access_token
        通过查阅微信公众号的开发说明就清晰明了了
        """
        url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}'. \
            format(self.appID, self.appsecret)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36'
        }
        response = requests.get(url, headers=headers).json()
        access_token = response.get('access_token')
        print(access_token)
        return access_token

    def push_media(self):
        # 指定目录路径
        # 获取随机图片的绝对路径
        file_path = self.get_random_image_path()
        # 构建API请求URL
        url = f"https://api.weixin.qq.com/cgi-bin/media/upload?access_token={self.access_token}&type=image"
        # 使用requests库发送POST请求
        files = {'media': (file_path, open(file_path, 'rb'))}
        response = requests.post(url, files=files)
        # 解析返回的JSON数据
        result = response.json()
        media_id = result.get("media_id")
        data={
        "articles": [	 
                {
                    "thumb_media_id":media_id,
                    "author":"RUO",		
                    "title":"看看今天的美照吧",		 
                    "content_source_url":"https://www.baidu.com/",		#查看原文的跳转链接，可以改为自己的网页
                    "content":"嘿嘿",		 
                    "digest":"好看不",
                    "show_cover_pic":1,
                    "need_open_comment":1,
                    "only_fans_can_comment":1
                }
        ]
        }
        url=f'https://api.weixin.qq.com/cgi-bin/media/uploadnews?access_token={self.access_token}'
        data = bytes(json.dumps(data, ensure_ascii=False).encode('utf-8'))  # 将数据编码json并转换为bytes型
        response = requests.post(url, data=data)
        result = response.json()  # 将返回信息json解码
        media_id2=result.get("media_id")
        return media_id2
    
    def sendmsg(self):
        """
        给所有用户发送消息
        """
        url = "https://api.weixin.qq.com/cgi-bin/message/mass/send?access_token={}".format(self.access_token)
        data={
            "touser":[
            ],
            "mpnews":{      
            "media_id":self.media
            },
            "msgtype":"mpnews" ,
            "send_ignore_reprint":0
        }
        for opend_id in self.opend_ids:
            data["touser"].append(opend_id)
        data = bytes(json.dumps(data, ensure_ascii=False).encode('utf-8'))  # 将数据编码json并转换为bytes型
        response = requests.post(url, data=data)
        result = response.json()  # 将返回信息json解码
        print(result)  # 根据response查看是否广播成功

if __name__ == "__main__":
    sends = sharephoto()
    sends.sendmsg()



