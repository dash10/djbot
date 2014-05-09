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

# this is included in plugins/Pandora
from nbstreamreader import NonBlockingStreamReader as NBSR

# pandora subprocess


class Pandora(callbacks.Plugin):
    """plays Pandora locally
        """
    def __init__(self, irc):
        self.__parent = super(Pandora, self)
        self.__parent.__init__(irc)
        self.p = Popen('pianobar', stdin=PIPE, stdout=PIPE, stderr=PIPE)
        self.nbsr = NBSR(self.p.stdout)

    # this prevents pianobar from running after unload
    def die(self):
        self.p.terminate()

    # gets the most recent line of output
    def getOutput(self):
        temp = ''
        while True:
            output = temp
            temp = self.nbsr.readline(0.1)
            if not temp:
                break
        return output

    # gets output from command
    def respondTo(self, cmd):

        # get to last line of output
        self.getOutput()

        self.p.stdin.write(cmd)
        sleep(0.2)
        # get response from command
        temp = ''
        output = ''
        while True:
            output += temp
            temp = self.nbsr.readline(0.1)
            if not temp:
                break
        return output

    # all the usual commands for pianobar
    def love(self, irc, msg, args):
        """takes no arguments

        loves currently playing song
        """
        output = self.respondTo('+')
        irc.reply(output)

    def ban(self, irc, msg, args):
        """takes no arguments

        bans currently playing song
        """
        irc.reply(self.respondTo('-'))

    def addmusic(self, irc, msg, args):
        """takes no arguments

        add music to station
        """
        irc.reply(self.respondTo('a'))

    def create(self, irc, msg, args):
        """takes no arguments

        create new station
        """
        irc.reply(self.respondTo('c'))

    def delete(self, irc, msg, args):
        """takes no arguments

        delete current station
        """
        irc.reply(self.respondTo('d'))

    def explain(self, irc, msg, args):
        """takes no arguments

        explain why current song is playing
        """
        irc.reply(self.respondTo('e'))

    def addgenre(self, irc, msg, args):
        """takes no arguments

        add genre station
        """
        irc.reply(self.respondTo('g'))

    def history(self, irc, msg, args):
        """takes no arguments

        return recently played songs
        """
        irc.reply(self.respondTo('h'))

    def info(self, irc, msg, args):
        """takes no arguments

        returns title, artist, album, and station
        """
        irc.reply(self.respondTo('i'))

    def skip(self, irc, msg, args):
        """takes no arguments

        moves to next song
        """
        self.p.stdin.write('n')
        irc.reply('skipped')

    def pause(self, irc, msg, args):
        """takes no arguments

        pause or unpause playback
        """
        irc.reply(self.respondTo('p'))

    def quit(self, irc, msg, args):
        """takes no arguments

        causes pandora to exit
        """
        irc.reply('You can\'t be serious')

    def rename(self, irc, msg, args):
        """takes no arguments

        rename station
        """
        irc.reply(self.respondTo('r'))

    def station(self, irc, msg, args):
        """takes no arguments

        select station
        """
        irc.reply(self.respondTo('s'))

    def tired(self, irc, msg, args):
        """takes no arguments

        do not play again for one month
        """
        irc.reply(self.respondTo('t'))

    def upcoming(self, irc, msg, args):
        """takes no arguments

        returns upcoming songs
        """
        irc.reply(self.respondTo('u'))

    def quickmix(self, irc, msg, args):
        """takes no arguments

        select quickmix station
        """
        irc.reply(self.respondTo('x'))

    def bookmark(self, irc, msg, args):
        """takes no arguments

        bookmark song
        """
        irc.reply(self.respondTo('b'))

    def volup(self, irc, msg, args):
        """takes no arguments

        increase the volume
        """
        self.p.stdin.write(')')

    def voldown(self, irc, msg, args):
        """takes no arguments

        decrease the volume
        """
        self.p.stdin.write('(')

    def removeseed(self, irc, msg, args):
        """takes no arguments

        remove seed from station
        """
        irc.reply(self.respondTo('='))

    def newfromsong(self, irc, msg, args):
        """takes no arguments

        new station from song
        """
        irc.reply(self.respondTo('v'))

    def select(self, irc, msg, args, cmd):
        """integer

        use to select options from a list
        """
        if 0 <= cmd < 100:
            irc.reply(self.respondTo(str(cmd)))
        else:
            irc.reply('value out of range')
    select = wrap(select, ['int'])
    def title(self, irc, msg, args):
        """takes no arguments

        returns song title
        """
        irc.reply('not yet implemented')

    def artist(self, irc, msg, args):
        """takes no arguments

        returns song artist
        """
        irc.reply('not yet implemented')

    def album(self, irc, msg, args):
        """takes no arguments

        returns song album
        """
        irc.reply('not yet implemented')

    def songinfo(self, irc, msg, args):
        """takes no arguments

        returns title, artist, and album
        """
        irc.reply(getOutput)



Class = Pandora


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:


