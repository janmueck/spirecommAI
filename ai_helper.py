from spirecomm.spire.game import Game
from spirecomm.spire.character import Intent, PlayerClass
import spirecomm.spire.card
from spirecomm.spire.screen import RestOption
from spirecomm.communication.action import *
from spirecomm.ai.priorities import *
import json
try:
    with open('actions.json') as jsonfile:
        actions=json.load(jsonfile)
except FileNotFoundError:
    actions={}

legal_actions=actions

def get_combat_actions(game,actions):
    other_cards = [card for card in game.hand if (card.is_playable and not card.has_target)]
    targeted_cards = [card for card in game.hand if (card.is_playable and card.has_target)]
    available_monsters = [monster for monster in game.monsters if monster.current_hp > 0 and not monster.half_dead and not monster.is_gone]
    targeted_potions =[]
    other_potions =[]
    for potion in game.get_real_potions():
            if potion.can_use:
                if potion.requires_target and potion.can_use:
                    targeted_potions.append(potion)
                elif potion.can_use:
                    other_potions.append(potion)
    end=game.end_available
    #Cards without target
    for i,card in enumerate(other_cards):
        key='playNonTargetCard:'+str(i)
        actions[key]=1
        legal_actions[key]=1
    #Cards with Target
    for i,card in enumerate(targeted_cards):
        for j,target in enumerate(available_monsters):
            key='playCard:{}|Target:{}'.format(i,j)
            actions[key]=1
            legal_actions[key]=1
    #Potinons to use with target and to discard
    for i,potion in other_potions:
        key='usePotion:'+str(i)
        actions[key]=1
        legal_actions[key]=1
    for i,potion in enumerate(targeted_potions):
        for j,target in enumerate(available_monsters):
            key='playPotion:{}|Target:{}'.format(i,j)
            actions[key]=1
            legal_actions[key]=1
    for i,_ in enumerate(game.get_real_potions()):
        key='discardPotion:'+str(i)
        actions[key]=1
        legal_actions[key]=1
    #End turn 
    if end:
        key='endTurn:'
        actions[key]=1
        legal_actions[key]=1


def get_oocombat_actions(game):
    

