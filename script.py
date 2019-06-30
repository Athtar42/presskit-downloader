#coding=utf-8

import re
import os
import errno
from bs4 import BeautifulSoup
import urllib.request
import requests
from urllib.parse import urlparse

r = "https://presskit.season-of-mist.com/"

bandname = input("请输入乐队名称(保证大小写正确和名称中的空格)：")
ifInactive = input("该乐队是否在Inactve文件夹内(是请输入1，否请直接回车)：")
if ifInactive == "1":
	print("Sorry 暂时不支持Inactive Bands, 请等我更新")
	exit()
customePath = input("请输入保存目录(例子:'C:\\TEMP',请保证目录结尾没有斜杠否则会保存错误)：")

def rep(bandname): # 将空格转换为下划线
	li = []
	for i in bandname:
		li.append(i)
	for i in range(len(li)):
		if li[i] == ' ':
			li[i] = '_'
	return ''.join(li)

def replaceslash(url): 
	li = []
	for i in url:
		li.append(i)
	for i in range(len(li)):
		if li[i] == '/':
			li[i] = '\\'
	return ''.join(li)

bandname = rep(bandname)
url = r + bandname + "/"
links = []
links.append(url)

def getFolderUrl(url):
	html_page = urllib.request.urlopen(url,timeout=10).read()
	soup = BeautifulSoup(html_page, "html.parser")
	
	print(url)
	links = []

	contents = soup.find_all('td', valign = 'top')
	for td in contents:
		atags = td.find_all('a', attrs = {'href': re.compile("^(?!/)\S{1,}/$")})
		if len(atags) > 0:	
			for a in atags:
				links.append(url + a.get('href')) 
	return links

def getFileUrl(url):
	html_page = urllib.request.urlopen(url,timeout=10).read()
	soup = BeautifulSoup(html_page, "html.parser")
	print(url)
	links = []

	contents = soup.find_all('td', valign = 'top')
	for td in contents:
		atags = td.find_all('a', attrs = {'href': re.compile("^(?!/)\S{1,}(?<!/)$")})
		if len(atags) > 0:
			for a in atags:
				links.append(url + a.get('href')) 
	return links

links = links + getFolderUrl(url)

folderUrls = links

	
if len(links) > 0:

	for link in links:
		print(link)
		findUrls = getFolderUrl(link)	
		if len(findUrls) > 0:
			for url in findUrls:
				if url not in folderUrls:
					links.append(url)
					folderUrls.append(url)
print(folderUrls)

fileUrls = []

if len(folderUrls) > 0:

	for link in folderUrls:
		findUrls = getFileUrl(link)
		if len(findUrls) > 0:
			for url in findUrls:
				if url not in fileUrls:
					fileUrls.append(url)
print(fileUrls)

for fileUrl in fileUrls:
	#file_name = fileUrl.split('/')[-1]
	urlPath = urlparse(fileUrl)
	finalPath = replaceslash(urlPath.path)

	if not os.path.exists(os.path.dirname(customePath+ finalPath)):
		try:
			os.makedirs(os.path.dirname(customePath+ finalPath))
		except OSError as exc: # Guard against race condition
			if exc.errno != errno.EEXIST:
				raise

	try:
		r = requests.get(fileUrl)
		with open(r''+ customePath+ finalPath, 'wb') as f:
			f.write(r.content)
			print("正在保存" + fileUrl)
	except Exception as e:
		print(path +" error")

print("All Done!")
