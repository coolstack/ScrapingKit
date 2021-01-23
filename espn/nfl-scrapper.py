# -*- coding: utf-8 -*-
import requests
import json


def get_scoreboard(league, year, seasontype, week): ## year,season type, week id
    URL = "https://www.espn.com/"+league+"/scoreboard/_/year/"+year+"/seasontype/"+seasontype +"/week/"+week+"?xhr=1"
    
    #get response from website
    response = requests.get(URL)
    data = response.json()
    
    #start parsing
    events = data['content']['sbData']['events']  
    result = []
    prevdate = ''
    date =[]
    events_of_the_day=[]
    redultOfaDay = {}
    for i in range(len(events)+1):
        if i==len(events):
            result.append(redultOfaDay)
            break
        date.append(events[i]['date'][:10].replace('-', ''))
        if len(date)>1:
            if date[-1] != date[-2]:#if date changes      
                result.append(redultOfaDay)
                events_of_the_day=[]#clear memory
                
        gameid = events[i]['id']
        status = events[i]['status']['type']['description']
        competitions = events[i]['competitions']
        for competition in competitions: #single loops, rarely multiple
            competitors = competition['competitors']
            for Team in competitors: #2 loops
                if Team["homeAway"] == "home":
                    score_home = []
                    if status == "Final":
                        for i in Team['linescores']: #4 loops
                            score_home.append(i['value'])
                        T_home = Team['score']
                        record_home = Team['records']
                        detail_home = record_home[0]['summary'] + ", "+ record_home[1]['summary'] + " Home"
                    
                    nickname_home = Team['team']['shortDisplayName']
                    teamid_home = Team['team']['abbreviation']
                    
                if Team["homeAway"] == "away":
                    score_away = []
                    if status == "Final":
                        for i in Team['linescores']:
                            score_away.append(i['value'])
                        T_away = Team['score']
                        record_away = Team['records']
                        detail_away = record_away[0]['summary'] + ", "+ record_away[2]['summary'] + " Away"
                    
                    nickname_away = Team['team']['shortDisplayName']
                    teamid_away = Team['team']['abbreviation']
                                            
        if status == "Final":
            single_event_result = {
                'status' : status,
        		'awayTeam' : { 'nickname' : nickname_away, 'teamid' : teamid_away, 'score' : score_away, 'T' : T_away, 'detail' : detail_away },
        		'homeTeam' : { 'nickname' : nickname_home, 'teamid' : teamid_home, 'score' : score_home, 'T' : T_home, 'detail' : detail_home },
        		'gameid' : gameid
        	}
        else:
            single_event_result = {
                'status' : status,
        		'awayTeam' : { 'nickname' : nickname_away, 'teamid' : teamid_away},
        		'homeTeam' : { 'nickname' : nickname_home, 'teamid' : teamid_home},
        		'gameid' : gameid
        	}
        
        events_of_the_day.append(single_event_result)
        redultOfaDay = {
                    'date':date[-1],
                    'event' : events_of_the_day
                    }
    return result



try:
    result = get_scoreboard('nfl','2020','1', '3')
    print(result)
except:
      print("No Data found!!!")




