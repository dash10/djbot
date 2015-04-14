Supybot plugin to control Pianobar via IRC

### IMPORTANT ###
This is still a work in progress, please be patient.

Several of the commands below are not yet implemented.


### Setup ###
Assuming fresh install of Raspbian:

1. Set up pianobar and bc
    
    sudo apt-get update
    sudo apt-get install pianobar bc
    configure pianobar appropriately

    ** NOTE ** pianobar in repos may still be broken, if so install from source. 
        I know version 2013.05.19 works, unsure of more recent versions.

2. Set up Limnoria (Supybot fork)

    git clone https://github.com/ProgVal/Limnoria
    cd Limnoria
    python setup.py build
    sudo python setup.py install
    supybot-wizard

3. Set up djbot

    cd <bot dir>/plugins
    git clone https://github.com/dash10/djbot
    
4. Set up TTS
    
    ** todo **
    currently I use Cepstral Swift, in my opinion it was worth the money. I don't
    know if they will still provide the Raspberry Pi version of swift.
    I eventually will set this up with something else / free, not a priority at this point.



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
