select g.id, g.name, g.maker,g.game_type_id,
            g.description,
                    g.number_of_players,
                    g.skill_level,
                    u.id user_id,
                    u.first_name || ' ' || u.last_name AS full_name
                from levelupapi_game g
                join levelupapi_gamer gr on g.gamer_id = gr.id
                join auth_user u on gr.user_id = u.id;
