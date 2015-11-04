#!/usr/bin/env python3
from PIL import Image
from time import time
import f_des


def ECB(data,key,mode):
    result=""
    keyarray = f_des.key_schedule(key)
    if mode == "1":
        for i in range(0,len(data),64):
            result+=f_des.DES(data[i:i+64],keyarray)
    else:
        for i in range(0,len(data),64):
            result+=f_des.de_DES(data[i:i+64],keyarray)

    return result



def CBC(data,key,mode,iv):
    result=""
    keyarray = f_des.key_schedule(key)
    if mode == "1":
        for i in range(0,len(data),64):
            tmp = f_des.xor_func(data[i:i+64],iv)
            iv = f_des.DES(tmp,keyarray)
            result+=iv
    else:
        for i in range(0,len(data),64):
            tmp = f_des.de_DES(data[i:i+64],keyarray)
            result += f_des.xor_func(tmp,iv)
            iv = data[i:i+64]

    return result



def OFB(data,key,mode,iv):
    result=""
    keyarray = f_des.key_schedule(key)
    for i in range(0,len(data),64):
        iv = f_des.DES(iv,keyarray)
        result += f_des.xor_func(data[i:i+64],iv)

    return result



def CTR(data,key,mode,iv):
    def add_1(d):
        if d == "1"*64:
            return "0"*64
        return bin(int(d,2)+1)[2:].zfill(64)

    result=""
    keyarray = f_des.key_schedule(key)
    for i in range(0,len(data),64):
        iv = add_1(iv)
        tmp = f_des.DES(iv,keyarray)
        result += f_des.xor_func(data[i:i+64],tmp)

    return result




KEY = input("please enter KEY (you can enter 0 to get default value) : ")
IV = input("please enter IV (you can enter 0 to get default value) : ")

if KEY=="0":
    KEY = "1010111110101111101011111010111110101111101011111010111110101111"
if IV=="0":
    IV  = "1111101011111010111110101111101011111010111110101111101011111010"


imgname = input("please enter image name(ex:cat.bmp) : ")   
im = Image.open(imgname)       
width,height = im.size                  #get image size
pix = im.load()                         #pix[x,y]   [640,480]

data=""
for i in range(height):
    for j in range(width):
        for k in range(3):
            data+=bin(pix[j,i][k])[2:].zfill(8)


#-----------------------------------
option = input("\nplease select cipher operation\n1.ECB 2.CBC 3.OFB 4.CTR : ")
m = input("1.encode 2.decode : ")

start_time = time()
print("running......")

if option == "1":
    n_data = ECB(data,KEY,m)
elif option == "2":
    n_data = CBC(data,KEY,m,IV)
elif option == "3":
    n_data = OFB(data,KEY,m,IV)
elif option == "4":
    n_data = CTR(data,KEY,m,IV)

print("\nrun time : %fs" % (time()-start_time))
print("success......\n")
#-----------------------------------


save_name = input("please enter output image name(ex:o_cat.bmp) : ")
n_im = Image.new("RGB",(width,height))
n_pix = n_im.load()

for i in range(height):
    for j in range(width):
        tmp = n_data[(i*width+j)*24:(i*width+j+1)*24]
        n_pix[j,i] = (int(tmp[:8],2),int(tmp[8:16],2),int(tmp[16:],2))

n_im.save(save_name)

im.close()
n_im.close()
print("done......")

