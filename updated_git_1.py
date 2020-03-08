#!/usr/bin/python3

import os,shutil
import glob,hashlib
from colorama import Fore
from sys import argv,exit


# flag=0

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
                temp=l_file[0]
                l_file.pop(0)
                map[temp]=l_file

        for k,v in map.items():
            print(k,v)

        dirs = os.listdir( path )
        for file in dirs:
                checkfile=path+"/"+file
                if(os.path.isfile(checkfile)):
                        sha1 = hash_file(file)
                        if(map.get(file)==None):
                            l_items=[]
                            l_items.append(sha1)
                            l_items.append(v_no) #parent
                            l_items.append("O")
                            l_items.append(v_no)
                            map[file]=l_items
                            shutil.copy(file,path1+"/"+file)
                        else:
                                if(map.get(file)[0]==sha1):
                                        print("already present : ",file)
                                        continue
                                else:
                                        map[file][0]=sha1
                                        if (map[file][1]==v_no):# and map[file][2]=="O"):
                                                shutil.copy(file,path1+"/"+file)
                                        else:
                                                fetch_file(v_no,file,map[file][3:],path1)
                                                if(map[file][-1]!=v_no):
                                                        map[file].append(v_no)

        findex=open(ind_file,"w")
        for k,v in map.items():
                findex.write(str(k)+" ")
                for vv in v:
                    findex.write(str(vv)+" ")
                findex.write("\n")
        findex.close()

def fetch_file(v_no,file,list,path1):
    path=os.getcwd()
    if(list[-1]==v_no):
        list.pop(-1)
    if(len(list)==1):
            p_path=path+"/git/version/v_"+list[0]+"/"+file
            print("p_path:"+p_path)
            cmd="diff "+p_path+" "+ path+"/"+file + " > " + path1+"/"+file
            print(cmd)
            os.system(cmd)
    else:
            p_path=path+"/git/version/v_"
            temp_file=path+"/git/version/temp"
            patchcmd="patch "+p_path+list[0]+"/"+file+" "+p_path+list[1]+"/"+file+" -o "+temp_file+"2;"
            i=2
            while(i<len(list)):
               patchcmd+="patch "+temp_file+str(i)+" "+p_path+list[i]+"/"+file+" -o "+temp_file+str(i+1)+";"
               i+=1
            print(patchcmd)
            os.system(patchcmd)
            cmd="diff "+temp_file+str(i)+" "+ path+"/"+file + " > " + path1+"/"+file
            print(cmd)
            os.system(cmd)
            # os.system("rm "+temp_file)




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
            print(line)
            l_file=line.split()
            temp=l_file[0]
            l_file.pop(0)
            map[temp]=l_file

        
        checkfile=path+"/"+file
        print(checkfile)
        if(os.path.isfile(checkfile)):
                sha1 = hash_file(file)
                if(map.get(file)==None):
                    l_items=[]
                    l_items.append(sha1)
                    l_items.append(v_no)
                    l_items.append("O")
                    map[file]=l_items
                    shutil.copy(file,path1+"/"+file)
                else:
                        if(map.get(file)[0]==sha1):
                            print("already present : ",file)
                                # pass
                        else:
                                map[file][0]=sha1
                                if (map[file][1]==v_no):
                                    shutil.copy(file,path1+"/"+file)
                                else:
                                    p_path=path+"/git/version/v_"+map[file][1]+"/"+file
                                    print("p_path:"+p_path)
                                    cmd="diff "+p_path+" "+ path+"/"+file + " > " + path1+"/"+file
                                    print(cmd)
                                    os.system(cmd)


        findex=open(ind_file,"w")
        for k,v in map.items():
                findex.write(str(k)+" ")
                for vv in v:
                    findex.write(str(vv)+" ")
                findex.write("\n")
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
                                        print(Fore.GREEN+"newfile added : " +file)
                                        newfile.append(file)
                                else:
                                        print(Fore.RED+"modified : " +file)
                                        modified.append(file)


def handle_commit():
        path=os.getcwd()
        #print(path)
        #print(glob.glob(path))
        fv=open(path+"/git/ver.txt","r")
        data=fv.readline().strip()
        fv.close()

        v_no=int(data)
        v_no+=1
        fv=open(path+"/git/ver.txt","w")
        fv.write(str(v_no)+"\n")
        fv.close()

        path1=path+"/git/version/v_"+str(v_no)
        prev_index=path+"/git/version/v_"+str(v_no-1)+"/index.txt"

        try:
                os.makedirs(path1,0o777,exist_ok=False)
        except OSError:
                print ("Creation of the directory %s failed" % path)
        else:
                print ("Successfully created the directory %s " % path1)

        shutil.copy(prev_index,path1+"/index.txt")




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
                        exit(0)
                else:
                        print("Already Created")
                        exit(0)

        if(argv[1]=="status"):
                if(os.path.isdir(gitdir)):
                        handle_status()
                        exit(0)
                else:
                        print("Not a git directory")
                        # sys.exit(0)
                        exit(0)

        if(argv[1]=="commit"):
                if(os.path.isdir(gitdir)):
                        handle_commit()
                        exit(0)
                else:
                        print("Not a git directory")
                        exit(0)

        print("Invalid")

elif(argc==3):
        # print(argv[1],argv[2])
        if(os.path.isdir(gitdir)):
                if(argv[1]=="add" and argv[2]=="."):
                        handle_add_dot()
                elif(argv[1]=="add"):
                        handle_add_file(argv[2])
        else:
                print("Not a git directory")
else:
        print("Invalid")

