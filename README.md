# community-references

A computational analysis of the pop culture profile created through textual references in Dan Harmon's "Community".

![Pop pop!](https://media.giphy.com/media/xtIYfyKf16xJm/giphy.gif)

TOC:
- [Installation](#installation)
- [Usage](#usage)
- [Dependencies](#dependencies)
- [Acknowledgements](#acknowledgements)
- [Notes](#notes)

## Installation

1. Install [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/).

2. Create a conda environment from the environment.yaml file.

```
$ conda env create -f environment.yaml
```

## Usage

Mini-TOC for things we can do:

- [Manage references](#manage-references)
- [Generate site](#generate-site)
- [Create episode supercuts](#create-episode-supercuts)

Before running scripts, make sure you activate the virtual environment. This makes sure that the dependencies the Python scripts need are there. You should see "(references)" at the start of the line.

```
(base) $ conda activate references
(references) $
```

Now you can run any of the Python scripts. Run from the main directory, not the py/ directory, or it won't be able to find data files!

For each script, you can access its help file by adding "-h" or "--help" after the file name, as illustrated in the examples below.

### Manage references

**py/references.py**:

Manage references.

```
$ python py/references.py -h
usage: references.py [-h] {add-ref,analyse,indices,update-refs} ...

Manage references.

optional arguments:
  -h, --help            show this help message and exit

subcommands:
  command

  {add-ref,analyse,indices,update-refs}
    add-ref             Add reference through interactive interface.
    analyse             Analyse references and referents data. By default,
                        analyses everything (names, titles, episodes). Add -h
                        to see more options.
    indices             Checks references file for mismatches with transcripts
                        (audit), identifies correct indices and shifts indices
                        (fix), and helps with manual indices fixes (find). Add
                        -h to see more options.
    update-refs         Generate referents file from references file.
```

### Generate site

**py/web.py**:

Generate content and files for site.

```
$ python py/web.py -h
> usage: annotate | top
    annotate: generate annotated transcripts
    top: generate charts for episodes with the most references
```

You can see the site by running the command below and navigating to localhost:3000/site in a web browser.

```
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

Using the data in references.json, we can use the incredible Videogrep library to get a generated supercut video of references!

**py/supercut.py**

Generate a supercut of references in a given episode or season.

```
$ python py/supercut.py -h
usage: supercut.py [-h] code

Create supercut videos of references in an episode or season.

positional arguments:
  code        code of episode (s01e01) or season (s01) to supercut

optional arguments:
  -h, --help  show this help message and exit
```

Videogrep will print out a log and eventually place a video file with a title like "supercut-s01e01.mp4" or "supercut-s01.mp4" in video/supercuts/.

See the [Videogrep documentation](https://antiboredom.github.io/videogrep/) for more background.

### Utilities used to get data

**py/getdata/dbs.py**: 

Curate IMDb databases based on chosen criteria.

No CLI at the moment, but uncomment lines to get one of:
- db/name.basics.tsv → db/name.basics.min.tsv
- db/title.basics.tsv → db/title.basics.min.tsv
- db/title.ratings.tsv → db/title.ratings.min.tsv

**py/getdata/episodes.py**

Scrapes IMDb for all episodes, writing to data/community/episodes.json under each episode code with: tconst, title, description, date, image, writers (name, nconst), ratings (ratingCount, bestRating, worstRating, ratingValue).

**py/getdata/transcripts.py**

Scrapes episode transcripts from [Springfield! Springfield!](https://www.springfieldspringfield.co.uk/episode_scripts.php?tv-show=community) *(link is no longer live?)* into scrape/.

## Dependencies

This project uses these very helpful libraries:

- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/)
- [PyInquirer](https://github.com/CITGuru/PyInquirer/)
- [Pyperclip](https://github.com/asweigart/pyperclip)
- [Requests](https://2.python-requests.org/en/master/)
- [spaCy](https://spacy.io/)
- [Videogrep](https://antiboredom.github.io/videogrep/)

## Acknowledgements

Much appreciated guidance and support from Sarah Ciston and the [Creative Code Collective](https://www.instagram.com/creativecodecollective/), Holly Willis, and the MA+P department :)

## Notes

- Reference: an instance of referring to something. Referent: the thing being referred to.
- Search for entity and generate supercut
- [Mosaic](https://trac.ffmpeg.org/wiki/Create%20a%20mosaic%20out%20of%20several%20input%20videos)
- [Pattern](https://web.archive.org/web/20190318015618/https://www.clips.uantwerpen.be/pages/pattern-search)