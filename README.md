## Lichess Stats

This project was done with basic coding skills, when I first approached Python.\
Room for improvement is large and also the depth of the analysis can be deepened remarkably.\
But I'm out of time

**Lichess_cmd.py** and **Opening_cmd.py** are two programs meant to be run on the command prompt.\
These return stats for the searched [**Lichess**](https://lichess.org) player.\
Results are printed on the Command Line and the plots allow for a graphical display.

-------------------------------------------------------------------------------------------

### Structure of the Repo:

* **Lichess_cmd.py** filters the games of the desired player by:
>* <u>rated</u> or <u>not rated</u> gemes  
>* time control (**bullet**, **blitz**, **rapid**, **classical**)

the output shows:
* the number of games **won** (with both colors), **lost** and **drawn**
* the causes of defeat (**CheckMate**, **Resignation**, **OutOfTime**) for <u>lost games</u>


* **Opening_cmd.py** filters the games of the desired player by:
>* **side** for which he played (<u>black</u> or <u>white</u>)
>* <u>rated</u> or <u>not rated</u> gemes  
>* time control (**bullet**, **blitz**, **rapid**, **classical**)

the output shows:
* the **most played openings** from that side
* the **performance** on those openings (**wins**, **draws** and **losses**)
