import os
import time

source_path = 'source'

dirs = os.listdir(source_path)
files = []
for file in dirs:
    if not file.endswith('.py') and not file.endswith('.pdf'):
        files.append(os.path.join(source_path, file))

for file in files:
    if file.endswith('.MOV'):
        os.system('mkdir ' + file.removesuffix('.MOV'))
        os.system('mkdir ' + file.removesuffix('.MOV') + '/images_orig')
        time.sleep(0.5)
        os.system('mv ' + file + ' ' + file.removesuffix('.MOV'))
    if file.endswith('.mp4'):
        os.system('mkdir ' + file.removesuffix('.mp4'))
        os.system('mkdir ' + file.removesuffix('.mp4') + '/images_orig')
        time.sleep(0.5)
        os.system('mv ' + file + ' ' + file.removesuffix('.mp4'))
