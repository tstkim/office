# folder_setup.py
import os
import shutil
from config import start_time, brand_code

# 폴더 생성
base_path = f'C:/Users/ME/Pictures/{start_time}{brand_code}'
thumbnail_path = f'{base_path}/cr'
output_path = f'{base_path}/output'

def setup_folders():
    if os.path.exists(base_path):
        shutil.rmtree(base_path)
    os.makedirs(thumbnail_path)
    os.makedirs(output_path)
    print("Folders created successfully.")

if __name__ == "__main__":
    setup_folders()
