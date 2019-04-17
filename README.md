# logstore

本应用旨在通过阿里云的ram+sts，将阿里云的logstore控制台独立在本地服务器内嵌网页中，从而免去每个要看logstore的人都需要阿里云登陆权限的尴尬。

具体原理：https://help.aliyun.com/document_detail/74971.html?spm=a2c4g.11186623.6.834.5fb66e159bXVTR

依赖：
```
#sudo pip install django==1.10.3
#sudo pip install aliyun-python-sdk-core
#sudo pip install aliyun-python-sdk-sts
#sudo pip install requests
```
编辑一下授权信息：
```
#vi logstore/myapp/utils/sts.py
    # Product
    # 调用AssumeRole接口的子用户AccessKeyId/Secret
    accessKeyId = 'xxxxxxxxxxxxxxxxxx'
    accessKeySecret = 'xxxxxxxxxxxxxxxxxxxxxx'
    # 指定要扮演的角色
    roleArn = 'acs:ram::xxxxxxxxxxxxxxx:role/logviewer'
    sessionName = 'default'
```
启动
```
#python manage.py runserver 0.0.0.0:80
```
打开网页: 

http://x.x.x.x/logtsore

