Supybot plugin to control Pianobar via IRC

### IMPORTANT ###
This is still a work in progress!

Several of the commands below are unimplemented, or do not yet work correctly.

### Useage ###
Pianobar will not be loaded until it is given the play command.

Non-Pianobar commands:

album - returns just the album of current song

artist - returns just the artist of current song

songannounce - speak song title and artist after every track

nosongannounce - don't speak unless asked

play - load pianobar and start playback

speak - speak given text (pauses music if playing)

stop - stop playback, unload pianobar

voldown - reduces system volume (not Pianobar volume)

volup - increases system volume (not Pianobar volume)



Pianobar commands:

addgenre - add genre station 

addmusic - add music to station

ban - ban current song on this station

bookmark - bookmark current artist or song

create - create station

delete - delete current station

explain - explain why current track is playing

history - show recently played tracks

info - show current title, artist, and album

love - love current song

newfromsong - new station from current song

pause - pause playback. Note that pausing for long periods (overnight) causes pianobar to crash)

quickmix - select stations for the quickmix station (only works when on quickmix station)

quit - does nothing constructive

removeseed - remove station seed

rename - rename station

skip - skip current song

songinfo - return current song title, artist, and album

station - select station

tired - do not play current song again for a month

upcoming - show upcoming tracks

### Setup ###
Clone into Djbot directory, in your bot's plugins directory.

Ensure that Pianobar is set up using default controls, and make sure it autoplays when started.

If you are running this on Raspbian you will likely need to compile Pianobar 2013.05.19

