import datetime

from src import plex

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
    star_trek = {'total': 0, 'watched': 0,'percent': 0 }
    lib_data = plex.request('/library/sections/1/all')
    for series in lib_data['MediaContainer']['Metadata']:
        if "Star Trek" in series['title']:
            star_trek[series['title']] = {}
            show_duration = 0
            show_data = plex.request(f"/library/metadata/{series['ratingKey']}/children")
            if int(series["childCount"]) > 1:
                for season in show_data['MediaContainer']['Metadata']:
                    if "Season" in (season["title"] or ["title"]):
                        season_duration = 0
                        season_data = plex.request(f"/library/metadata/{season['ratingKey']}/children")
                        for eppisode in season_data["MediaContainer"]["Metadata"]:
                            if series['title'] in completed_list:
                                if int(str(season['title']).replace('Season ', '')) in completed_list[series['title']]:
                                    star_trek['watched'] = star_trek['watched'] + int(eppisode['duration'])
                            star_trek['total'] = star_trek['total'] + int(eppisode['duration'])
                            show_duration = show_duration + int(eppisode['duration'])
                            season_duration = season_duration + int(eppisode['duration'])
                        star_trek[series['title']][season["title"]] = str(datetime.timedelta(milliseconds = season_duration))
            else:
                season_duration = 0
                season_data = plex.request(f"/library/metadata/{show_data['MediaContainer']['Metadata'][0]['ratingKey']}/children")
                for eppisode in season_data["MediaContainer"]["Metadata"]:
                    if series['title'] in completed_list:
                        if str(series['title'])in completed_list:
                            star_trek['watched'] = star_trek['watched'] + int(eppisode['duration'])
                    star_trek['total'] = star_trek['total'] + int(eppisode['duration'])
                    show_duration = show_duration + int(eppisode['duration'])
                    season_duration = season_duration + int(eppisode['duration'])
                star_trek[series['title']]['Season 1'] = str(datetime.timedelta(milliseconds = season_duration))
            star_trek[series['title']]['total'] = str(datetime.timedelta(milliseconds = show_duration))
    star_trek['percent'] = str(round(((star_trek['watched']/star_trek['total'])*100), 3)) + "%"
    star_trek['total'] = str(datetime.timedelta(milliseconds = star_trek['total']))
    star_trek['watched'] = str(datetime.timedelta(milliseconds = star_trek['watched']))

    for show in star_trek:
        if show != 'total' and show != 'watched' and show != 'percent':
            print(show + ":")
            for s in star_trek[show]:
                print(f"\t{s}: {star_trek[show][s]}")
            print(f"Series Total: {star_trek[show]['total']}\n---------------------------------------- \n")
    print(f"Total: {star_trek['total']}\n")
    print(f"Watched: {star_trek['watched']}\n")
    print(f"Percent: {star_trek['percent']}\n")

    

if __name__ == "__main__":
    getLib()