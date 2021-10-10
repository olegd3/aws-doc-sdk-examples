import os.path
# import sys
from datetime import datetime
import time
import cv2
import os
import boto3

local_path = os.getcwd()
local_path = os.path.join(local_path, '../media')

MEDIA_PATH = local_path


def url_compose(camera):
    """ Compose URL string for the camera """
    # rtsp://88.204.57.242:5533/user=admin&password=******&channel=1&stream=1.sdp?
    url: str = f'rtsp://{camera.ip_addr}:{camera.port}/user={camera.login}&password={camera.password}&channel=1&stream=0.sdp?'
    return url


def save_dsk(path_, name_, img_):
    try:
        save_path = os.path.join(MEDIA_PATH, path_)
        if not os.path.exists(save_path):
            os.makedirs(save_path, 0o775)
            print(f'Created directory  {save_path}')
        save_file = os.path.join(MEDIA_PATH, path_, name_)
        print(f'Saved FILE -> {name_} PATH -> {save_path}, ')
        cv2.imwrite(save_file, img_)  # if img is numpy array
        return save_file

    except Exception as error_conn:
        print('!!! save_dsk can''t save image')
        print(error_conn)


def save_s3(path_, name_, img_):
    try:
        s3_aws = boto3.client(
            service_name='s3',
            # region_name='ru-1',
            # aws_access_key_id='61972_tl ',
            # aws_secret_access_key='5r_)3uFQj>',
            # endpoint_url='https://s3.selcdn.ru'
        )

        save_file = save_dsk(path_, name_, img_)
        s3_object_fullname = os.path.join(path_, name_)
        s3_aws.upload_file(save_file, 'og-firstbucket', s3_object_fullname)
        print(f'Saved OBJECT -> {s3_object_fullname} from PATH -> {save_file}, ')

        return s3_object_fullname

    except Exception as error_conn:
        print('!!! save_dsk can''t save image')
        print(error_conn)


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
    def __init__(self, cam) -> object:
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


class snapshot:
    def __init__(self, source):
        self.source = source
        self.dt = datetime.today().strftime("%y%m%d")
        self.tm = datetime.today().strftime("%H%M%S")

    def rtsp(self):
        name_jpeg = self.dt + '-' + self.tm + '-' + self.source.name + ".jpg"
        path_jpeg = os.path.join('images', self.source.name, (self.dt + '_' + self.source.name))
        object_content = snapshot_rtsp.get_img(self.source)
        return path_jpeg, name_jpeg, object_content


def main():
    snapshot01 = snapshot(camera01)
    path_jpeg, name_jpeg, object_content = snapshot01.rtsp()
    save_dsk(path_jpeg, name_jpeg, object_content)


if __name__ == '__main__':
    main()
