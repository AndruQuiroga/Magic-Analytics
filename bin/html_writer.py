import os


def write_html(registered_players):
    with open(os.path.join("logs", "current_Ranked_ladder.html"), "w") as html:
        html.write("""<!DOCTYPE html><html lang="en" xmlns="http://www.w3.org/1999/html"><head><meta charset="UTF-8">
        <title>Ranked Ladder</title>
        </head><body><p><pre>""")
        for player in registered_players:
            if player.rank_num - player.prank_num > 0:
                sign = f"&#8599;"
            elif player.rank_num - player.prank_num < 0:
                sign = f"&#8600;"
            else:
                sign = f"&#8594;"

            html.write(f"{player.rank:>8} Rank {sign} {player.rank_num:3d} : {player.name}\n")
        html.write("""</pre></body></html>""")
