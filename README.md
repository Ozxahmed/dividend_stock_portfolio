# Readme

## Stocks Project — Dev Setup & Usage

### Prereqs

- macOS, zsh
- Homebrew- for system tools (/opt/homebrew)
- Miniforge/Conda- for Python (~/miniforge3)
- VS Code (Python + Jupyter extensions)
- Postgres (local or remote), credentials available

### Environment Setup

#### `environment.yml`

Create YAML file with the following parameters:

```yaml
name: stocks
channels:
  - conda-forge
channel_priority: strict
dependencies:
  - python=3.12
  - pandas
  - numpy
  - psycopg  # modern Postgres driver (psycopg3)
  - jupyterlab
  - ipykernel  # usually auto-installed via .condarc, kept for clarity
  # optional, nice to have:
  - ipython
  - pytz # provides accurate and cross-platform timezone calculations
  - requests
  - matplotlib
```

#### Create Environment

```bash
conda env create -f environment.yml
conda activate stocks
```
