import os

dirs = os.listdir()
current_folder = os.getcwd()
files = []
for file in dirs:
    if os.path.isdir(os.path.join(current_folder, file)) and not file.startswith('.'):
        files.append(file)

number_repetitions = 10
with open('pilot.sh', 'w') as arq:
    for k, file in enumerate(files):
        for i in range(1, number_repetitions + 1):
            arq.write(f'echo "Starting {k+1}:{i}/{len(files)}"\n')
            arq.write('mkdir ' + current_folder + '/' + file + '/teste_' + str(i)  + '\n')
            arq.write('ns-process-data images --data "' + current_folder + '/' + file + '/images_orig" --output-dir "' + current_folder + '/' + file + '/teste_' + str(i) + '" --matching-method exhaustive\n')
            arq.write('rm -rf "' + current_folder + '/' + file + '/teste_' + str(i) + '/images"\n')
            arq.write('rm -rf "' + current_folder + '/' + file + '/teste_' + str(i) + '/images_2"\n')
            arq.write('rm -rf "' + current_folder + '/' + file + '/teste_' + str(i) + '/images_4"\n')
            arq.write('rm -rf "' + current_folder + '/' + file + '/teste_' + str(i) + '/images_8"\n')
            arq.write('rm -rf "' + current_folder + '/' + file + '/teste_' + str(i) + '/sparse_pc.ply"\n')
            arq.write('rm -rf "' + current_folder + '/' + file + '/teste_' + str(i) + '/transforms.json"\n')
            arq.write('sleep 1\n')
        arq.write('rm -rf "' + current_folder + '/' + file + '/images_orig"\n')