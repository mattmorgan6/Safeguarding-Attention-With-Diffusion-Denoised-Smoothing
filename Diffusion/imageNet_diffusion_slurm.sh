#!/bin/bash
#SBATCH -J valid_cnn
#SBATCH -p class
#SBATCH -A cs479-579
#SBATCH --gres=gpu:1    
#SBATCH --mem=32G   
#SBATCH -c 16
#SBATCH -t 1-00:00:00       
#SBATCH --export=ALL
python3 ./imageNet/construct.py --sigma 0.25 --batch_size 1 --outfile output.txt --ptfile pretrained_coatnet.pt --data_folder /nfs/stak/users/morgamat/hpc-share/CS_499/CS_499_Term_Project/ImageNet-Models/val_images