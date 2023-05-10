# Discord_Elo_Bot
A discord bot implementing a Glicko / Elo rating system based on the python implementation of the Glicko2 system by Ryan Kirkman.

## Before running
1. Edit the ".env" file:
- Insert folder location
- Insert discord bot ID
- Insert discord channel ID

2. Edit the ".auth" file:
- Add your discord ID in the list after "member"->"5"
- Add further discord user/channel/role IDs to give certain users access to more commands, see below (highest permission applies)

Then run "Discord_Leaderboards.py"

## How to use
- Players can sign up in channels listed at least in ".auth"->"channel"->"1" using the "!add PlayerName" command
- Players can report scores using the "!report PlayerA ScoreA ScoreB PlayerB" command
- Players can see the current leaderboards using the "!ranking" command or a predicted leaderboard for the next rating period using the "!live" command (players with too few games in total or to few recent games are suppressed)
- Admins can end a rating period using the "!commit" command

## Commands
1. Unrestricted Commands
- "!ranking": show the current official rating
- "!live": show the prediction for the ranking of the next rating period
- "!pending": show the results of matches in the current rating period

2. Verified or above
- "!add PlayerName": Add a new player with name PlayerName
- "!submit PlayerA ScoreA ScoreB PlayerB": Report the outcome of a match between PlayerA and PlayerB with final score ScoreA : ScoreB.
- "!delete PlayerA ScoreA ScoreB PlayerB": Delete a result. Only works if the result is pending and was submitted by the same person.

3. Moderator or above
- "!ranking_details": show complete leaderboards without suppressed ratings
- "!live_details": show complete predicted leaderboards without suppressed ratings

4. Admin or above
- "!commit": end the current rating period and start the next one, resolving all pending results
- "!clear_results": Delete all pending results in the current rating period
- "!save": Save the current situation immediately

