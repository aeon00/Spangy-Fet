# Quick Reference Guide - Using Directories Module

## File Overview

### Installation and set-up
first create a virtual env

conda create --name devfet python=3.12

pip install brain-slam

pip install plotly

pip install pandas

### 1. directories.py
**Purpose**: Central configuration for all directory paths  
**Functions**:
- `input_directories()` - Returns input paths (surface data, mesh info)
- `output_directories(filename, participant_session)` - Returns output paths

### 2. main.py
**Purpose**: Main processing script  
**How it uses directories**:
```python
from directories import output_directories, input_directories

# Get paths
input_dirs = input_directories()
output_dirs = output_directories()

# Use them
surface_path = input_dirs['surface_path']
mesh_info_path = input_dirs['mesh_info_path']
output_file = output_dirs['output_csv_file']
```

### 3. spangy_analysis.py (process_single_file)
**Purpose**: Process individual surface files  
**How it uses directories**:
```python
from directories import output_directories

# Get paths with file-specific info
output_dirs = output_directories(filename=filename, participant_session=participant_session)

# Use them
mesh_save_path = output_dirs['mesh_save_path']
principal_tex_path = output_dirs['principal_tex_path']
```

## Complete Workflow

```
┌─────────────────────────────────────────────────────────────┐
│                      directories.py                          │
│  • Defines all input/output paths                           │
│  • input_directories() → surface_path, mesh_info_path       │
│  • output_directories() → all output directories            │
└─────────────────────────────────────────────────────────────┘
                              ▲
                              │
                 ┌────────────┴────────────┐
                 │                         │
    ┌────────────▼──────────┐   ┌─────────▼────────────┐
    │   main.py             │   │  spangy_analysis.py  │
    │  • Gets input paths   │   │  • Gets output paths │
    │  • Loads mesh data    │   │  • Processes files   │
    │  • Calls processor    │──→│  • Saves results     │
    │  • Saves final CSV    │   │                      │
    └───────────────────────┘   └──────────────────────┘
```

## Directory Structure Created

```
/scratch/hdienye/dhcp_full_info/
├── mesh/                          # Smoothed meshes
├── principal_curv_tex/            # Principal curvature textures
├── mean_curv_tex/                 # Mean curvature textures
├── spangy/
│   ├── plots/                     # Visualization plots
│   └── textures/                  # Spangy texture files
├── frecomposed/
│   ├── bands/                     # Band-specific data
│   └── full/                      # Full frecomposed arrays
└── info/
    ├── all_results.csv            # Combined results (local mode)
    └── chunk_*_results.csv        # Chunk results (SLURM mode)
```

## Quick Start

1. **Ensure all files are in the same directory:**
   ```
   your_project/
   ├── directories.py
   ├── main_modified.py
   ├── spangy_analysis.py
   └── utils.py
   ```

2. **Run the processing:**
   ```bash
   # Local mode (process all files)
   python main_modified.py
   
   # SLURM mode (parallel processing)
   sbatch --array=0-9 your_job.sh
   ```

3. **To change a directory path:**
   - Open `directories.py`
   - Update the path in the appropriate function
   - Save - all scripts automatically use the new path!

## Available Paths

### From `input_directories()`:
- `surface_path` - Location of surface files
- `mesh_info_path` - Path to participants.tsv

### From `output_directories()`:
- `mesh_save_path` - Smoothed mesh output
- `principal_tex_dir` - Principal curvature textures folder
- `principal_tex_path` - Specific principal curvature file
- `mean_tex_dir` - Mean curvature textures folder
- `mean_tex_path` - Specific mean curvature file
- `plots_dir` - Plots output folder
- `spangy_tex_path` - Specific spangy texture file
- `frecomposed_dir` - Frecomposed data folder
- `output_folder` - General output folder
- `output_csv_file` - Final CSV results file

## Example: Adding a New Output Directory

1. **Edit directories.py:**
   ```python
   def output_directories(filename=None, participant_session=None):
       # ... existing code ...
       
       # Add your new directory
       my_new_dir = "/scratch/hdienye/dhcp_full_info/my_new_output/"
       
       return {
           # ... existing paths ...
           'my_new_dir': my_new_dir
       }
   ```

2. **Use it in your code:**
   ```python
   from directories import output_directories
   
   output_dirs = output_directories()
   ensure_dir_exists(output_dirs['my_new_dir'])
   ```

