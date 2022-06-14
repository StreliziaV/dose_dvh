#!/data/anaconda3/bin/python3
# -*- coding: utf-8 -*-
from init_config import  *
from dicompylercore.dicomparser import DicomParser
from dicompylercore.dvh import *
from dicompylercore.dvhcalc import *
import datetime

# import pydicom
import numpy as np
# import jax.numpy as np

import argparse
import matplotlib.pyplot as plt
# Qt5Agg Qt4Agg TkAgg WX WXAgg Agg Cairo GDK PS PDF SVG
#matplotlib.use('TkAgg')
matplotlib.use('Agg')
# matplotlib.use('Qt4Agg')
import cv2
from scipy import misc
from skimage.transform import rescale
from glob import glob
import re
import json
import time

def get_files(root_dir):
    _files=[]
    file_name_list = os.listdir(root_dir)
    for i in range(0,len(file_name_list)):
        path = os.path.join(root_dir,file_name_list[i])
        if os.path.isdir(path):
            _files += get_files(path)
        if os.path.isfile(path):
            _files.append(path)
    return _files


def calc_dvh(root_dir,patientID):
    
    fo = open(dose_result_dir, 'a+')            
    fo.write('PatientID:{},StartTime:{}'.format(patientID,time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))+"\n")
    fo.close()

    image_data_path = os.path.join(root_dir,patientID)
    mask_data_path = os.path.join(image_data_path,'mask')
    print(mask_data_path)
    organ_list=[]
    mask_list = glob(os.path.join(mask_data_path,'*.npz'))
    for item in mask_list:
        print(item)
        pattern = re.compile(r'[(](.*)[)]', re.S)
        organ_list.append(re.findall(pattern, item)[0])
    organ_list = np.unique(organ_list)
    print(len(organ_list))

    if show_selected_organs == True: #判断是否需要选择一部分器官来查看DVH图
        with open(configFile, 'r') as f:
            input_config = json.loads(f.read())
            show_selected_organs_list = input_config["show_selected_organs_list"][cancer_class]
        organ_list = list(set(show_selected_organs_list).intersection(set(organ_list)))

    fig=plt.figure()
    plt.yticks(np.arange(0,1.01,0.05))
    # plt.xticks(np.arange(0, 6000.01, 1000))
    # plt.xlim(0,6000)
    plt.ylim(0,1)
    for organ in organ_list:
        print('process {}...'.format(organ))
        organ_data=[]
        fake_organ_data = []
        mask_files = [file for file in mask_list if organ in file]        

        if 0:
            for mask_file in mask_files:
                #temp_mask_file = mask_file
                corresponsing_dose_file = mask_file.replace('-({})'.format(organ),'')
                _,slice_name = os.path.split(corresponsing_dose_file)
                corresponsing_dose_file = os.path.join(image_data_path,slice_name)
                dose_data = np.load(corresponsing_dose_file)['dose']
                #print(mask_file)
                mask = np.load(mask_file)['mask']
                fig, ax = plt.subplots(1, 2, figsize=(8, 4))
                ax[0].imshow(dose_data)
                ax[1].imshow(mask)
                #fig.show()
                fig.close()
                print(mask_file)

        for mask_file in mask_files:
            #temp_mask_file = mask_file
            corresponsing_dose_file = mask_file.replace('-({})'.format(organ),'')
            _,slice_name = os.path.split(corresponsing_dose_file)
            corresponsing_dose_file = os.path.join(image_data_path,'',slice_name)#input for local,infer_new for predosepy
            dose_data = np.load(corresponsing_dose_file)['dose']
            #print(mask_file)
            mask = np.load(mask_file)['mask']
            #fig, ax = plt.subplots(1, 2, figsize=(8, 4))
            #ax[0].imshow(dose_data)
            #ax[1].imshow(mask)
            #fig.show()

            print(mask_file)
            print(corresponsing_dose_file)
            print(dose_data.shape)
            print(mask.shape)
            mask_value = ma.array(dose_data, mask=~mask)

            mask_data = mask_value.compressed().tolist()
            organ_data =organ_data+mask_data

            #prediction DVH
            fake_dose_file = os.path.join(image_data_path,'infer')
            fake_dose_file = os.path.join(fake_dose_file, slice_name)
            if os.path.exists(fake_dose_file):
                dose_data = np.load(fake_dose_file)['dose']
                mask_value = ma.array(dose_data, mask=~mask)
                mask_data = mask_value.compressed().tolist()
                print(mask_file)
                #print('Max dose:{}'.format(np.mean(mask_data)))
                fake_organ_data = fake_organ_data + mask_data

        #real dvh
        organ_data = np.array(organ_data) * 100
        if len(fake_organ_data) > 0:
            fake_organ_data = np.array(fake_organ_data) * 100
            print('Max dose(True,Predicted):%0.2f~%0.2f' % (np.max(organ_data) / 100,np.max(fake_organ_data) / 10))
            print('Mean dose(True,Predicted):%0.2f~%0.2f' % (np.mean(organ_data) / 100,np.mean(fake_organ_data) / 100))
            print('Min dose(True,Predicted):%0.2f~%0.2f' % (np.min(organ_data[organ_data > 0]) / 100,np.min(fake_organ_data[fake_organ_data > 0]) / 100))
             #ligui 
            fo = open(dose_result_dir, 'a+')            
            fo.write('OrganName:{}'.format(organ)+"\n")
            fo.write('Max dose(True,Predicted):%0.2f~%0.2f\n' % (np.max(organ_data) / 100,np.max(fake_organ_data) / 100))
            fo.write('Mean dose(True,Predicted):%0.2f~%0.2f\n' % (np.mean(organ_data) / 100,np.mean(fake_organ_data) / 100))
            fo.write('Min dose(True,Predicted):%0.2f~%0.2f\n' % (np.min(organ_data[organ_data > 0]) / 100,np.min(fake_organ_data[fake_organ_data > 0]) / 100))
            fo.close()
        else:
            print('Max dose:%0.2f' % (np.max(organ_data)/100))
            print('Mean dose:%0.2f' % (np.mean(organ_data)/100))
            print('Min dose:%0.2f' % (np.min(organ_data)/100))
             #ligui 
            fo = open(dose_result_dir, 'a+')            
            fo.write('OrganName:{}'.format(organ)+"\n")
            fo.write('Max dose:%0.2f' % (np.max(organ_data)/100))
            fo.write('Mean dose:%0.2f' % (np.mean(organ_data)/100))
            fo.write('Min dose:%0.2f' % (np.min(organ_data)/100))
            fo.close()
           # print('Min dose:{}'.format(np.min(organ_data[organ_data > 0]) / 100))
          
    
        organ_data = rescale(organ_data, scale=10, mode='symmetric', order=1, preserve_range=True)
        hist, edges = np.histogram(organ_data,bins=int(round(np.max(organ_data))),range=(0,np.max(organ_data)))
        hist=[sum(hist[i:]/sum(hist)) for i in range(len(hist))]
        color = np.array(list(patterns[organ]))/255
        plt.plot(.5*(edges[1:]+edges[:-1]),hist,color=color,label=organ)

        if len(fake_organ_data)>0:
            fake_organ_data = np.array(fake_organ_data)
            fake_organ_data = rescale(fake_organ_data, scale=10, mode='symmetric', order=1, preserve_range=True)
            hist, edges = np.histogram(fake_organ_data, bins=int(round(np.max(fake_organ_data))), range=(0, np.max(fake_organ_data)))
            hist = [sum(hist[i:] / sum(hist)) for i in range(len(hist))]
            plt.plot(.5 * (edges[1:] + edges[:-1]), hist,'--',color=color)


        #prediction DVH
    plt.title('DVH:True(solid) vs Predicted(dash)')
    plt.xlabel('Dose(cGray)')
    plt.ylabel('Fraction Volume')
    plt.grid(True)
    plt.legend(loc='upper left')
    now_time=datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    # dst_data_path = os.path.join(FLAGS.test_dir, now_time)
    dst_data_path = FLAGS.test_dir
    if not os.path.exists(dst_data_path):
        os.makedirs(dst_data_path)
    dst_data_path = os.path.join(dst_data_path, 'image-[{}].png'.format(patientID+'_'+now_time))
    fig.savefig(dst_data_path)
   # plt.show()
   # time.sleep(5)
    plt.close(1)



def show_dvh(patientID):
    FLAGS.patientID=patientID
    if FLAGS.mode2 == 'show_dvh':
        print('show 2D dvh')
        paths = os.listdir(FLAGS.infer_data_dir)
        for file in paths:
            if os.path.isdir(os.path.join(FLAGS.infer_data_dir, file)):
                print(FLAGS.infer_data_dir)
                calc_dvh(FLAGS.infer_data_dir,FLAGS.patientID)
                break
    else:
        raise ValueError("Function [{}] not implemented".format(FLAGS.mode2))


if __name__ == '__main__':
    FLAGS.patientID='CT0426987A'
    show_dvh(FLAGS.patientID)
