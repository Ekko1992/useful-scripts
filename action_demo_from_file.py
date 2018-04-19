#!/usr/bin/python
# -*- coding: utf-8 -*-
# vim: expandtab:ts=4:sw=4
# --------------------------------------------------------
# Author  : Long
# Contact : lcui@vmaxx.tech
# Desc    : Walmort Demo
# File    : action_demo_from_file.py
# Software: PyCharm
# Time    : 18-1-8
# Copyright (c) 2017 Vmaxx Inc.
# --------------------------------------------------------

import os
import colorsys
import cv2
import numpy as np
from enum import Enum


class CocoPart(Enum):
    Nose = 0
    Neck = 1
    RShoulder = 2
    RElbow = 3
    RWrist = 4
    LShoulder = 5
    LElbow = 6
    LWrist = 7
    RHip = 8
    RKnee = 9
    RAnkle = 10
    LHip = 11
    LKnee = 12
    LAnkle = 13
    REye = 14
    LEye = 15
    REar = 16
    LEar = 17
    Background = 18


CocoPairs = [
    (1, 2), (1, 5), (2, 3), (3, 4), (5, 6), (6, 7), (1, 8), (8, 9), (9, 10), (1, 11),
    (11, 12), (12, 13), (1, 0), (0, 14), (14, 16), (0, 15), (15, 17), (5, 17), (2, 16)
]  # = 19
CocoPairsRender = CocoPairs[:-2]


def create_unique_color_uchar(tag, hue_step=0.41):
    h, v = (tag * hue_step) % 1, 1. - (int(tag * hue_step) % 4) / 5.
    r, g, b = colorsys.hsv_to_rgb(h, 1., v)
    return int(255 * r), int(255 * g), int(255 * b)


def draw_humans(img, contents):
    img_copied = np.copy(img)

    # image_h, image_w = img_copied.shape[:2]
    centers = {}
    h_times = 0
    m_times = 0
    l_times = 0
    f_times = 0
    n_times = 0
    for idx, content in enumerate(contents):
        id = int(content[1])
        x = map(int, content[2:-5:2])
        y = map(int, content[3:-4:2])

        color = create_unique_color_uchar(id)

        # draw point
        for i in range(18):
            center = (int(x[i] + 0.5), int(y[i] + 0.5))
            centers[i] = center
            if center == (0, 0):
                continue
            cv2.circle(img_copied, center, 3, color, thickness=3, lineType=8, shift=0)

        # draw line
        for pair_order, pair in enumerate(CocoPairsRender):
            if centers[pair[0]] == (0, 0) or centers[pair[1]] == (0, 0):
                continue
            cv2.line(img_copied, centers[pair[0]], centers[pair[1]], color, 2)

        action = str(content[41]).strip()

        flag = False
        if action == 'h':
            label = 'Touch High'
            flag = True
        elif action == 'm':
            label = 'Touch Middle'
            flag = True
        elif action == 'l':
            flag = True
            label = 'Touch Low'

        flag2 = False
        distance = str(content[44]).strip()
        if distance == 'n':
            label2 = 'Touch Near'
            flag2 = True
        elif distance == 'f':
            label2 = 'Touch Far'
            flag2 = True

        id = str(content[1])

        x2 = []
        y2 = []
        for xi in x:
            if not int(xi) == 0:
                x2.append(xi)
        for yi in y:
            if not int(yi) == 0:
                y2.append(yi)

        cx = int((max(x2) + min(x2)) / 2)
        cy = int((max(y2) + min(y2)) / 2)

        # cv2.putText(img_copied, id, (centers[1][0], centers[1][1] - 60), cv2.FONT_HERSHEY_COMPLEX, 1, color, 2)

        if flag:
            cv2.putText(img_copied, label, (centers[1][0]-20, centers[1][1]-20), cv2.FONT_HERSHEY_COMPLEX, 1, color,2)
        if flag2:
            cv2.putText(img_copied, label2, (centers[1][0]-20, centers[1][1]+35), cv2.FONT_HERSHEY_COMPLEX, 1, color,2)

        h_times += int(content[38])
        m_times += int(content[39])
        l_times += int(content[40])
        n_times += int(content[43])
        f_times += int(content[42])
        
    return img_copied, h_times, m_times, l_times, f_times, n_times


def draw_linesAndPolygons(frame, polys):
    colors = [[0, 0, 255], [0, 255, 0], [255, 0, 0], [255, 255, 0], [255, 0, 255]]  # red, green, blue, ching
    color_idx = 0

    for poly in polys:
        polyLength = len(poly)
        poly_list = []
        for i in range(0, polyLength, 2):
            poly_list.append([poly[i], poly[i + 1]])
        img_cpy = frame.copy()
        cv2.fillConvexPoly(img_cpy, np.array(poly_list), colors[int(color_idx % 5)])
        cv2.addWeighted(frame, 0.7, img_cpy, 1 - 0.7, 0.0, frame)
        color_idx += 1
    return frame


if __name__ == "__main__":
    video_path = './test.mp4'
    max_frame = 3599
    polygon = [[1270, 120, 792, 359, 773, 941, 1346, 1074, 1535, 511, 1507, 174]]
    f = open('./pose.txt')
    vc = cv2.VideoCapture(video_path)
    h = int(vc.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))
    w = int(vc.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH))
    
    VIDEO_SAVE = True
    IMG_SAVE = True

    if VIDEO_SAVE:
        fourcc = cv2.cv.FOURCC('M', 'J', 'P', 'G')
        out = cv2.VideoWriter('./action_demo.avi', fourcc, 15, (w, h))  

    h_times = int(0)
    m_times = int(0)
    l_times = int(0)
    f_times = int(0)
    n_times = int(0)

    min_frame = 0

    lines = f.readlines()
    for frame_idx in range(min_frame, max_frame):
        vc_flag, frame = vc.read()
        flag = True
        contents = []

        while flag:
            line = lines[0]
            nums = line.split(',')
            if int(nums[0]) == frame_idx:
                contents.append(nums)
                flag = True
                lines.pop(0)
            elif int(nums[0]) > frame_idx:
                flag = False

        frame2 = frame.copy()
        cv2.rectangle(frame, (0, 0), (870, 100), (0, 0, 0), -1)
        cv2.addWeighted(frame2, 0.5, frame, 1 - 0.5, 0.0, frame)

        frame_res, h, m, l, f, n = draw_humans(frame, contents)
        #draw_linesAndPolygons(frame_res, polygon)
        cv2.addWeighted(frame_res, 1, frame, 1 - 1, 0.0, frame_res)

        h_times += h
        m_times += m
        l_times += l
        f_times += f
        n_times += n
        count_str1 = 'Touch High: ' + str(h_times)
        count_str2 = 'Touch Middle: ' + str(m_times)
        count_str3 = 'Touch Low: ' + str(l_times)

        count_str4 = 'Far Touch: ' + str(f_times)
        count_str5 = 'Near Touch: ' + str(n_times)

        # print count_str
        cv2.putText(frame_res, count_str1, (15, 40), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(frame_res, count_str2, (290, 40), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(frame_res, count_str3, (595, 40), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(frame_res, count_str4, (15, 80), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(frame_res, count_str5, (290, 80), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
        cv2.imshow('Walmart Action', frame_res)

        if VIDEO_SAVE:
            out.write(frame_res)

        print frame_idx
        if IMG_SAVE:
            p = str(frame_idx).zfill(6)
            cv2.imwrite('./result_action_detection/' + p + '.jpg', frame_res)
        key = cv2.waitKey(1)
        if key & 255 == 27:  # ESC
            break


