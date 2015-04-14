#!/bin/bash

# call swift with appropriate text
~/.local/bin/swift "$@" &

# get pid of background process
pid=$!

# wait for swift to catch up
sleep 1

# pause music
printf "S" > ~/.config/pianobar/ctl

# wait for swift to finish talking
wait $pid

# unpause music
printf "P" > ~/.config/pianobar/ctl

# if we made it this far, everything is good
exit 0

