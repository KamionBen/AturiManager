#!/usr/bin/python3.6
# -*-coding:Utf-8 -*

# +++ PILOT CLASS +++


class Pilot:
    """Class that represent a pilot"""
    def __init__(self, player, callsign):
        """This class contains :
- player : the name of the actual person that plays the pilot
- callsign : pilot's nickname
- pilot_skill : pilot's PS, set to 2 when creating the pilot
- xp : list that contains the current xp and the total xp
- hunt_table : dict that contains 'enemy name':'number of this enemy killed'
- missions : number of missions played
- upgrades : the list of Upgrade() purchased
- ship : False by default, then become a Ship() object"""

        self.player = player
        self.callsign = callsign

        self.pilot_skill = 2  # TODO: should be pilot_skill

        self.xp = [0,0]  # [current, total]

        self.hunt_table = {}
        self.missions = 0  # TODO: could be [won, played]

        self.upgrades = []

        self.ship = False

    # --- Edit functions ---
    def change_callsign(self, new):
        """Change the callsign to 'new'"""
        self.callsign = new

    def change_player(self, new):
        """Change the player to 'new'"""
        self.player = new

    # --- Ship functions ---
    def set_first_ship(self, ship):  # TODO: Error catching when ship =! 'X-Wing' or 'Y-Wing'
        """Set the first ship, where 'ship' can only ben : 'X-Wing' or 'Y-Wing'"""
        self.ship = Ship(ship)
        if ship == 'X-Wing':
            self.gain_xp(5)
        if ship == 'Y-Wing':
            self.gain_xp(8)

        for elt in self.ship.slots:
            if elt.level <= self.pilot_skill and elt.status != '':
                elt.set_free()

    def change_ship(self, ship):  # TODO: Other ships data + better function
        """Change the ship, spend 5 XP and set the new ship"""
        self.spend_xp(5)
        self.ship = Ship(ship)

    # --- XP functions ---
    def gain_xp(self, nb):  # TODO: Maybe raise an error if xp becomes negative
        """Add 'nb' to current XP and to total XP"""
        self.xp[0] += nb
        self.xp[1] += nb

    def spend_xp(self, nb):
        """Spend XP : remove 'nb' to the current XP"""
        self.xp[0] -= nb

    # --- PS function ---
    def increase_ps(self):
        """Increase Pilot Skill, spend ('newPS' * 2) XP, then free the newly unlocked upgrade slots"""
        self.spend_xp((self.pilot_skill + 1) * 2)
        self.pilot_skill += 1
        for slot in self.ship.slots:
            if slot.level == self.pilot_skill:
                slot.set_free()

    # --- Upgrades functions ---
    def get_upgrades_list(self, slot, all=False):
        """Get the selected slot upgrade list
if 'all'=False, return only the upgrades you can afford
return a 'list' object"""
        type = self.ship.slots[slot].type
        list = []
        for elt in upgrades:
            if elt.type == type:
                if elt.ship != self.ship:
                    pass
                elif all:
                    list.append(elt)
                else:
                    if elt.points <= self.xp[0]:
                        list.append(elt)

        return list

    def buy_upgrade(self, upgrade):  # TODO: (?) Set an error raiser ?
        """Buy an upgrade, add the Upgrade() object to the self.upgrades list
'upgrade' can be the upgrade name or id for my own convenience
then, spend the amount of XP """
        if type(upgrade) == str:
            for upg in upgrades:
                if upg.id == upgrade or upg.name == upgrade:
                    n_upgrade = upg
        else:
            n_upgrade = upgrade

        self.spend_xp(n_upgrade.points)
        self.upgrades.append(n_upgrade)

    def assign_upgrade(self, slot, upgrade):
        """Assign a purchased upgrade from upgrades' list to a slot"""
        self.ship.slots[slot].assign_upgrade(upgrade)

    # -- Others ---
    def add_victory(self, name, nb):
        """Add a victory : Look in the hunt table dict if 'nam' exists :
if so : add 'nb'
else : create it with 'nb'"""
        try:
            self.hunt_table[name] += nb
        except:
            self.hunt_table[name] = nb

    def add_mission(self, nb):
        """Add 'nb' to missions"""
        self.missions += nb

    # -- REPR FUNCTIONS ---
    def __repr__(self):  # TODO: Need to be obsolet : A pilot shouldn't be allowed not to have a ship assigned
        if self.ship is False:
            return "\"{}\" PS:{} No ship assigned (Player : {})".format(self.callsign, self.pilot_skill, self.player)
        else:
            return "\"{}\" PS:{} {} pilot (Player : {})".format(self.callsign, self.pilot_skill, self.ship, self.player)

    # --- Prez functions ---
    def prez(self, slot=False):
        """A "simple" console presentation ('slot' option can deactivate the slot display)"""
        print("Player : {}".format(self.player))
        print("Callsign : {}".format(self.callsign))
        print("Missions : {}".format(self.missions))
        print("Pilot Skill : {} / XP : {} ({})".format(self.pilot_skill, self.xp[0], self.xp[1]))
        stats = self.ship.reprStats()
        print("Stats : {}".format(stats))
        print("Actions : {}".format(self.ship.actions))
        if slot:
            i = 0
            for elt in self.ship.slots:
                print("slot{} : {}".format(i, elt))
                i += 1

            print("available upgrades: ")
            if len(self.upgrades)==0:
                print("none")
            else:
                for elt in self.upgrades:
                    print(elt.name)

            for elt, key in self.hunt_table.items():
                print("{} x{}".format(elt, key))

    def get_file(self):  # TODO: Delete whitespaces and special characters
        """Use to easily create a correct filename"""
        return self.callsign.lower()

    # TODO: Setters and Getters

# +++ SHIP CLASS +++


class Ship:
    """Class that represents a ship"""
    def __init__(self, ship):
        """This class contains :
- ship : the name of the ship
- stats : ['attack', 'agility', 'hull', 'shield']
- actions : the list of available actions
- slots : a list of Slots() objects (x12, 0 to 11)"""

        self.ship = ship
        self.stats = ships[ship]['stats']

        self.actions = ships[ship]['actions']

        self.slots = []

        for elt in ships[ship]['slots']:
            self.slots.append(elt)

    def __repr__(self):
        """Return the ship's name"""
        return self.ship

    def repr_actions(self):
        """Return a string object instead of a list"""
        i = 0
        text = ""
        for act in self.actions:
            if i == 0:
                text += act.capitalize()
            else:
                text += ", {}".format(act.capitalize())
            i += 1

        return text

    def repr_stats(self):  # TODO: Obsolet
        """Return a formated string to represent the stats"""
        return "{}|{}|{}|{}".format(self.stats[0], self.stats[1], self.stats[2], self.stats[3], )

    # TODO: Getters

# +++ SHIP CLASS +++


class Slots:
    """Class that represents an upgrade slot"""
    def __init__(self, type, level, double=False, title=False, status='LOCKED'):
        """This class contains :
- double : slot type can be double, set to False by default
- type : a 'str' if slot isn't double, otherwise, create type1 and type2
- level : the level needed to unlock this slot
- title : some slot have a title coming with, 'False' by default
- status : can be 'LOCKED', 'FREE' or 'TAKEN'
- usage : 'False' if the slot is free or locked, Upgrade() object if an upgrade is assigned to the slot"""

        self.double = double
        if self.double:
            self.type1 = type[0]
            self.type2 = type[1]
            self.type = "Double type"
        else:
            self.type = type

        self.level = level
        self.title = title
        self.status = status

        self.usage = False

    def __repr__(self):  # TODO: Should return 'usage' too
        """Return all the informations about the slot"""
        if self.type == '':
            return 'None'
        if self.level == 0:
            if self.double:
                return "{}/{} (Status : {})".format(self.type1, self.type2, self.status)
            else:
                if self.title == False:
                    return "{} (Status : {})".format(self.type, self.status)
                else:
                    return "{} title:{} (Status : {})".format(self.type, self.title, self.status)

        else:
            return "{} (lvl : {} Status : {})".format(self.type, self.level, self.status)

    def assign_upgrade(self, upgrade):
        """Assign an Upgrade() object to the slot, change the status to 'TAKEN'"""
        self.usage = upgrade
        self.status = 'TAKEN'

    def set_locked(self):
        """Set the status to 'LOCKED'"""
        self.status = 'LOCKED'

    def set_free(self):
        """Set the status to 'FREE', set usage to 'False'"""
        self.status = 'FREE'
        self.usage = False

# TODO: (?) 'ships' contains all the ships informations, but it's a bit messy ...
ships = {'X-Wing':{'slots': [Slots('Astromech',0),Slots('Torpedo',0),Slots('',0, status=''), Slots('',0, status=''), Slots('Modification',0), Slots('Elite', 3),
                             Slots('Modification',4), Slots('Elite',5), Slots('Modification', 6), Slots('Elite', 7),
                             Slots('Modification', 8), Slots('Elite', 9)],
                   'actions' : ['focus', 'lock'],
                   'stats':[3,2,3,2]},
         'Y-Wing': {'slots': [Slots('Astromech',0),Slots(['Torpedo','Bomb'],0, True),Slots("Turret",0, title="BTL-A4"), Slots(['Torpedo','Bomb'],0, True),
                              Slots('Modification',0), Slots('Elite', 3), Slots('Modification',4), Slots('Elite',5), Slots('Modification', 6), Slots('Elite', 7),
                             Slots('Modification', 8), Slots('Elite', 9)],
                              'actions': ['focus', 'lock'],
                            'stats': [3, 2, 3, 2]}
         }
# +++ UPGRADE CLASS +++


class Upgrade:
    """Class that represents an upgrade card"""
    def __init__(self, id, name, type, points, unique, limited, ship, attack, text):
        """This class contains :
id : a unique id to sort the upgrades
name : the name of the upgrade
type : the type of the upgrade
points : the cost of the upgrade
unique : 'True' if the upgrade is unique
limited : 'True' if the upgrade is limited
ship : if the upgrade can only be assigned to one ship, is 'ship'
attack : if the upgrade is an attack, is ['attack',[range]]
text : the description of the upgrade"""

        self.id = id
        self.name = name
        self.type = type
        self.points = points
        self.unique = unique
        self.limited = limited
        self.ship = ship
        self.attack = attack
        self.text = text

    def __repr__(self):
        """Return the name of the upgrade"""
        return self.name

    def descr(self):
        """Return a full description of the upgrade"""
        if self.attack:
            if type(self.attack[1]) == 'list':
                range = "(range:{}-{})".format(self.attack[1][0],self.attack[1][1])
            else:
                range = "(range:{}".format(self.attack[1])

            attack = " attack:{} {}".format(self.attack[0], range)
        else:
            attack = ""

        if self.unique:
            unique = " unique"
        else:
            unique = ""

        if self.limited:
            limited = " limited"
        else:
            limited = ""

        if self.ship != False:
            ship = " {}".format(self.ship)
        else:
            ship = ""

        return "id:{} type:{} name:{} cost:{}{}{}{}{} description:\"{}\"".format(self.id, self.type, self.name, self.points, unique, limited, ship, attack, self.text)


# TODO: (?) Another messy list of informations ...

upgrades = [Upgrade("a00",'R2-D2',"Astromech",4,True,False,False,False,"After executing a green maneuver, you may recover 1 shield (up to your shield value)."),
            Upgrade("a01",'R2-F2',"Astromech",3,True,False,False,False,"*ACTION* : Increase your agility value by 1 until the end of this game round."),
            Upgrade("a02",'R5-D8',"Astromech",3,True,False,False,False,"*ACTION* : Roll 1 defense die. On an evade or focus result, discard 1 of you facedown Damage cards."),
            Upgrade("a03",'R5-P9',"Astromech",3,True,False,False,False,"At the end of the Combat phase, you may spend 1 of your focus tokens to recover 1 shield (up to your shield value)"),
            Upgrade("a04",'R7-T1',"Astromech",3,True,False,False,False,"*ACTION* : Choose an enemy ship at Range 1-2. If you are inside that ship's firing arc, you may acquire a target lock on that ship. Then, you may perform a free boost action."),
            Upgrade("a05",'BB-8',"Astromech",2,True,False,False,False,"When you reveal a green maneuver, you may perform a free barrel roll action."),
            Upgrade("a06",'R3-A2',"Astromech",2,True,False,False,False,"When you declare the target of your attack, if the defender is inside your firing arc, you may receive 1 stress token to cause the defender to receive 1 stress token."),
            Upgrade("a07",'R5-K6',"Astromech",2,True,False,False,False,"After spending your target lock, roll 1 defense die. On an evade result, immediately acquire a target lock on that same ship. You cannot spend this target lock during this attack."),
            Upgrade("a08",'R7 Astromech',"Astromech",2,False,False,False,False,"Once per round when defending, if you have a target lock on the attacker, you may spend the target lock to choose any or all attack dice. The attacker must reroll the chosen dice."),
            Upgrade("a09",'Targeting Astromech',"Astromech",2,False,False,False,False,"After you execute a red maneuver, you may assign 1 focus token to your ship."),
            Upgrade("a10",'R2 Astromech',"Astromech",1,False,False,False,False,"You may treat all 1 and 2 speed maneuvers as green maneuvers"),
            Upgrade("a11",'R2-D6',"Astromech",1,True,False,False,False,"Your upgrade bar gains the 'elite' Upgrade icon. You cannot equip this upgrade if you already have the 'elite' Upgrade icon or if your pilot skill is 2 or lower."),
            Upgrade("a12",'R4-D6',"Astromech",1,True,False,False,False,"When you are hit by an attack and there are at least 3 uncanceled hit results, you may choose and cancel those results until there are 2 remaining. For each result canceled in this way, receive 1 stress token."),
            Upgrade("a13",'R5 Astromech',"Astromech",1,False,False,False,False,"During the End phase, you may choose 1 of your faceup Damage cards with the Ship trait and flip it facedown."),
            Upgrade("a14",'R5-X3',"Astromech",1,True,False,False,False,"Before you reveal your maneuver, you may discard this card to ignore obstacles until the end of the round"),
            Upgrade("b00",'Proton Bombs',"Bomb/Mine",5,False,False,False,False,"Dropped when maneuver dial is revealed. Detonates at the end of the activation phase in which it was dropped. All ships at range 1 suffer 1 face up damage card - ignores shields."),
            Upgrade("b01",'Cluster Mines',"Bomb/Mine",4,False,False,False,False,"*ACTION* : Drops as a set of 3 tokens. Each token detonates if a ship's maneuver template or base overlaps it. This ship rolls 2 attack dice and suffers hits rolled."),
            Upgrade("b02",'Conner Net',"Bomb/Mine",4,False,False,False,False,"*ACTION* : Detonates if a ship's maneuver template or base overlaps the bomb token. This ship suffers 1 damage, receives 2 ion tokens and skips its Perform Action step."),
            Upgrade("b03",'Proximity Mines',"Bomb/Mine",3,False,False,False,False,"*ACTION* : Detonates if a ship's maneuver template or base overlaps the bomb token. This ship rolls 3 attack dice and suffers all damage rolled."),
            Upgrade("b04",'Ion Bombs',"Bomb/Mine",2,False,False,False,False,"Dropped when maneuver dial is revealed. Detonates at the end of the activation phase in which it was dropped. All ships at range 1 receive 2 ion tokens."),
            Upgrade("b05",'Seismic Charges',"Bomb/Mine",2,False,False,False,False,"Dropped when maneuver dial is revealed. Detonates at the end of the activation phase in which it was dropped. All ships at range 1 suffer 1 damage."),
            Upgrade("b06",'Thermal Detonators',"Bomb/Mine",0,False,False,False,False,""),
            Upgrade("c00",'Heavy Laser Cannon',"Cannon",7,False,False,False,[4,[2,3]],"all criticals change to hits"),
            Upgrade("c01",'AutoBlaster',"Cannon",5,False,False,False,[3,[1]],"Hits cannot be cancelled with dice. Criticals are cancelled before hits"),
            Upgrade("c02",'"Mangler Cannon"',"Cannon",4,False,False,False,[3,[1,3]],"Change 1 hit to a critical"),
            Upgrade("c03",'Ion Cannon',"Cannon",3,False,False,False,[3,[1,3]],"Max 1 damage - 1 ion token if hit"),
            Upgrade("c04",'Flechette Cannon',"Cannon",2,False,False,False,[3,[1,3]],"Max 1 damage and if not stressed, receives a stress"),
            Upgrade("c05",'Tractor Beam',"Cannon",1,False,False,False,[3,[1,3]],"If this attack hits, the defender receives 1 tractor beam token. Then cancel all dice results. A tractor beam token reduces the ship's agility by 1 during the Combat Phase. The token is removed during the End Phase. Once per round, a small ship receiving a token can be forced into a barrel roll or straight boost, even onto an asteroid."),
            Upgrade("d00",'Luke Skywalker',"Crew",7,True,False,False,False,"After you perform an attack that does not hit, immediately perform a primary weapon attack. You may change 1 focus result to a hit result. You cannot perform another attack this round."),
            Upgrade("d01",'Gunner',"Crew",5,False,False,False,False,"After you perform an attack that does not hit, immediately perform a primary weapon attack. You cannot perform another attack this round."),
            Upgrade("d02",'Chewbacca',"Crew",4,True,False,False,False,"When you are dealt a Damage card, you may immediately discard that card and recover 1 shield. Then discard this Upgrade card."),
            Upgrade("d03",'Flight Instructor',"Crew",4,False,False,False,False,"When defending, you may reroll 1 of your focus results. If the attacker's pilot skill value is 2 or lower, you may reroll 1 of your blank results instead."),
            Upgrade("d04",'Leia Organa',"Crew",4,True,False,False,False,"At the start of the Activation phase, you may discard this card to allow all friendly ships that reveal a red maneuver to treat that maneuver as a white maneuver until the end of the phase."),
            Upgrade("d05",'R2-D2',"Crew",4,True,False,False,False,"At the end of the End phase, if you have no shields, you may recover 1 shield and roll 1 attack die. On a hit result, randomly flip 1 of your facedown Damage cards faceup and resolve it."),
            Upgrade("d06",'C-3PO',"Crew",3,True,False,False,False,"Once per round, before you roll 1 or more defense dice, you may guess aloud a number of evade results. If you roll that many evade results (before modifying dice), add 1 evade result."),
            Upgrade("d07",'Ezra Bridger',"Crew",3,True,False,False,False,"When attacking, if you are stressed, you may change 1 of your focus results to a critical result."),
            Upgrade("d08",'Kanan Jarrus',"Crew",3,True,False,False,False,"Once per round, after a friendly ship at Range 1-2 executes a white maneuver, you may remove 1 stress token from that ship"),
            Upgrade("d09",'Kyle Katarn',"Crew",3,True,False,False,False,"After you remove a stress token from your ship, you may assign a focus token to your ship."),
            Upgrade("d10",'Lando Calrissian',"Crew",3,True,False,False,False,"*ACTION* : Roll 2 defense dice. For each focus results, assign 1 focus token to your ship. For each evade result, assign 1 evade token to your ship."),
            Upgrade("d11",'Navigator',"Crew",3,False,False,False,False,"When you reveal a maneuver, you may rotate your dial to another maneuver with the same bearing. You cannot rotate to a red maneuver if you have any stress tokens."),
            Upgrade("d12",'Recon Specialist',"Crew",3,False,False,False,False,"When you perform a focus action, assign 1 additional focus token to your ship."),
            Upgrade("d13",'Weapons Engineer',"Crew",3,False,False,False,False,"You may maintain 2 target locks (only 1 per enemy ship). When you acquire a target lock, you may lock onto 2 different ships."),
            Upgrade("d14",'"Leebo"',"Crew",2,True,False,False,False,"*ACTION* : Perform a free boost action, then receive 1 ion token."),
            Upgrade("d15",'Dash Rendar',"Crew",2,True,False,False,False,"You may perform attacks while overlapping an obstacle. Your attacks cannot be obstructed."),
            Upgrade("d16",'Han Solo',"Crew",2,True,False,False,False,"When attacking, if you have a target lock on the defender, you may spend that target lock to change all of your Focus results to Hit results."),
            Upgrade("d17",'Jan Ors',"Crew",2,True,False,False,False,"Once per round, when a friendly ship at Range 1-3 performs a focus action or would be assigned a focus token, you may assign that ship an evade token instead."),
            Upgrade("d18",'Mercenary Copilot',"Crew",2,False,False,False,False,"When attacking at Range 3, you may change 1 of your hit results to a critical result."),
            Upgrade("d19",'Sabine Wren',"Crew",2,True,False,False,False,"Your upgrade bar gains the Bomb upgrade icon. Once per round, before a friendly bomb token is removed, choose 1 enemy ship at Range 1 of that token. That ship suffers 1 damage."),
            Upgrade("d20",'Saboteur',"Crew",2,False,False,False,False,"*ACTION* : Choose 1 enemy ship at Range 1 and roll 1 attack die. On a hit or critical result, choose 1 random facedown Damage card assigned to that ship, flip it faceup, and resolve it."),
            Upgrade("d21",'Tactician',"Crew",2,False,True,False,False,"After you perform at attack against a ship inside your firing arc at Range 2, that ship receives 1 stress token."),
            Upgrade("d22",'Bombardier',"Crew",1,False,False,False,False,"When dropping a bomb, you may use the [2 straight] template instead of the [1 straight] template."),
            Upgrade("d23",'Hera Syndulla',"Crew",1,True,False,False,False,"You can reveal and execute red maneuvers even while you are stressed"),
            Upgrade("d24",'Intelligence Agent',"Crew",1,False,False,False,False,"At the start of the Activation phase, choose 1 enemy ship at Range 1-2. You may look at that ship's chosen maneuver."),
            Upgrade("d25",'Nien Nunb',"Crew",1,True,False,False,False,"You may treat all straight maneuvers as green maneuvers"),
            Upgrade("d26",'Zeb Orrelios',"Crew",1,True,False,False,False,"Enemy ships inside your firing arc that you are touching are not considered to be touching you when either you or they activate during the combat phase."),
            Upgrade("d27",'Chopper',"Crew",0,True,False,False,False,"You may perform actions even while stressed. After you perform an action while you are stressed, suffer 1 damage."),
            Upgrade("e00",'Expose',"Elite",4,False,False,False,False,"*ACTION* : Until the end of the round, increase your primary weapon value by 1 and decrease your agility value by 1."),
            Upgrade("e01",'Opportunist',"Elite",4,False,False,False,False,"When attacking, if the defender does not have any focus or evade tokens, you may receive 1 stress token to roll 1 additional attack die. You cannot use this ability if you have any stress tokens."),
            Upgrade("e02",'Daredevil',"Elite",3,False,False,False,False,"*ACTION* : Execute a red hard 1 turn maneuver. Then if you do not have the Boost action icon, roll 2 attack dice. Suffer and hit or critical damage rolled."),
            Upgrade("e03",'Marksmanship',"Elite",3,False,False,False,False,"*ACTION* : When attacking this round, you may change 1 of your focus results to a critical result and all of your other focus results to a hit result."),
            Upgrade("e04",'Outmaneuver',"Elite",3,False,False,False,False,"When attacking a ship inside your firing arc, if you are not inside that ship's firing arc, reduc its agility value by 1 (to a minium of 0)"),
            Upgrade("e05",'Predator',"Elite",3,False,False,False,False,"When attacking, you may reroll 1 attack die. If the defenders pilot skill value is 2 or lower, you may instead reroll up to 2 attack dice."),
            Upgrade("e06",'Push the Limit',"Elite",3,False,False,False,False,"Once per round, after you perform an action, you may perform 1 free action shown in your action bar. Then receive 1 stress token."),
            Upgrade("e07",'Juke',"Elite",2,False,False,False,False,"When attacking, if you have an evade token, you may change 1 of the defender's Evade results to a Focus result."),
            Upgrade("e08",'Decoy',"Elite",2,False,False,False,False,"At the start of the Combat phase, you may choose 1 friendly ship at Range 1-2. Exchange your pilot skill with that ship's pilot skill until the end of the phase."),
            Upgrade("e09",'Elusiveness',"Elite",2,False,False,False,False,"When defending, you may receive 1 stress token to choose 1 attack die. The attacker must reroll that die. If you have at least 1 stress token, you cannot use this ability."),
            Upgrade("e10",'Expert Handling',"Elite",2,False,False,False,False,"*ACTION* : Perform a barrel roll. If you do not have the barrel roll action icon, receive 1 stress token. You may then remove 1 enemy target lock from your ship."),
            Upgrade("e11",'Intimidation',"Elite",2,False,False,False,False,"While you are touching an enemy ship, reduce that ship's agility value by 1."),
            Upgrade("e12",'Lone Wolf',"Elite",2,True,False,False,False,"When attacking or defending, if there are no other friendly ships at Range 1-2, you may reroll 1 of your blank results."),
            Upgrade("e13",'Squad Leader',"Elite",2,True,False,False,False,"*ACTION* : Choose 1 ship at Range 1 or 2 that has a lower pilot skill than you. The chosen ship may immediately perform 1 free action."),
            Upgrade("e14",'Stay on Target',"Elite",2,False,False,False,False,"When you reveal your maneuver, you may rotate your dial to another maneuver with the same speed. Treat that maneuver as a red maneuver."),
            Upgrade("e15",'Swarm Tactics',"Elite",2,False,False,False,False,"At the start of the Combat phase, choose 1 friendly ship at Range 1. Until the end of this phase, treat the chosen ship as if its pilot skill were equal to your pilot skill."),
            Upgrade("e16",'Wingman',"Elite",2,False,False,False,False,"At the start of the Combat phase, remove 1 stress token from another friendly ship at Range 1."),
            Upgrade("e17",'Lightning Reflexes',"Elite",1,False,False,False,False,"After you execute a white or green maneuver on your dial, you may discard this card to rotate your ship 180°. Then receive 1 stress token after the \"Check Pilot Stress\" step."),
            Upgrade("e18",'Adrenaline Rush',"Elite",1,False,False,False,False,"When you reveal a red maneuver, you may discard this card to treat that maneuver as a white maneuver until the end of the Activation phase."),
            Upgrade("e19",'Calculation',"Elite",1,False,False,False,False,"When attacking, you may spend a focus token to change 1 of your focus results to a critical result."),
            Upgrade("e20",'Cool Hand',"Elite",1,False,False,False,False,"When you receive a stress token, you may discard this card to assign 1 focus or evade token to your ship."),
            Upgrade("e21",'Crack Shot',"Elite",1,False,False,False,False,"When attacking a ship inside your firing arc, you may discard this card to cancel 1 of the defender's evade results."),
            Upgrade("e22",'Deadeye',"Elite",1,False,False,False,False,"You may treat the \"Attack:Target Lock\" header as \"Attack:Focus\". When an attack instructs you to spend a target lock, you may spend a focus token instead."),
            Upgrade("e23",'Determination',"Elite",1,False,False,False,False,"When you are dealt a faceup Damage card with a Pilot trait, discard it immediately without resolving its effect."),
            Upgrade("e24",'Draw Their Fire',"Elite",1,False,False,False,False,"When a friendly ship at Range 1 is hit by an attack, you may suffer 1 of the uncanceled critical results instead of the target ship."),
            Upgrade("e25",'Veteran Instincts',"Elite",1,False,False,False,False,"Increase your pilot skill value by 2."),
            Upgrade("e26",'Wired',"Elite",1,False,False,False,False,"When attacking or defending, if you are stressed, you may reroll 1 or more of your focus results."),
            Upgrade("e27",'Adaptability',"Elite",0,False,False,False,False,"Increase or Decrease your pilot skill value by 1."),
            Upgrade("f00",'"Hot Shot" Blaster',"Illicit",3,False,False,False,[3,[1,2]],"Discard this card to attack 1 ship (even a ship outside your firing arc)."),
            Upgrade("f01",'Cloaking Device',"Illicit",2,True,False,False,False,"*ACTION* : Perform a free cloak action. At the end of each round, if you are cloaked, roll 1 attack die. On a focus result, discard this card, then decloak or discard your cloak token."),
            Upgrade("f02","Dead Man's Switch","Illicit",2,False,False,False,False,"When you are destroyed, each ship at Range 1 suffers one damage."),
            Upgrade("f03",'Feedback Array',"Illicit",2,False,False,False,False,"During the Combat phase, instead of performing any attacks, you may receive 1 ion token and suffer 1 damage to choose 1 enemy ship at Range 1. That ship suffers 1 damage."),
            Upgrade("f04",'Glitterstim',"Illicit",2,False,False,False,False,"At the start of the Combat phase, you may discard this card and receive 1 stress token. If you do, until the end of the round, when attacking or defending, you may change all of your focus results to hit or evade results."),
            Upgrade("f05",'Inertial Dampeners',"Illicit",1,False,False,False,False,"When you reveal your maneuver, you may discard this card to instead perform a white [0] maneuver. Then receive 1 stress token."),
            Upgrade("g00",'Assault Missiles',"Missile",5,False,False,False,[4,[2,3]],"*ATTACK : Target Lock*If attack hits, all other ships at range 1 receive 1 damage"),
            Upgrade("g01",'Homing Missiles',"Missile",5,False,False,False,[4,[2,3]],"*ATTACK : Target Lock* Defender cannot spend evade tokens"),
            Upgrade("g02",'Cluster Missiles',"Missile",4,False,False,False,[3,[1,2]],"*ATTACK : Target Lock*perform attack twice"),
            Upgrade("g03",'Concussion Missiles',"Missile",4,False,False,False,[4,[2,3]],"*ATTACK : Target Lock*change 1 blank to hit"),
            Upgrade("g04",'Adv. Homing Missles',"Missile",3,False,False,False,[3,[2]],"*ATTACK : Target Lock*If attack hits, deal one faceup damage card, all results are cancelled"),
            Upgrade("g05",'Ion Pulse Missle',"Missile",3,False,False,False,[3,[2,3]],"*ATTACK : Target Lock*Max 1 damage - 2 ion tokens if hit"),
            Upgrade("g06",'Proton Rockets',"Missile",3,False,False,False,[2,[1]],"*ATTACK : Focus*You may roll additional attack dice equal to your agility - max 3"),
            Upgrade("g07",'XX-23 S-Thread Tracers',"Missile",1,False,False,False,[3,[1,3]],"*ATTACK : Focus*If this attack hits, each friendly ship at range 1-2 of you may acquire a target lock on the defender, then cancel all dice results."),
            Upgrade("g08",'Chardaan Refit',"Missile",-2,False,False,"A-Wing",False,"This card has a negative squad point cost."),
            Upgrade("h00",'Engine Upgrade',"Modification",4,False,False,False,False,"Your action bar gains the Boost action icon."),
            Upgrade("h01",'Shield Upgrade',"Modification",4,False,False,False,False,"Increase your shield value by 1."),
            Upgrade("h02",'Experimental Interface',"Modification",3,True,False,False,False,"Once per round, after you perform an action, you may perform 1 free action from an equipped Upgrade card with the \"Action\" header. Then receive 1 stress token."),
            Upgrade("h03",'Hull Upgrade',"Modification",3,False,False,False,False,"Increase your hull value by 1."),
            Upgrade("h04",'Stealth Device',"Modification",3,False,False,False,False,"Increase your agility value by 1. If you are hit by an attack, discard this card."),
            Upgrade("h05",'Advanced SLAM',"Modification",2,False,False,False,False,"After performing a SLAM action, if you did not overlap an obstacle or another ship, you may perform a free action."),
            Upgrade("h06",'Autothrusters',"Modification",2,False,False,False,False,"When defending, if you are beyond Range 2 or outside the attacker's firing arc, you may change 1 of your blank results to a evade result. You can equip this card only if you have the Boost action icon."),
            Upgrade("h07",'Stygium Particle Accelerator',"Modification",2,False,False,False,False,"When you either decloak or perform a cloak action, you may perform a free evade action."),
            Upgrade("h08",'Targeting Computer',"Modification",2,False,False,False,False,"Your action bar gains the target lock action icon."),
            Upgrade("h09",'B-Wing/E2',"Modification",1,False,False,"B-Wing",False,"Your upgrade bar gains the Crew upgrade icon."),
            Upgrade("h10",'Munitions Failsafe',"Modification",1,False,False,False,False,"When attacking with a secondary weapon that instructs you to discard it to perform the attack, do not discard it unless the attack hits."),
            Upgrade("h11",'Integrated Astromech',"Modification",0,False,False,"X-Wing",False,"When you are dealt a Damage card, you may discard 1 of your Astromech Upgrade cards to discard that Damage card (without resolving its effect)."),
            Upgrade("h12",'Guidance Chip',"Modification",0,False,False,False,False,"Once per round, when attacking with a torpedo or missile, you may change 1 die result to a hit result (or a critical result if your primary weapon value is 3 or higher)"),
            Upgrade("h13",'Long Range Scanners',"Modification",0,False,False,False,False,"You can acquire target locks on ships at Range 3 and beyond. You cannot acquire target locks on ships at Range 1-2. You can equip this card only if you have missile and torpedo in your upgrade bar."),
            Upgrade("i00",'R4-B11',"Salvaged Astromech",3,True,False,False,False,"When attacking, if you have a target lock on the defender, you may spend the target lock to choose any or all defense dice. The defender must reroll the chosen dice."),
            Upgrade("i01",'R4 Agromech',"Salvaged Astromech",2,False,False,False,False,"When attacking, after you spend a focus token, you may acquire a target lock on the defender."),
            Upgrade("i02",'Salvaged Astromech',"Salvaged Astromech",2,False,False,False,False,"When you are dealt a Damage card with the Ship trait, you may immediately discard that card (before resolving its effect). Then discard this Upgrade card."),
            Upgrade("i03",'Unhinged Astromech',"Salvaged Astromech",1,False,False,False,False,"You may treat all 3-speed maneuvers as green maneuvers."),
            Upgrade("i04",'"Genius"',"Salvaged Astromech",0,True,False,False,False,"If you are equipped with a bomb that can be dropped when you reveal your maneuver, you may drop the bomb after you execute your maneuver instead."),
            Upgrade("j00",'Sensor Jammer',"System",4,False,False,False,False,"When defending, you may change 1 of the attacker's hit results to a focus result. The attacker cannot reroll the die with the changed result."),
            Upgrade("j01",'Accuracy Corrector',"System",3,False,False,False,False,"When attacking, during the “Modify Attack Dice” step, you may cancel all of your dice results. Then, you may add 2 hit results to your roll. Your dice cannot be modified again during this attack."),
            Upgrade("j02",'Advanced Sensors',"System",3,False,False,False,False,"Immediately before you reveal your maneuver, you may perform 1 free action. If you use this ability, you must skip your \"Perform Action\" step during this round."),
            Upgrade("j03",'Fire-Control System',"System",2,False,False,False,False,"After you perform an attack, you may acquire a target lock on the defender."),
            Upgrade("j04",'Electronic Baffle',"System",1,False,False,False,False,"When you receive a stress token or an ion token, you may suffer 1 damage to discard that token."),
            Upgrade("j05",'Enhanced Scopes',"System",1,False,False,False,False,"During the Activation phase, treat your pilot skill value as \"0\"."),
            Upgrade("k00",'Moldy Crow',"Title",3,True,False,"HWK-290",False,"During the End phase, do not remove unused focus tokens from your ship."),
            Upgrade("k01",'A-Wing Test Pilot',"Title",0,False,False,"A-Wing",False,"Your upgrade bar gains 1 Elite upgrade icon. You cannot equip 2 of the same Elite Upgrade cards. You cannot equip this card if your pilot skill value is \"1\" or lower."),
            Upgrade("k02",'BTL-A4 Y-Wing',"Title",0,False,False,"Y-Wing",False,"You cannot attack ships outside your firing arc. After you perform a primary weapon attack, you may immediately perform an attack with a Turret secondary weapon."),
            Upgrade("l00",'Adv. Proton Torpedoes',"Torpedo",6,False,False,False,[5,[1]],"*ATTACK : Target Lock*change 3 blanks to focus"),
            Upgrade("l01",'Ion Torpedoes',"Torpedo",5,False,False,False,[4,[2,3]],"*ATTACK : Target Lock*If attack hits, defender and all other ships at range 1 receive 1 ion token"),
            Upgrade("l02",'Proton Torpedoes',"Torpedo",4,False,False,False,[4,[2,3]],"*ATTACK : Target Lock*change 1 focus to critical"),
            Upgrade("l03",'Plasma Torpedoes',"Torpedo",3,False,False,False,[3,[2,3]],"*ATTACK : Target Lock*If attack hits, after dealing damage, remove 1 shield from the defender"),
            Upgrade("l04",'Extra Munitions',"Torpedo",2,False,True,False,False,"Adds an extra of each equipped bomb, missile or torpedo"),
            Upgrade("l05",'Flechette Torpedoes',"Torpedo",2,False,False,False,[2,[2,3]],"*ATTACK : Target Lock*In addition to damage, 1 stress to defender if hull is 4 or less"),
            Upgrade("l06",'Bomb Loadout',"Torpedo",0,False,True,"Y-Wing",False,"Adds a bomb upgrade slot"),
            Upgrade("m00",'Twin Laser Turret',"Turret",6,False,False,False,[3,[2,3]],"Attack twice, max of 1 damage each attack, no crits"),
            Upgrade("m01",'Ion Cannon Turret',"Turret",5,False,False,False,[3,[1,2]],"Max 1 damage - 1 ion token if hit"),
            Upgrade("m02",'Blaster Turret',"Turret",4,False,False,False,[3,[1,2]],"*ATTACK : Focus*"),
            Upgrade("m03",'Dorsal Turret',"Turret",3,False,False,False,[2,[1,2]],"Add an attack die at range 1"),
            Upgrade("m04",'Autoblaster Turret',"Turret",2,False,False,False,[2,[1]],"Hits cannot be cancelled with dice. Criticals are cancelled before hits")]

