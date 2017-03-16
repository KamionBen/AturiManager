#!/usr/bin/python3.6
# -*-coding:Utf-8 -*

import pickle
# TODO: (?) I use pickle, but I knew another more efficient way, I need to look for it
import os.path
from os import remove, makedirs
import core

# TODO: Add the possibility for the user to not save files
# TODO: Check if 'pilots/' exists
# TODO: Create a 'config' file, maybe ...

dir_path = 'pilots/'


class FilesManager:
    """Class created to manage the pilot files"""
    def __init__(self, pilot_list = []):
        """This class contains :
- pilot_list : if no list, create an empty one"""

        self.pilot_list = pilot_list

    def pilots_dir_exist(self):
        """Check if the pilot directory exists"""
        if os.path.exists(dir_path):
            return True
        else:
            return False

    def create_pilot_dir(self, path=dir_path):
        """Create the pilot directory"""
        os.makedirs(dir_path)

    def save_pilots(self):
        """Save all the pilots in 'pilot_list' in a different file in the directory 'dir_path'"""
        for pilot in self.pilot_list:
            file_name = pilot.get_file()
            dir = dir_path + file_name
            with open(dir, 'wb') as fichier:
                mon_pickler = pickle.Pickler(fichier)
                mon_pickler.dump(pilot)

    def load_pilots(self):
        """Load all the pilots from 'dir_path' and add them to 'pilot_list"""
        file_list = []
        for root, dirs, files in os.walk(dir_path):
            for i in files:
                file_list.append(os.path.join(root, i))

        for file in file_list:
            with open(file, 'rb') as fichier:
                mon_depickler = pickle.Unpickler(fichier)
                pilot = mon_depickler.load()
                self.pilot_list.append(pilot)

    def delete_file(self, file):
        """Delete the 'file' in 'dir_path' """
        chemin = dir_path + file
        remove(chemin)

    def delete_all(self):
        """Delete all the pilot files found in 'pilot_list'"""
        # TODO : Should delete_title all the files
        for pilot in self.pilot_list:
            try:
                file = dir_path + pilot.get_file()
                remove(file)
            except:
                pass


def create_random_pilot_list():
    """Create a pilot list for test"""
    pilot_list = [core.Pilot('Benj', 'Zen'), core.Pilot('Antoine', 'Ballablanc')]
    for pilot in pilot_list:
        pilot.set_first_ship('X-Wing')
    fim = FilesManager(pilot_list)
    fim.delete_all()
    fim.save_pilots()
