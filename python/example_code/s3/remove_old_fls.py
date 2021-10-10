import shutil
from datetime import datetime

from web.services.opencv_settings import *


def main():
	deleted_folders_count = 0
	deleted_files_count = 0
	# specify the path
	# days = 3
	# seconds = time.time() - (days * 24 * 60 * 60)
	seconds = 3 * 24 * 60 * 60
	dt_ = datetime.today().strftime("%d.%m.%y")
	tm_ = datetime.today().strftime("%H:%M:%S")
	print(f'Started at {dt_} {tm_}')

	# converting days to seconds
	# time.time() returns current time in seconds
	if os.path.exists(local_path):
		# iterating over each and every folder and file in the path
		for root_folder, folders, files in os.walk(local_path):
			for folder in folders:
				print(f'IN FOLDER {folder}  ------------------------------------')
				delete_items(os.path.join(root_folder, folder), seconds)


def delete_items(path, seconds):
	deleted_folders_count = 0
	deleted_files_count = 0
	root_folder = path
	# checking whether the file is present in path or not
	if os.path.exists(path):
		# iterating over each and every folder and file in the path
		for root_folder, folders, files in os.walk(path):
			# comparing the days
			if seconds >= get_file_or_folder_age(root_folder):
				remove_folder(root_folder)
				deleted_folders_count += 1 
				# incrementing count
				# breaking after removing the root_folder
				break
			else:
				# checking folder from the root_folder
				for folder in folders:
					# folder path
					folder_path = os.path.join(root_folder, folder)
					# comparing with the days
					if seconds >= get_file_or_folder_age(folder_path):
						# print(folder_path)
						# invoking the remove_folder function
						remove_folder(folder_path)
						deleted_folders_count += 1 # incrementing count
				for file in files:
					# file path
					file_path = os.path.join(root_folder, file)
					# comparing the days
					if seconds >= get_file_or_folder_age(file_path):
						# invoking the remove_file function
						remove_file(file_path)
						# print(file_path)
						deleted_files_count += 1 # incrementing count
		else:
			# if the path is not a directory
			# comparing with the days
			if seconds >= get_file_or_folder_age(path):
				# invoking the file
				remove_file(path)
				# print(f'"{path}" is FILE')
				deleted_files_count += 1 # incrementing count
	else:
		# file/folder is not found
		print(f'"{path}" is not found')
		deleted_files_count += 1 # incrementing count
	if deleted_folders_count > 0:
		print(f"In {root_folder} folders deleted: {deleted_folders_count}")
	if deleted_files_count > 0:
		print(f"In {root_folder} files deleted: {deleted_files_count}")
	return()


def remove_folder(path):
	# removing the folder
	if not shutil.rmtree(path):
		# success message
		print(f"{path} is removed successfully")
	else:
		# failure message
		print(f"Unable to delete the {path}")


def remove_file(path):
	# removing the file
	if not os.remove(path):
		# success message
		print(f"{path} is removed successfully")
	else:
		# failure message
		print(f"Unable to delete the {path}")


def get_file_or_folder_age(path):
	# getting ctime of the file/folder
	# time will be in seconds
	ctime = os.stat(path).st_ctime
	print(f'Path {path} - age is {ctime}')
	# returning the time
	return ctime


if __name__ == '__main__':
	main()
