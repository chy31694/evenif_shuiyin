# encoding:utf-8

from PIL import Image

import os
import os
import subprocess
import os
import shutil
from cryptography.fernet import Fernet
from blind_watermark import WaterMark

from PIL import Image

# Convert encoding data into 8-bit binary
# form using ASCII value of characters
def genData(data):

		# list of binary codes
		# of given data
		newd = []

		for i in data:
			newd.append(format(ord(i), '08b'))
		return newd

# Pixels are modified according to the
# 8-bit binary data and finally returned
def modPix(pix, data):

	datalist = genData(data)
	lendata = len(datalist)
	imdata = iter(pix)

	for i in range(lendata):

		# Extracting 3 pixels at a time
		pix = [value for value in imdata.__next__()[:3] +
								imdata.__next__()[:3] +
								imdata.__next__()[:3]]

		# Pixel value should be made
		# odd for 1 and even for 0
		for j in range(0, 8):
			if (datalist[i][j] == '0' and pix[j]% 2 != 0):
				pix[j] -= 1

			elif (datalist[i][j] == '1' and pix[j] % 2 == 0):
				if(pix[j] != 0):
					pix[j] -= 1
				else:
					pix[j] += 1
				# pix[j] -= 1

		# Eighth pixel of every set tells
		# whether to stop ot read further.
		# 0 means keep reading; 1 means thec
		# message is over.
		if (i == lendata - 1):
			if (pix[-1] % 2 == 0):
				if(pix[-1] != 0):
					pix[-1] -= 1
				else:
					pix[-1] += 1

		else:
			if (pix[-1] % 2 != 0):
				pix[-1] -= 1

		pix = tuple(pix)
		yield pix[0:3]
		yield pix[3:6]
		yield pix[6:9]

def encode_enc(newimg, data):
	w = newimg.size[0]
	(x, y) = (0, 0)

	for pixel in modPix(newimg.getdata(), data):

		# Putting modified pixels in the new image
		newimg.putpixel((x, y), pixel)
		if (x == w - 1):
			x = 0
			y += 1
		else:
			x += 1

# Encode data into image
def encode(image_name,str_need_encode,output_name):
	img = image_name
	image = Image.open(img, 'r')

	data = str_need_encode
	if (len(data) == 0):
		raise ValueError('Data is empty')

	newimg = image.copy()
	encode_enc(newimg, data)

	new_img_name = output_name
	newimg.save(new_img_name, str(new_img_name.split(".")[2].upper()))

# Decode the data in the image
def decode(image_name):
	img = image_name
	image = Image.open(img, 'r')

	data = ''
	imgdata = iter(image.getdata())

	while (True):
		pixels = [value for value in imgdata.__next__()[:3] +
								imgdata.__next__()[:3] +
								imgdata.__next__()[:3]]

		# string of binary data
		binstr = ''

		for i in pixels[:8]:
			if (i % 2 == 0):
				binstr += '0'
			else:
				binstr += '1'

		data += chr(int(binstr, 2))
		if (pixels[-1] % 2 != 0):
			return data
# Main Function
#encode("./yuantu/1.png","ewewaewe","./shuchu/3.png")



def encrypt(message: bytes, key: bytes) -> bytes:
    return Fernet(key).encrypt(message)

def decrypt(token: bytes, key: bytes) -> bytes:
    return Fernet(key).decrypt(token)

def key_read(data):
    with open("key.txt", "r") as f: #打开文件
        data = f.read() #读取文件
    return data

def jia_mi(message_in,out):
    message = message_in
    data = "wewq"
    data = key_read(data)
    out=encrypt(message.encode(), data)
    return out
def jie_mi(jiami,out):
    message = jiami
    data = "wewq"
    data = key_read(data)
    out=decrypt(jiami, data).decode()
    return out



def check_mark(file_name_with_index):
    
    cmd11 = "exiftool  -SpectralSensitivity"+" " + file_name_with_index
    r2 = os.popen(cmd11)
    is_mark = "define"
    is_mark= r2.read()
    marked = "marked"
    is_mark=is_mark[34:40]
    #print(type(is_mark))


    #print(len(is_mark))
    #print(len(marked))
     
    if(is_mark == marked):
        print("此图片已经被打过标了，只有拥有原有打标人的密钥才能继续打标")
        input("按下回车进行密钥检查")
        try:


            jiemi_name = "abc"
            jiemi_name = file_name_with_index
            
            #cmd = ".\exiftool  -artist"+" " + jiemi_name
            #for imac
            cmd2 = "exiftool  -ImageHistory"+" " + jiemi_name 
            r2 = os.popen(cmd2)
        
            jiami_1 = r2.read()

            daijiemi=jiami_1[34:]
        
            out = "180"
            res = bytes(daijiemi, 'utf-8') 
            out = jie_mi(res,out)
            #print(out)
            #print(type(out))
            if(out == "pass" ):
                print("密钥检查通过")
                input("按下回车继续打标，此次打标将覆写原有打标内容")
                return 0
            if(out != "pass" ):
                print("密钥检查失败")
                while True:
                    input("请使用其他图片打标，请关闭此程序")
                    return -1
        except:
            print("密钥检查失败，你无权对此文件进行二次打标")
            while True:
                input("请使用其他图片打标，请关闭此程序")
            return -1





def mod_key_gen():

    try:
     
    
        if os.path.exists("key.txt"):
            print("密钥已经存在,是否替换或者覆盖，输入 \n 1: 不替换，不覆盖 \n 2 : 替换为新密钥，\n警告：用之前这个密钥加密过的水印将无法读取，除非密钥泄漏，请不要重新生成")
            
            work_mode = 0
            work_mode = get_value(work_mode,"请选输入工作模式序号")
            if work_mode != 0 and work_mode != 1 and work_mode != 2:
                print("你输入的模式序号不存在")
            if work_mode == 1:
                print("已关闭")
            if work_mode == 2:
                key = Fernet.generate_key()
                print("密钥数据，文件名：key.txt ,已经存储：", key.decode())
                with open("key.txt","w") as f:
                    f.write(key.decode()) 

        
        if not os.path.exists("key.txt"):
            key = Fernet.generate_key()
            print("密钥数据，文件名：key.txt ,已经存储：", key.decode())
            with open("key.txt","w") as f:
                f.write(key.decode()) 


    except:
        print("程序出错，请检查读写权限")

    return 0

def get_value(value_get,str_info):
   
    attempts = 0
    success = False
    while attempts < 30000 and not success:
        try:
            
            value = int(input(str_info+"\n"))
            success = True
        except:
            print("输入错误请重新输入")
            attempts += 1
            if attempts == 3000:
                break
    return value
def get_str(str_get,str_info):
   
    attempts = 0
    success = False
    while attempts < 3000 and not success:
        try:
            
            str_get = str(input(str_info+"\n"))
            success = True
        except:
            print("输入错误请重新输入"+str_info)
            attempts += 1
            if attempts == 3000:
                break
    return str_get

def mod_00():
   
    attempts = 0
    success = False
    while attempts < 3000 and not success:
        try:
            yuantu_name_head = "abc"
            yuantu_name_head = get_str(yuantu_name_head,"输入你的原图文件名,要带后缀,例如：abc.png/abc.jpg|不支持带汉字文件名")
            source = './yuantu/'+yuantu_name_head
            target = './shuchu/233313213.jpg'
            res = check_mark(source)
            shu_liang = 50
            shu_liang = get_value(shu_liang,"输入你想生成的图片数量，数量无限制！")
            i = 1
            int(i)
            int(shu_liang)
            while i < shu_liang+1:
                ge_shi = str('.png') 
                



                source_in_loop = source
                target_in_loop = './shuchu/out_'+str(i)+"_"+yuantu_name_head

                #print(target)
                #print(source)
                #shutil.copy(source, target_in_loop) 
                #print("复制完成")
                message = '1'


                jiami = " "
                message = str(i)
                jiami = jia_mi(message,jiami)
                jiami= jiami.decode('UTF-8')
                
                chanllage = jia_mi("pass",jiami)
                chanllage= chanllage.decode('UTF-8')
                encode(source,jiami,target_in_loop)  
                cmd = "exiftool  -artist="+jiami+" "+"-SpectralSensitivity="+"marked"+" "+"-ImageHistory="+chanllage+" "+"-overwrite_original"+" "+target_in_loop
                #print (cmd)
                r1 = os.popen(cmd)
                print(r1.read())
                print(str(i/shu_liang*100)+"%已经完成")
                i =i+ 1
    
            input("复制完成")   
                
                                
                            
        except:
            print("程序出错，可能是你输入的文件名称错误,,请从头开始")
            attempts += 1
            if attempts == 3000:
                break
    return 0




def mod_auto_gen():
   
    attempts = 0
    success = False
    while attempts < 3000 and not success:
        try:
            print("模式说明：程序将自动查询yuantu文件夹下的所有文件并添加水印，\n使用此模式，请将你的待添加文件丢进yuantu文件夹即可，程序将自动寻找文件")
            shu_liang = 5
            shu_liang = get_value(shu_liang,"输入你想生成的图片数量，数量无限制！")
            for filename in os.listdir('./yuantu'):
                print (filename)
                yuantu_name_head = "abc"
                yuantu_name_head = filename
                source = './yuantu/'+yuantu_name_head
                target = './shuchu/233313213.jpg'
                check_mark(source)
                
                i = 1
                int(i)
                int(shu_liang)
                while i < shu_liang+1:
                    ge_shi = str('.png') 
                    



                    source_in_loop = source
                    target_in_loop = './shuchu/out_'+str(i)+"_"+yuantu_name_head

                    #print(target)
                    #print(source)
                    #shutil.copy(source, target_in_loop) 
                    #print("复制完成")
                    message = '1'


                    jiami = " "
                    message = str(i)
                    jiami = jia_mi(message,jiami)
                    jiami= jiami.decode('UTF-8')

                    chanllage = jia_mi("pass",jiami)
                    chanllage= chanllage.decode('UTF-8')
                    encode(source,jiami,target_in_loop)
                      
                    cmd = "exiftool  -artist="+jiami+" "+"-SpectralSensitivity="+"marked"+" "+"-ImageHistory="+chanllage+" "+"-overwrite_original"+" "+target_in_loop
                    #print (cmd)
                    r1 = os.popen(cmd)
                    print(r1.read())
                    print(str(i/shu_liang*100)+"%已经完成")
                    i =i+ 1
                      
                
                                
                            
        except:
            print("程序出错，可能是你输入的文件名称错误,,请从头开始")
            attempts += 1
            if attempts == 3000:
                break
    return 0

def mod_auto_zidingyi():
   
    attempts = 0
    success = False
    while attempts < 3000 and not success:
        try:
            print("模式说明：程序将自动查询yuantu文件夹下的所有文件并添加水印，\n使用此模式，请将你的待添加文件丢进yuantu文件夹即可，程序将自动寻找文件")
            shu_liang = 1
            #shu_liang = get_value(shu_liang,"输入你想生成的图片数量，数量无限制！")
            str_insert = "test"
            str_insert = get_str(str_insert,"请输入你想要插入的内容，！")
            for filename in os.listdir('./yuantu'):
                print (filename)
                yuantu_name_head = "abc"
                yuantu_name_head = filename
                source = './yuantu/'+yuantu_name_head
                target = './shuchu/233313213.jpg'
                check_mark(source)
                
                i = 1
                int(i)
                int(shu_liang)
                while i < shu_liang+1:
                    ge_shi = str('.png') 
                    



                    source_in_loop = source
                    target_in_loop = './shuchu/out_'+str(i)+"_"+yuantu_name_head

                    #print(target)
                    #print(source)
                    #shutil.copy(source, target_in_loop) 
                    #print("复制完成")
                    message = '1'


                    jiami = " "
                    message = str_insert
                    jiami = jia_mi(message,jiami)
                    jiami= jiami.decode('UTF-8')

                    chanllage = jia_mi("pass",jiami)
                    chanllage= chanllage.decode('UTF-8')
                    encode(source,jiami,target_in_loop)
      
                    cmd = "exiftool  -artist="+jiami+" "+"-SpectralSensitivity="+"marked"+" "+"-ImageHistory="+chanllage+" "+"-overwrite_original"+" "+target_in_loop
                    #print (cmd)
                    r1 = os.popen(cmd)
                    print(r1.read())
                    print(str(i/shu_liang*100)+"%已经完成")
                    i =i+ 1
                      
                
                                
                            
        except:
            print("程序出错，可能是你输入的文件名称错误,,请从头开始")
            attempts += 1
            if attempts == 3000:
                break
    return 0


def mod_02():
   
    attempts = 0
    success = False
    while attempts < 3000 and not success:
        try:
            yuantu_name_head = "abc"
            yuantu_name_head = get_str(yuantu_name_head,"输入你的原图文件名,要带后缀,例如：abc.png/abc.jpg|不支持带汉字文件名")
            source = './yuantu/'+yuantu_name_head
            target = './shuchu/233313213.jpg'
            check_mark(source)
            str_insert = "test"
            str_insert = get_str(str_insert,"请输入你想要插入的内容，！")
            source_in_loop = source
            target_in_loop = './shuchu/zidingyi_'+"_"+yuantu_name_head

            #print(target)
            #print(source)
            #shutil.copy(source, target_in_loop) 
            #print("复制完成")

            message = str_insert
            jiami = ""
            jiami = jia_mi(message,jiami)
            jiami = jiami.decode('UTF-8')

            chanllage = jia_mi("pass",jiami)
            chanllage= chanllage.decode('UTF-8')
            encode(source,jiami,target_in_loop)
      
            cmd = "exiftool  -artist="+jiami+" "+"-SpectralSensitivity="+"marked"+" "+"-ImageHistory="+chanllage+" "+"-overwrite_original"+" "+target_in_loop
            r1 = os.popen(cmd)
            print(r1.read())


            
            print("数据插入完成，数据已经被加密为")
            cmd2 = "exiftool  -artist"+" " + target_in_loop
            r2 = os.popen(cmd2)
            print(r2.read())


            
               
                            
        except:
            print("程序出错，可能是你输入的文件名称错误,,请从头开始")
            attempts += 1
            if attempts == 3000:
                break
    return 0
def mod_01():
   
    attempts = 0
    success = False
    while attempts < 3000 and not success:
        try:
            print("EXFI_图片水印解密模式：")
            print("请将你需要解密文件放置于jiemi文件夹下")
            jiemi_name = "abc"
            jiemi_name = get_str(jiemi_name,"输入你想要解密的文件名,要带后缀,例如：abc.png/abc.jpg|不支持带汉字文件名")
            jiemi_name = 'jiemi/'+jiemi_name
            print("正在寻找"+jiemi_name+"待解密文件")
            #cmd = ".\exiftool  -artist"+" " + jiemi_name
            #for imac
            cmd2 = "exiftool  -artist"+" " + jiemi_name 
            r2 = os.popen(cmd2)
            print("解密数据如下：")
            jiami_1 = r2.read()

            
            daijiemi=decode(jiemi_name)
            out = "180"
            res = bytes(daijiemi, 'utf-8') 
            out = jie_mi(res,out)
            print("隐写解密数据："+out)
            daijiemi=jiami_1[34:]
            out = "180"
            res = bytes(daijiemi, 'utf-8') 
            out = jie_mi(res,out)
            print("exif解密数据："+out)
            print("解密完成")

        except:
            print("程序出错，可能是你输入文件名称错误,或文件不含待解密信息,请从头开始")
            attempts += 1
            if attempts == 3000:
                break
    return 0
def mod_1():
   
    attempts = 0
    success = False
    while attempts < 3000 and not success:
        try:
            print("默认工作模式：")
            password_wm = 123
            password_img = 123
            password_wm = get_value(password_wm,"请输入水印加密密码，只能是数字组合")
            password_img = get_value(password_img,"请输入原图加密密码，只能是数字组合")
            bwm1 = WaterMark(password_wm, password_img)
            print("请将你的原图放置于yuantu文件夹下")
            yuantu_name_head = "abc"
            yuantu_name_head = get_str(yuantu_name_head,"输入你的原图文件名,要带后缀,例如：abc.png/abc.jpg|不支持带汉字文件名")
            yuantu_name = 'yuantu/'+yuantu_name_head
            check_mark(yuantu_name)
            print("正在寻找"+yuantu_name+"文件")
            bwm1.read_img(yuantu_name)
            print("图片已经被读取")
            shu_liang = 50
            shu_liang = get_value(shu_liang,"输入你想生成的图片数量，目前最大支持60张，\n 你可以自行放入wm_61/wm_62...，然后输入数量即可")
            i = 1
            int(i)
            int(shu_liang)
            while i < shu_liang+1:
                    ge_shi = str('.png') 
                    shuiyin_tu = str('shuiyin/wm_')
                    shuiyin_name = shuiyin_tu+str(i)+ge_shi
                    shuchu_tu = str('shuchu/img_')
                    shuchu_name = shuchu_tu+str(i)+"_"+yuantu_name_head
                    str(shuiyin_name)
                    str(shuchu_name)
                    print(shuiyin_name+"水印读取中")
                    print(shuchu_name+"输出图生成中")
                    
                    bwm1.read_wm(shuiyin_name)

                    bwm1.embed(shuchu_name)
                    print(str(i/shu_liang*100)+"%已经完成")
                    i =i+ 1
                    
                            
        except:
            print("程序出错，可能是你输入的图片过小，没有足够空间添加水印，或输入文件名称错误,,请从头开始")
            attempts += 1
            if attempts == 3000:
                break
    return 0
def mod_2():
   
    attempts = 0
    success = False
    while attempts < 3000 and not success:
        try:
            print("自定义工作模式：")
            print("提示：此模式可以添加任意水印到任意图中，请注意本程序限制了水印的大小\n 以防止过大水印造成的画质损失，水印推荐使用透明底黑色标记符号或高反差图像，\n 原图越大，你可以写入的水印就越大，对于更大的图片，建议放置白底黑色二维码，\n 如果程序窗口出错，请注意出错内容中，可容纳大小提示")
            password_wm = 123
            password_img = 123
            password_wm = get_value(password_wm,"请输入水印加密密码，只能是数字组合")
            password_img = get_value(password_img,"请输入原图加密密码，只能是数字组合")
            bwm1 = WaterMark(password_wm, password_img)
            print("请将你的原图放置于yuantu文件夹下")
            yuantu_name = "abc"
            yuantu_name = get_str(yuantu_name,"输入你的原图文件名,要带后缀,例如：abc.png/abc.jpg|不支持带汉字文件名")
            yuantu_name = 'yuantu/'+yuantu_name
            print("正在寻找"+yuantu_name+"原图文件")
            bwm1.read_img(yuantu_name)
            shuiyin_name = "abc"
            shuiyin_name = get_str(shuiyin_name,"输入你的水印文件名,要带后缀,例如：abc.png/abc.jpg|不支持带汉字文件名")
            shuiyin_name = 'shuiyin/'+shuiyin_name
            check_mark(yuantu_name)
            print("正在寻找"+shuiyin_name+"水印文件")	
            bwm1.read_wm(shuiyin_name)
            shuchu_name = "abc"
            shuchu_name = get_str(shuchu_name,"输入你想要的输出文件名,要带后缀,例如：abc.png/abc.jpg|不支持带汉字文件名")
            shuchu_name = 'shuchu/'+shuchu_name
            print("正在输出"+shuchu_name+"已加水印文件,请等待结束提示")
            bwm1.embed(shuchu_name)
            print("输出完毕\n\n\n\n")
                    
                            
        except:
            print("程序出错，可能是你输入的图片过小，没有足够空间添加水印，或输入文件名称错误,请从头开始")
            attempts += 1
            if attempts == 3000:
                break
    return 0
def mod_3():
   
    attempts = 0
    success = False
    while attempts < 3000 and not success:
        try:
            print("图片水印解密模式：")
            print("请将你需要解密文件放置于jiemi文件夹下")
            jiemi_name = "abc"
            jiemi_name = get_str(jiemi_name,"输入你想要解密的文件名,要带后缀,例如：abc.png/abc.jpg|不支持带汉字文件名")
            jiemi_name = 'jiemi/'+jiemi_name
            print("正在寻找"+jiemi_name+"待解密文件")
            password_wm = 123
            password_img = 123
            password_wm = get_value(password_wm,"请输入水印加密密码，只能是数字组合")
            password_img = get_value(password_img,"请输入原图加密密码，只能是数字组合")
            bwm1 = WaterMark(password_wm, password_img)
            print("请输入你曾经对这张图加的水印尺寸：例如如果你的水印是640 x 480的，则它的长是640，宽是480，如果是使用默认水印，请两次输入100 \n")
            x = 0
            y = 0 
            x = get_value(x,"请输入长:")
            y = get_value(y,"请输入宽:")
            print("你输入的长宽是%dx%d"%(x,y))
            print("正在运行。请等待结束提示")
            
            bwm1.extract(filename=jiemi_name, wm_shape=(x, y), out_wm_name='shuchu/jiemi.png', )	
            print("解密数据已经输出到shuichu文件夹下，名称为jiemi.png\n\n\n\n")
                    
                            
        except:
            print("程序出错，可能是输入文件名称或水印参数错误,,请从头开始")
            attempts += 1
            if attempts == 3000:
                break
    return 0






print("开发者：evenif/风栖木兮")
print("开源代码地址：https://github.com/guofei9987/blind_watermark")
print("本程序免费提供使用！")
print("程序开始运行：所有选择请输入后按回车才会继续执行")
print("使用本程序前，请先运行一次本文件夹下的exiftool.exe，\n 本程序调用其对exif信息进行读写")
print("如程序出错，请检查你的输入内容，重新打开此程序即可")
print("请注意，请直接解压文件夹使用，请勿更改文件结构\n本程序需要和其下文件夹配合工作他们分别是:\n yuantu:放置原图\n shuiyin；存放水印\n jiemi存放等待解密文件\n shuichu输出文件夹\n 复制此程序时，请直接打包本程序所在文件夹")

#选择工作核心
print("请选择程序工作内核：\n 1: 常用水印模式（原画、qq传输均可查） \n 2: 盲水印模式（增加噪点，截图可查）")
core_mode = 0
core_mode=get_value(core_mode,"请选输入工作内核序号")
if core_mode != 0 and core_mode != 1 and  core_mode != 2:
    print("你输入的核心序号不存在")
    
if core_mode == 0:
    print("核心选择，错误次数过多，已关闭")
if core_mode == 1:
    print("已选择EXIF水印模式")
    if os.path.exists("key.txt"):
        print("已经检测到密钥文件key.txt")
    if not os.path.exists("key.txt"):
        print("\n\n密钥文件key.txt不存在，请在exfi模式选择4创建密钥！！！！\n\n")
    if os.path.exists("exiftool.exe"):
        print("已经检测到exiftool.exe")
    if not os.path.exists("exiftool.exe"):
        print("\n\nexiftool.exe不存在，请检查你的文件夹结构！！！！\n\n")
    print("请选择程序工作模式：\n 1: 默认工作模式\n 2: 自定义模式 \n 3:水印解密模式  \n 4: 生成水印加密密钥（加解密需要，自动生成，“key.txt”文件, 如需自定义，请更改其为44位密码，不够的可以用0补全）\n 5: 多图自动打标模式（请将所有要打标文件放入yuantu文件夹）\n 6: 多图自动自定义打标模式")
    work_mode = 0
    work_mode=get_value(work_mode,"请选输入工作模式序号")
    if work_mode != 1 and work_mode != 1 and work_mode != 2 and work_mode != 3 and work_mode != 4 and work_mode != 5and work_mode != 6:
        print("你输入的工作模式序号不存在")
    if work_mode == 1 :    
        res = 1
        res = mod_00()
    if work_mode == 3 :
        res = 1
        res = mod_01()
    if work_mode == 2 :
        res = 1
        res = mod_02()
    if work_mode == 4 :
        res = 1
        res = mod_key_gen()
    if work_mode == 5 :
        res = 1
        res = mod_auto_gen()
    if work_mode == 6 :
        res = 1
        res = mod_auto_zidingyi()

if core_mode ==2:
    #选择工作模式
    print("已选择盲水印模式")
    print("请选择程序工作模式：\n 1: 默认工作模式（自动添加一定数量水印）\n 2: 自定义模式（请在文件夹添加你的自定义水印）\n 3: 水印解密模式（需要输入密码）")
    work_mode = 0
    work_mode=get_value(work_mode,"请选输入工作模式序号")
    if work_mode != 0 and work_mode != 1 and work_mode != 2 and work_mode != 3:
        print("你输入的工作模式序号不存在")
    if work_mode == 0:
        print("错误次数过多，已关闭")
    if work_mode == 1:
            res = 1 
            res = mod_1()
            
            

    if work_mode == 2:
            res = 1 
            res = mod_2()
    if work_mode == 3:
            res = 1 
            res = mod_3()

input("程序运行完毕，需要再次使用请重新打开")



