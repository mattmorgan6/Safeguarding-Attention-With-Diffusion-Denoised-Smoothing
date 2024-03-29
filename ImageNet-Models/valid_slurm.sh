#!/bin/bash
#SBATCH -J valid_cnn
#SBATCH -p class
#SBATCH -A cs479-579
#SBATCH --gres=gpu:1    
#SBATCH --mem=32G   
#SBATCH -c 16
#SBATCH -t 1-00:00:00       
#SBATCH --export=ALL
python3 valid.py --data_folder=/nfs/stak/users/morgamat/hpc-share/CS_499/CS_499_Term_Project/ImageNet-Models/adv_images/e_0.05_n_5_s_0.00784313725490196
