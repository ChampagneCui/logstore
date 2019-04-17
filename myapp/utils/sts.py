#!/usr/bin/env python
#coding=utf-8

# sudo pip install aliyun-python-sdk-core
# sudo pip install aliyun-python-sdk-sts
# sudo pip install requests

from aliyunsdkcore import client
from aliyunsdksts.request.v20150401 import AssumeRoleRequest
from requests.adapters import HTTPAdapter
import requests.packages.urllib3.util.ssl_
import ssl
import json
import requests
from requests import Request
requests.packages.urllib3.util.ssl_._DEFAULT_CIPHERS = 'ALL'
if(hasattr(ssl, '_create_unverified_context')):
    ssl._create_default_https_context = ssl._create_unverified_context

#SigninHost='http://signin.aliyun.test' # Daily
SigninHost='https://signin.aliyun.com' # Product

def getStsToken(accessKeyId, accessKeySecret, roleArn, sessionName):
    clt = client.AcsClient(accessKeyId, accessKeySecret, 'cn-hangzhou')
    request = AssumeRoleRequest.AssumeRoleRequest()
    request.set_RoleArn(roleArn)
    request.set_RoleSessionName(sessionName)
    request.set_accept_format('json')
    response = clt.do_action(request)
    return json.loads(response)

def getSigninToken(stsAccessKeyId, stsAccessKeySecret, securityToken):
    requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL'
    response = requests.get(SigninHost + '/federation',
                              verify = False,
                              params = { 'Action' : 'GetSigninToken',
                                         'AccessKeyId' : stsAccessKeyId,
                                         'AccessKeySecret' : stsAccessKeySecret,
                                         'SecurityToken' : securityToken,
                                         'TicketType': 'mini'})
    return response.json()
def genSigninUrl(signinToken, loginPage, destination):
    req = Request('GET', SigninHost + '/federation',
                    params = {'Action': 'Login',
                              'LoginUrl': loginPage,
                              'Destination': destination,
                              'SigninToken': signinToken})
    url = req.prepare().url
    return url

def return_sts():
    ## Daily
    ## 调用AssumeRole接口的子用户AccessKeyId/Secret
    #accessKeyId = 't95u5wZGsfhx9rMa'
    #accessKeySecret = 'hvcki9NC6Rp0G9wRL0mhqtrWwR1owR'
    ### 指定要扮演的角色
    #roleArn = 'acs:ram::1696930024067095:role/admin-role'
    #sessionName = 'default'

    # Product
    # 调用AssumeRole接口的子用户AccessKeyId/Secret
    accessKeyId = 'xxxxxxxxxxxxxxxxxx'
    accessKeySecret = 'xxxxxxxxxxxxxxxxxxxxxx'
    # 指定要扮演的角色
    roleArn = 'acs:ram::xxxxxxxxxxxxxxx:role/logviewer'
    sessionName = 'default'

    #print('################### Step 1: 扮演角色，获取STS Token ####################')
    stsToken = getStsToken(accessKeyId, accessKeySecret, roleArn, sessionName)
    #print(stsToken)
    #print('')


    #print('################### Step 2: 使用STS Token换取控制台Signin Token ####################')
    response = getSigninToken(stsToken['Credentials']['AccessKeyId'],
                              stsToken['Credentials']['AccessKeySecret'],
                              stsToken['Credentials']['SecurityToken'])
    signinToken = response["SigninToken"]
    #print(signinToken)
    #print('')

    # 因为登录页不在阿里云，这里需要指定登录Session失效后，需要调回的登录页
    loginUrl = 'http://www.aliyun.com'
    destination = 'http://sls4service.console.aliyun.com'
    #print('################### Step 3: 生成登录链接 ####################')
    signinUrl = genSigninUrl(signinToken, loginUrl, destination)
    return signinUrl
