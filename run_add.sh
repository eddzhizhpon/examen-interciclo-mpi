#!/bin/bash

if [ -z "$1" ] || [ -z "$2" ]; then
    echo "ERROR >> Ingrese un directorio con los archivos con las dos matrices"
    exit 1
fi
echo "Comenzando suma en: $1 y $2"
DIR_1="$1/*.npy"
DIR_2="$2/*.npy"

mkdir -p reports
echo "amount,serial_time,mpi_time" > reports/times.csv

arr_dir1=()
arr_dir2=()

for d in $DIR_1; do
    arr_dir1=(${arr_dir1[@]} "$d")
done

for d in $DIR_2; do
    arr_dir2=(${arr_dir2[@]} "$d")
done

LEN=${#arr_dir1[@]}
LEN=$(($LEN - 1))

for i in $(seq 0 $LEN); do

    start_time=`date +%s%N`
    amount=`python main.py -d1 ${arr_dir1[i]} -d2 ${arr_dir2[i]} --serial`
    end_time=`date +%s%N`
    let serial_time=($end_time-$start_time)/1000000

    start_time=`date +%s%N`
    amount=`mpiexec -n 16 python main.py -d1 ${arr_dir1[i]} -d2 ${arr_dir2[i]} --mpi`
    end_time=`date +%s%N`
    let mpi_time=($end_time-$start_time)/1000000

    echo "$amount,$serial_time,$mpi_time" >> reports/times.csv
    echo "${arr_dir1[i]} -- ${arr_dir2[i]} | serial: $serial_time [ms], mpi:$mpi_time [ms]"
done
exit 0