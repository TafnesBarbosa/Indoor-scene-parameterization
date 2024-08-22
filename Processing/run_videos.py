import os
from time import time, sleep
import subprocess

COLMAP_LIMIT = 3

def is_wrong(path, file):
    diri_colmap = os.path.join(path, file, 'colmap/sparse')
    if len(os.listdir(diri_colmap)) > 1 or len(os.listdir(diri_colmap)) == 0:
        return True
    else:
        return False
    
def delete_dir(path, file, diri):
    if os.path.exists(os.path.join(path, file, diri)):
        os.system('rm -rf ' + os.path.join(path, file, diri))

def delete_colmap_dirs(path, file):
    delete_dir(path, file, 'colmap')
    delete_dir(path, file, 'images')
    delete_dir(path, file, 'images_2')
    delete_dir(path, file, 'images_4')
    delete_dir(path, file, 'images_8')
    delete_dir(path, file, 'transforms.json')
    delete_dir(path, file, 'sparse_pc.ply')

# Function to get GPU usage
def get_gpu_usage():
    try:
        result = subprocess.run(
            ["nvidia-smi", "--query-gpu=memory.used", "--format=csv,noheader,nounits"],
            capture_output=True,
            text=True,
            check=True
        )
        gpu_usage = result.stdout.strip()
        return gpu_usage
    except subprocess.CalledProcessError as e:
        print(f"Error querying GPU usage: {e}")
        return None
    
# Function to get GPU usage
def get_ram_usage():
    try:
        result = subprocess.run(
            ["free"],
            capture_output=True,
            text=True,
            check=True
        )
        ram_usage = result.stdout.strip()
        return ram_usage
    except subprocess.CalledProcessError as e:
        print(f"Error querying RAM usage: {e}")
        return None
    
def get_evaluations(source_folder, file, destination_folder, model):
    elems = [*range(10000, 100000, 10000)]
    elems.append(99999)
    for elem in elems:
        os.system('mv ' + source_folder + '/' + file + '/output/' + file + '/' + model + '/*/nerfstudio_models/step-0000' + str(elem) + '.ckpt ' + source_folder + '/' + file + '/output/' + file + '/' + model + '/*/')
        sleep(1)
    
    for elem in elems:
        os.system('mv ' + source_folder + '/' + file + '/output/' + file + '/' + model + '/*/step-0000' + str(elem) + '.ckpt ' + source_folder + '/' + file + '/output/' + file + '/' + model + '/*/nerfstudio_models/')
        sleep(1)
        os.system('mkdir "' + destination_folder + '/' + file + '"')
        os.system('ns-eval --load-config ' + source_folder + '/' + file + '/output/' + file + '/' + model + '/*/config.yml --output-source_folder "' + destination_folder + '/' + file + '/output_' + str(elem) + '.json"')

def main(source_folder, destination_folder, colmap=True, nerfacto=True, splatfacto=True, evaluate=True):
    files = []
    for file in os.listdir(source_folder):
        if not file.endswith('.py') and not file.endswith('.pdf') and not file.endswith('.txt'):
            files.append(file)

    with open(destination_folder + '/tempo_gasto.txt', 'w') as tempo_file:
        tempo_file.write('1 2 3\n')
        if colmap:
            # Colmap
            for k, file in enumerate(files):
                with open(os.source_folder.join(destination_folder, 'colmap/GPU', file) + '_gpu.txt', 'w') as gpu_file, open(os.source_folder.join(destination_folder, 'colmap/RAM', file) + '_ram.txt', 'w') as ram_file:
                    tempo_file.write('COLMAP ' + file + '\n')
                    print(f'Starting {k+1}/{len(files)}')
                    number_iterations = 0
                    is_wrong_flag = True
                    start = time()
                    while is_wrong_flag and number_iterations < COLMAP_LIMIT:
                        delete_colmap_dirs(source_folder, file)
                        cmd = [
                            "ns-process-data", "images", 
                            "--data", source_folder + "/" + file + "/images_orig", 
                            "--output-dir", source_folder + "/" + file, 
                            "--matching-method", "exhaustive"
                        ]
                        process = subprocess.Popen(cmd)
                        # Monitor GPU usage while the command is running
                        try:
                            while process.poll() is None:  # Check if process is still running
                                gpu_usage = get_gpu_usage()
                                ram_usage = get_ram_usage()
                                if gpu_usage:
                                    gpu_file.write(f"{gpu_usage}" + '\n')
                                if ram_usage:
                                    ram_file.write(f"{ram_usage}" + '\n')
                                sleep(1)  # Adjust the interval as needed
                        finally:
                            process.wait()  # Ensure the process completes
                            gpu_usage = get_gpu_usage()
                            ram_usage = get_ram_usage()
                            if gpu_usage:
                                gpu_file.write(f"{gpu_usage}" + '\n')
                            if ram_usage:
                                ram_file.write(f"{ram_usage}" + '\n')
                        is_wrong_flag = is_wrong(source_folder, file)
                        number_iterations += 1
                    end = time()
                    tempo_file.write(f'time: {end-start} s' + '\n')
                    tempo_file.write(f'colmap_iterations: {number_iterations}' + '\n')
                    os.system('rm -rf ' + os.source_folder.join(source_folder, file, 'images_orig'))
                    sleep(1.0)
        if nerfacto:
            # Nerfacto
            for k, file in enumerate(files):
                with open(os.source_folder.join(destination_folder, 'nerfacto/GPU', file) + '_gpu.txt', 'w') as gpu_file, open(os.source_folder.join(destination_folder, 'nerfacto/RAM', file) + '_ram.txt', 'w') as ram_file:
                    tempo_file.write('nerfacto ' + file + '\n')
                    print(f'Starting {k+1}/{len(files)}')
                    start = time()
                    cmd = [
                        "ns-train", "nerfacto", 
                        "--data", source_folder + "/" + file, 
                        "--pipeline.model.predict-normals", "True", 
                        "--pipeline.model.background-color", "random", 
                        "--max-num-iterations", "100000", 
                        "--viewer.quit-on-train-completion", "True", 
                        "--pipeline.datamanager.pixel-sampler.ignore-mask", "True", 
                        "--pipeline.datamanager.pixel-sampler.rejection-sample-mask", "False", 
                        "--steps-per-save", "10000", 
                        "--save-only-latest-checkpoint", "False",
                        "--output-dir", source_folder + "/" + file + "/output"
                    ]
                    process = subprocess.Popen(cmd)
                    # Monitor GPU usage while the command is running
                    try:
                        while process.poll() is None:  # Check if process is still running
                            gpu_usage = get_gpu_usage()
                            ram_usage = get_ram_usage()
                            if gpu_usage:
                                gpu_file.write(f"{gpu_usage}" + '\n')
                            if ram_usage:
                                ram_file.write(f"{ram_usage}" + '\n')
                            sleep(1)  # Adjust the interval as needed
                    finally:
                        process.wait()  # Ensure the process completes
                        gpu_usage = get_gpu_usage()
                        ram_usage = get_ram_usage()
                        if gpu_usage:
                            gpu_file.write(f"{gpu_usage}" + '\n')
                        if ram_usage:
                            ram_file.write(f"{ram_usage}" + '\n')

                    end = time()
                    tempo_file.write(f'time: {end-start} s' + '\n')
                    sleep(1.0)
        if splatfacto:
            # Splatfacto
            for k, file in enumerate(files):
                with open(os.source_folder.join(destination_folder, 'splatfacto/GPU', file) + '_gpu.txt', 'w') as gpu_file, open(os.source_folder.join(destination_folder, 'splatfacto/RAM', file) + '_ram.txt', 'w') as ram_file:
                    tempo_file.write('splatfacto ' + file + '\n')
                    print(f'Starting {k+1}/{len(files)}')
                    start = time()
                    cmd = [
                        "ns-train", "splatfacto", 
                        "--data", source_folder + "/" + file, 
                        "--max-num-iterations", "100000", 
                        "--viewer.quit-on-train-completion", "True",
                        "--steps-per-save", "10000", 
                        "--pipeline.model.cull_alpha_thresh", "0.005",
                        "--pipeline.model.continue_cull_post_densification", "False",
                        "--pipeline.model.stop-split-at", "50000",
                        "--save-only-latest-checkpoint", "False",
                        "--output-dir", source_folder + "/" + file + "/output"
                    ]
                    process = subprocess.Popen(cmd)
                    # Monitor GPU usage while the command is running
                    try:
                        while process.poll() is None:  # Check if process is still running
                            gpu_usage = get_gpu_usage()
                            ram_usage = get_ram_usage()
                            if gpu_usage:
                                gpu_file.write(f"{gpu_usage}" + '\n')
                            if ram_usage:
                                ram_file.write(f"{ram_usage}" + '\n')
                            sleep(1)  # Adjust the interval as needed
                    finally:
                        process.wait()  # Ensure the process completes
                        gpu_usage = get_gpu_usage()
                        ram_usage = get_ram_usage()
                        if gpu_usage:
                            gpu_file.write(f"{gpu_usage}" + '\n')
                        if ram_usage:
                            ram_file.write(f"{ram_usage}" + '\n')

                    end = time()
                    tempo_file.write(f'time: {end-start} s' + '\n')
                    sleep(1.0)

    if evaluate and nerfacto:
        for k, file in enumerate(files):
            print(f'Starting {k+1}/{len(files)}')
            get_evaluations(source_folder, file, destination_folder + '/Evaluations', 'nerfacto')

    if evaluate and splatfacto:    
        for k, file in enumerate(files):
            print(f'Starting {k+1}/{len(files)}')
            get_evaluations(source_folder, file, destination_folder + '/Evaluations_splatfacto', 'splatfacto')

source_folder = '/media/tafnes/0E94B37D94B365BD/Users/tafne/Documents/new_gaussians'
destination_folder = '/home/tafnes/Documentos/Python/Artigo/new gaussians'
main(source_folder, destination_folder, colmap=True, nerfacto=True, splatfacto=True)
