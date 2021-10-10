import json
import os
import boto3
from datetime import datetime, timedelta
import time

from botocore.exceptions import ClientError


def lambda_handler(event, context):
    c_name = 'dobr'
    st_hr = '09'
    end_hr = '20'
    dt_ = '191030'
    _range = '1'
    rg = int(_range)

    # camera_ = 'cam_02'
    # start_hour = '10'
    # end_hour = '11'
    # start_date = '210827'
    # _range = '1'
    # rg = int(_range)

    res = '1280x720'
    dur = '30'

    if res == '1920x1080':
        res = '1920x1080'
        bitr = '11000'
    elif res == '1280x720':
        res = '1280x720'
        bitr = '1000k'

    txt_list_time = time.time()
    s3 = boto3.resource('s3')
    my_bucket = s3.Bucket('og-firstbucket')
    # hr_ = '08:00-17:00' #  DELETE IT
    res_im_list = ['', 0]

    # camera_ = 'dobr'
    # start_hour = '09'
    # end_hour = '15'
    # start_date = '191030'
    # _range = '1'
    # rg = int(_range)

    ffmpeg_txt = dt_ + '_' + _range + '-' + st_hr + '-' + end_hr + '.txt'

    i = 0
    dt = dt_
    for r in range(0, rg):
        dir_path = os.path.join('images', c_name, dt + '_' + c_name)

        files = []
        for object_summary in my_bucket.objects.filter(Prefix=dir_path):
            files.append(object_summary.key)
            jpg_lst = list(filter(lambda x: x.endswith('.jpg'), files))
        # print(f'1. {dt} qty of files in directory {dir_path} --> {len(jpg_lst)}, {start_hour}  --> {end_hour}')
        lst = list(range(int(st_hr), int(end_hr)))
        images = []
        for l in lst:
            st = str(l)
            if len(str(l)) < 2:
                st = '0' + str(l)
            im = list(filter(lambda x: (dt + '-' + st) in x, jpg_lst))
            images.extend(im)
        # print(f'2.{dt}-{start_hour} im list in {dt}  -->  {dt} IMAGES --> {len(images)}')
        images = sorted(images)

        ffmpeg_txt_path = f'/tmp/' + ffmpeg_txt
        f = open(ffmpeg_txt_path, 'w')
        f.close()
        s3_client = boto3.client('s3')
        for im in images:
            i += 1
            im_lambda_path = f'/tmp/' + im.split('/')[-1]
            s3_client.download_file('og-firstbucket', im, im_lambda_path)
            st = 'file ' + "\'" + im.split('/')[-1] + "\'\n"
            f = open(ffmpeg_txt_path, 'a')
            f.write(st)
            f.close()
        # print(images)

        date_obj = datetime.strptime(dt, '%y%m%d')  # datetime.strptime(cht_sets[c_cam][field_name], '%y%m%d')
        date_obj += timedelta(days=1)
        dt = datetime.strftime(date_obj, "%y%m%d")
    txt_list_time = time.time() - txt_list_time
    files = os.listdir(f'/tmp/')
    jpg_lst = list(filter(lambda x: x.endswith('.jpg'), files))
    # print(f'JPGs in lambda\'s /tmp/: {jpg_lst}')
    # os.system(f"cat /tmp/{ffmpeg_txt}")
    im_list_fl = [f'/tmp/' + ffmpeg_txt, i]  # List of 2 ->  [0] - path to list image file, [1] - count of image files

    #   FFMPEG section -----------------

    ffmpeg_time = time.time()
    print(im_list_fl)
    print("quantity of jpeg's --> ", im_list_fl[1])
    print(f'\nDuration for 60 fps - {i / 60}'
          f'\nDuration for 30 fps - {i / 30}'
          f'\nDuration for 20 fps - {i / 20}')

    r_in = im_list_fl[1] // int(dur)  # Frames per sec
    if r_in == 0:
        r_in = 5 - (im_list_fl[1] // 60)
        print("r_in = 0")
    elif r_in > 20:
        r_in = 15
        print("r_in > 20")

    ffmpeg_mp4 = dt_ + '_' + _range + '-' + st_hr + '-' + end_hr + '.mp4'
    lambda_video_output = f'/tmp/' + ffmpeg_mp4
    s3_video_output = os.path.join('video', ffmpeg_mp4)

    print("VIDEO_PATH --> ", lambda_video_output)
    print('Prepare data for FFMPEG now complete: ', s3_video_output)

    try:
        # myCmd = f"ffmpeg -loglevel error -stats -r {r_in} -y -f concat -safe 0 -i {im_list_fl[0]} -c:v libx264 -vf scale={res} -b:v {bitr} -pix_fmt yuv420p {video_path}"
        os.system(
            f"/opt/ffmpeglib/ffmpeg -loglevel error -stats -r {r_in} -y -f concat -safe 0 -i {im_list_fl[0]} -c:v libx264 -vf scale={res} -b:v {bitr} -pix_fmt yuv420p {lambda_video_output}")
        # os.system(f"ffmpeg -loglevel error -stats -r {r_in} -y -f concat -safe 0 -i {im_list_fl[0]} -c:v libx264 -vf scale={res} -b:v {bitr} -pix_fmt yuv420p {lambda_video_output}")

    except Exception as e:
        print(e)

    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(lambda_video_output, 'og-firstbucket', s3_video_output)
        print(f'{s3_video_output} -- {response}')

    except ClientError as e:
        print(f'{s3_video_output} -- {e}')
        return False
    ffmpeg_time = ffmpeg_time - time.time()
    print(f"-----\nTotal images - {i} in list for FFMPEG for  {txt_list_time} seconds / {txt_list_time / i} /---")
    print(f"-----\nTotal images - {i} in list for FFMPEG for  {ffmpeg_time} seconds / {ffmpeg_time / i} /---")

    return s3_video_output
# import boto3
#
# def st1():
#     client = boto3.client('s3')
#     paginator = client.get_paginator('list_objects')
#     result = paginator.paginate(Bucket='og-firstbucket', Delimiter='/')
#     for prefix in result.search('CommonPrefixes'):
#         print(prefix.get('prefix'))
#
#
# def st2():
#     s3 = boto3.resource('s3')
#
#     my_bucket = s3.Bucket('bucket_name')
#
#     for file in my_bucket.objects.all():
#         print(file.key)
#
#
# st1()