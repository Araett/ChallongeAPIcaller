#Challonge API caller and parser v0.2
#Made by Martynas Saulius
#martynas575@gmail.com00

import challonge
import time
import xml.etree.ElementTree as ET
import sys

def GetMaxRounds(matches):
    rounds = 0
    for match in matches:
        if rounds < abs(match["round"]):
            rounds = abs(match["round"])
    return rounds

def GetActivePlayers(match, participants):
    player1 = "None"
    player2 = "None"
    for part in participants:
        if match["player1_id"] == part["id"]:
            player1 = part["name"]
            continue
        if match["player2_id"] == part["id"]:
            player2 = part["name"]
            continue
    return [player1, player2]

def GetTwoOpenMatches(matches):
    maxRounds = GetMaxRounds(matches)
    for r in range(1, maxRounds):
        for match in matches:
            if abs(match["round"]) != r:
                continue 
            if match["state"] != "open":
                continue
            for nextmatch in matches:
                if nextmatch is match:
                    continue
                if nextmatch["state"] != "open":
                    continue
                if abs(nextmatch["round"]) != r:
                    continue 
                return [match, nextmatch] 

def GetNextMatch(currentActive, match):
    curmatch = match[int(currentActive) - 1]
    for match in matches:
        if match["state"] != "open":
            continue
        elif match is curmatch:
            continue
        return [curmatch, match] 

credentialsFile = open("cred.txt", "r")

accountName = credentialsFile.readline()
accountName = accountName.replace('\n', '')

apiKey = credentialsFile.readline()
apiKey = apiKey.replace('\n', '')

url = credentialsFile.readline()
url = url.replace('\n', '')

credentialsFile.close()

challonge.set_credentials(accountName, apiKey)

root = ET.Element("CurrentStatus")

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

while True:
    print("Getting open matches.")
    openMatches = GetTwoOpenMatches(matches)
    ET.SubElement(root, "TournamentName", name=tournament["name"])
    print(GetMaxRounds(matches))
    activeM = ET.SubElement(root, "ActiveMatch")
    activeMatch = GetActivePlayers(openMatches[0], participants)
    ET.SubElement(activeM, "Player1", name=activeMatch[0])
    ET.SubElement(activeM, "Player2", name=activeMatch[1])

    nextM = ET.SubElement(root, "Next Match")
    nextMatch = GetActivePlayers(openMatches[1], participants)
    ET.SubElement(nextM, "Player1", name=nextMatch[0])
    ET.SubElement(nextM, "Player2", name=nextMatch[1])

    print("Matches parsed. Writing to file.")
    tree = ET.ElementTree(root)
    tree.write("matches.xml")
    print("Done!")
    time.sleep(5)