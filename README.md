# Lichess_Stats

This project was done with basic coding skills, when I first approached Python.\
Room for improvement is large and also the depth of the analysis can be deepened remarkably.\
But I'm out of time

X and Y are two programs meant to be run on the command prompt.\
These return stats for the searched lichess player.\
Results are printed on the Command Line and the plots allow for a graphical display.

Particularly:

In **'Lichess_cmd.py'** we can filter the games of the desired player by:[^1]
- rated or not rated gemes  
- time control (bullet, blitz, rapid, classical)

the output shows:
- the number of games won (with both colors), lost and drawn
- the causes of defeat (CheckMate, Resignation, OutofTime) for lost games


In **Opening.py** we can filter the games of the desired player by: [^2]
- side for which he played (black or white)
- rated or not rated gemes
- time control (bullet, blitz, rapid, classical)

the output shows:
- the most played openings from that side
- the performance on those openings (wins, draws and losses)
