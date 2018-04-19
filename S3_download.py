
import boto3
import os


s3 = boto3.resource('s3')
bucket = s3.Bucket('vmaxx-disney')

def videoname_generator():
    for obj in bucket.objects.filter(Prefix="Disney/DisneySprings/"):
        if obj.key.endswith('mp4'):
            yield obj.key


for i in videoname_generator():

    root_path = '/home/ftptest/original_video/'
    name_list = i.split('/')
    if os.path.isdir(root_path + '/'.join(name_list[1:2]))==False:
        os.mkdir(root_path + '/'.join(name_list[1:2]))
    if os.path.isdir(root_path + '/'.join(name_list[1:3]))==False:
        os.mkdir(root_path + '/'.join(name_list[1:3]))
    if os.path.isdir(root_path + '/'.join(name_list[1:4]))==False:
        os.mkdir(root_path + '/'.join(name_list[1:4]))
    if os.path.isdir(root_path + '/'.join(name_list[1:5]))==False:
        os.mkdir(root_path + '/'.join(name_list[1:5]))

    s3.Object('vmaxx-disney',i).download_file(root_path + '/'.join(name_list[1:6]))
    print(i + '  ' + 'download success')

