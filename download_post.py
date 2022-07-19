from astropy.io import fits
import numpy as np
import requests
from tqdm import tqdm
import cv2
import os
import pandas as pd
from glob import glob

def get_data():
    data = np.load("merge_ra_dec_post.npy", allow_pickle=True)
    return data

def download(info):
    # url = 'http://skyserver.sdss.org/dr16/SkyServerWS/ImgCutout/getjpeg?TaskName=Skyserver.Chart.List&ra=' + str(info[0]) + '&dec=' + str(info[1]) + '&scale=0.3&width=120&height=120&opt=Ω'
    url = 'https://www.legacysurvey.org/viewer/fits-cutout?ra=' + str(info[0]) + '&dec=' + str(info[1]) + '&layer=dr8-south&pixscale=0.262&bands=grz'
    if os.path.exists('/data/pair/merge/' + str(info[0]) + '_' + str(info[1]) + '_' + str(info[4])  + '.fits') !=True:
        response = requests.get(url)
        img = response.content
        with open('/data/pair/merge/' + str(info[0]) + '_' + str(info[1]) + '_' + str(info[4])  + '.fits', 'wb') as f:
            f.write(img)
    else:
        print('/data/pair/merge/' + str(info[0]) + '_' + str(info[1]) + '_' + str(info[4])  + '.fits' + '已经存在！')

def label(belabed):
    ans = []
    for i, line in enumerate(belabed):
        if float(line[5]) > 0.7:
            ans.append([line[0], line[1], line[2:5], "merger", 0])
        elif float(line[4]) > 0.6:
            ans.append([line[0], line[1], line[2:5], "post-merger", 1])
        elif float(line[3]) > 0.4:
            ans.append([line[0], line[1], line[2:5], "asymmetric-low", 2])
        else:
            ans.append([line[0], line[1], line[2:5], "none", 3])
    return ans

def simple_rename(data, path='merge_FITS/'):
    for info in data:
        file_path = 'merge_FITS/' + str(info[0]) + '_' + str(info[1]) + '_grz_' + '.fits'
        final_name = 'merge_FITS/' + str(info[0]) + '_' + str(info[1]) + '_' + str(info[4])  + '.fits'
        cmd = 'mv ' + file_path + ' ' + final_name
        os.system(cmd)



if __name__ == '__main__':
    merge_post = get_data()
    ans = label(merge_post)
    for info in tqdm(ans):
        download(info)
    print(vis)
