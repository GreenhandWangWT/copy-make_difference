"""
@author: 1000283597
-----------------------------------------------
      \    ^__^
       \   (oo)\_________
           (__)\         )\/
               ||———————w|
               ||       ||
----------------------------------------------

# usage: please see the attached file 
"""

import os
import time
import difflib
import hashlib
import re
import shutil

#process time
titleTime =time.strftime('%Y%m%d_%H%M%S',time.localtime())

#find the target file
pattern = re.compile(r'configuration.txt')


def getFileMd5(filename):
    if not os.path.isfile(filename):
        print('file not exist: ' + filename)
        return
    myhash = hashlib.md5()
    #use the rb to read for save the memory
    f = open(filename,'rb')
    while True:
        #read bytes multitimes for big data and future use
        b = f.read(8096)
        if not b :
            break
        myhash.update(b)
    f.close()
    return myhash.hexdigest()


def getAllFiles(path):
    flist=[]
    folderList = []
    for folders, subfolders, filenames in os.walk(path):
        #find the testprogram's version 00/D0/T0
        for filename in filenames:
            f_fullpath = os.path.join(folders, filename)
            folderTempName = re.split(r'[//|/|\|\\]',folders)
            folderName = folderTempName[-1].split('_')[0]
            folderList.append(folderName)
            #select the items format like 4XP\\B6_ABE.pbd
            # the len(MH84I003D0_) is 12 
            f_relativepath = f_fullpath[len(path)+12:]           
            flist.append(f_relativepath)
    return flist,set(folderList)



def _read_file(file):
    try:
        with open(file,'rb') as fp:
            lines = fp.read().decode('utf-8')
            text = lines.splitlines()
            return text
    except Exception as e:
        print("When open the config file, there exist Errors: %s" % str(e))


def calculateDiffence(path1,path2,splitItem):
    #path1/2 example: C://Users//1000283597//01_workspace//01_2020//03_Code_project//08_copy-config_file//own_test//new\MH84I00300_6ZP\configuration.txt
    #splitItem example: MH84I00300
    #In path2, we will generate a new foler to storage the changed items
    #named 01_Differnet_item , file name is for example MH84I003D0_6ZP 
    newFolder = path2.split(splitItem)[0][:-1] + '\\' + '01_Differet_item' +'_' + titleTime
    if not os.path.exists(newFolder):
        os.mkdir(newFolder)
    #part1 output the diffence compare file
    fileTemp1 = _read_file(path1)
    fuleTemp2 = _read_file(path2)
    compare = difflib.HtmlDiff()
    compare_result = compare.make_file(fileTemp1,fuleTemp2)
    outPutnameTemp = re.split(r'[//|/|\|\\]',path2)[-2]
    outPutname = outPutnameTemp+'.html'
    with open(os.path.join(newFolder,outPutname),'w+') as f:
        f.writelines(compare_result)
    #part2 copy the raw config file
    shutil.copy(path1,path2)
    print("The %s 's config file had been changed, please pay attention" %str(outPutnameTemp))



def dirCompare(apath,bpath):
    #afilesTemp format '4XP\\B6_ABE.pbd',{'MH84I003D0'}
    afilesTemp = getAllFiles(apath)

    afiles = afilesTemp[0]
    afilesName = list(afilesTemp[1])[0]
    bfilesTemp = getAllFiles(bpath)
    bfiles = bfilesTemp[0]
    bfilesName = list(bfilesTemp[1])[0]
    setA = set(afiles)
    setB = set(bfiles)
    #avoid there are some noise file
    #dispose the common files
    commonfiles = setA & setB  

    for f in sorted(commonfiles):
        #example 6ZP\\configuration.txt
        mo = re.search(pattern,f)
        if mo:
            apath1 = apath+'\\'+ afilesName + '_' + f
            bpath1 = bpath+'\\'+ bfilesName + '_' + f
            amd=getFileMd5(apath1)
            bmd=getFileMd5(bpath1)
            if amd != bmd:  
                calculateDiffence(apath1,bpath1,bfilesName)


if __name__ == '__main__':
    print("Processing......\n")
    #define the config file 
    path1 = input("please input the old test program address: ")
    path2 = input("please input the new test program address: ")

#    path1 = "C://Users//1000283597//01_workspace//01_2020//03_Code_project//08_copy-config_file//03_Old_Program"
#    path2 = "C://Users//1000283597//01_workspace//01_2020//03_Code_project//08_copy-config_file//02_New_Program"    
    dirCompare(path1, path2)
    print("\nDone!")
