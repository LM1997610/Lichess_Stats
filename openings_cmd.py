
import berserk
import numpy as np
from tqdm import tqdm
from collections import Counter
from matplotlib import pyplot as plt
import re

import config

session = berserk.TokenSession(config.lichess_token)
client = berserk.Client(session)

_max = None
cadenze = ["blitz", "rapid", "bullet", "classical"]
colori = ["black", "white"]
numero = 5

def search_request():
    print(" ")
    player = input(" - Chess player account : ")
    side = input(" - black or white : ")
    type_ = input(" - Time control : ")
    rated = input(" - Rated or not? (yes/NO) : ")
    print(" ")

    if rated == "NO" and type_ in cadenze and side in colori:
        search = {"player" : player, "type" : type_, "rated": False, "side" : side, "max" : _max }
        print(" Search : ", search)
        try:
            search = {"player" : player, "type" : type_, "rated": "not rated", "max" : _max, "side" : side }
            info = client.users.get_realtime_statuses(search["player"])
            print(" info : ", info, "\n")

            c = client.games.export_by_player(player, color = search["side"], rated = False , opening = True,  perf_type = search["type"], max = search["max"])
            games_w = list(tqdm(c, total= 5000) )

            games_w = win_counting(side, games_w )

            print("  ... downloaded games = ", len(games_w))
            games_w, c  = find_most_played(games_w)
        
            dati, games_w = openings_stats(games_w, c)
            print(" ")
            for q in dati:
                print(q["apertura"], " = giocate : ", q["giocate"], ", vinte : ", q['vinte'],", perse : ", q['perse'],", pareggi : ", q['pareggi'] )
            labels, sizes, winss, losses, pareggi = plot_pie_op(dati, search, games_w)
            search_request()
            
        except berserk.exceptions.ResponseError:
            print(" Error 404 : Player not found \n")
            search_request()

    elif rated == "yes" and type_ in cadenze and side in colori:
        search = {"player" : player, "type" : type_, "rated": True, "side" : side, "max" : _max}
        print(" Search : ", search)
        try:
            search["rated"] = "rated"
            c = client.games.export_by_player(player, color = search["side"], rated = True, opening = True,  perf_type = search["type"], max = search["max"])
            games_w = list(tqdm(c, total=5000) )
            games_w = win_counting(side, games_w )

            print("  ... downloaded games = ", len(games_w))
            games_w, c = find_most_played(games_w)
            
            dati, games_w = openings_stats(games_w, c)
            print(" ")
            for q in dati:
                print(" ",q["apertura"], " = { giocate : ", q["giocate"], ", vinte : ", q['vinte'],", perse : ", q['perse'],", pareggi : ", q['pareggi'], "}" )
            
            labels, sizes, winss, losses, pareggi = plot_pie_op(dati, search, games_w)
            search_request()
            
        except berserk.exceptions.ResponseError:
            print("  Error 404 : Player not found \n")
            search_request()
    else:
        print("  Error 111 : mistake in query ...")
        search_request()


def win_counting(side, games):

    colori = ["black", "white"]
    colori.remove(side)

    for game in list(games):
        if "winner" in game and game["winner"] == side:
            game["WIN"] = "yes"
            #print("sono una vittoria del ",side )
        elif "winner" in game and game["winner"] == colori[0]:
            #print("sono una SCONFITTA del ", side )
            game["WIN"] = "no"
        else:
            game["WIN"] = "pareggio"

    return games

############ Find_most_played_Openings ###########
def find_most_played(games):
    most_played_op = []

    for g in games:
        try:
            d = [g["opening"]["name"], g["WIN"]]
            most_played_op.append( d )
        except KeyError:
            games.remove(g)

    r = '[,:]'
    for part in range(len(most_played_op)):
        most_played_op[part][0] = re.split(r, most_played_op[part][0])[0]

    top_10 = []
    for part in range(len(most_played_op)):
            top_10.append(most_played_op[part][0])
    c = Counter(top_10)
    top_cinque = (c.most_common(5))
    top_cinque = [el[0] for el in top_cinque]

    return most_played_op, top_cinque

######################################################
############## STAT for each Opening  ################

def openings_stats(most_played_openings, top_cinque):
    stat_op = []
    #opening = { "giocate" : 0, "vinte":0, "perse":0, "pareggi":0}
    #opening = { "giocate" : 0, "vinte":0, "perse":0, "pareggi":0}

    for op in top_cinque:
        d = {"apertura": op, "giocate" : 0, "vinte":0, "perse":0, "pareggi":0}
        for g in most_played_openings:
            if g[0] == op:
                d ["giocate"] += 1
                if g[1] == "yes":
                    d ["vinte"] += 1
                elif g[1] == "no":
                    d ["perse"] += 1
                elif g[1] == "pareggio":
                    d ["pareggi"] += 1
        stat_op.append(d)

    return stat_op, most_played_openings

#################################################################
############# Plot Pie delle aperture #############

def plot_pie_op(questo, serach, games):

    stringa = serach["player"] + " : " + serach["type"] + " " + serach["side"] +" ("+ serach["rated"]+ ") "
    labels = []
    sizes = []
    altro = len(games)
    y1, y2, y3 = [], [], []

    for i in range(len(questo)):
            labels.append(questo[i]["apertura"])
            sizes.append(questo[i]["giocate"])
            altro = altro - int(questo[i]["giocate"])
            y1.append(questo[i]["vinte"])
            y2.append(questo[i]["perse"])
            y3.append(questo[i]["pareggi"])
    winss = np.array(y1)
    losses = np.array(y2)
    pareggi = np.array(y3)
    
    sizes.append(altro)
    labels.append("Other Openings")


    #######################################################
    ################# double-check ########
    if len(games) == sum(sizes):
        controllo = sum(x for x in sizes[:-1])
        print("\n \t ", sizes, " = ", sum(sizes),"| tot games =", len(games), "| sum(sizes[:-1]) = ", controllo )

        #print(" \n \t controllo = ", controllo)
    else:
        print(False)
    ######################################
    #################################
    colors = ["#59e46d",'#cb5731','#325289','#5997e0','#ffcc99',"#d9d764", "#d6e0d3"]
    k = 7 - len(labels)
    kolor = colors[k:]
    esplode = (0.01,)*len(labels)


    fig = plt.figure(figsize =(13, 7), dpi = 80)   
    # Plot
    patches, texts, autopcts = plt.pie(sizes, labels=labels, colors = kolor, shadow = False, explode = esplode, autopct="%1.1f%%", center=(0, 0), radius = 1, startangle =140 )
    elle = [f'{l} : {s} ' for l, s in zip(labels, sizes)]
    plt.legend( loc="lower left", bbox_to_anchor=(0.045, 0.12), labels = elle, prop={'size': 9},  bbox_transform=plt.gcf().transFigure) # patches, bbox_transform=plt.gcf().transFigure
    plt.setp(autopcts, **{'color':'white', 'weight':'bold', 'fontsize':11.8})
    plt.title(stringa, loc="left", fontstyle='italic', fontsize = 19.2, pad =35 )

    plt.text(-2.5, 0.75, "total games = {}".format(len(games)), horizontalalignment='left', fontsize=14.4,  fontstyle= "italic")
    plt.axis('equal')
    bar_plot(labels, sizes, winss, losses, pareggi)
    plt.show(block = False)
    #plt.show()
    return labels,sizes, winss, losses, pareggi

##################################################
########################################################
##########################################################
def bar_plot(lables, sizes, winss, lossess, pareggi):

    print(" ")
    print(" ")
    #stringa =  search["player"] + " : " + search["type"] + " " + search["side"] +" ("+ search["rated"]+ ") "
    fig = plt.figure(figsize =(13, 7), dpi=80)
    ax = plt.subplot()


    rects1 = ax.bar(lables[:-1], winss, color='#1ba1d1')
    rects2 = ax.bar(lables[:-1], lossess, bottom=winss, color='#d65222')
    ax.bar(lables[:-1], pareggi, bottom=winss+lossess, color='y')
    ax.legend(["Wins","Lost","Draws"])
    ax.grid(True)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')
    ax.set_ylabel(" games played ",labelpad=30,fontsize=11)
    ax.set_ylim([0, sizes[0] + 60 ])

    #new_list = per_maker(winss, sizes)
    for p in rects1.patches:
        width, height = p.get_width(), p.get_height()
        if height > 14:
            x, y = p.get_xy()
            ax.text(x+width/2, y+height/2, '{:.0f} '.format(height),
                horizontalalignment='center', verticalalignment='center', fontsize=13, color ="white")

    #new_list2 = per_maker(lossess, sizes)
    for p in rects2.patches:
        width, height = p.get_width(), p.get_height()
        x, y = p.get_xy()
        if height > 14:
            ax.text(x+width/2, y+height/2, '{:.0f} '.format(height),
                horizontalalignment='center', verticalalignment='center', fontsize=13, color ="white")

    plt.title("... info most played openings :", loc="left", fontstyle='italic', fontsize = 18, pad = 32 )

    plt.show(block = False)
  
def per_maker(lista1, sizze):
    new_list = []
    for elem in range(len(lista1)):
        x = lista1[elem] / sizze[elem]
        new_list.append(x)
    return new_list



search_request()
