#!/bin/bash
#SBATCH --job-name=pm25_hpc_sim
#SBATCH --output=result_%j.log
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --time=00:10:00

echo "Menjalankan Job Simulasi PM2.5 pada HPC Cluster..."
module load python/3.9

python3 src/parallel_processing.py
python3 src/visualize.py