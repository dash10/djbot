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

from subprocess import Popen, PIPE
from time import sleep
import re

# this is included in plugins/Pandora
from nbstreamreader import NonBlockingStreamReader as NBSR


class Pandora(callbacks.Plugin):
    """plays Pandora locally
        """
    # initialize plugin
    def __init__(self, irc):
        self.__parent = super(Pandora, self)
        self.__parent.__init__(irc)
        
        # pianobar subprocess
        self.p = Popen('pianobar', stdin=PIPE, stdout=PIPE, stderr=PIPE)
        
        # non-blocking stream reader
        self.nbsr = NBSR(self.p.stdout)

    # this prevents pianobar from running after unload
    def die(self):
        self.p.terminate()

    # gets the most recent line of output
    def getLast(self):
        temp = ''
        while True:
            output = temp
            temp = self.nbsr.readline(0.1)
            if not temp:
                break
        return output

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
        self.p.stdin.write('a')
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
        self.p.stdin.write('c')
        irc.reply('todo')

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
        self.p.stdin.write('e')
        irc.reply('todo')
    
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
        self.p.stdin.write('g')
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
        self.p.stdin.write('h')
        irc.reply('todo')

    # input: i
    # expect: |> Station "<station>" (<station id>)
    # "<title>" by "<artist>" on "<album>"
    def info(self, irc, msg, args):
        """takes no arguments

        returns title, artist, album, and station
        """
        self.p.stdin.write('i')
        irc.reply('todo')

    # input: n
    # no response, next song plays
    def skip(self, irc, msg, args):
        """takes no arguments

        moves to next song
        """
        self.p.stdin.write('n')
        irc.reply('skipping...')
    skip = wrap(skip)

    # input: p
    # no response, music pauses / unpauses
    def pause(self, irc, msg, args):
        """takes no arguments

        pause or unpause playback
        """
        self.p.stdin.write('p')
    pause = wrap(pause)

    # input: q
    # pianobar closes
    # we don't want this to happen without unloading the plugin
    def quit(self, irc, msg, args):
        """takes no arguments

        exit pianobar
        """
        irc.reply('Please unload the plugin instead')

    # input: r
    # expect: [?] New name:
    # input: <name>
    # expect: Renaming station... Ok.
    def rename(self, irc, msg, args, newname):
        """takes no arguments

        rename station
        """
        self.p.stdin.write('r' + newname)
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
            self.getLast()

            self.p.stdin.write('s' + "\n")
            sleep(0.1)
            # get response from command
            temp = ''
            output = ''
            # there must be a better way to filter this
            while True:
                output += temp.expandtabs(0).replace('\x1b[2K',
                    '').replace('\n', '').replace(' q ', 
                    '').replace(' Q ', '') + ' '
                temp = self.nbsr.readline(0.1)
                if not temp:
                    break
            irc.reply(str(output))
        elif (0 <= int(cmd) < 100):
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
        self.p.stdin.write('u')
        irc.reply('todo')

    # input: x
    # expect: 0) <station>
    # 1) <station>
    # 2) ...
    # [?] Toggle quickmix for station:
    # this only works when we are on the quickmix station!
    # selection repeats until we give it \n
    # if we are not on a quickmix station, it replies with
    # /!\ Not a QuickMix station
    def quickmix(self, irc, msg, args):
        """takes no arguments

        select quickmix station
        """
        self.p.stdin.write('x')
        irc.reply('todo')

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

    # input: )
    # no response, volume increases slightly (1/50?)
    def volup(self, irc, msg, args):
        """takes no arguments

        increase the volume
        """
        self.p.stdin.write(')')
    volup = wrap(volup)

    # input: (
    # no response, volume decreases slightly (1/50?)
    def voldown(self, irc, msg, args):
        """takes no arguments

        decrease the volume
        """
        self.p.stdin.write('(')
    voldown = wrap(voldown)

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
        self.p.stdin.write('=')
        irc.reply('todo')

    # input: v
    # expect: [?] Create station from [s]ong or [a]rtist?
    # input: s
    # expect: (i) Creating station... Ok.
    def newfromsong(self, irc, msg, args):
        """takes no arguments

        new station from song
        """
        self.p.stdin.write('v')
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



Class = Pandora


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:


