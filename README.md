# Investigation of the Feasibility of Individual Identification Based on Pupil Diameter Changes Caused by Visual Stimuli

## Overview
This repository contains software, stimulus assets, datasets, and analysis code for biometric identification using pupil diameter responses to visual stimuli.

The project has two main experiment applications:
- `Programs/experiment1.py`: 4 stimulus families, each with tutorial/start flow.
- `Programs/experiment2.py`: 8 stimulus patterns in a menu-driven interface.

The repository also includes:
- Measured data under `Data/`
- Analysis workflow in `Data Analysis/analysis.ipynb`
- Precomputed EER outputs in JSON

## Repository Structure
- `Programs/`
- `Programs/Images/`: image assets used by experiment scripts
- `Programs/experiment1.py`: Experiment 1 app (Stimulus 1-4)
- `Programs/experiment2.py`: Experiment 2 app (Stimulus 1-8)
- `Programs/Experimental1 settings copy.txt`: experiment design notes
- `Programs/Experimental2 settings.txt`: experiment design notes
- `Data/Experiment1/Participant*/E1-E4.(CSV|xlsx)`: Experiment 1 data
- `Data/Experiment2/Participant*/Stimulus1-8.(CSV|xlsx)`: Experiment 2 data
- `Data Analysis/analysis.ipynb`: preprocessing + DTW/DBA + EER computation
- `Data Analysis/EER_data.json`: stored EER results (Experiment 1)
- `Data Analysis/EER_data_for_experiment2.json`: stored EER results (Experiment 2)
- `Data Analysis/run.bat`: launches Jupyter in conda env `timeseries`
- `Dissertation/`, `UWW/`: thesis/presentation materials and figures

## Requirements
Recommended environment: Windows + Python 3.

### Runtime dependencies (experiment apps)
- `pygame`

### Analysis dependencies (`analysis.ipynb`)
- `pandas`
- `numpy`
- `matplotlib`
- `scipy`
- `dtaidistance`
- `tslearn`
- `jupyter`

Install example:

```powershell
pip install pygame pandas numpy matplotlib scipy dtaidistance tslearn jupyter
```

## Running the Experiments
Run from `Programs/` so relative image paths resolve correctly.

### Experiment Program 1 (Stimulus 1-4)

```powershell
cd Programs
python experiment1.py
```

Main menu:
- `Stimulus 1`
- `Stimulus 2`
- `Stimulus 3`
- `Stimulus 4`
- `Quit`

Each stimulus submenu has:
- `Tutorial`
- `Start`
- `Back`

### Experiment Program 2 (Stimulus 1-8)

```powershell
cd Programs
python experiment2.py
```

Main menu has 8 stimulus buttons in two columns.

Key parameters in `Programs/experiment2.py`:
- `number_of_set = 5`
- `time_of_preparation = 2` seconds
- `time_of_stimulus = 2` seconds

Most stimulus routines run 10 cycles per set (50 cycles total with defaults).

## Data Layout
### Experiment 1
- Path: `Data/Experiment1/Participant1` ... `Data/Experiment1/Participant6`
- Files per participant: `E1.CSV` ... `E4.CSV` (+ `.xlsx` copies)

### Experiment 2
- Path: `Data/Experiment2/Participant1` ... `Data/Experiment2/Participant5`
- Files per participant: `Stimulus1.CSV` ... `Stimulus8.CSV` (+ `.xlsx` copies)

The notebook expects this directory/file naming layout.

## Running Analysis
### Option A: Start Jupyter directly

```powershell
cd "Data Analysis"
jupyter notebook analysis.ipynb
```

### Option B: Use provided launcher

```powershell
cd "Data Analysis"
run.bat
```

`run.bat` activates conda and starts Jupyter Notebook in environment `timeseries`.

## Analysis Pipeline (`analysis.ipynb`)
The notebook includes:
- Data loading for Experiment 1 and 2
- Preprocessing (linear interpolation + lowpass filtering)
- DTW distance computation
- DBA (DTW Barycenter Averaging)
- FAR/FRR threshold sweep and EER estimation
- Aggregated reporting by participant/stimulus

Output JSON files:
- `Data Analysis/EER_data.json`
- `Data Analysis/EER_data_for_experiment2.json`

## Notes
- Some notebook cells contain absolute local paths from the original environment. Update them for your local clone before full execution.
- Both `.CSV` and `.xlsx` data are present; analysis cells read CSV files.
- `Programs/backup/` contains older script versions and is not the main execution path.

## Reproducibility Checklist
1. Keep the same folder structure under `Data/`.
2. Run experiment scripts from inside `Programs/`.
3. Update notebook path variables to your local repository path.
4. Run preprocessing cells before EER computation cells.
5. Save/read EER outputs via the JSON files in `Data Analysis/`.

## Citation
If you use this repository in academic work, cite the related dissertation/presentation materials in `Dissertation/` and `UWW/`.

## License
No explicit license file is currently included in this repository.
