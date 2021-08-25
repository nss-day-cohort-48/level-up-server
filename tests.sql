-- select g.id, g.name, g.maker,g.game_type_id,
--             g.description,
--                     g.number_of_players,
--                     g.skill_level,
--                     u.id user_id,
--                     u.first_name || ' ' || u.last_name AS full_name
--                 from levelupapi_game g
--                 join levelupapi_gamer gr on g.gamer_id = gr.id
--                 join auth_user u on gr.user_id = u.id;

select g.id,
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
                on e.game_id = gm.id;
insert into levelupapi_eventgamer values (null, 5, 3);
