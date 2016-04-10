# -*- coding: utf-8 -*-

import qrcode
import xlrd
import tarfile
import os

class Data(object):

	def __init__(self, filePath):
		self.filePath = filePath

	def openExcel(self):
		try:
			file = xlrd.open_workbook((self.filePath))
			return file
		except Exception, e:
			print str(e)

	def readExcel(self):
		file = self.openExcel()
		table = file.sheets()[0]
		rows = table.nrows #行数
		cols = table.ncols
		colnames = table.row_values()
		list = []

	def openTxt(self):
		try:
			file = open(self.filePath, 'r')
			return file
		except Exception, e:
			print str(e)		

	def readTxt(self):
		try:
			file = self.openTxt()
			list = []
			for line in file:
				#oneline = line.decode('utf-8').encode('gbk')
				oneline = line
				list.append(oneline)
			file.close()
			#删掉第一个元素，是标题
			list.pop(0)
			return list
		except Exception, e:
			print str(e)	

	def getData(self):
		return self.data

class MyQrCode(object):

	def __init__(self):
		return

	def genPng(self, text, picName):
		self.drawPic(text)
		self.savePng(picName)

	def drawPic(self, text):
		qr = qrcode.QRCode(
			version=5,
			error_correction=qrcode.constants.ERROR_CORRECT_H,
			box_size=8,
			border=2,
		)
		qr.add_data(text)
		qr.make(fit=True)

		img = qr.make_image()
		self.img = img

	def savePng(self, picName):
		#f = open(unicode(picName, 'utf-8'), 'wb')
		f = open(picName, 'wb')
		self.img.save(f)
		f.close()

#url前缀
urlPrefix = 'http://t10ocs.nuomi.com/diancaiui/wap/dishlist?merchant_id='

#当前绝对路径
pwd = os.path.abspath('.')

data = Data(pwd + '\poi.txt')
myQrCode = MyQrCode()

list = data.readTxt()

#目标文件目录
aimDir = os.path.join(pwd, 'arrJpg')
os.mkdir(aimDir)

for i in list:
	oneline = str(i).strip('\n')
	res = str.split(oneline, ' ')
	merchantId = res[0]
	merchantName = res[1].decode('utf-8').encode('gbk')

	text = urlPrefix + merchantId
	picName = aimDir + '\\' + merchantName + '_' + merchantId + '.jpg'

	print picName

	#print res[0] + res[1].decode('utf-8').encode('gbk')
	myQrCode.genPng(text, picName)


#txtName = '你好' + '_' + 'hello.txt'
#f = open(aimDir + '\\' + unicode(txtName, 'utf-8'), 'w')
#f.write('hello')
#f.close()

tar = tarfile.open(aimDir + '.tar', 'w')
for root, dir, files in os.walk(aimDir):
	for file in files:
		fullpath = os.path.join(root, file)
		tar.add(fullpath, arcname = file)
tar.close()