import http.client
import datetime
import json

plex_token = "redacted"
plex_url = "redacted"

#list of the star trek series i have finished watching
# completed_list = []
completed_list = {
    "Star Trek":[1,2,3], 
    "Star Trek: The Animated Series":[1,2], 
    "Star Trek: The Next Generation":[1,2,3,4,5,6,7], 
    "Star Trek: Deep Space Nine":[1,2,3,4,5,6,7], 
    "Star Trek: Voyager":[1,2,3,4,5,6,7], 
    "Star Trek Continues":[1], 
    "Star Trek: Discovery":[1,2,3],
    "Star Trek: Lower Decks":[1,2,3,4], 
    "Star Trek: Prodigy":[1], 
    "Star Trek: Strange New Worlds":[1,2] 
}

def getLib():
    headers = {
        "Accept": "application/json"
    }
    api_url = http.client.HTTPSConnection(f"{plex_url}")
    api_url.request("GET", f"/library/sections/1/all?X-Plex-Token={plex_token}", headers=headers)
    lib_data = api_url.getresponse().read()
    lib_data_dict = json.loads(lib_data)

    star_trek_dict = {'total': 0, 'watched': 0,'percent': 0 }

    for series in lib_data_dict['MediaContainer']['Metadata']:
        if "Star Trek" in series['title']:
            star_trek_dict[series['title']] = {}
            # print("\n" + series['title'] + ":")
            show_duration = 0
            showID = series['ratingKey']
            api_url.request("GET", f"/library/metadata/{showID}/children?X-Plex-Token={plex_token}", headers=headers)
            show_data = api_url.getresponse().read()
            show_data_dict = json.loads(show_data)
            if int(series["childCount"]) > 1:
                for season in show_data_dict['MediaContainer']['Metadata']:
                    if "Season" in (season["title"] or ["title"]):
                        season_duration = 0
                        seasonID = season['ratingKey']
                        api_url.request("GET", f"/library/metadata/{seasonID}/children?X-Plex-Token={plex_token}", headers=headers)
                        season_data = api_url.getresponse().read()
                        season_data_dict = json.loads(season_data)
                        for eppisode in season_data_dict["MediaContainer"]["Metadata"]:
                            if series['title'] in completed_list:
                                if int(str(season['title']).replace('Season ', '')) in completed_list[series['title']]:
                                    star_trek_dict['watched'] = star_trek_dict['watched'] + int(eppisode['duration'])
                            star_trek_dict['total'] = star_trek_dict['total'] + int(eppisode['duration'])
                            show_duration = show_duration + int(eppisode['duration'])
                            season_duration = season_duration + int(eppisode['duration'])
                        star_trek_dict[series['title']][season["title"]] = str(datetime.timedelta(milliseconds = season_duration))
                        # print("\t" + season["title"] + ": " + str(datetime.timedelta(milliseconds = season_duration)))
            else:
                season_duration = 0
                seasonID = show_data_dict['MediaContainer']['Metadata'][0]['ratingKey']
                api_url.request("GET", f"/library/metadata/{seasonID}/children?X-Plex-Token={plex_token}", headers=headers)
                season_data = api_url.getresponse().read()
                season_data_dict = json.loads(season_data)
                for eppisode in season_data_dict["MediaContainer"]["Metadata"]:
                    if series['title'] in completed_list:
                        if str(series['title'])in completed_list:
                            star_trek_dict['watched'] = star_trek_dict['watched'] + int(eppisode['duration'])
                    star_trek_dict['total'] = star_trek_dict['total'] + int(eppisode['duration'])
                    show_duration = show_duration + int(eppisode['duration'])
                    season_duration = season_duration + int(eppisode['duration'])
                # print("\tSeason 1: " + str(datetime.timedelta(milliseconds = show_duration)))
                star_trek_dict[series['title']]['Season 1'] = str(datetime.timedelta(milliseconds = season_duration))
            star_trek_dict[series['title']]['total'] = str(datetime.timedelta(milliseconds = show_duration))
    star_trek_dict['percent'] = str(round(((star_trek_dict['watched']/star_trek_dict['total'])*100), 3)) + "%"
    star_trek_dict['total'] = str(datetime.timedelta(milliseconds = star_trek_dict['total']))
    star_trek_dict['watched'] = str(datetime.timedelta(milliseconds = star_trek_dict['watched']))


    for show in star_trek_dict:
        
        if show != 'total' and show != 'watched' and show != 'percent':
            print(show + ":")
            for s in star_trek_dict[show]:
                print(f"\t{s}: {star_trek_dict[show][s]}")
            print(f"Series Total: {star_trek_dict[show]['total']}\n---------------------------------------- \n")
    print(f"Total: {star_trek_dict['total']}\n")
    print(f"Watched: {star_trek_dict['watched']}\n")
    print(f"Percent: {star_trek_dict['percent']}\n")

    

if __name__ == "__main__":
    getLib()