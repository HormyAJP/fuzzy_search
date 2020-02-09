# Simple fuzzy matcher

Not meant for anyone to use. Just me playing around.

## How to use

Just write a file called `fuzzy_input.txt` and set `STRING_TO_MATCH` in the file to some string.
The script will print all lines in `fuzzy_input.txt` which matched the `STRING_TO_MATCH`.

## Overview

There are two sets of methods:

* `fuzzy_search` and `fuzzy_match`
  * These just look for matches. They don't give you any meta information about the matches
* `fuzzy_search_with_highlights` and `fuzzy_match_with_highlights`
  * These look for matches and return the match in pieces showing what characters the fuzzy match
    matched against. Used to give visual context around how strings were matched.
