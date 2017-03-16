#!/usr/bin/python3.6
# -*-coding:Utf-8 -*

import filesmanager as fm
import core
from format import Color


debug = False
version = 0.2
# --- TRY TO LOAD PILOT FILES ---

# TODO: A better loading function

try:
    fim = fm.FilesManager()
    fim.load_pilots()
    pilot_list = fim.pilot_list
    if debug:
        print("{} file(s) loaded".format(len(pilot_list)))
except:  # TODO: Learn the proper use of errors
    pilot_list = []
    if debug:
        print("No file")

# ... or create it

#fm.create_random_pilot_list()

# --- GENERAL FUNCTIONS ---


def clear():
    """Print 100 '\n' to clear the screen"""
    print("\n"*100)

# TODO: (?) Those four next functions should be elsewhere I think ...

def top(x):
    return '.' + '-' * x + '.'


def blank(x):
    return "%-2s %-{}s %2s".format(x - 4) % ('|', ' ', '|')


def bottom(x):
    return "|" + "_" * x + "|"


def empty(x):
    return "%{}s".format(x) % ' '


# --- TITLES VARIABLES ---

# TODO: Learn to generate ASCII titles instead of goig to http://patorjk.com/software/taag/
main_title = """     ___   .___________. __    __  .______       __       ______      ___      .___  ___. .______      ___       __    _______ .__   __.
    /   \  |           ||  |  |  | |   _  \     |  |     /      |    /   \     |   \/   | |   _  \    /   \     |  |  /  _____||  \ |  |
   /  ^  \ `---|  |----`|  |  |  | |  |_)  |    |  |    |  ,----'   /  ^  \    |  \  /  | |  |_)  |  /  ^  \    |  | |  |  __  |   \|  |
  /  /_\  \    |  |     |  |  |  | |      /     |  |    |  |       /  /_\  \   |  |\/|  | |   ___/  /  /_\  \   |  | |  | |_ | |  . `  |
 /  _____  \   |  |     |  `--'  | |  |\  \----.|  |    |  `----. /  _____  \  |  |  |  | |  |     /  _____  \  |  | |  |__| | |  |\   |
/__/     \__\  |__|      \______/  | _| `._____||__|     \______|/__/     \__\ |__|  |__| | _|    /__/     \__\ |__|  \______| |__| \__|                                                                                                                                         """
submain_title = """             ___   _  __      __    __  ___
            / _ \ (_)/ /___  / /_  /  |/  /___ _ ___  ___ _ ___ _ ___  ____
           / ___// // // _ \/ __/ / /|_/ // _ `// _ \/ _ `// _ `// -_)/ __/
          /_/   /_//_/ \___/\__/ /_/  /_/ \_,_//_//_/\_,_/ \_, / \__//_/
                                                          /___/            """
delete_title = """  ___        _       _                 ___  _  _       _
 |   \  ___ | | ___ | |_  ___   __ _  | _ \(_)| | ___ | |_
 | |) |/ -_)| |/ -_)|  _|/ -_) / _` | |  _/| || |/ _ \|  _|
 |___/ \___||_|\___| \__|\___| \__,_| |_|  |_||_|\___/ \__|
                                                           """
newpilot_title = """  _  _                ___  _  _       _
 | \| | ___ __ __ __ | _ \(_)| | ___ | |_
 | .` |/ -_)\ V  V / |  _/| || |/ _ \|  _|
 |_|\_|\___| \_/\_/  |_|  |_||_|\___/ \__|
                                          """
xwingpilot_title = """ __  __    __        __ _                 ____   _  _         _
 \ \/ /    \ \      / /(_) _ __    __ _  |  _ \ (_)| |  ___  | |_
  \  / _____\ \ /\ / / | || '_ \  / _` | | |_) || || | / _ \ | __|
  /  \|_____|\ V  V /  | || | | || (_| | |  __/ | || || (_) || |_
 /_/\_\       \_/\_/   |_||_| |_| \__, | |_|    |_||_| \___/  \__|
                                  |___/                           """
ywingpilot_title = """ __   __   __        __ _                 ____   _  _         _
 \ \ / /   \ \      / /(_) _ __    __ _  |  _ \ (_)| |  ___  | |_
  \ V /_____\ \ /\ / / | || '_ \  / _` | | |_) || || | / _ \ | __|
   | ||_____|\ V  V /  | || | | || (_| | |  __/ | || || (_) || |_
   |_|        \_/\_/   |_||_| |_| \__, | |_|    |_||_| \___/  \__|
                                  |___/                           """


# --- CREATE APP CLASS ---


class App:
    """Main class"""
    def __init__(self):
        """Initiate the Main Menu"""

        # TODO: Check if 'pilots/' exist, try to load, display informations, etc ...
        self.initiate_app()
        self.main_menu()

    def initiate_app(self):
        initiate = True
        while initiate:
            print("Check for {}".format(fm.dir_path))
            if fm.FilesManager().pilots_dir_exist():
                self.save = True
            else:

                validate = True
                while validate:
                    print("To allow you to save you pilots, you need to give the permission to create a {} repertorie".format(fm.dir_path))
                    print(Color("Caution : I'm a noob, I don't know where you repertorie will be created ... You should say no", 'RED'))
                    print("Do you allow it ? (Y/N)")
                    choice = input()

                    if choice.lower() == 'y':
                        fm.FilesManager().create_pilot_dir()
                        self.save = True
                        validate = False
                    elif choice.lower() == 'n':
                        self.save = False
                        validate = False
                    else:
                        pass
            initiate = False



    def main_menu(self):
        """Main menu function, primary loop"""

        main_menu = True
        while main_menu:

            clear()

            print(Color(main_title, 'BLUE'))
            print(submain_title)
            print("                         +++ version {} +++\n\n".format(version))

            # -- Menu --

            # TODO: Better pilot display

            i = 1
            for pilot in pilot_list:  # List and display the pilots
                print(Color("{} : {}".format(i, pilot),'BOLD'))
                i += 1

            print(Color("0 : New Pilot", 'BOLD'))
            print(Color("x : Delete a pilot", "BOLD"))
            print("\nWhat do you want to do ? (Type 'quit' to close the program)")
            choice = input()

            # -- Choice --

            # TODO: Create "functions" like 'help', 'save', 'load' ...

            try:
                if choice == '0':
                    self.new_pilot()
                elif int(choice) in range(1, len(pilot_list)+1):
                    self.pilot_menu(pilot_list[int(choice) - 1])

            except:
                if choice == 'x':
                    self.delete_pilot()
                elif choice == 'quit':
                    main_menu = False
                else:
                    pass

    def new_pilot(self):
        """New Pilot Menu Loop"""

        clear()
        new_pilot = True
        while new_pilot:
            print(newpilot_title + "\n")

            # -- Menu --
            print(Color("Creating a new pilot", 'BOLD'))
            print("Choose you callsign :\n")
            callsign = input()

            print("\nChoose the player")
            player = input()

            noship = True
            while noship:
                print("\nChoose your first ship :")
                print("1 : X-Wing (XP +5)")
                print("2 : Y-Wing (XP +8)")
                ship = input()

                if ship == '1':
                    the_new_pilot = core.Pilot(player, callsign)
                    the_new_pilot.set_first_ship('X-Wing')
                    pilot_list.append(the_new_pilot)
                    noship = False
                    new_pilot = False
                    self.pilot_menu(pilot_list[len(pilot_list)])
                    # TODO: This doesn't work, I want it to directly go the this pilot menu
                elif ship == '2':
                    the_new_pilot = core.Pilot(player, callsign)
                    the_new_pilot.set_first_ship('Y-Wing')
                    pilot_list.append(the_new_pilot)
                    noship = False
                    new_pilot = False
                    self.pilot_menu(pilot_list[len(pilot_list)])
                else:
                    pass

    def delete_pilot(self):
        """Function to delete a pilot"""
        # TODO: (?) Should be static ... ? Maybe just create a function in the main loop

        delete_pilot = True
        while delete_pilot:
            clear()

            print(delete_title + "\n\n")

            # -- Menu --
            i = 1
            for pilot in pilot_list:
                print("{} : Delete \"{}\" ?".format(i, pilot.callsign))
                i += 1
            print("x : Go back")
            choice = input()

            # -- Choice --
            try:
                if int(choice) in range(1, len(pilot_list)+1):
                    pilot = pilot_list[int(choice)-1]
                    confirm = True
                    while confirm:
                        print("Do you really want to delete_title \"{}\" ? (Y/N)".format(pilot.callsign))
                        yesno = input()
                        if yesno.lower() == 'y':
                            try:
                                pilot_list.remove(pilot)
                                fm.FilesManager().delete_file(pilot.get_file())
                            except:
                                if debug:
                                    print("No such file")

                            confirm = False
                            delete_pilot = False
                        elif yesno.lower() == 'n':
                            confirm = False
                            delete_pilot = False
                        else:
                            pass
                else:
                    pass
            except:
                if choice == 'x':
                    delete_pilot = False
                else:
                    pass

    def pilot_menu(self, pilot):
        """Pilot # menu"""

        pilot_error = ''
        pilot_menu = True
        while pilot_menu:
            clear()

            # -- Pilot --
            # TODO: Create the others ships titles and put them all in a dict
            if pilot.ship.ship == 'X-Wing':
                print(xwingpilot_title + "\n\n")
            if pilot.ship.ship == 'Y-Wing':
                print(ywingpilot_title + "\n\n")

            # -- Show Pilot --

            # TODO: Maybe create a static function to display this mess

            infos = "%-2s %-36s %2s" % (" ", "General Informations", " ")
            upgrades = "%-2s %-36s %2s" % (" ", "Upgrades", " ")

            print(infos + upgrades)
            up_width = 40

            print(top(40) + top(up_width) * 2)
            call = "%-10s %-25s %5s" % ('|', 'Callsign : ' + pilot.callsign, '|')
            play = "%-10s %-25s %5s" % ('|', 'Player : ' + pilot.player, '|')

            types = []
            i = 0
            for slot in pilot.ship.slots:
                types.append("%-2s %-{}s %2s".format(up_width - 4) % ('|', '[' + str(i) + ']' + ":" + slot.type, '|'))
                i += 1

            status = []
            x = 2
            for slot in pilot.ship.slots:
                if slot.status == 'LOCKED':
                    stat = Color('LOCKED lvl' + str(slot.level) + ' ' * 23, 'RED')
                elif slot.status == 'FREE':
                    stat = Color('FREE' + ' ' * 30, 'GREEN')
                elif slot.status == 'TAKEN':
                    usage = Color(str(slot.usage), 'BLUE')
                    stat = str(usage) + ' ' * (34 - len(usage))
                else:
                    stat = slot.status
                status.append("%-2s %-{}s %2s".format(up_width - 4) % ('|', str(' ' * x + str(stat)), '|'))

            print(call + types[0] + types[1])
            print(play + status[0] + status[1])
            print(bottom(40) + bottom(up_width) * 2)
            print(blank(40) + top(up_width) * 2)

            x = 2
            stat0 = str(Color("|{}|".format(pilot.ship.stats[0]), 'RED')) + ' ' * x
            stat1 = str(Color("|{}|".format(pilot.ship.stats[1]), 'GREEN')) + ' ' * x
            stat2 = str(Color("|{}|".format(pilot.ship.stats[2]), 'YELLOW')) + ' ' * x
            stat3 = str(Color("|{}|".format(pilot.ship.stats[3]), 'BLUE')) + ' ' * x

            stats = "%-2s %-10s %-10s %-5s %-5s %-5s %4s" % ('|', 'PS : {}'.format(pilot.pilotSkill),
                                                            stat0, stat1, stat2, stat3, '|')
            print(stats + types[2] + types[3])

            actions = "%-2s %-35s  %2s" % ('|', 'Actions : ' + pilot.ship.repr_actions(), '|')
            print(actions + status[2] + status[3])
            print(bottom(40) + bottom(up_width) * 2)

            missionxp = "%-2s %-16s %-16s %5s" % (
                '|', 'Mission : ' + str(pilot.missions), 'XP : {}({})'.format(pilot.xp[0], pilot.xp[1]), '|')
            print(blank(40) + top(up_width) * 2)
            print(missionxp + types[4] + types[5])
            print(bottom(40) + status[4] + status[5])
            print(blank(40) + bottom(up_width) * 2)
            victories = "%-2s %-36s %2s" % ('|', 'Victories : 0', '|')
            print(victories + top(up_width) * 2)
            print(bottom(40) + types[6] + types[7])
            print(empty(42) + status[6] + status[7])
            print(empty(42) + bottom(up_width) * 2)

            print(empty(42) + top(up_width) * 2)
            print(empty(42) + types[8] + types[9])
            print(empty(42) + status[8] + status[9])
            print(empty(42) + bottom(up_width) * 2)

            print(empty(42) + top(up_width) * 2)
            print(empty(42) + types[10] + types[11])
            print(empty(42) + status[10] + status[11])
            print(empty(42) + bottom(up_width) * 2)

            # -- Menu --
            print(pilot_error)
            print("What do you want to do ? (Type 'help' to show the menu)")
            choice = input()
            pilot_error = ''
            # -- Choice --
            choice = choice.lower()

            # -- Decode --
            # TODO: Maybe create a function to decode these fucntion. (They look like 'help' or 'gainxp:2')
            decode = False
            for elt in choice:
                if elt == ':':
                    decode = True
                else:
                    pass

            code = ''
            nb = ''
            if decode:
                for elt in choice:
                    if elt == ':':
                        break
                    else:
                        code += elt
                nan = True
                for elt in choice:
                    if elt == ':':
                        nan = False
                    elif nan:
                        pass
                    else:
                        nb += elt

            try:
                nb = int(nb)
            except:
                decode = False

            # -- Pilot functions --

            if decode:
                if code == 'gainxp':
                    pilot.gain_xp(nb)
                elif code == 'mission':
                    pilot.add_mission(nb)
                elif code == 'slot':
                    self.upgrades_menu(pilot, nb)
                else:
                    pilot_error = Color("ERROR : Unkonown command '{}'".format(code), 'RED')
            else:
                if choice == 'back':
                    pilot_menu = False
                elif choice == 'help':
                    self.pilot_help()
                elif choice == 'psup':
                    if (pilot.pilotSkill+1)*2 > pilot.xp[0]:
                        pilot_error = Color("XP ERROR : You need {} XP to do that, you only have {} XP".format(
                            (pilot.pilotSkill + 1) * 2, pilot.xp[0]), 'RED')
                    else:
                        pilot.increase_ps()
                else:
                    pilot_error = Color("ERROR : Unkonown command '{}'".format(choice), 'RED')

    def pilot_help(self):
        """Displayed if 'help' : show the available functions"""
        clear()
        pilot_help = True
        while pilot_help:
            print("Help Menu\n\n")
            print("{}\nType 'gainxp:#', with # as the amount of XP you want to add\n".format(Color('gainxp','BOLD')))

            print("{}\nType 'mission:#', with # as the amount of missions you want to add\n".format(
                Color('mission', 'BOLD')))

            print("{}\nType 'slot:#', with # as the upgrade slot you want to edit\n".format(
                Color('slot', 'BOLD')))

            print("{}\nType 'psup' to increase you Pilot Skill\n".format(
                Color('psup', 'BOLD')))

            print("{}\nType 'back' to go back te the Main Menu\n".format(
                Color('back', 'BOLD')))

            print("\n\nType anything to go back")
            input()
            pilot_help = False

    def upgrades_menu(self, pilot, nb):
        """Pilot # upgrades menu"""

        upgrades_menu = True
        while upgrades_menu:
            clear()

            slot = pilot.ship.slots[nb]

            # -- Display Upgrades Menu --
            # TODO: Better display

            print("UPGRADES MENU")

            print("Type : {} | Status : {}".format(slot.type, slot.status))
            if slot.usage == False:
                print("No upgrade assigned")
            else:
                print("slot.usage")
                print("slot.text")

            print("\n\n")
            print("Buy and assign an upgrades :\n")
            list = pilot.get_upgrades_list(nb)
            i = 1
            for elt in list:
                print("%10s %-25s %-1s" % ("[{}]  ".format(i), "{} ({})".format(elt.name, elt.points), elt.text))
                i += 1

            # -- Menu --

            print("x : Go back")  # TODO: Maybe create a 'back' function, like the rest
            choice = input()

            # -- Choice --
            try:
                if int(choice) in range(1, len(list)+1):
                    upgrade = list[int(choice)-1]
                    if upgrade.points > pilot.xp[0]:
                        print(Color("XP ERROR : You cannot purchase this upgrade", 'RED'))
                    else:
                        confirm = True
                        while confirm:
                            print("Buy and assign \"{}\" for {} XP ? (Y/N)".format(upgrade.name, upgrade.points))
                            validate = input()
                            if validate.lower() == 'n':
                                confirm = False
                            elif validate.lower() == 'y':
                                pilot.buy_upgrade(upgrade)
                                pilot.assign_upgrade(nb, upgrade)
                                confirm = False
                                upgrades_menu = False
            except:
                if choice == 'x':
                    upgrades_menu = False
                else:
                    pass

    def victories_menu(self, pilot):
        """Show the victory table"""

        # TODO: Everything

        victories_menu = True
        while victories_menu:
            clear()

            print("VICTORIES MENU")
            print(pilot)

            # -- Menu --
            print("1 : Do something")
            print("x : Go back")
            choice = input()

            # -- Choice --
            if choice == 'x':
                victories_menu = False
            else:
                pass

    def change_ship(self, pilot):
        """Show all the ships, allow the user to pick one if he can"""

        # TODO: Everything

        change_ship_menu = True
        while change_ship_menu:
            clear()

            print("CHANGE SHIP OR PS MENU")
            print(pilot)

            # -- Menu --
            print("1 : Do something")
            print("x : Go back")
            choice = input()

            # -- Choice --
            if choice == 'x':
                change_ship_menu = False
            else:
                pass

if __name__ == '__main__':
    app = App()

if app.save:
    fim = fm.FilesManager(pilot_list)
    fim.delete_all()
    fim.save_pilots()
