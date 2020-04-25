# community-references

A computational analysis of the pop culture profile created through textual references in Dan Harmon's "Community".

![Pop pop!](https://media.giphy.com/media/xtIYfyKf16xJm/giphy.gif)

## Installation

1. Install [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/).

2. Create a conda environment from the environment.yml file.
```
conda env create -f environment.yml
```

## Usage

1. Activate the virtual environment. This makes sure that the dependencies the Python scripts need are there.
```
conda activate references
```

2. Run one of the Python scripts. (Run from the main directory, not the /scripts directory, or it won't be able to find data files!)

For each script, you can access its help file by adding "-h" or "--help" after the file name:
```
python scripts/references.py -h
```

**scripts/references.py**:
```
usage: add | analyse | indices | updateReferents
  add: add reference through interactive interface
  analyse: generate summary statistics
  indices: manage indices
  updateReferents: generate referents file from references file
```

**scripts/site.py**:
```
usage: annotate | top
  annotate: generate annotated transcripts
  top: generate charts for episodes with the most references
```