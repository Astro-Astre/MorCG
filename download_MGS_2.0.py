from astropy.io import fits
import numpy as np
import pandas as pd
import requests
from tqdm import tqdm
import cv2
import os

def get_data():
    hdu_list = fits.open("MGS_out_DECaLS.fits")
    # hdu_list.info()
    hdu_data = hdu_list[1].data
    title = hdu_list[1].data.dtype
    return hdu_data, title

def download(info):
    # url = 'http://skyserver.sdss.org/dr16/SkyServerWS/ImgCutout/getjpeg?TaskName=Skyserver.Chart.List&ra=' + str(
    #     info[0]) + '&dec=' + str(info[1]) + '&scale=0.3&width=120&height=120&opt=Ω'
    url = 'https://www.legacysurvey.org/viewer/fits-cutout?ra=' + str(info[0]) + '&dec=' + str(info[1]) + '&layer=ls-dr9&pixscale=0.262&bands=grz'
    if os.path.exists('/data/pair/MGS_out_DECaLS/' + str(info[0]) + '_' + str(info[1]) + '_0.262' + '_grz_'  '.fits') !=True:
        response = requests.get(url)
        img = response.content
        with open('/data/pair/MGS_out_DECaLS/' + str(info[0]) + '_' + str(info[1]) + '_0.262' + '_grz_'  '.fits', 'wb') as f: #/Users/cmloveczy/Desktop/shao/Galaxy_classification/TEST #/data/pair/MGS_out_DECaLS/
            f.write(img)
    else:
        print('/data/pair/MGS_out_DECaLS/' + str(info[0]) + '_' + str(info[1]) + '_0.262' + '_grz_' + '.fits' + '已经存在！')


if __name__ == '__main__':
    hdu_data, title = get_data()
    #print(np.shape(hdu_data))#476890
    ans=[]
    for i in tqdm(range(0, 476890)):
        ans.append([hdu_data[i][1], hdu_data[i][2]])

    #print(np.shape(ans))
    #print(ans[0])
    for info in tqdm(ans):
        download(info)



