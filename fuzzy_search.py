#!/usr/bin/env python3

import sys

with open("fuzzy_input.txt") as f:
    lines = [line.strip() for line in f.readlines()]

def fuzzy_match(search_string, string_to_search):
    search_index = 0
    searchee_index = 0
    while searchee_index < len(string_to_search) and search_index < len(search_string):
        ch = search_string[search_index].lower()
        if ch == string_to_search[searchee_index].lower():
            search_index += 1
            searchee_index += 1
            continue
        searchee_index += 1

    return search_index == len(search_string)

def fuzzy_search(search_string, data):
    matches = []
    for string in data:
        if fuzzy_match(search_string, string):
            matches.append(string)

    return matches

# for matched in fuzzy_search("hello", lines):
#     print(matched)


NO_HIGHLIGHT = 0
HIGHLIGHT = 1

def fuzzy_match_with_highlights(search_string, string_to_search):
    ret = []
    current_highlight = None
    current_group = []
    search_index = 0
    searchee_index = 0
    while searchee_index < len(string_to_search) and search_index < len(search_string):
        search_char = search_string[search_index]
        searchee_char = string_to_search[searchee_index]
        # print(f"Searching for {search_char}")
        # print(f"Current char {searchee_char}")
        if search_char.lower() == searchee_char.lower():
            search_index += 1
            searchee_index += 1
            # print(f"Matched {search_char} == {searchee_char}")
            if current_highlight != HIGHLIGHT:
                # print(f"current_highlight is not HIGHLIGHT, it is {current_highlight}")
                if len(current_group) != 0:
                    # print(f"Storing existing: {current_group}")
                    ret.append((current_highlight, ''.join(current_group)))
                    # print(ret)
                    current_group = []
                current_highlight = HIGHLIGHT
            current_group.append(searchee_char)
            continue
        if current_highlight != NO_HIGHLIGHT:
            if len(current_group) != 0:
                ret.append((current_highlight, ''.join(current_group)))
                current_group = []
            current_highlight = NO_HIGHLIGHT
        current_group.append(searchee_char)
        searchee_index += 1

    if searchee_index != len(string_to_search):
        if current_highlight != NO_HIGHLIGHT and len(current_group) != 0:
            ret.append((current_highlight, ''.join(current_group)))
            current_group = []
            current_highlight = NO_HIGHLIGHT
        current_group += string_to_search[searchee_index:]

    if len(current_group) != 0:
        ret.append((current_highlight, ''.join(current_group)))

    if search_index == len(search_string):
        return ret
    return []

def fuzzy_search_with_highlights(search_string, data):
    matches = []
    for string in data:
        ret = fuzzy_match_with_highlights(search_string, string)
        if len(ret) != 0:
            matches.append(ret)

    return matches

for matched in fuzzy_search_with_highlights("module", lines):
    # \033[4mhello\033[0m
    for part in matched:
        if part[0] == NO_HIGHLIGHT:
            sys.stdout.write(part[1])
        else:
            sys.stdout.write(f"\033[92m{part[1]}\033[0m")
    print("")
