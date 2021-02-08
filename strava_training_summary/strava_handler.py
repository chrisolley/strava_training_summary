import requests
import logging
import time
from .datetime_utils import unix_time_from_string

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)


class StravaHandler:
    activities_endpoint = "activities"
    requests_per_hour = 400

    def __init__(self, strava_client):
        self.strava_client = strava_client

    def get_summary_activities(self, start_date, end_date, per_page=20):
        start_date_unix = unix_time_from_string(start_date)
        end_date_unix = unix_time_from_string(end_date)
        activities = []
        params = {
            'before': end_date_unix,
            'after': start_date_unix,
            'per_page': per_page,
            'page': 1
        }
        while True:
            self.strava_client.refresh_token()
            r = requests.get(
                self.strava_client.url(StravaHandler.activities_endpoint),
                headers=self.strava_client.header,
                params=params)
            if not r.ok:
                logging.info(f"Exiting due to {r.status_code}: {r.reason}")
                logging.info(f"{r.content}")
                break
            response = r.json()
            if not response:
                break
            activities.append(response)
            params['page'] += 1
            logging.info(f"Fetched {per_page} activities, sleeping for "
                         f"{(StravaHandler.requests_per_hour / 3600)} seconds")
            time.sleep((StravaHandler.requests_per_hour / 3600))
        return [item for page in activities for item in page]

    def get_detailed_activity(self, activity_id):
        self.strava_client.refresh_token()
        r = requests.get(
            self.strava_client.url(StravaHandler.activities_endpoint) + "/" + f"{activity_id}",
            headers=self.strava_client.header
        )
        return r.json()

    def get_detailed_activities(self, start_date, end_date):
        activities = []
        summary_activities = self.get_summary_activities(start_date, end_date)
        activity_ids = [int(summary['id']) for summary in summary_activities]
        for activity_id in activity_ids:
            activities.append(self.get_detailed_activity(activity_id))
        return activities
