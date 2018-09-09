import json
import time
import xml.etree.ElementTree as ET
from operator import itemgetter
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


def make_next_match_etree(
        matches: List[dict],
        participants: List[dict],
        tournament: dict,
) -> ET.ElementTree:
    root = ET.Element("CurrentStatus")
    print("Getting open matches.")
    active_match, next_match = get_two_open_matches(matches)
    ET.SubElement(root, "TournamentName", name=tournament["name"])
    active_match_elem = ET.SubElement(root, "ActiveMatch")
    active_pl_1, active_pl_2 = get_active_players(
        match=active_match,
        participants=participants,
    )
    ET.SubElement(active_match_elem, "Player1", name=active_pl_1)
    ET.SubElement(active_match_elem, "Player2", name=active_pl_2)
    next_match_elem = ET.SubElement(root, "NextMatch")
    next_pl_1, next_pl_2 = get_active_players(
        match=next_match,
        participants=participants,
    )
    ET.SubElement(next_match_elem, "Player1", name=next_pl_1)
    ET.SubElement(next_match_elem, "Player2", name=next_pl_2)
    tree = ET.ElementTree(root)
    return tree


def main():
    with open('creds.json') as f:
        creds = json.loads(f.read())
    challonge.set_credentials(creds['username'], creds['APIKey'])
    tournament_name = creds['tournamentName']
    tournament = challonge.tournaments.show(tournament_name)

    print("Awaiting tournament...")
    while tournament["started_at"] == None:
        tournament = challonge.tournaments.show(tournament_name)
        time.sleep(2)
        continue
    print("Tournament found!")

    participants = challonge.participants.index(tournament["id"])
    matches = challonge.matches.index(tournament["id"])
    while True:
        tree = make_next_match_etree(matches, participants, tournament)
        print("Matches parsed. Writing to file.")
        tree.write("matches.xml")
        print("Done!")
        time.sleep(5)


if __name__ == '__main__':
    main()
