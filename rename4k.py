import re

from src import plex


def process_video_codec(object):
    if object['extendedDisplayTitle'] == "4K DoVi/HDR10 (HEVC Main 10)":
        hdr = "[Dolby Vision - HDR10]"
    elif "HDR10" in object['extendedDisplayTitle'] and "HEVC" in object['extendedDisplayTitle']:
        hdr = "[HDR10]"
    else:
        hdr = "[SDR]"

    return hdr


def process_audio_codec(object):
    if "5.1" in object['displayTitle']:
        channels = "5.1"
    elif "7.1" in object['displayTitle']:
        channels = "7.1"
    else: 
        channels = "Stereo"

    if object['codec'] == "truehd":
        if "Atmos" in object['extendedDisplayTitle']:
            audio = "Dolby Atmos TrueHD"
        else:
            audio = "TrueHD"
    elif object['codec'] == "dca":
        audio = "DTS-HD"
    elif object['codec'] == "eac3":
        audio = "EAC3"
    else:
        audio = object['codec']

    if audio and channels:
        audio_codec = '[' + audio + " " + channels + ']'
    elif channels:
        audio_codec = '[' + audio + ']'
    elif audio:
        audio_codec = '[' + channels + ']'

    return audio_codec


def getLib():
    lib_data = plex.request('/library/sections/4/all')

    for i in lib_data['MediaContainer']['Metadata']:
        movie_id = i['ratingKey']
        movie_data = plex.request(f"/library/metadata/{movie_id}")

        title = movie_data['MediaContainer']['Metadata'][0]['title']
        year = f"({movie_data['MediaContainer']['Metadata'][0]['year']})"
        resolution = f"[{movie_data['MediaContainer']['Metadata'][0]['Media'][0]['videoResolution']}]"

        codec = f"[{movie_data['MediaContainer']['Metadata'][0]['Media'][0]['videoCodec']}]"
        original_file_name = movie_data['MediaContainer']['Metadata'][0]['Media'][0]['Part'][0]['file']

        for v in movie_data['MediaContainer']['Metadata'][0]['Media'][0]['Part'][0]['Stream']:
            if v['streamType'] == 1 and v['index'] == 0:
                hdr = process_video_codec(v)
            elif v['streamType'] == 2 and v['index'] == 1:
                audio_codec = process_audio_codec(v)


        file = f"{movie_id} - {str(title).replace(' [4K]', '').replace(' [4k]', '')} {year} {resolution.upper()} [source] [REMUX?] {codec.upper()} {hdr} {audio_codec}"
        file_name = re.sub(r'[\\/*?:"<>|]',"", file)
        # os.rename(file)
        print(file_name)


if __name__ == "__main__":
    getLib()