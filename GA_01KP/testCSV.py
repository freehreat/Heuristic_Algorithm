f = open("./data","r")   #设置文件对象
line = f.readline()
line = line[:-1]
while line:             #直到读取完文件
    print(float(line.split()[0]))
    line = f.readline()  #读取一行文件，包括换行符
    line = line[:-1]     #去掉换行符，也可以不去
f.close() #关闭文件