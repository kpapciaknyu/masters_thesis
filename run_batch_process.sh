#!/bin/bash
#SBATCH --job-name=llm_cancer_processing
#SBATCH --output=/gpfs/data/pcc_lab/kep9496-dir/practice_files/llm_job_%j.log
#SBATCH --error=/gpfs/data/pcc_lab/kep9496-dir/practice_files/llm_job_%j.err
#SBATCH --time=12:00:00
#SBATCH --mem=16G
#SBATCH --cpus-per-task=4

# Load required modules
export PYTHONPATH=$PYTHONPATH:/gpfs/data/pcc_lab/shared/py_packages
module load python/gpu/3.7.6

# Create a virtual environment if it doesn't exist
VENV_DIR="/gpfs/data/pcc_lab/kep9496-dir/practice_files/venv"
if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv $VENV_DIR
    source $VENV_DIR/bin/activate
    pip install pandas requests tqdm
else
    source $VENV_DIR/bin/activate
fi

# Navigate to the directory with your scripts
cd /gpfs/data/pcc_lab/kep9496-dir/practice_files

# Run the batch processing script
python3 batch_process_llms.py

echo "Job completed"
