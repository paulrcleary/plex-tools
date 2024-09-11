import http.client
import xmltodict
import datetime

plex_token = "redacted"
plex_url = "redacted"

#list of the star trek series i have finished watching
completed_list = []
# completed_list = ["Star Trek", "Star Trek Continues", "Star Trek: Deep Space Nine", "Star Trek: Voyager", "Star Trek: Lower Decks", "Star Trek: Prodigy", "Star Trek: Strange New Worlds", "Star Trek: The Next Generation", "Star Trek: The Animated Series"]

def getLib():
    api_url = http.client.HTTPSConnection(f"{plex_url}")
    api_url.request("GET", f"/library/sections/1/all?X-Plex-Token={plex_token}")
    lib_data = api_url.getresponse().read()
    lib_data_dict = xmltodict.parse(lib_data)

    total_duration = 0
    watched_duration = 0

    for i in lib_data_dict['MediaContainer']['Directory']:
        if "Star Trek" in i['@title']:
            print("\n" + i['@title'] + ":")
            show_duration = 0
            showID = i['@ratingKey']
            api_url.request("GET", f"/library/metadata/{showID}/children?X-Plex-Token={plex_token}")
            show_data = api_url.getresponse().read()
            show_data_dict = xmltodict.parse(show_data)
            if int(i["@childCount"]) > 1:
                for s in show_data_dict['MediaContainer']['Directory']:
                    try:
                        if "Season" in (s["@title"] or ["@title"]):
                            season_duration = 0
                            seasonID = s['@ratingKey']
                            api_url.request("GET", f"/library/metadata/{seasonID}/children?X-Plex-Token={plex_token}")
                            season_data = api_url.getresponse().read()
                            season_data_dict = xmltodict.parse(season_data)
                            for e in season_data_dict["MediaContainer"]["Video"]:
                                if i['@title'] in completed_list:
                                    watched_duration = watched_duration + int(e['@duration'])
                                total_duration = total_duration + int(e['@duration'])
                                show_duration = show_duration + int(e['@duration'])
                                season_duration = season_duration + int(e['@duration'])

                            print("\t" + s["@title"] + ": " + str(datetime.timedelta(milliseconds = season_duration)))
                        else:
                            pass
                    except:
                        pass
            else:
                    season_duration = 0
                    seasonID = show_data_dict['MediaContainer']['Directory']['@ratingKey']
                    api_url.request("GET", f"/library/metadata/{seasonID}/children?X-Plex-Token={plex_token}")
                    season_data = api_url.getresponse().read()
                    season_data_dict = xmltodict.parse(season_data)
                    if i['@title'] in completed_list:
                        for e in season_data_dict["MediaContainer"]["Video"]:
                            if i['@title'] in completed_list:
                                watched_duration = watched_duration + int(e['@duration'])
                            total_duration = total_duration + int(e['@duration'])
                            show_duration = show_duration + int(e['@duration'])
                            season_duration = season_duration + int(e['@duration'])
                    print("\tSeason 1: " + str(datetime.timedelta(milliseconds = show_duration)))


            print("\nSeries Total: ",str(datetime.timedelta(milliseconds = show_duration)) + "\n---------------------------------------- \n")
    print("Total: " + str(datetime.timedelta(milliseconds = total_duration)))
    print("Watched: " + str(datetime.timedelta(milliseconds = watched_duration)))
    print(str(round(((watched_duration/total_duration)*100), 3)) + "%")
    

if __name__ == "__main__":
    getLib()