import http.client
import xmltodict
import datetime

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
    api_url = http.client.HTTPSConnection(f"{plex_url}")
    api_url.request("GET", f"/library/sections/1/all?X-Plex-Token={plex_token}")
    lib_data = api_url.getresponse().read()
    lib_data_dict = xmltodict.parse(lib_data)

    my_clever_var = {}

    total_duration = 0
    watched_duration = 0

    for series in lib_data_dict['MediaContainer']['Directory']:
        if "Star Trek" in series['@title']:
            my_clever_var[series['@title']] = {}
            # print("\n" + series['@title'] + ":")
            show_duration = 0
            showID = series['@ratingKey']
            api_url.request("GET", f"/library/metadata/{showID}/children?X-Plex-Token={plex_token}")
            show_data = api_url.getresponse().read()
            show_data_dict = xmltodict.parse(show_data)
            if int(series["@childCount"]) > 1:
                for season in show_data_dict['MediaContainer']['Directory']:
                    if "Season" in (season["@title"] or ["@title"]):
                        season_duration = 0
                        seasonID = season['@ratingKey']
                        api_url.request("GET", f"/library/metadata/{seasonID}/children?X-Plex-Token={plex_token}")
                        season_data = api_url.getresponse().read()
                        season_data_dict = xmltodict.parse(season_data)
                        for eppisode in season_data_dict["MediaContainer"]["Video"]:
                            if series['@title'] in completed_list:
                                if int(str(season['@title']).replace('Season ', '')) in completed_list[series['@title']]:
                                    watched_duration = watched_duration + int(eppisode['@duration'])
                            total_duration = total_duration + int(eppisode['@duration'])
                            show_duration = show_duration + int(eppisode['@duration'])
                            season_duration = season_duration + int(eppisode['@duration'])
                        my_clever_var[series['@title']][season["@title"]] = str(datetime.timedelta(milliseconds = season_duration))
                        # print("\t" + season["@title"] + ": " + str(datetime.timedelta(milliseconds = season_duration)))
            else:
                season_duration = 0
                seasonID = show_data_dict['MediaContainer']['Directory']['@ratingKey']
                api_url.request("GET", f"/library/metadata/{seasonID}/children?X-Plex-Token={plex_token}")
                season_data = api_url.getresponse().read()
                season_data_dict = xmltodict.parse(season_data)
                for eppisode in season_data_dict["MediaContainer"]["Video"]:
                    if series['@title'] in completed_list:
                        if str(series['@title'])in completed_list:
                            watched_duration = watched_duration + int(eppisode['@duration'])
                    total_duration = total_duration + int(eppisode['@duration'])
                    show_duration = show_duration + int(eppisode['@duration'])
                    season_duration = season_duration + int(eppisode['@duration'])
                # print("\tSeason 1: " + str(datetime.timedelta(milliseconds = show_duration)))
                my_clever_var[series['@title']]['Season 1'] = str(datetime.timedelta(milliseconds = season_duration))
            my_clever_var[series['@title']]['total'] = str(datetime.timedelta(milliseconds = show_duration))
    my_clever_var['total'] = str(datetime.timedelta(milliseconds = total_duration))
    my_clever_var['watched'] = str(datetime.timedelta(milliseconds = watched_duration))
    my_clever_var['percent'] = str(round(((watched_duration/total_duration)*100), 3)) + "%"




            # print("\nSeries Total: ",str(datetime.timedelta(milliseconds = show_duration)) + "\n---------------------------------------- \n")
    # print("Total: " + str(datetime.timedelta(milliseconds = total_duration)))
    # print("Watched: " + str(datetime.timedelta(milliseconds = watched_duration)))
    # print(str(round(((watched_duration/total_duration)*100), 3)) + "%")


    for show in my_clever_var:
        
        if show != 'total' and show != 'watched' and show != 'percent':
            print(show + ":")
            for s in my_clever_var[show]:
                print(f"\t{s}: {my_clever_var[show][s]}")
            print(f"Series Total: {my_clever_var[show]['total']}\n---------------------------------------- \n")
    print(f"Total: {my_clever_var['total']}\n")
    print(f"Watched: {my_clever_var['watched']}\n")
    print(f"Percent: {my_clever_var['percent']}\n")

    

if __name__ == "__main__":
    getLib()