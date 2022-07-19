import numpy as np
import requests
from tqdm import tqdm
import os

import pandas as pd

def get_data():#提取数据
    feature_merge = pd.read_csv("not_merge.csv")
    decals_voteab_post = pd.read_csv("gz_decals_volunteers_ab.csv")
    decals_votec_post = pd.read_csv("gz_decals_volunteers_c.csv")
    return feature_merge, decals_voteab_post, decals_votec_post

def get_nomerge():
    nomerge = np.load("nomerge.npy", allow_pickle=True)
    return nomerge

def match_feature_post(dapm, voteab, votec):#赤经、纬、四个投票数据
    ans = []
    cntc = 0
#range里是匹配者的长度
    for i in tqdm(range(310579)):#310579
        a = voteab[(voteab.iauname == dapm.iloc[i, 0])].index.tolist()
        #print(a)
        if len(a) != 0:
            cntc = cntc+1
            ans.append([str(voteab.iloc[a[0], 1]), str(voteab.iloc[a[0], 2]), str(dapm.iloc[i, 2]), str(dapm.iloc[i, 4])]) #赤经赤纬，需要的投票数据的列数

        elif len(a) == 0:
            b = votec[(votec.iauname == dapm.iloc[i, 0])].index.tolist()
            #print(b)
            if len(b) != 0:
                cntc = cntc + 1
                ans.append([str(votec.iloc[b[0], 1]), str(votec.iloc[b[0], 2]), str(dapm.iloc[i, 2]), str(dapm.iloc[i, 4])])#赤经赤纬，需要的投票数据的列数

            # else:
            #     cntc = cntc +1 #cntc：未匹配上的个数
    #print(cntc)
    #print(np.shape(ans))
    return ans, cntc

def download(info):
    # url = 'http://skyserver.sdss.org/dr16/SkyServerWS/ImgCutout/getjpeg?TaskName=Skyserver.Chart.List&ra=' + str(info[0]) + '&dec=' + str(info[1]) + '&scale=0.3&width=120&height=120&opt=Ω'
    url = 'https://www.legacysurvey.org/viewer/fits-cutout?ra=' + str(info[0]) + '&dec=' + str(info[1]) + '&layer=dr8-south&pixscale=0.262&bands=grz'
    if os.path.exists('/data/pair/nomerge/' + str(info[0]) + '_' + str(info[1]) + '_' + str(info[3]) + '.fits') != True:
        response = requests.get(url)
        img = response.content
        with open('/data/pair/nomerge/' + str(info[0]) + '_' + str(info[1]) + '_' + str(info[3]) + '.fits', 'wb') as f:
            f.write(img)
    else:
        print('/data/pair/nomerge/' + str(info[0]) + '_' + str(info[1]) + '_' + str(info[3]) + '.fits' + '已经存在！')

if __name__ =='__main__':
    feature_merge, voteab, votec = get_data()
    cnt = False
    abs = []
    #print(np.shape(feature_merge))
    if os.path.exists('nomerge.npy') != True:
        ans = []
        cntc = 0
        ans, cntc = match_feature_post(feature_merge, voteab, votec)
        np.save('nomerge.npy', np.array(ans))
        cnt = True
        print(cntc)
        print(np.shape(ans))
    else:
        cnt = True
    #print(np.shape(feature_merge))
    #print(np.shape(ans))

    if cnt:
        abs = []
        abs = get_nomerge()
        #
        print(np.shape(abs))
        for info in tqdm(abs):
            #print(ans[0])
            download(info)



