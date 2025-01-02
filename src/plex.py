import os
import http.client
import json


def request(endpoint):
    request = http.client.HTTPSConnection(os.environ["PLEX_URL"])
    request.request("GET", f"{endpoint}?X-Plex-Token={os.environ['PLEX_TOKEN']}", headers={"Accept": "application/json"})
    plex_data = json.loads(request.getresponse().read())
    return plex_data
