###
# Copyright (c) 2014, dash
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

###

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks

import subprocess, re, string
from subprocess import Popen, PIPE
from time import sleep

SWIFT = '/home/djbot/djbot/plugins/djbot/say.sh'
MUTE = '/home/djbot/.config/pianobar/mute'

# this is included in plugins/Djbot/nonblockingstreamreader.py
from nbstreamreader import NonBlockingStreamReader as NBSR


class Djbot(callbacks.Plugin):
    """plays Pandora locally
        """
    # initialize plugin
    def __init__(self, irc):
        self.__parent = super(Djbot, self)
        self.__parent.__init__(irc)
        self.isPlaying = False
	# don't initialize pianobar and streamreader yet

    # start pianobar
    def play(self, irc, msg, args):
	""" takes no arguments

	loads pandora and starts music
	"""

	if not self.isPlaying:

	    # pianobar subprocess
	    self.p = Popen('pianobar', stdin=PIPE, stdout=PIPE, stderr=PIPE,
                shell=True)
	    
	    # non-blocking stream reader
	    self.nbsr = NBSR(self.p.stdout)
	    self.isPlaying = True
	    irc.reply('playing...')
	else:
	    irc.reply('already playing')
    play = wrap(play)

    # stop pianobar
    def stop(self, irc, msg, args):
	""" takes no arguments

	stops music and unloads pandora
	"""
	if self.isPlaying:
            # exit pianobar
            self.p.stdin.write('q')
	    # kill pianobar subprocess
            sleep(1)
	    self.p.terminate()
            self.isPlaying = False

	    irc.reply('stopping...')
	else:
	    irc.reply('not playing')
    stop = wrap(stop)

    # this prevents pianobar from running after unload
    def die(self):
        if self.isPlaying:
            self.p.stdin.write('q')
            sleep(1)
        self.p.terminate()
        self.isPlaying = False

    # increase system volume
    def volup(self, irc, msg, args):
        """takes no arguments

        increase the volume 5%
        """
        subprocess.call(['amixer', '-c0', 'set', 'PCM', '5dB+'])
    volup = wrap(volup)

    # decrease system volume
    def voldown(self, irc, msg, args):
        """takes no arguments

        decrease the volume 5db
        """
        subprocess.call(['amixer', '-c0', 'set', 'PCM', '5dB-'])
    voldown = wrap(voldown)

    # get recent output, formatted (somewhat) nicely
    def getOutput(self):
        temp = ''
        output = ''
        while True:	# clean up output and format for irc
            output += temp.expandtabs(0).replace('\x1b[2K',
                '').replace('\n', ' ') + ' '
            temp = self.nbsr.readline(0.3) #sometimes it takes time
            if not temp:
                break
        return output

    # clears output buffer so we don't get detritus
    def clearOutput(self):
	self.getOutput()

    # checks text for unwanted characters
    def isSafe(self, text):
        
        # check if all characters are allowed (zero tolerance)
	allowed = string.letters + string.digits + ' ?,.'
        for i in text:
            if not i in allowed:
                return False
        return True

    # speak text using shell wrapper
    def speak(self, irc, msg, args, text):
        """text

        pauses music, speaks given text, resumes music
        """
        if self.isSafe(text):

            # speak text
            subprocess.call([SWIFT, text])
    speak = wrap(speak, ['text'])
    
    # stop song announcements (driven by eventcmd)
    def nosongannounce(self, irc, msg, args):
        """takes no arguments

        causes djbot not to announce songs
        """

        subprocess.call(['touch', MUTE])
        irc.reply('song announce off')
    nosonganounce = wrap(nosongannounce)

    # start song announcements (driven by eventcmd)
    def songannounce(self, irc, msg, args):
        """takes no arguments

        causes djbot to announce songs
        """

        subprocess.call(['rm', '-f', MUTE])
        irc.reply('song announce on')
    songannounce = wrap(songannounce)


    ### Pianobar control
    # if there is a pending query when a song ends, the next song
    # will not start until the query has been answered
    # to dismiss a query without action, give it a newline

    # input: + 
    # expect: (i) Loving song... Ok.
    def love(self, irc, msg, args):
        """takes no arguments

        loves currently playing song
        """
        self.p.stdin.write('+')
        irc.reply('loving song...')
    love = wrap(love)


    # input: -
    # expect: (i) Banning song... Ok.
    def hate(self, irc, msg, args):
        """takes no arguments

        hates currently playing song
        """
        self.p.stdin.write('-')
        irc.reply('SUCH HATE!')
    hate = wrap(hate)

    # input: -
    # expect: (i) Banning song... Ok.
    def ban(self, irc, msg, args):
        """takes no arguments

        bans currently playing song
        """
        self.p.stdin.write('-')
        irc.reply('banning song')
    ban = wrap(ban)

    # input: a
    # expect: [?] Add artist or title to station:
    # input: <artist or title>
    # expect: (i) Searching... Ok.
    # 0) <artist>
    # 1) <artist>
    # [?] Select artist:
    # input: <number>
    # expect: (i) Adding music to station... Ok.
    def addmusic(self, irc, msg, args):
        """takes no arguments

        adds music to current station
        """
        #self.p.stdin.write('a')
        irc.reply('todo')

    # input: c
    # expect: [?] Create station from artist or title:
    # input: <artist or title>
    # expect: (i) Searching... Ok.
    # 0) <artist>
    # 1) <artist>
    # [?] Select artist:
    # input: <number>
    # expect: Creating station... Ok.
    def create(self, irc, msg, args):
        """takes no arguments

        creates new station, but does not switch to it
        """
        #self.p.stdin.write('c')
        #irc.reply(self.getOutput().replace(' |>  ', ''))
        irc.reply('not yet implemented')

    # input: d
    # expect: [?] Really delete "<station>"? [yN]
    # input: y
    # expect: (i) Deleting station... Ok.
    # Playback stops pending station selection
    def delete(self, irc, msg, args):
        """takes no arguments

        deletes current station
        """
        self.p.stdin.write('dy')
        irc.reply('Station deleted')

    # input: e
    # expect: (i) Receiving explanation... Ok.
    # (i) We're playing this track because ... (2-4 lines)
    def explain(self, irc, msg, args):
        """takes no arguments

        explains why current song is playing
        """
	self.getOutput()
        self.p.stdin.write('e')
        irc.reply(self.getOutput())
    
    # input: g
    # expect: (i) Receiving genre stations... Ok.
    # 0) <category>
    # 1) ... (about 30 lines)
    # [?] Select category:
    # input: <number>
    # expect: 0) <genre>
    # 1) ... (fewer lines)
    # [?] Select genre:
    # input: <number>
    # expect: (i) Adding genre station "<genre>"... Ok.
    def addgenre(self, irc, msg, args):
        """takes no arguments

        adds genre station, but does not switch to it
        """
        #self.p.stdin.write('g')
        irc.reply('todo')

    # input: h
    # expect: 0) <artist> - <title>
    # 1) <artist> - <title>
    # 2) ...
    # [?] Select song:
    # input: <number>
    # expect: [?] What to do with this song?
    # (I assume we can love / ban / explain from history)
    def history(self, irc, msg, args):
        """takes no arguments

        return recently played songs
        """
	self.getOutput()
        self.p.stdin.write('h\n')
        irc.reply(self.getOutput())

    # input: i
    # expect: |> Station "<station>" (<station id>)
    # "<title>" by "<artist>" on "<album>"
    def info(self, irc, msg, args):
        """takes no arguments

        returns title, artist, and album
        """
        self.clearOutput()
	self.p.stdin.write('i')
        irc.reply(self.getOutput().replace(' |>  ', ''))

    # input: n
    # no response, next song plays
    def skip(self, irc, msg, args):
        """takes no arguments

        moves to next song
        """
        self.p.stdin.write('n')
        irc.reply('skipping...')
    skip = wrap(skip)

    # input: S
    # no response, music pauses playback
    def pause(self, irc, msg, args):
        """takes no arguments

        pause playback (use resume to continue)
        """
        self.p.stdin.write('S')
        irc.reply('paused. use resume to continue')
    pause = wrap(pause)

    # input: P
    # no response, music resumes playback
    def resume(self, irc, msg, args):
        """takes no arguments

        resume playback after pause
        """
        self.p.stdin.write('P')
        irc.reply('resuming playback...')
    resume = wrap(resume)

    # input: q
    # pianobar closes
    # we don't want this to happen without unloading the plugin
#    def quit(self, irc, msg, args):
#        """takes no arguments
#
#        exit pianobar
#        """
#        irc.reply('Please unload the plugin instead')
#
    # input: r
    # expect: [?] New name:
    # input: <name>
    # expect: Renaming station... Ok.
    def rename(self, irc, msg, args, newname):
        """takes no arguments

        rename station
        """
        #if isSafe(newname):
        #	self.p.stdin.write('r' + newname)
        irc.reply('todo')
    rename = wrap(rename, ['text'])

    # input: s
    # expect: 0) <station>
    # 1) <station>
    # 2) <station>
    # (etc)
    # [?] Select station:
    # input: <number>
    # expect: |> Station "<station>" (<station id>)
    # selected station plays
    def station(self, irc, msg, args, cmd):
        """<list> or <integer>

        list returns a list of available stations
        integer selects corresponding station
        """
        if cmd == "list":
            self.clearOutput()
            self.p.stdin.write('s\n') # select station, but cancel
            irc.reply(self.getOutput().replace(' q  ', '')
		.replace('  Q  ', ' ')) # get station list
        elif self.isSafe(cmd) and (0 <= int(cmd) < 100):
            self.p.stdin.write('s' + cmd + '\n')
            irc.reply('selected ' + cmd)
    station = wrap(station, ['text'])

    # input: t
    # expect: (i) Putting song on shelf... Ok.
    # will not play again for one month
    def tired(self, irc, msg, args):
        """takes no arguments

        do not play this song again for one month
        """
        self.p.stdin.write('t')
        irc.reply('shelving...')
    tired = wrap(tired)

    # input: u
    # expect: 0) <next song>
    # 1) <song after next>
    def upcoming(self, irc, msg, args):
        """takes no arguments

        returns upcoming songs
        """
        self.clearOutput()
        self.p.stdin.write('u')
        irc.reply(self.getOutput())

    # input: x
    # expect: 0) <station>
    # 1) <station>
    # 2) ...
    # [?] Toggle quickmix for station:
    # this only works when we are on the quickmix station!
    # selection repeats until we give it \n
    # if we are not on a quickmix station, it replies with
    # /!\ Not a QuickMix station
    def quickmix(self, irc, msg, args, cmd):
        """<list> or <integer>

        toggle quickmix stations
        """
        if cmd == 'list':
	    self.clearOutput()
            self.p.stdin.write('x')
	    output = self.getOutput()
	    if 'Not a QuickMix station' in output:
	        irc.reply('you must be listening to the QuickMix station first')
            else:
                irc.reply(output)
        elif isSafe(cmd) and 0 <= int(cmd) < 100:
		self.clearOutput()
		self.p.stdin.write('x' + cmd)
		irc.reply(self.getOutput())
    quickmix = wrap(quickmix, ['text'])

    # input: b
    # expect: [?] Bookmark [s]ong or [a]rtist?
    # input: s
    # expect: (i) Bookmarking song... Ok.
    def bookmark(self, irc, msg, args, option):
        """'artist' or 'song'

        bookmark song
        """
        if option == 'artist':
            cmd = 'a'
        elif option == 'song':
            cmd = 's'
        self.p.stdin.write('b' + cmd)
        irc.reply('Bookmarked ' + option)
    bookmark = wrap(bookmark, ['text'])


    # input: =
    # expect: (i) Fetching station info... Ok.
    # [?] Delete [a]rtist/[s]ong seeds or [f]eedback?
    # input: s
    # expect: 0) <station seed>
    # 1) ...
    # [?] Select song:
    # input: 0
    # expect: (i) Deleting artist seed... Ok.
    def removeseed(self, irc, msg, args):
        """takes no arguments

        remove seed from station
        """
        #self.p.stdin.write('=')
        irc.reply('todo')

    # input: v
    # expect: [?] Create station from [s]ong or [a]rtist?
    # input: s
    # expect: (i) Creating station... Ok.
    def newfromsong(self, irc, msg, args):
        """takes no arguments

        new station from song
        """
        #self.p.stdin.write('v')
        irc.reply('todo')
    
    # parse info command and return only song title
    def title(self, irc, msg, args):
        """takes no arguments

        returns song title
        """
        irc.reply('todo')

    # parse info command and return only artist name
    def artist(self, irc, msg, args):
        """takes no arguments

        returns song artist
        """
        irc.reply('todo')

    # parse info command and return only album name
    def album(self, irc, msg, args):
        """takes no arguments

        returns song album
        """
        irc.reply('todo')

    # get song info
    def songinfo(self, irc, msg, args):
        """takes no arguments

        returns title, artist, and album
        """
        irc.reply('todo')



Class = Djbot


# vim: set shiftwidth=4 softtabstop=4 expandtab textwidth=79:

