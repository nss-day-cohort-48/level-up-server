import sqlite3
from django.shortcuts import render
from levelupapi.models import Game
from levelupreports.views import Connection
from datetime import datetime

def events_by_user(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute(
                """
                select g.id as user_id,
                u.first_name || " " || u.last_name as full_name,
                e.id,
                e.date,
                e.time,
                gm.name
                from levelupapi_event e
                join levelupapi_eventgamer eg
                on e.id = eg.event_id
                join levelupapi_gamer g
                on g.id = eg.gamer_id
                join auth_user u
                on u.id = g.user_id
                join levelupapi_game gm
                on e.game_id = gm.id
                """
            )

            dataset = db_cursor.fetchall()

            events_by_user = {}

            for row in dataset:
                uid = row['user_id']
                if uid in events_by_user:
                    events_by_user[uid]['events'].append({
                        "id": row['id'],
                        "date": row["date"],
                        "time": row["time"],
                        "game_name": row['name']
                    })
                else:
                    time_list = row['time'].split(':')
                    events_by_user[uid] = {
                        "gamer_id": uid,
                        "full_name": row['full_name'],
                        "events": [{
                            "id": row['id'],
                            "date": row["date"],
                            "time": datetime.strptime(row['time'], "%H:%M:%S"),
                            "game_name": row['name']
                        }]
                    }

            events = events_by_user.values()
            context = { "user_with_events": events }
            template = "users/list_with_events.html"
            return render(request, template, context)
