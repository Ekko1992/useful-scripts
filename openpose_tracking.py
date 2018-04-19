#!/usr/bin/python
# -*- coding: utf-8 -*-
# vim: expandtab:ts=4:sw=4
# --------------------------------------------------------
# Author  : Long
# Contact : lcui@vmaxx.tech
# Desc    : For Walmart Action Demo
# File    : demo_generator.py
# Software: PyCharm
# Time    : 18-1-5
# Copyright (c) 2018 Vmaxx Inc.
# --------------------------------------------------------

import json
import cv2
import argparse
import os
import numpy as np
from enum import Enum
import colorsys
from lib.deep_sort import nn_matching
from lib.deep_sort.detection import Detection
from lib.deep_sort.tracker import Tracker



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
]   # = 19
CocoPairsRender = CocoPairs[:-2]


def create_unique_color_uchar(tag, hue_step=0.41):
    h, v = (tag * hue_step) % 1, 1. - (int(tag * hue_step) % 4) / 5.
    r, g, b = colorsys.hsv_to_rgb(h, 1., v)
    return int(255*r), int(255*g), int(255*b)


def draw_humans(img, human_list, box_ids, frame_idx):
    img_copied = np.copy(img)
    content = ''
    # image_h, image_w = img_copied.shape[:2]
    centers = {}
    for idx, human in enumerate(human_list):
        pose_key_points = human.get('pose_keypoints')

        x = pose_key_points[::3]
        
        y = pose_key_points[1::3]
        
        x_tmp = []
        y_tmp = []
        for xi in x:
            if not int(xi) == 0:
                x_tmp.append(xi)
        for yi in y:
            if not int(yi) == 0:
                y_tmp.append(yi)
        

        x1 = float(min(x_tmp))
        y1 = float(min(y_tmp))
        x2 = float(max(x_tmp))
        y2 = float(max(y_tmp))

        iou = []
        for box in box_ids:
            box_x1 = box[1]
            box_y1 = box[2]
            box_x2 = box[1] + box[2]
            box_y2 = box[2] + box[4]
            w = min(x2, box_x2) - max(x1, box_x1) - 1
            h = min(y2, box_y2) - max(y1, box_y1) - 1
            if w <= 0 or h <= 0:
                iou.append(0)
            else:
                inter = float(w * h)
                aarea = (x1 - x2 + 1) * (y1 - y2 + 1);
                barea = (box_x1 - box_x2 + 1) * (box_y1 - box_y2 + 1);
                iou.append(inter / (aarea + barea - inter))
        max_iou_idx = iou.index(max(iou))

        color = create_unique_color_uchar(box_ids[max_iou_idx][0])

        content += '%d %d ' % (frame_idx, box_ids[max_iou_idx][0])
        for i in range(18):
            content += '%d %d ' % (pose_key_points[i*3], pose_key_points[i*3+1])
        content += 'None \n'

        # draw point
        for i in range(18):
            center = (int(pose_key_points[i*3] + 0.5), int(pose_key_points[i*3+1] + 0.5))
            centers[i] = center
            if center == (0, 0):
                continue
            cv2.circle(img_copied, center, 3, color, thickness=3, lineType=8, shift=0)

        # draw line
        for pair_order, pair in enumerate(CocoPairsRender):
            if centers[pair[0]] == (0, 0) or centers[pair[1]] == (0, 0):
                continue
            cv2.line(img_copied, centers[pair[0]], centers[pair[1]], color, 2)

        # cv2.putText(img_copied, 'aaa', (centers[0][0]-20, centers[0][1]-20), cv2.FONT_HERSHEY_COMPLEX, 1, color, 2)

    return img_copied, content


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


def is_in_zone(center, poly):
    poly_x = poly[::2]
    poly_y = poly[1::2]
    res = False
    i = -1
    l = len(poly_x)
    j = l - 1
    while i < l - 1:
        i += 1
        if ((poly_x[i] <= center[0] and center[0] < poly_x[j]) or
                (poly_x[j] <= center[0] and center[0] < poly_x[i])):
            if (center[1] < (poly_y[j] - poly_y[i]) * (center[0] - poly_x[i]) / (poly_x[j] - poly_x[i]) + poly_y[i]):
                res = not res
        j = i
    return res


def polygon_filter(human_list, polygon):
    new_list = []
    boxes = []
    for idx, human in enumerate(human_list):
        pose_key_points = human.get('pose_keypoints')
        x = pose_key_points[::3]
        y = pose_key_points[1::3]

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

        x_min = float(min(x2))
        y_min = float(min(y2))
        w = float(max(x2) - x_min + 1)
        h = float(max(y2) - y_min + 1)
        if w * h < 5000:
            continue

        flag = False
        for poly in polygon:
            if is_in_zone((cx, cy), poly):
                flag =  True
        if flag:
            new_list.append(human)
            boxes.append([x_min, y_min, w, h])
    return new_list, boxes


def draw_trackers(frame, tracks):
    boxes_ids = []
    for track in tracks:
        # if not track.is_confirmed() or track.time_since_update > 0:
        #     continue
        if track.time_since_update > 0:
             continue
        color = create_unique_color_uchar(track.track_id)
        x, y, w, h = track.to_tlwh()
        pt1 = int(x), int(y)
        pt2 = int(x + w), int(y + h)
        cv2.rectangle(frame, pt1, pt2, color, 1)
        label = str(track.track_id)
        text_size = cv2.getTextSize(
            label, cv2.FONT_HERSHEY_PLAIN, 0.4, 1)
        center = pt1[0] + 2, pt1[1] + 5 + text_size[0][1]
        pt2 = pt1[0] + 29 + text_size[0][0], pt1[1] + 10 + \
              text_size[0][1]
        cv2.rectangle(frame, pt1, pt2, color, -1)
        cv2.putText(frame, label, center, cv2.FONT_HERSHEY_COMPLEX,
                    0.4, (255, 255, 255), 1)
        boxes_ids.append([track.track_id, x, y, w, h])
    return boxes_ids

        # self.viewer.rectangle(
        #     *track.to_tlwh().astype(np.int),alpha=0.5,thickness=thick,color="null", copyedImage=self.viewer.image ,label=str(track.track_id))



def parse_args():
    """ Parse command line arguments.
    """
    parser = argparse.ArgumentParser(description="Action Demo")
    parser.add_argument(
        "-video_dir", help="Path to input vedio",
        default=None, required=True)
    parser.add_argument(
        "-json_dir", help="Path to input json",
        default=None, required=True)
    parser.add_argument(
        "-polygon", action='append', nargs='*', type=int, help="Points list for zones",
        default=[], required=False)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    vc = cv2.VideoCapture(args.video_dir)
    h = int(vc.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))
    w = int(vc.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH))
    fps = float(vc.get(cv2.cv.CV_CAP_PROP_FPS))
    max_frame_idx = int(vc.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))

    VIDEO_SAVE = True
    IMG_SAVE = False
    if VIDEO_SAVE:
        fourcc = cv2.cv.CV_FOURCC('M','J','P','G')
        videoWriter = cv2.VideoWriter('./openpose_tracking_video.avi', fourcc, 15, (w, h))

    json_list = os.listdir(args.json_dir)
    json_list.sort()

    max_cosine_distance_person = 0.1
    nn_budget = 128
    max_age_person = 30
    metric_person = nn_matching.NearestNeighborDistanceMetric(
        "cosine", max_cosine_distance_person, nn_budget)
    tracker_person = Tracker(metric_person, 0.7, max_age_person, 3)

    #with open('pose_tmp.txt', 'w+') as fpose:
    for i, json_path in enumerate(json_list):
        with open(args.json_dir + json_path.strip(), 'r') as f:
            json_content = json.load(f)
        human_list = json_content.get('people')

        human_list, boxes = polygon_filter(human_list, args.polygon)
        print len(human_list), len(boxes), i
        flag, frame = vc.read()
        detections_person = []
        for box in boxes:
            detections_person.append(Detection(np.array(box[0:4]), 1.0, range(128)))
            x = box[0]
            y = box[1]
            w = box[2]
            h = box[3]
            pt1 = int(x), int(y)
            pt2 = int(x + w), int(y + h)
            # cv2.rectangle(frame, pt1, pt2, (0,255,0), 1)
        tracker_person.predict()
        person_del_id, person_feat_list = tracker_person.update(detections_person)

        boxes_ids = draw_trackers(frame, tracker_person.tracks)
        frame_res, content = draw_humans(frame, human_list, boxes_ids, i)
        # print content
        #if not content == '':
        #    fpose.write(content)
        draw_linesAndPolygons(frame_res, args.polygon)
        cv2.addWeighted(frame_res, 0.5, frame, 1 - 0.5, 0.0, frame_res)
        
        cv2.imshow('Walmart Action', frame_res)
        if VIDEO_SAVE:
            videoWriter.write(frame_res)
        if IMG_SAVE:
            p = str(i).zfill(6)
            cv2.imwrite('./res_tracking/'+p+'.jpg', frame_res)

        key = cv2.waitKey(1)
        if key & 255 == 27:  # ESC
            break
