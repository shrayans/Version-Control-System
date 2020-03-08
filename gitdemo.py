#!/usr/bin/python3

import os,shutil
import glob,hashlib
from colorama import Fore
from sys import argv


flag=0



def hash_file(filename):
   h = hashlib.sha1()
   with open(filename,'rb') as file:
       chunk = 0
       while chunk != b'':
           chunk = file.read(1024)
           h.update(chunk)
   return h.hexdigest()


def handle_init():
    # global flag
    # flag=1
    path=os.getcwd()

    path1=path+"/git/version/v_1"
    file=path+"/git/version/v_1/index.txt"
    file_v=path+"/git/ver.txt"
    try:
        os.makedirs(path1,0o777,exist_ok=False)
    except OSError:
        print ("Creation of the directory %s failed" % path)
    else:
        print ("Successfully created the directory %s " % path)

    fv=open(file_v,"w")
    fv.write(str(1)+"\n")
    fv.close()

    findex=open(file,"w")
    findex.close()



def handle_add_dot():
    # global flag
    path=os.getcwd()
    #print(path)
    #print(glob.glob(path))
    fv=open(path+"/git/ver.txt","r")
    data=fv.readline().strip()
    fv.close()
    v_no=str(data)

    path1=path+"/git/version/v_"+v_no
    ind_file=path1+"/index.txt"
    
    findex=open(ind_file,"r")
    data=findex.readlines()
    findex.close()

    map={}
    for line in data:
        l_file=line.split()
        map[l_file[0]]=l_file[1]

    dirs = os.listdir( path )
    for file in dirs:
        checkfile=path+"/"+file
        if(os.path.isfile(checkfile)):
            sha1 = hash_file(file)
            if(map.get(file)==None):
                map[file]=sha1
                shutil.copy(file,path1+"/"+file)
            else:
                if(map.get(file)==sha1):
                    continue
                else:
                    map[file]=sha1
                    shutil.copy(file,path1+"/"+file)

    findex=open(ind_file,"w")
    for k,v in map.items():
        findex.write(str(k)+" "+str(v)+"\n")

    findex.close()



def handle_add_file(file):
    # global flag
    path=os.getcwd()
    #print(path)
    #print(glob.glob(path))
    fv=open(path+"/git/ver.txt","r")
    data=fv.readline().strip()
    fv.close()
    v_no=str(data)

    path1=path+"/git/version/v_"+v_no
    ind_file=path1+"/index.txt"
    
    findex=open(ind_file,"r")
    data=findex.readlines()
    findex.close()

    map={}
    for line in data:
        l_file=line.split()
        map[l_file[0]]=l_file[1]

    
    checkfile=path+"/"+file
    if(os.path.isfile(checkfile)):
        sha1 = hash_file(file)
        if(map.get(file)==None):
            map[file]=sha1
            shutil.copy(file,path1+"/"+file)
        else:
            if(map.get(file)==sha1):
                pass
            else:
                map[file]=sha1
                shutil.copy(file,path1+"/"+file)

    findex=open(ind_file,"w")
    for k,v in map.items():
        findex.write(str(k)+" "+str(v)+"\n")

    findex.close()
    



def handle_status():
    path=os.getcwd()
    #print(path)
    #print(glob.glob(path))
    fv=open(path+"/git/ver.txt","r")
    data=fv.readline().strip()
    fv.close()
    v_no=str(data)

    # print(v_no)

    path1=path+"/git/version/v_"+v_no
    ind_file=path1+"/index.txt"

    # print(ind_file)

    findex=open(ind_file,"r")
    data=findex.readlines()
    findex.close()

    map={}
    for line in data:
        l_file=line.split()
        map[l_file[0]]=l_file[1]

    # checkfile=path+"/"+file

    untracked=[]
    newfile=[]
    modified=[]

    dirs = os.listdir(path)
    for file in dirs:
        checkfile=path+"/"+file
        if(os.path.isfile(checkfile)):
            if(map.get(file)==None):
                print(Fore.RED+"untracked : " +file)
                untracked.append(file)
            else:
                sha1 = hash_file(file)
                if(map.get(file)==sha1):
                    print(Fore.GREEN+"newfile : " +file)
                    newfile.append(file)
                else:
                    print(Fore.RED+"modified : " +file)
                    modified.append(file)





# while True:
    # command=input(Fore.WHITE + "Enter command ")
    # if(command=="git init" and flag==0):
    #     handle_init()
    # elif(command=="git status" and flag==1):
    #     handle_status()
    # elif(command=="git add ." and flag==1):
    #     handle_add_dot()
    # elif(command=="exit"):
    #     break




# main program
argc=len(argv)
# print(argc)
path=os.getcwd()
gitdir=path+"/"+"git"

if(argc==2):
    # print(argv[1])
    if(argv[1]=="init"):
        if(not os.path.isdir(gitdir)):
            handle_init()
        else:
            print("Already Created")

    if(argv[1]=="status"):
        if(os.path.isdir(gitdir)):
                handle_status()
        else:
            print("Not a git directory")
elif(argc==3):
    # print(argv[1],argv[2])
    if(os.path.isdir(gitdir)):
        if(argv[1]=="add" and argv[2]=="."):
            handle_add_dot()
        elif(argv[1]=="add"):
            handle_add_file(argv[1])
    else:
        print("Not a git directory")
else:
    print("Invalid")


