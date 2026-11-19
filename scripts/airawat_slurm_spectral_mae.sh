#!/bin/bash
#SBATCH --job-name=spectral_mae_airawat
#SBATCH --partition=gpu
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=8
#SBATCH --gres=gpu:8
#SBATCH --cpus-per-task=8
#SBATCH --time=04:00:00
#SBATCH --output=logs/spectral_mae_%j.out
#SBATCH --error=logs/spectral_mae_%j.err

echo "=========================================================="
echo "AIRAWAT DGX A100 Distributed Spectral-MAE Pre-training"
echo "Job ID: $SLURM_JOB_ID | Host: $(hostname)"
echo "Start Time: $(date)"
echo "=========================================================="

# 1. Load Modules & Activate Environment
module purge
module load cuda/12.1 cudnn/8.9.2
source ~/miniconda3/bin/activate hyperspectral_env

# 2. Set Distributed Environment Variables
export MASTER_ADDR=$(scontrol show hostnames $SLURM_JOB_NODELIST | head -n 1)
export MASTER_PORT=29500
export OMP_NUM_THREADS=8
export NCCL_DEBUG=INFO

# 3. Launch PyTorch Distributed Data Parallel (DDP)
torchrun     --nproc_per_node=8     --master_addr=$MASTER_ADDR     --master_port=$MASTER_PORT     scripts/train_spectral_mae.py     --data_dir /scratch/datasets/aviris_ng_india_zarr     --bands 192     --patch_size 16 4 4     --mask_ratio 0.75     --batch_size 32     --epochs 100     --lr 1.5e-4     --amp_dtype bfloat16     --checkpoint_dir checkpoints/spectral_mae     --resume_latest

echo "Training Completed at: $(date)"
