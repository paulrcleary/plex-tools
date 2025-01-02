
import http.client
import os
import json
import re


def getLib():
    api_url = http.client.HTTPSConnection(f"{os.environ['PLEX_URL']}")
    api_url.request("GET", f"/library/sections/4/all?X-Plex-Token={os.environ['PLEX_TOKEN']}", headers={"Accept": "application/json"})
    lib_data = api_url.getresponse().read()
    lib_data_dict = json.loads(lib_data)

    for i in lib_data_dict['MediaContainer']['Metadata']:
        movieID = i['ratingKey']
        api_url.request("GET", f"/library/metadata/{movieID}?X-Plex-Token={os.environ['PLEX_TOKEN']}", headers={"Accept": "application/json"})
        movie_data = api_url.getresponse().read()
        movie_data_dict = json.loads(movie_data)
        title = ''
        year = ''
        hdr = ''
        codec = ''
        audio = ''
        channels = ''

        title = movie_data_dict['MediaContainer']['Metadata'][0]['title']
        year = f"({movie_data_dict['MediaContainer']['Metadata'][0]['year']})"
        resolution = f"[{movie_data_dict['MediaContainer']['Metadata'][0]['Media'][0]['videoResolution']}]"
        codec = f"[{movie_data_dict['MediaContainer']['Metadata'][0]['Media'][0]['videoCodec']}]"
        original_file_name = movie_data_dict['MediaContainer']['Metadata'][0]['Media'][0]['Part'][0]['file']
        for v in movie_data_dict['MediaContainer']['Metadata'][0]['Media'][0]['Part'][0]['Stream']:
            if v['streamType'] == 1 and v['index'] == 0:
                if v['extendedDisplayTitle'] == "4K DoVi/HDR10 (HEVC Main 10)":
                    hdr = "[Dolby Vision - HDR10]"
                elif "HDR10" in v['extendedDisplayTitle'] and "HEVC" in v['extendedDisplayTitle']:
                    hdr = "[HDR10]"
                else:
                    hdr = "[SDR]"
            elif v['streamType'] == 2 and v['index'] == 1:
                if "5.1" in v['displayTitle']:
                    channels = "5.1"
                elif "7.1" in v['displayTitle']:
                    channels = "7.1"
                else: pass
                if v['codec'] == "truehd":
                    if "Atmos" in v['extendedDisplayTitle']:
                        audio = "Dolby Atmos TrueHD"
                    else:
                        audio = "TrueHD"
                elif v['codec'] == "dca":
                    audio = "DTS-HD"
                elif v['codec'] == "eac3":
                    audio = "EAC3"
                else: pass
                if audio and channels:
                    audioCodec = '[' + audio + " " + channels + ']'
                elif codec:
                    audioCodec = '[' + audio + ']'
                elif audio:
                    audioCodec = '[' + channels + ']'
                else: pass
            elif v['streamType'] == '3':
                pass


        file = f"{movieID} - {str(title).replace(' [4K]', '').replace(' [4k]', '')} {year} {resolution.upper()} [source] [REMUX?] {codec.upper()} {hdr} {audioCodec}"
        fileName = re.sub(r'[\\/*?:"<>|]',"", file)
        # os.rename(file)
        print(fileName)



if __name__ == "__main__":
    getLib()