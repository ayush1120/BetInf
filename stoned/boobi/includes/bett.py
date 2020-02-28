import pickle
from os import system, name, path, makedirs
from time import sleep
from datetime import datetime
import math


YES = ['Y','y','yes','YES','Yes','YEs','yEs','yeS','YeS','yES']
NO = ['N','n',"NO",'no','No','nO']


class BET:
    def __init__(self, idx, m_id, side, amount, ratio):
        self.idx = idx
        self.m_id = m_id
        self.side = side
        self.amount = amount
        self.ratio = ratio
    def __str__(self):
        return ("BET SUMMARY \n id : {}\n match : {}\n side : {}\n amount : {}\n payout : {} \n".format(self.idx,self.m_id,self.side,self.amount,self.ratio*self.amount))


def water_down(ratio):
    ratio *= 100
    ratio = math.floor(ratio)
    return ratio/100

def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')


def get_odds(x,y):
    o1,o2 = 1,1
    o1 += (y/x)*0.88
    o2 += (x/y)*0.88
    return water_down(o1),water_down(o2)

def show_odds(team1, team2, x, y):
    clear()
    print(team1,team2,x,y)
    print('############# Team 0: {} ||| Payout : {} #############'.format(team1,get_odds(x,y)[0]))

    print('############# Team 1: {} ||| Payout : {} #############'.format(team2,get_odds(x,y)[1]))

    sleep(5)

def create_bet(m_id,team1,team2,x,y):
    clear()
    show_odds(team1, team2, x, y)
    idx = int(input("Roll : "))
    side = int(input("Team : "))
    amount = int(input("Amount : "))
    if side == 0:
        ratio = get_odds(x,y)[0]
        x = x + amount
    else:
        ratio = get_odds(x,y)[1]
        y = y + amount
    bet = BET(idx,m_id,side,amount,ratio)
    print(bet)
    print("\n\n CONFIRM BET?")
    tp = input(':')
    if tp in YES:
        return bet, x, y
    else:
        return None, x, y

def save_bets(bets,m_id):
    now = len(bets)
    if not path.exists(m_id):
        makedirs(m_id)
    with open(path.join(m_id,str(now)+'.pkl'),'wb') as f:
        pickle.dump(bets,f)

def get_prof(x,y,bets,winner):
    t_poff = 0
    for i in bets:
        if i.side == winner:
            t_poff += i.ratio*i.amount
    print("Profit = ",x+y-t_poff,"with winner ",winner)

def looper(m_id, team1, team2, x, y):
    bets = []
    clear()
    print("^^     MENU     ^^\n1. Show Odds\n2. Make Bet\n3. Complete Session \n $:")
    inp = int(input())
    while(True):
        if inp == 1:
            show_odds(team1, team2, x, y)
            clear()
            print("^^     MENU     ^^\n1. Show Odds\n2. Make Bet\n3. Complete Session \n $:")
            inp = int(input())
        elif inp==2:
            bet, x, y = create_bet(m_id, team1, team2, x, y)
            if bet is not None:
                bets.append(bet)
                save_bets(bets,m_id)
            clear()
            print("^^     MENU     ^^\n1. Show Odds\n2. Make Bet\n3. Complete Session \n $:")
            inp = int(input())
        elif inp==3:
            get_prof(x,y,bets,0)
            get_prof(x,y,bets,1)
            return


if __name__ == "__main__":
    m_id = input("Enter Match ID : ")
    team1 = input("Enter First Team name : ")
    x = int(input("Enter initial bet on Team 1 : "))
    team2 = input("Enter Second Team name : ")
    y = int(input("Enter initial bet on Team 2 : "))

    looper(m_id, team1, team2, x, y)