
import berserk
import numpy as np
from tqdm import tqdm
from collections import Counter
from matplotlib import pyplot as plt

import config

session = berserk.TokenSession(config.lichess_token) 
client = berserk.Client(session)

def search_request():
   
    _max = None
    cadenze = ["blitz", "rapid", "bullet", "classical"]
    print(" ")
    ############################################################
    player = input(" - Chess player account : ")
    type_ = input(" - Time control : ")
    rated = input(" - Rated or not? (yes/NO) : ")
    print(" ")
    #################################################################
    if rated == "yes" and type_ in cadenze:
        try:
            search = {"player" : player, "type" : type_, "rated": True, "max" : _max }
            print(" Search :", search)
            
            info = client.users.get_realtime_statuses(search["player"])
            print(" info :", info, "\n")
            Stat, D_lost, search = Blitz_Stat(search)
            search["rated"] = " ( rated )"
            pie_plot(Stat, D_lost, search)
            search_request()
        except berserk.exceptions.ResponseError:
            print("  Error 404: User not found \n")
            search_request()

    elif rated == "NO" and type_ in cadenze:
        try:
            search = {"player" : player, "type" : type_, "rated": False, "max" : _max }
            print(" Search :", search)
            info = client.users.get_realtime_statuses(search["player"])
            print(" info :", info, "\n")
            Stat, D_lost, search = Blitz_Stat(search)
            search["rated"] = " ( not rated )"
            pie_plot(Stat, D_lost, search)
            search_request()
        except berserk.exceptions.ResponseError:
            print("  Error 404 : User not found \n")
            search_request()
    else:
        print("  Error 111 : mistake in query ...\n")
        search_request()

def Blitz_Stat(search):

    player = search["player"]
    c = (client.games.export_by_player(player, rated = search["rated"],
                                            opening = True, perf_type = search["type"], max = search["max"]))
    games = list(tqdm(c, total= 5000) )
    games = [game for game in games if game["players"]["white"]]
    games = [game for game in games if game["players"]["black"]]
    print(" ")
    decisivi = [game for game in games if "winner" in game ]
    draw = ([game for game in games if "winner" not in game.keys()])
    white_wins = [game for game in decisivi if game["players"]["white"]["user"]["name"] == player and game["winner"] == "white"]
    black_wins = [game for game in decisivi if game["players"]["black"]["user"]["name"] == player and game["winner"] == "black"]
    black_losses = [game for game in decisivi if game["players"]["black"]["user"]["name"] != player and game["winner"] == "black"]
    white_losses = [game for game in decisivi if game["players"]["white"]["user"]["name"] != player and game["winner"] == "white"]

    tot_losses = black_losses + white_losses

    Stat = {"tot_games" : len(games), "win Black" : len(black_wins), "win White" : len(white_wins), "Draws" : len(draw), "Losses": len(tot_losses)}
    print(" ")
    print("  Lichess = | Games :", len(games) ," | Vttorie :",len(white_wins)+len(black_wins), " | Sconfitte : ", len(tot_losses))
    print(" ")
    D_lost = Counter([game["status"] for game in tot_losses])
    #D_lost  = dict(Counter(D_lost))
    print(" d4t4 = ", Stat)
    print(" ")
    print(" Cause of defeats : ", D_lost, "\t Perse  = ", D_lost["outoftime"] + D_lost["mate"] + D_lost["resign"] )

    return Stat, D_lost, search

def func(pct, allvalues):
    absolute = int(pct / 100.*np.sum(allvalues))
    return "{:.1f}%\n\n({:d} games)".format(pct, absolute)
def func2(pct, allvalues):
    absolute = int(pct / 100.*np.sum(allvalues))
    return "{:.1f}%\n({:d} games)".format(pct, absolute)

def pie_plot(Stat, D_lost, search):
    print(" ")

    labels = [x for x in Stat.keys()][1:]
    sizes = [y for y in Stat.values()][1:]
    etichette = [x for x in D_lost.keys()]
    dimens = [y for y in D_lost.values()]
    fig = plt.figure(figsize = (13, 7.7), dpi=80)  #12 6.8
    ax = fig.add_subplot(121)
    explode = (0.01, 0.01, 0.01, 0.0207)
    colors = ( "#404540", "#d0dbd3", "#1152a8", "#de5d2f") # blcak, white, "blue", "red" = losses

    _, _, autopcts = ax.pie( sizes , labels = labels, explode = explode,
                    autopct = lambda pct: func(pct, sizes),
                    colors = colors, shadow = False, radius= 1.23, startangle = 270 )

    plt.legend(labels = labels, loc='upper right', bbox_to_anchor=(0.12, 0.085), ncol=1)
    plt.setp(autopcts, **{'color':'white', 'weight':'bold', 'fontsize':12.2})
    plt.text(0.87, 1.48, "total games = {}\n won games = {}\n lost games = {}".format(Stat["tot_games"],Stat["win Black"]+Stat["win White"],Stat["Losses"]),
                                                                                horizontalalignment='left', fontsize=12.4)

    plt.title('{}\n {} {} games'.format(search["player"], search["rated"] ,search["type"]), y = 1.14, loc="left", fontstyle='italic', fontsize = 18, fontweight = 709)

    x = fig.add_subplot(122)

    c = ["#179c10","#dedb92","#9c5513","#C1CB12","#F83535"]
    colo = tuple(c[:len(dimens)])
    ex = [0.013, 0.013, 0.023, 0.013,0.017]
    explo = tuple(ex[:len(dimens)])

    _, _, autopcts = plt.pie( dimens , labels = etichette, radius=.94,
                    autopct = lambda pct: func2(pct, dimens),
                    explode = explo, startangle = 190, colors = colo)
    #plt.text(-0.19, 1.08, "Causes of defeat:", horizontalalignment='left', fontsize=14, fontweight = 709, fontstyle='italic' )
    plt.setp(autopcts, **{'color':'white', 'weight':'bold', 'fontsize':9.8})
    plt.title("Causes of defeat: ", loc="left", fontstyle='italic', fontsize = 16, fontweight = 619 )
    plt.legend(labels = etichette, loc='lower right', ncol=1) #bbox_to_anchor=(096.15, 0.95))
    plt.tight_layout()
    plt.margins(0.2)
    plt.show(block=False)
    #plt.close()



search_request()

