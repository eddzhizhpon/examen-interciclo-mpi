import random
import numpy as np
import os

mat1_name = 'mat1.txt'
mat2_name = 'mat2.txt'
result_name = 'result.txt'
result_name = 'results'

def add_vector(vec1, vec2, len_vec=0):
    if (len_vec==0):
        len_vec = len(vec2)
    vec_result = list()
    for index in range(len_vec):
        vec_result.extend([vec1[index] + vec2[index]])
    del vec1
    del vec2
    return vec_result

def add_mat(mat1, mat2):
    i = len(mat1)
    j = len(mat1[0])
    mat_result = list()
    for row in range(i):
        mat_result.append(add_vector(mat1[row], mat2[row], j))
    del mat1
    del mat2
    return mat_result

def add_mat_process(mat1, mat2, n_core=6):
    i = len(mat1)
    j = len(mat1[0])

    step = i/n_core

def generate_mat(len_mat, file_name='mat.txt'):
    with open(file_name,'w') as f:
        for e in range(len_mat):
            row = [random.randint(0, 10) for e in range(len_mat)]
            for item in row:
                f.write(str(item) + ' ')
            f.write('\n')
        f.close()

def append_row(row, file_name):
    with open(file_name,'w+') as f:
        for item in row:
            item = str(item) + " "
            f.write(item)
        f.write('\n')
        f.close()

def read_row_by_index(index, file_name):
    i = 0
    with open(file_name,'r') as f:
        while True:
            row = f.readline()
            if not row:
                break
            elif i == index:
                row = list(map(int, row.split(' ')[:-1]))
                return row
            i += 1
        f.close()

def gen_mat(len_mat):
    return [[random.randint(0, 10) for e in range(len_mat)] for e in range(len_mat)]

def main():
    if not os.path.exists(result_name):
        os.makedirs(result_name)
    
    # mat1 = generate_mat(1000, file_name=mat2_name)


    # row = read_row_by_index(3, mat1_name)
    # print(row)
    # print(len(row))
    # mat = gen_mat(31623)
    # print(len(mat), '|', len(mat[0]))

    # mat1 = generate_mat(31623)
    # mat2 = create_mat(1000000000)
    
    # mat_result = add_mat(mat1, mat2)
    # print(mat1, '\n')
    # print(mat2, '\n')
    # print(mat_result)

if __name__=='__main__':
    main()
