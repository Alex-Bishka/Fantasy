import requests
import csv
from datetime import date

def generateADPFromAPI():
    """
    Obtains ADP rankings from an API
    We are currently using Fantasy Football Calculator's free api - note this is missing key players

    For more info:
    https://help.fantasyfootballcalculator.com/article/42-adp-rest-api
    """
    NUM_TEAMS = 12
    LEAGUE_TYPE = "standard"
    year = date.today().year


    url = f"https://fantasyfootballcalculator.com/api/v1/adp/{LEAGUE_TYPE}?teams={NUM_TEAMS}&year={year}"
    r = requests.get(url)
    
    status = r.status_code
    if status == 200:
        print("\nSuccesfully grabbed ADP values ")
        adp_rankings = r.json()
        return adp_rankings
    else:
        raise Exception(f"\nError occured, status {status} - could not obtain ADP values.")

def parseADPRankings(rankings):
    """
    Given the adp rankings of all players, this function separates them
    by position and returns a sorted list (by adp) of each position

    Note that all info needed should be present for creating a cheat sheet

    Note that the rankings are provided in order from Fantasy Football 
    Calculator's api, so no sorting is required on our end
    """
    if type(rankings) == dict:
        qb_list = []
        rb_list = []
        wr_list = []
        te_list = []
        pk_list = []
        def_list = []
        for player in rankings["players"]:
            pos = player["position"]
            roundNum = (player["adp"] // 12) + 1
            # a list for writing to csv
            data = [roundNum, player["adp"], player["name"], player["team"], player["position"], player["high"], player["low"]]
            if pos == "QB":
                qb_list.append(data)
            if pos == "RB":
                rb_list.append(data)
            if pos == "WR":
                wr_list.append(data)
            if pos == "TE":
                te_list.append(data)
            if pos == "PK":
                pk_list.append(data)
            if pos == "DEF":
                def_list.append(data)

        return qb_list, rb_list, wr_list, te_list, pk_list, def_list
    else:
        raise Exception(f'\nInvalid rankings passed in. The following was passed in: \n{rankings} ')

def createCSV(position_list):
    """
    Takes in a position list with the players' info and creates a csv file 
    """
    position = position_list[0][4]
    filename = f'./CSVRankings/{position}_Ranking.csv'
    header = ["Round", "ADP", "Name", "Team", "Pos", "Highest Draft Pos", "Lowest Draft Pos"]
    with open(filename, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)

        # write the header
        writer.writerow(header)

        # write the data
        writer.writerows(position_list)

    print(f'\nFinshed writing to {filename}\n')

if True:
    adp_rankings = generateADPFromAPI()
    position_lists = parseADPRankings(adp_rankings)

    for position_list in position_lists:
        createCSV(position_list)
