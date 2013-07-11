from os import getcwd

curr_dir = getcwd()
read_file = open(curr_dir+"\\yahoo_chenhui_copy.txt",'r')
try:
    datadict={}
    datalist=[]
    head= True
    for line in read_file:
        if head:
            header=line.split(",")
            head=False
        else:
            paramters=line.split(",")
            index=0
            for parameter in paramters:
                datadict[header[index]]=parameter
                index+=1        
            datalist.append(datadict)
            ndex=0
            datadict={}
finally:
    read_file.close()

print len(datalist)
print datalist[1]
