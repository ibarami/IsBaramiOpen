# coding: utf-8

import git
from glob import glob
import numpy as np
import math
import time
import header
import metricUpload
import sys

OPEN = 1
CLOSE = 0
IsBaramiOpen = 1  # 0이면 닫혀있다는 의미다. 임의로 설정하였다.
path_git_repo = r'/home/pi/ibarami.github.io/'
Gyro_Threshold = 400  # Open Close를 판단하는 기준
# commit_message = 'change condition'
INIT_RUN = True  # 처음에는 바라미실이 열렸는지 안 열렸는지 확인해야하니 돌리자


def pushToGit(OpenCheck):
    global IsBaramiOpen
    global INIT_RUN
    if (IsBaramiOpen != OpenCheck) or (INIT_RUN is True):
        readme = open("/home/pi/ibarami.github.io/index.md",
                      'r+t', encoding='utf-8')
        edit = readme.read()
        readme.close()
        if INIT_RUN is True:
            barami_message = -1
            INIT_RUN = False

        if OpenCheck is CLOSE:
            edit = edit.replace('**열림**', '**닫힘**')
            IsBaramiOpen = OpenCheck
            barami_message = CLOSE
        else:  # OpenCheck is OPEN
            edit = edit.replace('**닫힘**', '**열림**')
            IsBaramiOpen = OpenCheck
            barami_message = OPEN

        readme = open("/home/pi/ibarami.github.io/index.md",
                      'w+', encoding='utf-8')
        readme.write(edit)
        readme.close()
        while True:
            try:
                git_function(barami_message)
                break
            except IOError:
                pass

            # 안 될 것 같으면 except Exception을 추가해보자


def git_function(barami_status):
    repo = git.Repo(path_git_repo)
    repo.git.add(update=True)
    if barami_status is -1:
        git_message = 'init run'

    elif barami_status is CLOSE:
        git_message = '닫힘'

    else:
        git_message = '열림'

    changed_time = time.strftime(
        '%Y-%m-%d %H:%M:%S '+git_message, time.localtime(time.time()))
    repo.index.commit(changed_time)
    origin = repo.remote(name='origin')
    while 1:
        try:
            origin.push()
            break
        except git.exc.GitCommandError:
            pass

        # try:
        #     repo=git.Repo(path_git_repo)
        #     repo.git.add(update=True)
        #     repo.index.commit(commit_message)
        #     origin=repo.remote(name='origin')
        #     origin.push()
        # except:
        #     print("Some error occured while pushing the code")


def globalExceptionHandler(exctype, value, traceback):
    metricUpload.uploadErrorLog('error', "type: {0}, value: {1}, trace: {2}".format(exctype, value, traceback))


if __name__ == "__main__":
    sys.excepthook = globalExceptionHandler
    check = 0
    mag_list = list()
    metricUpload.parseConfigure()
    metricUpload.uploadErrorLog('info', "start application loop")

    while True:
        metricUpload.uploadHeartbeat()
        mpu9250 = header.MPU9250()
        mag = mpu9250.readMagnet()
        mag_total = math.sqrt(mag['x']**2+mag['y']**2+mag['z']**2)
        time.sleep(1)

        if check < 3:
            mag_list.append(mag_total)
            check += 1

        else:
            mag_avg = np.mean(mag_list)
            # print(mag_avg)
            if mag_avg > Gyro_Threshold:
                # print("close")
                pushToGit(CLOSE)
            else:
                # print("open")
                pushToGit(OPEN)

            del (mag_list)
            mag_list = list()
            check = 1
