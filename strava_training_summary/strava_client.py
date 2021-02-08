import requests
import configparser
import time
import os


class StravaClient:
    API_URL = "https://www.strava.com/api/"
    API_VERSION = 'v3'

    def __init__(self, config_file_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'conf.ini')):
        print(config_file_path)
        self.config_file_path = config_file_path
        self.config, self.api_data, self.header = None, None, None

    def _reload_config(self):
        self.config = configparser.ConfigParser()
        self.config.read(self.config_file_path)
        self.api_data = self.config['strava']
        self.header = {'Authorization': f"Bearer {self.api_data['access_token']}"}

    @staticmethod
    def url(path):
        return f"{StravaClient.API_URL}/{StravaClient.API_VERSION}/{path}"

    def _is_expired(self):
        return time.time() > float(self.api_data['expires_at'])

    def _update_header(self):
        self.header = {'Authorization': f"Bearer {self.api_data['access_token']}"}

    def refresh_token(self):
        self._reload_config()
        if self._is_expired():
            r = requests.post(
                StravaClient.url("oauth/token"),
                data={
                    "client_id": self.api_data['client_id'],
                    "client_secret": self.api_data['client_secret'],
                    "grant_type": 'refresh_token',
                    "refresh_token": self.api_data['refresh_token']}
            )
            response = r.json()
            for entry in ['access_token', 'refresh_token', 'expires_at']:
                self.api_data[entry] = str(response[entry])
            with open(self.config_file_path, 'w') as config_file:
                self.config.write(config_file)
            self._update_header()



