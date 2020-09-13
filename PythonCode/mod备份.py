import os
import shutil
import time

gameDir = 'G:/epicgame/GTAV1/'
modDir = 'F:/BaiduNetdiskDownload/[游戏MOD] GTA5 豪华车包 添加替换 380辆载具 中国风/1.豪华车包/'
modFilesPath = []
gameFilesPath = {}


def copyfile():
    for root, dirs, files in os.walk(modDir):
        for fileName in files:
            filePath = root.replace(modDir, '') + '/' + fileName
            filePath = filePath.replace('\\', '/')
            if filePath[0] == '/':
                filePath = filePath[1:]
            modFilesPath.append(filePath)

    for root, dirs, files in os.walk(gameDir):
        for fileName in files:
            filePath = root.replace(gameDir, '') + '/' + fileName
            filePath = filePath.replace('\\', '/')
            if filePath[0] == '/':
                filePath = filePath[1:]
            gameFilesPath[filePath] = 1

    for i in modFilesPath:
        # 第一次时创建备份文件夹
        if i == modFilesPath[0]:
            backDir = gameDir + 'back-' + time.strftime('%m%d_%H_%M_%S', time.localtime(time.time())) + '/'
            os.mkdir(backDir)
        #     覆盖
        if i in gameFilesPath.keys():
            st = time.time()
            fileSplit = i.split('/')
            # 主页文件
            if len(fileSplit) == 1:
                shutil.copyfile(gameDir + i, backDir + i)
                os.remove(gameDir + i)
                shutil.copyfile(modDir + i, gameDir + i)
            # 子文件夹文件
            else:
                newDir = '/'.join(fileSplit[:-1]) + '/'
                if not os.path.exists(gameDir + newDir):
                    os.makedirs(gameDir + newDir)
                if not os.path.exists(backDir + newDir):
                    os.makedirs(backDir + newDir)
                shutil.copyfile(gameDir + i, backDir + i)
                os.remove(gameDir + i)
                shutil.copyfile(modDir + i, gameDir + i)
            ed = str(time.time() - st)[:4]
            print(f'覆盖文件：{i} 完成，耗时{ed}s')
        #     新增
        # else:
        #     st = time.time()
        #     fileSplit = i.split('/')
        #     if len(fileSplit) == 1:
        #         shutil.copyfile(modDir + '/' + i, gameDir + '/' + i)
        #     else:
        #         newDir = gameDir + '/' + '/'.join(fileSplit[:-1])
        #         if not os.path.exists(newDir):
        #             os.makedirs(newDir)
        #         shutil.copyfile(modDir + '/' + i, gameDir + '/' + i)
        #     ed = int(time.time() - st)
        #     print(f'新增文件：{i} 完成，耗时{ed}s')


def check_copy_progress(oldPath: str, newPath: str):
    pass


copyfile()
