# Imports
import sys
import os
import shutil
import argparse
import urllib
import pypresence
import PySimpleGUI as sg

# pyinstaller --onefile --noconsole --icon=Icon32.ico --add-data "resources;resources" interclient.py

# Variables
version = '1.0'
mcversion = '1.18'
sg.theme('LightBlue2')


# Argparse magic
parser = argparse.ArgumentParser()
parser.add_argument("-d", "--directory", help="Specify a specific directory to install to. If this argument isn't used, the installer will prompt you for the destination directory.")
graphicsmods = parser.add_mutually_exclusive_group()
graphicsmods.add_argument("--optifine", action="store_true", default=False, help="Bypasses the prompt asking which graphics mod to use, and adds OptiFine. (Not recommended for most users)")
graphicsmods.add_argument("--sodium", action="store_true", default=False, help="Bypasses the prompt asking which graphics mod to use, and adds Sodium with Sodium Extra. (Recommended for most users)")
graphicsmods.add_argument("--iris", action="store_true", default=False, help="Bypasses the prompt asking which graphics mod to use, and adds Sodium with Iris. (Recommended for users who want shaders)")
args = parser.parse_args()

# Set variables based on args
use_optifine = args.optifine
use_iris = args.iris


# Helper Methods
def get_full_path(relpath):
    # Takes a relative path and converts it to an absolute path, and validates said path
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller onefile compatibility
        os.chdir(sys._MEIPASS)
        fullpath = os.path.join(sys._MEIPASS, relpath)
    else:
        fullpath = os.path.abspath(os.path.join(os.path.dirname(__file__), relpath))

    if not os.path.isdir(fullpath):
        error_popup(f'{fullpath} is missing. Please re-download the package or make sure the resources folder is in the same folder as this program and has not been altered.')
    else:
        message_log(f'Validated {relpath}')
        return fullpath

def copydir(sourcedir, destdir):
    # Walks the given folder and copies all files and subdirectories to the destination
    for subdir, dirs, files in os.walk(sourcedir):
        for filename in files:
            filepath = subdir + os.sep + filename
            destination = subdir.replace(sourcedir, '')
            os.makedirs(destdir + destination, exist_ok=True)
            fulldestpath = destpath + destination + os.sep + filename
            shutil.copyfile(filepath, fulldestpath)
            file_log(f'Copied {destination + os.sep + filename} to {fulldestpath}')

def error_popup(error):
    error_log(error)
    sg.Window('Error!', [[sg.T(error)], [sg.Exit()]], disable_close=True).read(close=True)
    sys.exit()

def exit_popup():
    sg.Window('Installer Exited', [[sg.T('The installer has been exited and no changes have been made.')], [sg.Exit()]], disable_close=True).read(close=True)
    sys.exit()

def message_log(message):
    print(f'[LOG]\t{message}')

def error_log(error):
    print(f'[ERROR]\t{error}')

def file_log(text):
    print(f'[FILE_WRITE]\t{text}')

def custom_log(type, message):
    print(f'[{type}]\t{message}')



if args.directory:
    destpath = args.directory
else:
    event, values = sg.Window(f'InterClient Installer v{version}', [[sg.T(f'Welcome to the InterClient Installer for {mcversion}!\nPlease read the instructions on the website before installing.')],
                                                                    [sg.T('While unlikely, this program has the chance of screwing up your system if used incorrectly.\nI AM NOT RESPONSIBLE FOR ANY DATA LOSS INCURRED BY USING THIS SCRIPT.\nFor best results, use this on a fresh minecraft profile, and Fabric MUST be installed.')],
                                                                    [sg.T('Installer made with <3 by Josh/Agent256')],
                                                                    [sg.Frame('Install Directory', layout=[[sg.InputText(key='inputpath', expand_x=True), sg.FolderBrowse(key='browsepath')]], tooltip='The director for InterClient to be installed', expand_x=True)],
                                                                    [sg.B('Continue'), sg.B('Exit')]]).read(close=True)
    if event == sg.WIN_CLOSED or event == 'Exit':
        sys.exit(0)
    elif event == 'Continue':
        if values['inputpath']:
            destpath = values['inputpath']
        else:
            destpath = values['browsepath']
        message_log('Recieved \"{destpath}\" from window.')

# Validates that the installation path is valid
isdir = os.path.isdir(destpath)
if not isdir:
    error_popup(f'Uh oh, \"{destpath}\" is not a folder on your computer! Please check for any typos!')
else:
    message_log(f'\"{destpath}\" is a valid directory')

    # Prompts user to confirm install directory
    event, values = sg.Window('Confirm Install Directory', [[sg.T(f'Are you sure you want to install InterClient to \"{destpath}\"?')], [sg.B('Yes'), sg.B('No')]], disable_close=True).read(close=True)
    if event == sg.WIN_CLOSED or event == 'No':
        exit_popup()
    else:
        message_log('Directory confirmed by user')

        # Prompts user for graphics Version
        event, values = sg.Window('Confirm Install Directory', [[sg.T(f'Please select which graphics mod to install\nIris is recommended!')], [sg.B('Sodium'), sg.B('Iris'), sg.B('Optifine')]], disable_close=True).read(close=True)
    if event == 'Optifine':
        use_iris = False;
        use_optifine = True

    if event == 'Iris':
        use_iris = True;
        use_optifine = False
    else:
        message_log('Graphics Mod confirmed by user')

 

    

# Validates and copies files
# commonpath = get_full_path(os.path.join('resources', 'common'))
commonpath = True #make this into an ftp on replit
copydir(commonpath, destpath)
if(use_optifine):
    optifinepath = get_full_path(os.path.join('resources', 'optifine'))
    copydir(optifinepath, destpath)
elif(use_iris):
    irispath = get_full_path(os.path.join('resources', 'iris'))
    copydir(irispath, destpath)
else:
    sodiumpath = get_full_path(os.path.join('resources', 'sodium'))
    copydir(sodiumpath, destpath)

# Success Message
message_log('Install Completed')
sg.Window('Installation Completed', [[sg.T('Thank you for installing InterClient!')], [sg.Exit()]], disable_close=True).read(close=True)