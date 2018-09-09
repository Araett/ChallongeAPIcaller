from operator import itemgetter
import time
import sys
import xml.etree.ElementTree as ET
from typing import List

import challonge


def get_max_rounds(matches: List[dict]) -> int:
    rounds = map(itemgetter('round'), matches)
    return max(map(abs, rounds))


def get_active_players(match: dict, participants: List[dict]) -> [str, str]:
    participant_id_to_name_map = {
        part['id']: part['name']
        for part
        in participants
    }
    return [
        participant_id_to_name_map[match["player1_id"]],
        participant_id_to_name_map[match["player2_id"]],
    ]


def get_two_open_matches(matches: List[dict]) -> [dict, dict]:
    max_rounds = get_max_rounds(matches)
    for round_ in range(1, max_rounds):
        for match in matches:
            if abs(match["round"]) != round_:
                continue 
            if match["state"] != "open":
                continue
            for next_match in matches:
                if next_match is match:
                    continue
                if next_match["state"] != "open":
                    continue
                if abs(next_match["round"]) != round_:
                    continue 
                return [match, next_match]


def sort_this(matches):
    def keyfunc(item):
        # `pending` is after `open` which is what we need in `state`.
        return abs(item['round']), item['state'], item['id']
    return list(sorted(matches, key=keyfunc))


# def get_next_match(currentActive, matches):
#     curmatch = matches[int(currentActive) - 1]
#     for match in matches:
#         if match["state"] != "open":
#             continue
#         elif match is curmatch:
#             continue
#         return [curmatch, match]


def main():
    with open('cred.txt') as f:
        creds = f.readlines()
    account_name, apiKey, url = (cred.replace('\n', '') for cred in creds)
    challonge.set_credentials(account_name, apiKey)


    tournament = challonge.tournaments.show(url)
    playedMatches = 0

    print("Awaiting tournament...")
    while tournament["started_at"] == None:
        tournament = challonge.tournaments.show(sys.argv[1])
        time.sleep(2)
        continue
    print("Tournament found!")
    participants = challonge.participants.index(tournament["id"])
    matches = challonge.matches.index(tournament["id"])

    root = ET.Element("CurrentStatus")
    while True:
        print("Getting open matches.")
        openMatches = get_two_open_matches(matches)
        ET.SubElement(root, "TournamentName", name=tournament["name"])
        print(get_max_rounds(matches))
        activeM = ET.SubElement(root, "ActiveMatch")
        activeMatch = get_active_players(openMatches[0], participants)
        ET.SubElement(activeM, "Player1", name=activeMatch[0])
        ET.SubElement(activeM, "Player2", name=activeMatch[1])

        nextM = ET.SubElement(root, "NextMatch")
        nextMatch = get_active_players(openMatches[1], participants)
        ET.SubElement(nextM, "Player1", name=nextMatch[0])
        ET.SubElement(nextM, "Player2", name=nextMatch[1])

        print("Matches parsed. Writing to file.")
        tree = ET.ElementTree(root)
        tree.write("matches.xml")
        print("Done!")
        time.sleep(5)


if __name__ == '__main__':
    main()
