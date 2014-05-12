Supybot plugin to control Pianobar via IRC

### IMPORTANT ###
This is not yet complete. Many commands simply return "todo" at this point.


I am having some trouble parsing the time remaining bit from pianobar, so I disabled it. In pianobar/src/main.c comment out line 392 as follows:

old:
				BarMainPrintTime (app);
new:
//				BarMainPrintTime (app);

then compile and install as usual (don't forget to set ffmpeg version in Makefile).

To compile current pianobar on fedora 20, I needed to install gnutls-devel, json-c-devel, ffmpeg-devel, libgcrypt-devel, and libao-devel. YMMV.

The most recent version of pianobar does not currently compile on Raspbian, due to the ffmpeg version. 2013.09.15 appears to work, however.

Setup:
1. You must already have Limnoria installed and configured.
2. Clone into djbot in your bot's plugins directory

Usage:
Pianobar should start playing when you load the plugin.
