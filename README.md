# plex-tools

A personal library of python scripts to interact with a Plex Server.

# Star Trek Durations
A simple script to query a plex server (via http request) and return durations of star trek seasons and episodes.
1. Retrieve your plex token and set it as the environment variable `PLEX_TOKEN`
2. Set your plex URL as the environment variable `PLEX_URL`
3. Fill in which Star Trek shows/seasons you have seen (optional)
4. Run.
## Example output
```
Star Trek:
        Season 1: 1 day, 0:25:20.777000
        Season 2: 21:54:23.193000
        Season 3: 20:19:13.542000
Series Total:  2 days, 18:38:57.512000
---------------------------------------- 
...
Total: 28 days, 20:50:22.133000
Watched: 0:00:00
0.0%
```

# Plex File Renamer
A simple script to query a plex server (via http request) and return video file format information.
1. Retrieve your plex token and set it as the environment variable `PLEX_TOKEN`
2. Set your plex URL as the environment variable `PLEX_URL`
3. Run the script from your plex library folder.
4. Done