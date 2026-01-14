#!/bin/bash
set -eu

CUR_VENV_NAME=leh_venv
CUR_VENV_DIR=./$CUR_VENV_NAME

source $(conda info --base)/etc/profile.d/conda.sh

if [[ ! -d "$CUR_VENV_DIR" ]]; then
  conda create -y --prefix "$CUR_VENV_DIR" python=3.12
else
  echo "Conda environment already exists at $CUR_VENV_DIR – skipping creation."
fi
# deactivating default environment
conda deactivate
# activating custom enviroment
conda activate $CUR_VENV_DIR

echo $(python --version)

echo $(pip --version)

pip install -e .

pip install "lm_eval[hf]"

echo "Setup complete, to activate conda environment run: conda activate ${CUR_VENV_DIR}"
