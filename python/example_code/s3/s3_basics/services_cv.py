import os.path
from datetime import datetime
import time
import cv2
import os
import boto3


local_path = os.getcwd()
local_path = os.path.join(local_path, '../media')


def url_compose(camera):
    """ Compose URL string for the camera """
    # rtsp://88.204.57.242:5533/user=admin&password=******&channel=1&stream=1.sdp?
    url: str = f'rtsp://{camera.ip_addr}:{camera.port}/user={camera.login}&password={camera.password}&channel=1&stream=1.sdp?'
    return url


class Camera:
    def __init__(self):
        self.name = ''
        self.login = ''
        self.password = ''
        self.ip_addr = ''
        self.port = ''
        self.cam_url = ''

    def get_img(self):
        return None


class Movie:
    def __init__(self):
        self.file_name = ''

    @staticmethod
    def get_img():
        return None


camera01 = Camera()
camera01.name = 'cam_01'
camera01.login = 'admin'
camera01.password = 'Ad-654321'
camera01.ip_addr = '88.204.57.242'
camera01.port = '5535'
camera01.cam_url = url_compose(camera01)

camera02 = Camera()
camera02.name = 'cam_02'
camera02.login = 'admin'
camera02.password = 'Ad-654321'
camera02.ip_addr = '88.204.57.242'
camera02.port = '5533'
camera02.cam_url = url_compose(camera02)


class snapshot_rtsp(Camera):
    def __init__(self, cam):
        Camera.__init__(self)
        self.cam_url = url_compose(cam)
        self.name = cam.name

    def get_img(self):
        t1 = time.time()
        # frame = []
        try:
            print(f'cam_name is  {self.name} URI - {self.cam_url}')
            cap = cv2.VideoCapture(self.cam_url)
            ret, frame = cap.read()
            return frame
        except Exception as error_conn:
            print('!!! Lost connection - ' + self.cam_url + datetime.today().strftime("%d.%m.%y") + '/' + datetime.today().strftime("%H-%M-%S"))
            print(error_conn)
        print(time.time() - t1)


class snapshot_movie(Movie):
    pass


def context_path(context, cam_name):
    dt = datetime.today().strftime("%y%m%d")
    tm = datetime.today().strftime("%H%M%S")
    s_path = os.path.join(context, cam_name, (dt + '_' + cam_name))
    if not os.path.exists(s_path):
        os.makedirs(s_path, 0o775)
    im_fl = os.path.join(s_path, (dt + '-' + tm + '-' + cam_name + ".jpg"))
    print(f'context_path {im_fl}')
    return im_fl


def save_dsk(img, cam_name):
    try:
        im_fl = os.path.join(local_path, context_path("images", cam_name))
        print(im_fl)
        cv2.imwrite(im_fl, img)  # if img is numpy array
        print(f'save_dsk {im_fl}')
        return im_fl

    except Exception as error_conn:
        print('!!! save_dsk can''t save image')
        print(error_conn)


def save_s3(img, cam_name):
    try:
        s3_aws = boto3.client(
            service_name='s3',
            # region_name='ru-1',
            # aws_access_key_id='61972_tl ',
            # aws_secret_access_key='5r_)3uFQj>',
            # endpoint_url='https://s3.selcdn.ru'
        )

        im_fl = save_dsk(img, cam_name)
        im_fl_s3 = context_path("images", cam_name)
        s3_aws.upload_file(im_fl, 'og-firstbucket', im_fl_s3)

        return im_fl

    except Exception as error_conn:
        print('!!! save_dsk can''t save image')
        print(error_conn)


def main():
    img01 = snapshot_rtsp.get_img(camera01)
    file01 = save_s3(img01, camera01.name)


if __name__ == '__main__':
    main()
