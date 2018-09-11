import json
import time
import xml.etree.ElementTree as ET
from operator import itemgetter
from typing import List

import challonge

def get_and_parse_custom_parameters() -> dict: 
    params = {}
    try:
        with open('matchparam.json') as p:
            raw_params = json.loads(p.read())
        params["ACPN"] = raw_params.get("AreCustomParametersNeeded", "false")
        if params["ACPN"].upper() not in ("TRUE", "FALSE"):
            params["ACPN"] = "false"
        try:
            params["MatchNo1"] = int(raw_params.get("MatchNo1", 0))
        except ValueError:
            params["MatchNo1"] = 0
        
        try:
            params["MatchNo2"] = int(raw_params.get("MatchNo2", 0))
        except ValueError:
            params["MatchNo2"] = 0
            
    except OSError:
        print("No matchparam.json wes found, or editing wasn't finished.")
        params["ACPN"] = "false"
    return params


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


def filter_completed_matches(matches: List[dict]) -> List[dict]:
    filtered_matches = [
        match for match in matches if match['state'] != 'completed'
    ]
    return filtered_matches


def sort_this(matches: List[dict]) -> List[dict]:
    def keyfunc(item):
        # `pending` is after `open` which is what we need in `state`.
        return abs(item['round']), item['state'], item['id']
    return list(sorted(matches, key=keyfunc))


def get_given_match(
    matches: List[dict],
    MatchNo: int,
) -> dict:
    for match_ in matches:
        if int(match_["suggested_play_order"]) == MatchNo:
            return match_
    return find_next_open_match(matches)


def find_next_open_match(
    matches: List[dict],
    skip_sugg_play_order_no=0,
) -> dict:
    for match_ in matches:
        if (
            match_['state'] == 'open' 
            and match_["suggested_play_order"] != skip_sugg_play_order_no
        ):
            return match_
    return None


def make_element_tree_element_with_player_info(
    tournament: dict,
    active_match: dict,
    next_match: dict,
) -> ET.Element:
    root = ET.Element("CurrentStatus")
    participants = challonge.participants.index(tournament["id"])
    ET.SubElement(root, "TournamentName", name=tournament["name"])
    active_match_elem = ET.SubElement(root, "ActiveMatch")
    if active_match:
        active_pl_1, active_pl_2 = get_active_players(
            match=active_match,
            participants=participants,
        )
    else:
        print("""No more open matches were found.""")
        active_pl_1 = "null"
        active_pl_2 = "null"
    ET.SubElement(active_match_elem, "Player1", name=active_pl_1)
    ET.SubElement(active_match_elem, "Player2", name=active_pl_2)
    next_match_elem = ET.SubElement(root, "NextMatch")
    if next_match:
        next_pl_1, next_pl_2 = get_active_players(
            match=next_match,
            participants=participants,
        )
    else:
        print("Next match was not found.")
        next_pl_1 = "null"
        next_pl_2 = "null"
    ET.SubElement(next_match_elem, "Player1", name=next_pl_1)
    ET.SubElement(next_match_elem, "Player2", name=next_pl_2)
    print("Active Match: " + active_pl_1 + " vs. " + active_pl_2)
    print("Next Match: " + next_pl_1 + " vs. " + next_pl_2)
    return root


def make_next_match_etree(
        tournament: dict,
) -> ET.ElementTree:
    root = ET.Element("CurrentStatus")
    print("Getting open matches.")
    matches = challonge.matches.index(tournament["id"])
    matches = sort_this(matches)
    matches = filter_completed_matches(matches)
    active_match = find_next_open_match(matches)
    next_match = find_next_open_match(matches, int(active_match["suggested_play_order"]))
    root = make_element_tree_element_with_player_info(
        tournament, 
        active_match, 
        next_match
    )
    tree = ET.ElementTree(root)
    return tree


def make_next_match_etree_with_custom_parameters(
        tournament: dict,
        parameters: dict,
) -> ET.ElementTree:
    print("Custom parameters file found with parameters:")
    print(parameters)
    if parameters["MatchNo1"] == 0 and parameters["MatchNo2"] == 0:
        tree = make_next_match_etree(tournament)
    else:
        matches = challonge.matches.index(tournament["id"])
        matches = sort_this(matches)
        if parameters["MatchNo1"] != 0:
            active_match = get_given_match(matches, parameters["MatchNo1"])
        else:
            active_match = find_next_open_match(matches, parameters["MatchNo2"])
        if parameters["MatchNo2"] != 0:
            next_match = get_given_match(matches, parameters["MatchNo2"])
        else:
            next_match = find_next_open_match(matches, parameters["MatchNo1"])
        
        root = make_element_tree_element_with_player_info(
            tournament, 
            active_match, 
            next_match
        )
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
   
    while True:
        params = get_and_parse_custom_parameters()
        if params["ACPN"].upper() == "TRUE":
            tree = make_next_match_etree_with_custom_parameters(tournament, params)
        else:
            tree = make_next_match_etree(tournament)
        print("Matches parsed. Writing to file.")
        tree.write("matches.xml")
        print("Done! Refreshing in 5 seconds.\n")
        time.sleep(5)


if __name__ == '__main__':
    main()
