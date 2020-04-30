# community-references

A computational analysis of the pop culture profile created through textual references in Dan Harmon's "Community".

![Pop pop!](https://media.giphy.com/media/xtIYfyKf16xJm/giphy.gif)

TOC:
* [Installation](#installation)
* [Usage](#usage)
* [Dependencies](#dependencies)
* [Acknowledgements](#acknowledgements)

## Installation

1. Install [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/).

2. Create a conda environment from the environment.yml file.

```bash
$ conda env create -f environment.yml
```

## Usage

Mini-TOC for things we can do:

* [Manage references](#manage-references)
* [Produce site](#produce-site)
* [Create episode supercuts](#creating-episode-supercuts)

Before running scripts, make sure you activate the virtual environment. This makes sure that the dependencies the Python scripts need are there. You should see "(references)" at the start of the line.

```bash
(base) $ conda activate references
(references) $
```

Now you can run any of the Python scripts. Run from the main directory, not the scripts directory, or it won't be able to find data files!

For each script, you can access its help file by adding "-h" or "--help" after the file name, as illustrated in the examples below.

### Manage references

**scripts/references.py**:

Manage references.

```bash
$ python scripts/references.py -h
> usage: add | analyse | indices | updateReferents
    add: add reference through interactive interface
    analyse: generate summary statistics
    indices: manage indices
    updateReferents: generate referents file from references file
```

### Produce site

**scripts/site.py**:

Produce content and files for site.

```bash
$ python scripts/site.py -h
> usage: annotate | top
    annotate: generate annotated transcripts
    top: generate charts for episodes with the most references
```

You can see the site by running the command below and navigating to localhost:3000/site in a web browser.

```bash
$ python -m http.server 3000
> Serving HTTP on 0.0.0.0 port 3000 (http://0.0.0.0:3000/) ...
```

Site directory for reference:

```
|-- byEntity/
|-- byEpisode/
    |-- ep/
        |-- s01e01/
        |-- s01e02/
        ...
|-- byYear/
|-- top/
```

### Create episode supercuts

Using data/references.json, we can use the incredible Videogrep library to get a generated supercut of all the references in an episode! I'm running into issues making Videogrep work as a Python module, so this is a Python + command line mismash workaround.

1. Get search string.

**scripts/getsearch.py**

Get RegEx search string for use in Videogrep.

```bash
$ python scripts/getsearch.py -h
> usage: [season|episode]
    season: s01 for season 1
    episode: s01e01 for season 1 episode 1
```

Example for s01e01:

```bash
$ python scripts/getsearch.py s01e01
> (Breakfast\ Club|Bill\ Murray|Michael\ Douglas|Seinfeld|Dirty\ Dancing|Seacrest|Slumdog\ Millionaire|Elisabeth\ Shue|The\ Breakfast\ Club|Stripes|Ben\ Affleck|Meatballs)
> Copied to clipboard!
```

2. Navigate to video/. (Video files not included in repository.)

```bash
$ cd video
```

2. Run Videogrep.

```bash
$ videogrep -i INPUT -s SEARCH -o OUTPUT
```

Example for s01e01 using the search string given by getsearch.py (lines broken up for slightly better readability):

```bash
$ videogrep -i video/Community.S01.Season.1.720p.5.1Ch.Web-DL.ReEnc-DeeJayAhmed/Community.S01E01.720p.5.1Ch.Web-DL.ReEnc-DeeJayAhmed.mkv \
-s "(Elisabeth\ Shue|Michael\ Douglas|Bill\ Murray|Ben\ Affleck|Dirty\ Dancing|Stripes|Meatballs|Slumdog\ Millionaire|Breakfast\ Club|Seacrest|Seinfeld|The\ Breakfast\ Club)" \
-o video/supercuts/s01e01.mp4
```

See [Videogrep documentation](https://antiboredom.github.io/videogrep/) for more options!

### Other helper utilities used

**scripts/dbs.py**: 

Curate IMDb databases based on chosen criteria.

No CLI at the moment, but uncomment lines to get one of:
* db/name.basics.tsv → db/name.basics.min.tsv
* db/title.basics.tsv → db/title.basics.min.tsv
* db/title.ratings.tsv → db/title.ratings.min.tsv

**scripts/episodes.py**

Scrapes IMDb for all episodes, writing to data/episodes.json under each episode code with: tconst, description, writers (name, nconst, credit).

```bash
$ python scripts/episodes.py -h
> usage: scrape
    scrape: scrape IMDb for episode data and save to episodes.json
```

**scripts/transcripts.py**

Scrapes episode transcripts from [Springfield! Springfield!](https://www.springfieldspringfield.co.uk/episode_scripts.php?tv-show=community) *(link is no longer live?)* into scrape/.

```bash
$ python scripts/transcripts.py
> usage: scrape
    scrape: scrape transcripts into scrape/
```

# Dependencies

This project uses these very helpful libraries:

* [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/)
* [PyInquirer](https://github.com/CITGuru/PyInquirer/)
* [Pyperclip](https://github.com/asweigart/pyperclip)
* [Requests](https://2.python-requests.org/en/master/)
* [spaCy](https://spacy.io/)
* [Videogrep](https://antiboredom.github.io/videogrep/)

# Acknowledgements

Much appreciated guidance and support from Sarah Ciston and the [Creative Code Collective](https://www.instagram.com/creativecodecollective/), Holly Willis, and the MA+P department :)