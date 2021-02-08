## Strava Training Summary Generator

This repo contains a simple CLI to generate training summaries from Strava that can be installed as a Python package.

### Requirements

In order to access the Strava API, you'll need to create a `conf.ini` file similar to the `template-conf.ini` file, in the same location.
The values can be filled out using this guide: https://developers.strava.com/docs/getting-started/.

### Installation

To install, clone the repository, navigate to the root directory and run `pip install -e .` from the command line (preferably within an isolated Python environment using e.g. conda or venv).


### Running

Once the package has been installed, the CLI can be run by typing `strava_training_summary` into the command line. You will be prompted for a date range to pull the records from.
