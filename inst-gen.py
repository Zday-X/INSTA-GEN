from json import JSONDecodeError
import sys
import pymailtm
from pymailtm.pymailtm import CouldNotGetAccountException
from prettytable import PrettyTable
import os
import time
from inputimeout import inputimeout, TimeoutOccurred
import requests
from datetime import datetime
import platform




class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

instagen = """
██╗███╗   ██╗███████╗████████╗ █████╗        ██████╗ ███████╗███╗   ██╗
██║████╗  ██║██╔════╝╚══██╔══╝██╔══██╗      ██╔════╝ ██╔════╝████╗  ██║
██║██╔██╗ ██║███████╗   ██║   ███████║█████╗██║  ███╗█████╗  ██╔██╗ ██║
██║██║╚██╗██║╚════██║   ██║   ██╔══██║╚════╝██║   ██║██╔══╝  ██║╚██╗██║
██║██║ ╚████║███████║   ██║   ██║  ██║      ╚██████╔╝███████╗██║ ╚████║
╚═╝╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═╝  ╚═╝       ╚═════╝ ╚══════╝╚═╝  ╚═══╝
"""
author = "💀 ZDAY-X 💀"
disclaimer = "This Tool Was Purely Built For Education Purposes Only"
os.system("cls") # Change this to [clear] to work in linux
sys.stdout.write(instagen)

# Make this one as not equals too in future
if platform.system().lower() == "windows":
    print(f"\t\t\t\t\t\t\t\t\t{bcolors.HEADER} DEV :-",end='')
    sys.stdout.write(f"{bcolors.FAIL }{author}")



    for i in range(3):
        print()
    time.sleep(2)

    for word in disclaimer.split():
        print(f"{bcolors.WARNING} {word}",end="")
        time.sleep(0.25)
    for i in range(4):
        print()

    spin_load = ["|","/","-","\\","|"]
    
    animation = "|/-\\"
    idx = 0
    i = 0
    end_ = 30
    while i <= end_:
        print(bcolors.OKCYAN+"Initializing "+animation[idx % len(animation)], end="\r")
        idx += 1
        time.sleep(0.1)
        i += 1
    os.system("cls") # Change to clear



    while 1:    
        print(f"{bcolors.OKGREEN} {instagen}")
        print(bcolors.OKBLUE+
        """
        [1] Create Instagram Accounts
        """
        )
        des_1 = input(bcolors.HEADER + ">>> ")

        if des_1.lower() == "1":
            print("""\n\nIT IS ADVICED TO NOT CREATE MORE THAN 15 ACCOUNT AT A TIME TO PREVENT IP BAN""")
            print("However the choice is yours ;)\n\n\n")
            print(f"{bcolors.ENDC}NUMBER OF ACCOUNTS TO CREATE: ", end =" ")
            number_of_account = input()

            manual_creation = input(f"{bcolors.WARNING}Do you want to manually enter account credentials? [y/n]: ").lower()

            if manual_creation == 'y':
                "Code to manual enter"

            elif manual_creation == "n":
                
                "Code to automate creation"
            else:
                print()
                time.sleep(1)
                print(f'{bcolors.FAIL}What the fuck do you just said? huh ? BYE!')
                time.sleep(2)
                sys.exit()





            sys.exit()
        else:
            print("|ERROR | INVALID ENTRY :<, TRY AGAIN")
            time.sleep(3)
            os.system("cls") # Change to clear
            continue

    



else:
    print("You have to run this tool in linux :(")
    for i in range(7,1,-1):
        print(f"Exiting The Application in {i}",end="\r")
        time.sleep(1)
    sys.exit()