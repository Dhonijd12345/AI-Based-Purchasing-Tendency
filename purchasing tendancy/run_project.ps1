# Run Project Script for Multi-Feature Search-Based Purchasing Tendency Community Classification
Write-Host "Starting Project Pipeline..." -ForegroundColor Cyan

# Set PYTHONPATH
$env:PYTHONPATH = $PSScriptRoot

# 1. Generate Synthetic Data
Write-Host "Phase 1: Generating Synthetic Data..." -ForegroundColor Green
python scripts/data_generator.py

# 2. Initialize Database
Write-Host "Phase 2: Initializing Database..." -ForegroundColor Green
python utils/database.py

# 3. Train ML Models (GNN + SASRec)
Write-Host "Phase 3: Training ML Models... (This may take a minute)" -ForegroundColor Green
python scripts/train_pipeline.py

# 4. Launch Flask Application
Write-Host "Phase 4: Launching Dashboard..." -ForegroundColor Green
Write-Host "Open your browser at http://127.0.0.1:5000" -ForegroundColor Yellow
python app.py
