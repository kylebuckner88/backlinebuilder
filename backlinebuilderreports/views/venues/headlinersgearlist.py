from django.shortcuts import render
from django.db import connection
from django.views import View
from backlinebuilderreports.views.helpers import dict_fetch_all

class HeadlinersGearList(View):
    def get(self, request):
        with connection.cursor() as db_cursor:
            
            db_cursor.execute("""
                SELECT
                    venue.name as venue_name
                    venue.id venue_id,
                    gear.*
                FROM backlinebuilderapi_gear gear
                JOIN venue
                ON venue.id = gear.gear_id
            """)
            
            dataset = dict_fetch_all(db_cursor)
            
            [
                {
                    "id": 2,
                    "venue_name": "Headliners Music Hall",
                    "gear_list": [
                        {
                            "id": 1,
                            "type": "guitar amp",
                            "name": "AC15",
                            "maker": "Vox"
                        },
                        {
                            "id": 3,
                            "type": "keyboard amp",
                            "name": "KC200",
                            "maker": "Roland"
                        },
                        {
                            "id": 4,
                            "type": "bass amp",
                            "name": "SVT",
                            "maker": "Ampeg"
                        },
                        {
                            "id": 5,
                            "type": "microphone",
                            "name": "SM57",
                            "maker": "Shure"
                        },
                        {
                            "id": 7,
                            "type": "condenser microphone(pair)",
                            "name": "KSM137",
                            "maker": "Shure"
                        },
                        {
                            "id": 8,
                            "type": "drum kit",
                            "name": "Catalina Club",
                            "maker": "Gretsch"
                        },
                        {
                            "id": 10,
                            "type": "DI",
                            "name": "ProDI",
                            "maker": "Radial"
                        },
                        {
                            "id": 13,
                            "type": "guitar",
                            "name": "Acoustasonic",
                            "maker": "Fender"
                        }
                    ]
                },
            ]
            
            headliners_gear_list = []
            
            for row in dataset:
                
                gear = {
                    "type": row['type'],
                    "name": row['name'],
                    "maker": row['maker']
                }
                
                headliners_dict = next(
                    (
                        headliners_gear for headliners_gear in headliners_gear_list
                        if headliners_gear['venue_id'] == row['venue_id']
                    ),
                    None
                )
                
                if headliners_dict:
                    headliners_dict['gear_list'].append(gear)
                else:
                    headliners_gear_list.append({
                        "venue_id": row['venue_id'],
                        "venue_name": row['venue_name'],
                        "gear_list": [gear]
                    })
                    
        template = 'venues/list_with_gear_list.html'

        context = {
            "headlinersgear_list": headliners_gear_list
         }
        
        return render(request, template, context)