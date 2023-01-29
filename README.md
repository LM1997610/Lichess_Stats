# Lichess Stats

This project was done with basic coding skills, when I first approached Python.\
Room for improvement is large, and depth of game analysis can also be significantly deepened... but I'm out of time\
The goal was to practice with an API and to do some plots

**Lichess_cmd.py** and **Opening_cmd.py** are two programs meant to be run on the Command Prompt.\
These return stats for the searched <a href="https://lichess.org" target="_blank">**Lichess**</a> player.\
Results are printed on the Command Line and plots allow for a graphical display.
[go](http://stackoverflow.com){:target="_blank" rel="noopener"}

------------------------------------
## Requirements :
Core of the project is [**Berserk**](https://pypi.org/project/berserk): python client for the [**Lichess API**](https://lichess.org/api)\
It requires a **Token**: click your username in top right corner → preferences → API Access Tokens\
Replace with your own token in the codes

------------------------------------
## Structure of the Repo :

**Lichess_cmd.py** → filters the games of the desired player by:
<br>

&ensp;&thinsp;&ensp;&thinsp;&ensp;&thinsp; - <u>rated</u> or <u>not rated</u> games  
&ensp;&thinsp;&ensp;&thinsp;&ensp;&thinsp; - time control (**bullet**, **blitz**, **rapid**, **classical**)

the output shows:
* the number of games **won** (with both colors), **lost** and **drawn**
* the causes of defeat (**CheckMate**, **Resignation**, **OutOfTime**) for <u>lost games</u>
---------------

**Opening_cmd.py** → filters the games of the desired player by:
<br>

&ensp;&thinsp;&ensp;&thinsp;&ensp;&thinsp; -  **side** for which he played (<u>black</u> or <u>white</u>)\
&ensp;&thinsp;&ensp;&thinsp;&ensp;&thinsp; -  <u>rated</u> or <u>not rated</u> games\
&ensp;&thinsp;&ensp;&thinsp;&ensp;&thinsp; -  time control (**bullet**, **blitz**, **rapid**, **classical**)

the output shows:
* the **most played openings** from that side
* the **performance** on those openings (**wins**, **draws** and **losses**)
-------------------------

**example.ipynb** → **NoteBook** created just to show the results, adapting the source code.\
Here stats computed for two example players

---------------------------------
