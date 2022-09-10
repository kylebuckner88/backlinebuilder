"""Module for generating games by user report"""
from django.shortcuts import render
from django.db import connection
from django.views import View
from backlinebuilderapi.models import Event

from backlinebuilderreports.views.helpers import dict_fetch_all


class UserEventList(View):
    def get(self, request):
        with connection.cursor() as db_cursor:

            db_cursor.execute("""
                SELECT
                    e.id,
                    e.artist_id
                    e.venue_id,
                    e.notes,
                    e.date,
                    e.time,
                    a.name AS artist_name
                    v.name AS venue_name
                FROM 
                    backlinebuilderapi_event e
                JOIN
                    backlinebuilderapi_artist a ON a.user_id = a.artist_id
                JOIN 
                    auth_user u ON a.user_id = u.id
            """)
            # Pass the db_cursor to the dict_fetch_all function to turn the fetch_all() response into a dictionary
            dataset = dict_fetch_all(db_cursor)

            [
              {
                "id": 1,
                "artist_name": "Mountain Movers",
                "events": [
                  {
                    "id": 1,
                    "venue_id": "1",
                    "notes": "WOW",
                    "date": "2022-10-25",
                    "time": "07:00",
                  },
                  {
                    "id": 2,
                    "venue_id": "2",
                    "notes": "bring extra cymbals",
                    "date": "2022-10-27",
                    "time": "07:30"
                  },
                  {
                    "id": 3,
                    "venue_id": "3",
                    "notes": "gear storage in back",
                    "date": "2022-10-28",
                    "time": "08:00"
                  }
                ]
              },
            ]
            
            events_by_user = []

            for row in dataset:
            
                event = Event()
                event.artist_name = event.artist.name
                event.venue_name = event.venue.name 
                event.notes = row["notes"]    
                event.date = row["date"]
                event.time = row["time"]
                
                # This is using a generator comprehension to find the user_dict in the games_by_user list
                # The next function grabs the dictionary at the beginning of the generator, if the generator is empty it returns None
                # This code is equivalent to:
                # user_dict = None
                # for user_game in games_by_user:
                #     if user_game['gamer_id'] == row['gamer_id']:
                #         user_dict = user_game
                
                user_dict = next(
                    (
                        user_game for user_game in events_by_user
                        if user_event['gamer_id'] == row['gamer_id']
                    ),
                    None
                )
                
                if user_dict:
                    # If the user_dict is already in the games_by_user list, append the game to the games list
                    user_dict['games'].append(game)
                else:
                    # If the user is not on the games_by_user list, create and add the user to the list
                    games_by_user.append({
                        "gamer_id": row['gamer_id'],
                        "full_name": row['full_name'],
                        "games": [game]
                    })
        
        # The template string must match the file name of the html template
        template = 'users/list_with_games.html'
        
        # The context will be a dictionary that the template can access to show data
        context = {
            "usergame_list": games_by_user
        }

        return render(request, template, context)
