import random, csv, copy, codecs

# list of songs
songlist = set([])
# number of songs each member should be in
playerLim = dict()
# the members and their list of ordered preferences
P = {}
#number of players
playerNum = 0
# the songs and their list of ordered preferences
S = {}

Sconflict = {}

Sopen = {}

# read the players' song preferences and number of songs they can be in
with open('preferences.csv') as preffile:
	prefreader = csv.reader(preffile)
	for row in prefreader:
		if row[0] != "":
			player = row[0].strip()
			playerNum += 1
			# associate player name and song number limit
			playerLim[player] = int(row[1])
			# associate player name and song preference ordering
			P[player] = row[2:]
			P[player] = list(filter(None,P[player]))
			# make sure all songs have been added to song list
			for i in range(2,len(row)):
				songlist |= set([row[i].strip()])

with open('songleaderpref.csv') as songfile:
	songreader = csv.reader(songfile)
	for row in songreader:
		song = row[0].strip()
		if song != "":
			S[song] = {}
			titlePart = song.split(" ")
			if len(titlePart)>1:
				broadSong = titlePart[0]
				if broadSong not in Sconflict.keys():
					Sconflict[broadSong]=[song]
				else:
					Sconflict[broadSong].append(song)
			else:
				Sconflict[song] = [song]
			Sopen[song] = int(row[1])
			S[song] = row[2:]

songlist = set(filter(None,songlist))
songMatchs = {s:[] for s in songlist}

playerSongNum = {player : 0 for player in P.keys()}
freeP 	= []
checkP  =copy.deepcopy(P)

def insertSort(song, player):
	for other in songMatchs[song]:
		if S[song].index(player) < S[song].index(other):
			songMatchs[song].insert(songMatchs[song].index(other),player)
			return
	songMatchs[song].append(player)

# check if song is filled or not
def filled():
	for song in songlist:
		if len(songMatchs[song]) != Sopen[song]:
			return False
	return True

# check how many players have enough songs

def playersSatisfied():
	result = 0
	for player in playerSongNum:
		if playerSongNum[player] >= playerLim[player]:
			result+=1
		else:
			print("***"+player+" needs "+str(playerLim[player] - playerSongNum[player])+"song(s)\n")
	return result

def isConflict(player, song):
	if player in songMatchs[song]:
		return True
	broadSong = song.split(" ")[0]
	for conflict in Sconflict[broadSong]:
		if player in songMatchs[conflict]:
			return True
	return False

def matching(player):
	'''Find the free song available to a player '''
	# print("Matching %s"%(player))

	P[player] = list(checkP[player])
	'''If player not have song again, remove from free player '''
	if(len(P[player])==0):
		freeP.remove(player)
		# print('- player %s not have song to check again '%(player))
					
	else:
		for song in P[player]:
			#Check whether song is full or not
			if len(songMatchs[song]) < Sopen[song]:
				if player not in S[song] or isConflict(player, song) or playerSongNum[player] >= playerLim[player]:
					# print('- player %s not exist in list player in song %s '%(player,song))
					checkP[player].remove(song)
				else:	
					insertSort(song,player)
					playerSongNum[player] += 1
					if playerSongNum[player] >= playerLim[player]:
						freeP.remove(player)
					# print('- %s is no longer a free player and is now tentatively get song %s'%(player, song))
					break
			else:
				# print('- %s is full (%s participant) '%(song,Sopen[song]))

				if player not in S[song] or isConflict(player, song) or playerSongNum[player] >= playerLim[player]:
					# print('- player %s not exist in list player in song %s '%(player,song))
					checkP[player].remove(song)
				else :
					# get player who can remove, 
					playerRemove = player
					for playerMatch in songMatchs[song]:
						if S[song].index(playerRemove) < S[song].index(playerMatch): 
							playerRemove = playerMatch

					if playerRemove==player:
						# print('- Rank player %s in song %s is bigger then other current player match '%(player,song))
						checkP[player].remove(song)
					else:
						# print('- %s is better than %s'%(player, playerRemove))
						# print('- Making %s free again.. and tentatively match %s and %s'%(playerRemove, player, song))

						#The new player have match 
						insertSort(song,player)
						playerSongNum[player] += 1
						if playerSongNum[player] >= playerLim[player]:
							freeP.remove(player)

						#The old player is now not match anymore
						playerSongNum[playerRemove] -= 1
						if playerSongNum[playerRemove] < playerLim[playerRemove]:
							freeP.append(playerRemove)
							checkP[playerRemove] = P[playerRemove]
						songMatchs[song].remove(playerRemove)
						for formerConflict in Sconflict[song.split(" ")[0]]:
							if formerConflict != song:
								checkP[playerRemove].append(formerConflict)
						break

# init all applicant free and not have program
for player in P.keys():
	freeP.append(player)

# init programMatch
for song in S.keys():
	songMatchs[song]=[]

# Matching algorithm until stable match terminates
while playersSatisfied() < playerNum:

	print("================================\n")
	while (len(freeP) > 0):
		for player in freeP:
			matching(player)
	# init all applicant free and not have program
	for player in P.keys():
		freeP.append(player)
	for song in sorted(songMatchs.keys()):
		print(song+":"+str(songMatchs[song])+" "+str(len(songMatchs[song]))+"/"+str(Sopen[song])+"\n")
