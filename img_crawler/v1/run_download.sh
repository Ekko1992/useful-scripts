#!/bin/bash
CODE_PATH="/home/zhao/img_crawler"
DEFAULT_SAVE_PATH="res_pics"

################# download image from bing ####################
echo "start download images from Bing"
echo "$1"
sh "$CODE_PATH"/download_img/Bing_Download_Img.sh "$1" "$DEFAULT_SAVE_PATH" "$CODE_PATH"

echo "download images end"
###############################################################
