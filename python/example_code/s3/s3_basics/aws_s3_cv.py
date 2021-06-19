from bucket_basics import get_s3, list_my_buckets
import boto3
from  file_transfer import upload_with_default_configuration

file_path = '/home/oleg/PycharmProjects/opencv-ffmpeg-services/media/images/cam_01/210615_cam_01/210615-105431-cam_01.jpg'

# Авторизация
s3_aws = boto3.client(
                  service_name='s3',
)


# s3_selectel = boto3.client(
#                   service_name='s3',
#                   # region_name='ru-1',
#                   # aws_access_key_id='61972_tl ',
#                   # aws_secret_access_key='5r_)3uFQj>',
#                   endpoint_url='https://s3.selcdn.ru'
# )


s3 = s3_aws

# Загрузка объекта из строки
# s3.put_object(Bucket='og-firstbucket', Key='ObjectName1', Body='Test')

# Загрузка объекта из файла
s3.upload_file(file_path, 'og-firstbucket', 'ObjectName2')


# # Получение списка объектов в бакете
# for key in s3.list_objects(Bucket='og-firstbucket')['Contents']:
#     print(key['Key'])


# # Скачивание объекта
# get_object_response = s3.get_object(Bucket='og-firstbucket', Key='ObjectName2')
# print(get_object_response['Body'].read())

# # Удаление нескольких объектов
# objects_to_delete = [{'Key': 'ObjectName1'}, {'Key': 'ObjectName2'}]
# s3.delete_objects(Bucket='og-firstbucket', Delete={'Objects': objects_to_delete})
