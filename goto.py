# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os,sys
from ssh_goto_utils.utils.prettytable import PrettyTable
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import collections
import json

reload(sys)
sys.setdefaultencoding('utf-8')

def PrintRegion():
	regidict = collections.OrderedDict()
	regidict["1"] = {"name":"俄勒冈","regsimp":"us-west-2"}
	regidict["2"] = {"name":"孟买","regsimp":"ap-south-1"}
	regidict["3"] = {"name":"新加坡","regsimp":"ap-southeast-1"}
	regidict["4"] = {"name":"东京","regsimp":"ap-northeast-1"}
	regidict["5"] = {"name":"沙河机房","regsimp":"bjsh"}
	regidict["6"] = {"name":"兆维机房","regsimp":"bjzw"}
	regidict["7"] = {"name":"博兴机房","regsimp":"bjbx"}
	regidict["8"] = {"name":"大族机房","regsimp":"bjdz"}
	print("############## SSH GOTO ##############")
	tb = PrettyTable()
	tb.field_names = ["区域ID","区域名称","区域简写"]
	for regid,regname in regidict.items():
		tb.add_row([regid,regname["name"],regname["regsimp"]])
	print(tb)
	return tb,regidict

def juggleInput(regidict):
	while True:
		regid = raw_input("请输入你需要连接的区域机器：")
		if regid.isdigit():
			if int(regid) > len(regidict) or int(regid) == 0:
				print("输入区域id不存在，请重新输入")
				continue
			else:
				return regidict[regid]["regsimp"]
				break
		elif regid in ['exit','EXIT']:
			sys.exit()
		else:
			print("输入有误，请重新输入！")
			continue

def getPrettyTable(regionlist):
	tb = PrettyTable()
	num = 1
	tb.field_names = ['实例编号','实例名称','实例id','所在区域','内网IP','公网IP','运行状态']
	for i in regionlist:
		if i[0]['instanceName'] == None:
			tb.add_row([num,i[0]['instanceName'],i[0]['instanceID'],i[0]['region'],i[0]['privateIP'],i[0]['publicIP'],i[0]['status']])
		else:
			tb.add_row([num,i[0]['instanceName'][0],i[0]['instanceID'],i[0]['region'],i[0]['privateIP'],i[0]['publicIP'],i[0]['status']])
		num += 1
	print tb
	return num

def sshConnect(ssh_ip):
	comm = "ssh %s" % ssh_ip
	os.system(comm)

def myfuzzywuzzy(regionlist,search_instance):
	after_search = process.extract(search_instance,regionlist)
	tb = PrettyTable()
	num = 1
	tb.field_names = ['实例编号','实例名称','实例id','所在区域','内网IP','公网IP','运行状态']
	for i in after_search:
		if i[0][0]['instanceName'] == None:
			tb.add_row([num,i[0][0]['instanceName'],i[0][0]['instanceID'],i[0][0]['region'],i[0][0]['privateIP'],i[0][0]['publicIP'],i[0][0]['status']])
		else:
			tb.add_row([num,i[0][0]['instanceName'][0],i[0][0]['instanceID'],i[0][0]['region'],i[0][0]['privateIP'],i[0][0]['publicIP'],i[0][0]['status']])
		num += 1
	print tb
	while True:
		search_instance = raw_input("请输入要查询的主机或ssh主机的id：")
		if search_instance.isdigit() and int(search_instance) <= len(after_search):
			ipaddr = after_search[int(search_instance) - 1][0][0]['privateIP']
			print("开始ssh：%s" % (after_search[int(search_instance) - 1][0][0]['privateIP']))
			sshConnect(ipaddr)
			break
		elif search_instance.strip() == '':
			print getPrettyTable(regionlist)
		elif search_instance in ['exit','EXIT']:
			sys.exit()
		else:
			myfuzzywuzzy(regionlist,search_instance)
	


def getRegionMachine(regsimp):
	try:
		with open("./ssh_goto_utils/jsonfile/%s.json" % regsimp , "r") as jsonfile:
			regidict = json.load(jsonfile)
			num = getPrettyTable(regidict)
			search_instance = raw_input("请输入要查询的主机或ssh主机的id：")
			if search_instance.isdigit() and int(search_instance) <= num and int(search_instance) > 0:
				ipaddr = regidict[int(search_instance) - 1][0]['privateIP']
				print("开始ssh：%s" % (regidict[int(search_instance) - 1][0]['privateIP']))
				sshConnect(ipaddr)
			elif search_instance in ['exit','EXIT']:
				sys.exit()
			else:
				myfuzzywuzzy(regidict,search_instance)
	except IOError as e:
		print("该区域的机器还没有添加，请重新选择区域。")

if __name__ == '__main__':
	regtb,regidict = PrintRegion()
	regsimp = juggleInput(regidict)
	getRegionMachine(regsimp)
