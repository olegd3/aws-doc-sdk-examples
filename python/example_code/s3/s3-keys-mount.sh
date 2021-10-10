# S3 Mount with Keys
# ---------------------
#!/bin/bash
#Purpose: S3 Mount via Access Keys
#Maintainer: Muhammad Asim <quickbook2018@gmail.com>
# OS: Ubuntu/Mac
# S3: Permissions Level Full Access


ACCESS_KEY_ID=AKIA5OFEI5DFSF24DRM2
SECRET_ACCESS_KEY=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
mount_point=/home/oleg/s3
#  mount_point=""$PWD"/s3"
bucket_name=og-firstbucket

# Ubuntu
#apt update -y
#apt install -y s3fs

# AmazonLinux
#amazon-linux-extras install -y epel
#yum install -y s3fs-fuse

# MACOS
#brew install --cask osxfuse
#brew install s3fs

echo ""$ACCESS_KEY_ID":"$SECRET_ACCESS_KEY"" > ${HOME}/.passwd-s3fs
chmod 600 ${HOME}/.passwd-s3fs

mkdir -p $mount_point

#/usr/bin/s3fs "$bucket_name" "$mount_point" -o passwd_file=${HOME}/.passwd-s3fs -o allow_other -o use_path_request_style
#/usr/bin/s3fs "$bucket_name" "$mount_point" -o passwd_file=${HOME}/.passwd-s3fs -o allow_other -o use_path_request_style o dbglevel=info -f -o curldbg
#/usr/bin/s3fs "$bucket_name" "$mount_point" -o passwd_file=${HOME}/.passwd-s3fs -o allow_other -o nonempty
/usr/bin/s3fs "$bucket_name" "$mount_point" -o passwd_file=${HOME}/.passwd-s3fs -o allow_other -o nonempty -o dbglevel=info -f -o curldbg