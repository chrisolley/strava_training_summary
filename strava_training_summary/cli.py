import click
from .strava_client import StravaClient
from .strava_handler import StravaHandler
from .utils import print_training_summary


@click.command()
@click.option('--from_date', prompt='From date', required=True, type=str)
@click.option('--to_date', prompt='To date', required=True, type=str)
def strava_training_summary(from_date, to_date):
    strava_client = StravaClient()
    strava_handler = StravaHandler(strava_client)
    detailed_activities = strava_handler.get_detailed_activities(from_date, to_date)
    print_training_summary(detailed_activities)
