#!/bin/python
import cv2
xml_dir = "../new_v2/Annotations/"
img_dir = "../new_v2/JPEGImages/"

#def xml_decoder():
	
'''
xml_name = xml_dir + "000001" + ".xml"
img_name = img_dir + "000001" + ".jpg"
'''
img = cv2.imread(img_name)

cv2.namedWindow("Image")
'''
cv2.rectangle(img,(783,316),(810,339),(55,255,155),1)
cv2.rectangle(img,(633,350),(666,371),(55,255,155),1)
cv2.rectangle(img,(410,327),(438,345),(55,255,155),1)
cv2.rectangle(img,(471,432),(506,457),(55,255,155),1)
cv2.rectangle(img,(431,420),(464,448),(55,255,155),1)
cv2.rectangle(img,(282,479),(333,508),(55,255,155),1)
cv2.rectangle(img,(164,673),(223,715),(55,255,155),1)
cv2.rectangle(img,(52,695),(146,741),(55,255,155),1)


cv2.rectangle(img,(780,316),(813,411),(155,55,255),1)
cv2.rectangle(img,(629,350),(670,437),(155,55,255),1)
cv2.rectangle(img,(407,327),(441,402),(155,55,255),1)
cv2.rectangle(img,(467,432),(510,535),(155,55,255),1)
cv2.rectangle(img,(427,420),(468,532),(155,55,255),1)
cv2.rectangle(img,(276,479),(339,596),(155,55,255),1)
cv2.rectangle(img,(157,673),(230,843),(155,55,255),1)
cv2.rectangle(img,(41,695),(157,882),(155,55,255),1)
'''
cv2.imshow("Image", img)
cv2.waitKey(0)




