# community-references

A computational analysis of the pop culture profile that Dan Harmon's "Community" creates through textual references.

![Pop pop!](https://media.giphy.com/media/xtIYfyKf16xJm/giphy.gif)

## Installation

1. Install [pipenv](https://pypi.org/project/pipenv/). (I installed it with Homebrew on Mac.)
```
brew install pipenv
```

2. Install the project dependencies.
```
pipenv install
```

## Usage

1. Activate the virtual environment. This makes sure that the dependencies the Python scripts need are there.
```
pipenv shell
```

2. Run one of the Python scripts.

**scrape-transcripts.py** scrapes all episode transcripts of Community from [Springfield! Springfield!](https://www.springfieldspringfield.co.uk/episode_scripts.php?tv-show=community) and stores them in the /transcripts folder.

*Note that the transcripts on the website are not always consistent and accurate! Running this command to re-compile the transcripts will delete all of the manual edits I've made.*

```
python scrape-transcripts.py
```

**extract-references.py** uses the [spaCy](https://spacy.io/) natural language processing library and [IMDb databases](https://www.imdb.com/interfaces/) to create lists of people and movie/TV references in the given Community episode(s).

* To generate and print the data for one episode, run the command with the episode code. For example, the command below would print the data for season 1, episode 1.

```
python extract-references.py s01e01
```

* To generate and save the data for all episode files in /transcripts, run the command with "all". This will save the data to "all.json" in /output.
```
python extract-references.py all
```

**analyse-names.py** uses the references data generated from **extract-references.py** to generate descriptive statistics about the people referenced.
```
python analyse-names.py
```

***analyse-titles.py*** *still in progress*