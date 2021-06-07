from os import path
from os import makedirs

import argparse
import pandas as pd
import matplotlib.pyplot as plt

report_path = 'reports'

def plot_time_results(name='results.png', df_name='dataframe.csv'):
    df = pd.read_csv(report_path + "/" + df_name)
    df.sort_values(by=['amount'], inplace=True)

    x = df['amount']
    serial_y = df['serial_time']
    mpi_y = df['mpi_time']

    plt.plot(x, serial_y, ls='--', marker='o')
    plt.plot(x, mpi_y, ls='--', marker='o')

    plt.title('Comparación de tiempos de ejecución')
    plt.legend(['Serial', 'MPI'])
    plt.xlabel('Cantidad de muestras')
    plt.ylabel('Tiempo de ejecución [s]')

    create_dir(report_path)
    plt.savefig(report_path + '/' + name, dpi=300)

def create_dir(report_path):
    if not path.exists(report_path):
        makedirs(report_path)

def convert_time(df_name='dataframe.csv'):
    df = pd.read_csv(report_path + "/" + df_name)
    df.sort_values(by=['amount'], inplace=True)

    df['serial_time'] = df['serial_time']/1000
    df['mpi_time'] = df['mpi_time']/1000

    return df

def main():
    df = convert_time(df_name='times.csv')
    df.to_csv(report_path + '/times_seconds.csv')
    plot_time_results(name='result_seconds.png', df_name='times_seconds.csv')

if __name__=='__main__':
    main()