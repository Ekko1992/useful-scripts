#!/bin/bash

##############################################################
# shell  script for download images
##############################################################
#download img from Bing
#$1 : keyword
#$2 : path of saving download images
#$3 : source code path

# step 1 

python3 "$3"/download_img/Bing_Download_Img_A.py "$1" "$2"

# step 2 

#bingcount_B=20
#max_num_page_B=1000
#echo bingcount_B=$bingcount_B
#echo max_num_page_B=$max_num_page_B
#for((num=900;num<max_num_page_B;num=num+bingcount_B))
#do
#python3 "$3"/download_img/Bing_Download_Img_B.py "$1" "$2" -p $num
#done

# step 3 end

rm ""$2"/download_img/"$1".txt"




