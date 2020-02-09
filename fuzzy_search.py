#!/usr/bin/env python3
import sys

STRING_TO_MATCH = "module"

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

NO_HIGHLIGHT = 0
HIGHLIGHT = 1

def fuzzy_match_with_highlights(search_string, string_to_search, case_sensitive=False):
    if len(search_string) == 0:
        return [(NO_HIGHLIGHT, string_to_search)]
    if len(string_to_search) == 0:
        return []


    def matches(left, right, case_sensitive):
        if case_sensitive:
            return left == right
        else:
            return left.lower() == right.lower()

    def close_group_if_needed(ret, current_highlight, expected_highlight, current_group):
        if current_highlight != expected_highlight:
            ret.append((current_highlight, ''.join(current_group)))
            return [], expected_highlight
        return current_group, expected_highlight

    ret = []
    current_highlight = None
    current_group = []
    search_index = 0

    # Minor optimization to prevent checking len(current_group) != 0 each loop
    search_char = search_string[search_index]
    searchee_char = string_to_search[0]
    current_group.append(searchee_char)
    if matches(search_char, searchee_char, case_sensitive):
        current_highlight = HIGHLIGHT
        search_index = 1
    else:
        current_highlight = NO_HIGHLIGHT

    searchee_index = 1
    while searchee_index < len(string_to_search) and search_index < len(search_string):
        if search_index == len(search_string):
            # We've matched every search character so we can stop
            break

        search_char = search_string[search_index]
        searchee_char = string_to_search[searchee_index]

        if matches(search_char, searchee_char, case_sensitive):
            search_index += 1
            searchee_index += 1
            current_group, current_highlight = close_group_if_needed(ret, current_highlight, HIGHLIGHT, current_group)
            current_group.append(searchee_char)
            continue

        current_group, current_highlight = close_group_if_needed(ret, current_highlight, NO_HIGHLIGHT, current_group)
        current_group.append(searchee_char)
        searchee_index += 1

    if searchee_index != len(string_to_search):
        current_group, current_highlight = close_group_if_needed(ret, current_highlight, NO_HIGHLIGHT, current_group)
        current_group += string_to_search[searchee_index:]

    if len(current_group) != 0:
        ret.append((current_highlight, ''.join(current_group)))

    if search_index != len(search_string):
        # Some of the search characters were unmatched. We consider this a failed match.
        return []
    return ret

assert fuzzy_match_with_highlights("", "") == [(0, "")]
assert fuzzy_match_with_highlights("abc", "") == []
assert fuzzy_match_with_highlights("birth", "happy birthday") == [(0, "happy "), (1, "birth"), (0, "day")]
assert fuzzy_match_with_highlights("day", "happy birthday") == [(0, "happy birth"), (1, "day")]
assert fuzzy_match_with_highlights("happy", "happy birthday") == [(1, "happy"), (0, " birthday")]
assert fuzzy_match_with_highlights("abc", "a big cat") == [(1, "a"), (0, " "), (1, "b"), (0, "ig "), (1, "c"), (0, "at")]
assert fuzzy_match_with_highlights("abc", "aching big cat") == [(1, "a"), (0, "ching "), (1, "b"), (0, "ig "), (1, "c"), (0, "at")]

def fuzzy_search_with_highlights(search_string, data):
    matches = []
    for string in data:
        ret = fuzzy_match_with_highlights(search_string, string, case_sensitive=True)
        if len(ret) != 0:
            matches.append(ret)

    return matches

# matches = fuzzy_search_with_highlights(STRING_TO_MATCH, lines)
# matches.sort(key=lambda x: len(x))
# for matched in matches:
#     for part in matched:
#         if part[0] == NO_HIGHLIGHT:
#             sys.stdout.write(part[1])
#         else:
#             sys.stdout.write(f"\033[92m{part[1]}\033[0m")
#     sys.stdout.write("\n")
