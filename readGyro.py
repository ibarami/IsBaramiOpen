# coding: utf-8

import header
import time
import sys
import math
import numpy as np
from glob import glob
import git
import time

IsBaramiOpen=1 #0이면 닫혀있다는 의미다. 임의로 설정하였다.
path_git_repo=r'/home/pi/ibarami.github.io/'
commit_message='change condition'
init_run=False#처음에는 바라미실이 열렸는지 안 열렸는지 확인해야하니 돌리자

def pushToGit(OpenCheck):
    global IsBaramiOpen
    global init_run
    if (IsBaramiOpen != OpenCheck) or (init_run is False):
        readme=open("/home/pi/ibarami.github.io/index.md",'r+t',encoding='utf-8')
        edit=readme.read()
        #print(edit)
        readme.close()
        init_run=True
        if OpenCheck is 0:
            edit=edit.replace('**열림**','**닫힘**')
            IsBaramiOpen=OpenCheck
        else:
            edit=edit.replace('**닫힘**','**열림**')
            #readme.write("열림")
            IsBaramiOpen=OpenCheck
        #print("==================")
        #print(edit)
        readme=open("/home/pi/ibarami.github.io/index.md",'w+',encoding='utf-8')
        readme.write(edit)
        readme.close()
        while True:
            try:
                git_function()
                break
            except IOError:
                pass

            #안 될 것 같으면 except Exception을 추가해보자

def git_function():
    repo=git.Repo(path_git_repo)
    repo.git.add(update=True)
    changed_time=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    repo.index.commit(changed_time)
    origin=repo.remote(name='origin')
    origin.push()

        # try:
        #     repo=git.Repo(path_git_repo)
        #     repo.git.add(update=True)
        #     repo.index.commit(commit_message)
        #     origin=repo.remote(name='origin')
        #     origin.push()
        # except:
        #     print("Some error occured while pushing the code")


if __name__== "__main__":
    check=0
    mag_list=list()

    while True:
        mpu9250 = header.MPU9250()
        mag=mpu9250.readMagnet()
        mag_total=math.sqrt(mag['x']**2+mag['y']**2+mag['z']**2)

        if check<3:
            mag_list.append(mag_total)
            check+=1

        else:
            mag_avg=np.mean(mag_list)
            #print(mag_avg)
            if mag_avg >1200:
                #print("close")
                pushToGit(0)
            else:
                #print("open")
                pushToGit(1)

            del(mag_list)
            mag_list=list()
            check=1
