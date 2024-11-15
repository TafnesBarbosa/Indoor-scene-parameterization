import cv2
import os
import numpy as np
from time import sleep

def compute_laplacian(images_paths):
    varis = []
    for k, image_path in enumerate(images_paths):
        if image_path.endswith('.png'):
            image = cv2.imread(image_path)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            var = cv2.Laplacian(gray, cv2.CV_64F).var()
            varis.append(var)
            if k % 50 == 0:
                print_progress_bar(k, len(images_paths))
    varis = np.array(varis)
    return varis

def delete_frames_with_more_blur(DIR, NUM_FRAMES, varis):
    divide = len(varis) // NUM_FRAMES
    for i in range(len(varis) // divide):
        idx = varis[i * divide:(i + 1) * divide].argmax() + i * divide
        for j in range(i * divide, (i + 1) * divide):
            if j != idx:
                os.system('rm ' + DIR + '/frame{:05d}.png'.format(j+1))
        print_progress_bar(i, len(varis) // divide)
    if divide * (len(varis) // divide) < len(varis):
        idx = varis[(len(varis) // divide) * divide:].argmax() + (i+1) * divide
        for j in range((len(varis) // divide) * divide,len(varis)):
            if j != idx:
                os.system('rm ' + DIR + '/frame{:05d}.png'.format(j+1))

def extract_frames(DIR, source_path, terminacao):
    if os.path.exists(DIR + '/images_orig'):
        os.system('rm ' + DIR + '/images_orig/*.jpg')
    else:
        os.system('mkdir ' + DIR + '/images_orig')
    os.system('ffmpeg -i ' + source_path + '/' + DIR + '/' + DIR + terminacao + ' ./' + DIR + r'/images_orig/frame%5d.png')

def preprocess_images(DIR):
    images_paths = os.listdir(DIR)
    images_paths = sorted(images_paths)
    images_paths = [DIR + '/' + image_path for image_path in images_paths]
    return images_paths

def print_progress_bar(iteration, total, bar_length=50):
    progress = (iteration / total)
    arrow = '█'
    spaces = ' ' * (bar_length - int(progress * bar_length))
    print(f'\rProgress: [{arrow * int(progress * bar_length)}{spaces}] {progress * 100:.2f}%', end='', flush=True)


DIRS = []
source_path = '/media/user/0E94B37D94B365BD/Users/user/Documents/new_gaussians'
files = os.listdir(source_path)
for file in files:
    if os.path.isdir(os.path.join(source_path, file)) and not file.startswith('.'):
        DIRS.append(file)

frame = 300 # approximated number of extracted frames
for DIR in DIRS:
    extract_frames(DIR, source_path, '.MOV')
    extract_frames(DIR, source_path, '.mp4')
    laplacians = compute_laplacian(preprocess_images(DIR + '/images_orig'))
    delete_frames_with_more_blur(DIR + '/images_orig', frame, laplacians)
    sleep(0.5)
