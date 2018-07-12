import urllib.request
import requests
from bs4 import BeautifulSoup
import sys, json
import io
import openpyxl
from openpyxl import load_workbook

#headers for html response
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
url = 'https://sports.bovada.lv/football'

#load response
response = requests.get(url, headers=headers)

#obtain content from html response and make a string
content = response.content
content = str(response.content)

#create a beautiful soup object to simplify parsing
soup = BeautifulSoup(response.content, 'html5lib')

#find all objects with script tag
soup_scripts = soup.body.find_all('script', attrs={'type':'text/javascript'})
#it's the last script on the page, make a string
odds_str = str(soup_scripts[-1])
#find beginning of json object
json_start = odds_str.find('{"items"')
#cut string to only json object
odds_str = odds_str[json_start-1:-11]+',"value"]}'

print(len(odds_str))

odds_js = json.loads(odds_str)
##print pretty json object
#print(json.dumps(odds_js, indent=4))

#list of odds are associated with a dictionary key 'items'
odds_lists = odds_js['items']

#NFL odds is the first list
nfl_odds = odds_lists[0]

#check if the index pulled the right dictionary
assert nfl_odds['description'] == 'NFL'
assert nfl_odds['type'] =='LEAGUE'

#dictioary value is stored in under key 'itemList'
nfl_odds = nfl_odds['itemList']

nfl_games, competitors, game_items, outcomes = list(), list(), list(), list()

for li in nfl_odds['items']:
	nfl_games.append(li)


for di in nfl_games:
	for k,v in di.items():
		if k == 'competitors':
			competitors.append(v)
		if k == 'displayGroups':
			spreadDict = v[0]
			for j, u in spreadDict.items():
				if j == 'itemList':
					game_items.append(u)


#print('nfl matchups')
#print(nfl_games)

#print('competitors')
#print(competitors)

for i in range(len(game_items)):
	for j in range(len(game_items[0])):
		for k,v in game_items[i][j].items():
			if k == 'outcomes':
				outcomes.append(v)

#print('outcomes')
#print(outcomes)

team_price = [[] for i in range(len(outcomes))]

for i in range(len(outcomes)):
	for j in range(len(outcomes[i])):
		for k, v in outcomes[i][j].items():
			if k == 'description':
				team_price[i].append(v)
			if k == 'price':
				price = v
				team_price[i].append(price['handicap'])
				team_price[i].append(price['american'])

#print('team prices')
#print(team_price)

team_spreads, over_under = list(), list()

for li in range(len(team_price)):
	if li % 2 == 0:
		team_spreads.append(team_price[li])
	else:
		over_under.append(team_price[li])

full_game_odds = list(zip(team_spreads, over_under))

print(full_game_odds)

lines_wb = load_workbook()
lines_ws = lines_wb['test']

row = 2

for game in full_game_odds:
	lines_ws['B'+str(row)] = game[0][0]
	lines_ws['C'+str(row)] = game[0][1]
	lines_ws['D'+str(row)] = game[0][2]
	#find money line
	lines_ws['F'+str(row)] = game[1][1]
	lines_ws['G'+str(row)] = game[1][2]
	row += 1
	lines_ws['B'+str(row)] = game[0][3]
	lines_ws['C'+str(row)] = game[0][4]
	lines_ws['D'+str(row)] = game[0][5]
	#find money line
	lines_ws['F'+str(row)] = game[1][4]
	lines_ws['G'+str(row)] = game[1][5]
	row += 2

lines_wb.save()