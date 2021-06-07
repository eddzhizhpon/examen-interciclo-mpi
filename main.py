import random
import numpy as np
import os
import time
import argparse

from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# mat1_name = 'mat1.npy'
# mat2_name = 'mat2.npy'
sample_path = 'sample'

# mat_size = 31623
max_len = 31624

def add_mat(mat1, mat2, index, mat_size):
    i = len(mat1)
    result = np.zeros(shape=(mat_size, mat_size), dtype=np.uint8)

    for row in range(i):
        for col in range(i):
            result[row][col] = mat1[row][col] + mat2[row][col]
            mat1[row][col] = 0
            mat2[row][col] = 0

    return [result, index]

def split_mat(mat1, mat2, mat_size, n_core):
    global size
    split_mat = list()
    step = int(mat_size/n_core)
    start = 0
    end = step
    for i in range(size):
        if i == size - 1:
            end = mat_size
        split_mat.append([mat1[start:end], mat2[start:end], i])
        start += step
        end += step
    return split_mat

def load_mat(file_name):
    with open(file_name,'rb') as f:
        mat = np.load(f)
        f.close()
    return mat

def save_mat(len_mat, file_name):
    mat = np.random.randint(9, size=(len_mat, len_mat), dtype=np.uint8)
    with open(file_name,'wb') as f:
        np.save(f, mat)
        f.close()
    return mat

def make_sample():
    mat1_name = sample_path + '/1'
    mat2_name = sample_path + '/2'
    if not os.path.exists(mat1_name):
        os.makedirs(mat1_name)
    if not os.path.exists(mat2_name):
        os.makedirs(mat2_name)
    files = 8
    step = int(max_len/files)
    amount = step
    for i in range(files):
        file_name = mat1_name + '/mat-' + str(amount) + '.npy'
        save_mat(amount, file_name)
        file_name = mat2_name + '/mat-' + str(amount) + '.npy'
        save_mat(amount, file_name)
        amount += step

def get_args():

    parser = argparse.ArgumentParser()

    parser.add_argument("-d1", "--directory1", type=str,  
                            help="Directorio con los archivos 1")

    parser.add_argument("-d2", "--directory2", type=str,  
                            help="Directorio con los archivos 2")

    parser.add_argument("-ms", "--make-sample", action='store_true',  
                                help="Crear muestreos aleatorios")
    
    parser.add_argument("-s", "--serial", action='store_true',  
                                help="Hacer suma serial")


    parser.add_argument("-m", "--mpi", action='store_true',  
                                help="Hacer suma con mpi")

    return vars(parser.parse_args())

def run_mpi(mat1, mat2):
    if rank == 0:
        mat_size = len(mat1)

        mat_to_share = split_mat(mat1, mat2, mat_size, size)
        print(f'{mat_size}')
        del mat1
        del mat2

    else:
        mat_to_share = None

    mat_to_share = comm.scatter(mat_to_share, root=0)

    amount = len(mat_to_share[0])
    result = add_mat(mat_to_share[0], mat_to_share[1], mat_to_share[2], amount)
    del mat_to_share
    del result


    # result = comm.gather(result, root=0)

    # if rank == 0:
    #     for r in result:
    #         print(r)
    
def run_serial(mat1, mat2):

    amount = len(mat1)
    result = add_mat(mat1, mat2, 0, amount)

    print(amount)

def main():
    args = get_args()

    if args['make_sample']:
        make_sample()
    elif args['serial']:
        mat1 = load_mat(args['directory1'])
        mat2 = load_mat(args['directory2'])
        run_serial(mat1, mat2)
    elif args['mpi']:
        mat1 = load_mat(args['directory1'])
        mat2 = load_mat(args['directory2'])
        run_mpi(mat1, mat2)

if __name__=='__main__':
    main()
        
