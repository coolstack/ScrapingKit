# -*- coding: utf-8 -*-
import requests
import json

def get_scoreboard(league, date): #for nba
    #get response from website
    response = requests.get("https://www.espn.com/"+league+"/scoreboard/_/date/"+date+"?xhr=1")#&fbclid=IwAR1uCJkpZuV2iLL68Dswn53xFcAlUajq0uv7ysTBj40CxwStweDZ2Eaonwg
    data = response.json()
    
    #start parsing
    events = data['content']['sbData']['events']  
    result = []
    for event in events:
        gameid = event['id']
        status = event['status']['type']['description']
        competitions = event['competitions']
        for competition in competitions: #single loops, rarely multiple
            competitors = competition['competitors']
            for Team in competitors: #2 loops
                if Team["homeAway"] == "home":
                    score_home = []
                    if status == "Final":
                        for i in Team['linescores']: #4 loops
                            score_home.append(i['value'])
                        T_home = Team['score']
                    
                    nickname_home = Team['team']['shortDisplayName']
                    teamid_home = Team['team']['abbreviation']
                    
                    record_home = Team['records']
                    detail_home = record_home[0]['summary'] + ", "+ record_home[1]['summary'] + " Home"
            
                    
                if Team["homeAway"] == "away":
                    score_away = []
                    if status == "Final":
                        for i in Team['linescores']:
                            score_away.append(i['value'])
                        T_away = Team['score']
                    
                    nickname_away = Team['team']['shortDisplayName']
                    teamid_away = Team['team']['abbreviation']
                    
                    record_away = Team['records']
                    detail_away = record_away[0]['summary'] + ", "+ record_away[2]['summary'] + " Away"
        
        if status == "Final":
            event_result = {
                'status' : status,
        		'awayTeam' : { 'nickname' : nickname_away, 'teamid' : teamid_away, 'score' : score_away, 'T' : T_away, 'detail' : detail_away },
        		'homeTeam' : { 'nickname' : nickname_home, 'teamid' : teamid_home, 'score' : score_home, 'T' : T_home, 'detail' : detail_home },
        		'gameid' : gameid
        	}
        else:
            event_result = {
                'status' : status,
        		'awayTeam' : { 'nickname' : nickname_away, 'teamid' : teamid_away},
        		'homeTeam' : { 'nickname' : nickname_home, 'teamid' : teamid_home},
        		'gameid' : gameid
        	}
        
        result.append(event_result)
    return result



try:
    result = get_scoreboard('nba', '20210117')
    print(result)
except:
     print("No Data found!!!")









