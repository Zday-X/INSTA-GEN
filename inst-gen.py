# Feel Free to READ :)

from json import JSONDecodeError
import sys
import pymailtm
from pymailtm.pymailtm import CouldNotGetAccountException
from random_username.generate import generate_username
import os
import random
import time
import requests
from password_generator import PasswordGenerator
from datetime import datetime
import platform

link = "https://www.instagram.com/"  # used to get the csrf token
create_url = "https://www.instagram.com/accounts/web_create_ajax/attempt/"
verify_mail = "https://i.instagram.com/api/v1/accounts/send_verify_email/"
check_confo = "https://i.instagram.com/api/v1/accounts/check_confirmation_code/"
final_create_url = "https://www.instagram.com/accounts/web_create_ajax/"


pwo = PasswordGenerator()


def _insta_gen(
    email,
    user_name=generate_username(1)[0] + str(random.randint(1, 1000)),
    first_name=generate_username(1)[0],
    password=str(pwo.generate()) + str(random.randint(1, 999999999999)),
):
    time = int(datetime.now().timestamp())

    try:
        with requests.Session() as s:
            s.get(link)
            csrf = s.cookies["csrftoken"]
            mid = s.cookies["mid"]

            # Payload to initialize the account.
            payload_creation = {
                "enc_password": f"#PWD_INSTAGRAM_BROWSER:0:{time}:{password}",
                "email": email,
                "username": user_name,
                "first_name": first_name,
                "opt_into_one_tap": "false",
                "client_id": mid,
                "seamless_login_enabled": "1",
            }

            s.post(
                create_url,
                data=payload_creation,
                headers={
                    "user-agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
                    "x-requested-with": "XMLHttpRequest",
                    "referer": "https://www.instagram.com/accounts/emailsignup/",
                    "x-csrftoken": csrf,
                },
            )

            payload_verify_mail = {"device_id": mid, "email": email}

            # Payload to request OTP to the temporary mail.
            s.post(
                verify_mail,
                data=payload_verify_mail,
                headers={
                    "user-agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
                    "x-requested-with": "XMLHttpRequest",
                    "referer": "https://www.instagram.com/",
                    "x-csrftoken": csrf,
                },
            )
            import time

            # Constantly Check for incomming email from instgram server in our mail inbox and get otp.
            while 1:
                time.sleep(1.5)
                messages = acc_inst.get_messages()
                try:
                    inst_mail = messages[0]
                    verification_code = inst_mail.subject[:6]
                    break
                except:
                    pass
            # Payload to verify OTP with instagram servers.
            payload_check_code = {
                "code": verification_code,
                "device_id": mid,
                "email": email,
            }

            resp_code = s.post(
                check_confo,
                data=payload_check_code,
                headers={
                    "user-agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
                    "x-requested-with": "XMLHttpRequest",
                    "referer": "https://www.instagram.com/",
                    "x-csrftoken": csrf,
                },
            )

            resp_json = resp_code.json()
            signup_code = resp_json["signup_code"]

            # Final payload to finalize creating the account.
            create_final_payload = {
                "enc_password": f"#PWD_INSTAGRAM_BROWSER:0:{time}:{password}",
                "email": email,
                "username": user_name,
                "first_name": first_name,
                "month": "1",
                "day": "18",
                "year": "1972",
                "opt_into_one_tap": "false",
                "client_id": mid,
                "seamless_login_enabled": "1",
                "tos_version": "row",
                "force_sign_up_code": signup_code,
            }

            s.post(
                final_create_url,
                data=create_final_payload,
                headers={
                    "user-agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
                    "x-requested-with": "XMLHttpRequest",
                    "referer": "https://www.instagram.com/accounts/emailsignup/",
                    "x-csrftoken": csrf,
                },
            )

            with open("cred.txt", "a") as f:
                f.write("\n\n")
                f.write(f"EMAIL: {email}\n")
                f.write(f"USERNAME: {user_name}\n")
                f.write(f"PASSWORD: {password}\n")
    except KeyError:
        print("ERROR: UNABLE TO FETCH CSRF_TOKEN")
        print("PROBABLE CAUSE: IP BANNING")


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


main_instance = pymailtm.MailTm()


c2 = 0


def _create_acc():
    global account
    global acc_inst

    while True:
        try:
            global acc_id
            global acc_password
            global mail_addre

            # print("generating mail id...")
            account = main_instance.get_account()
            acc_id = account.id_
            acc_password = account.password
            mail_addre = account.address
            # print("Creating account....")
            acc_inst = pymailtm.Account(acc_id, mail_addre, acc_password)
            break
        except JSONDecodeError:
            print("Ah fuck, Encountered an error.. Trying to resolve it..")
            try:
                account = main_instance.get_account()
            except CouldNotGetAccountException:
                print("Alright, im done on this shit.. ReRun the script")
                sys.exit()
            except:
                print("If you Dont Mind , just Re Run The Script...")
                sys.exit()
            time.sleep(5)
        except:
            global c2
            print("Hmm, Thats weird.. Retrying..")
            if c2 == 5:
                print("Wtf is happening?!, ReRun The Script...")
                sys.exit()
            c2 += 1

            time.sleep(5)
            continue


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
os.system("cls")  # Change this to [clear] to work in linux
sys.stdout.write(instagen)

# Make this one as not equals too in future
# Change this one to != to run in linux :)
if platform.system().lower() == "windows":
    print(f"\t\t\t\t\t\t\t\t\t{bcolors.HEADER} DEV :-", end="")
    sys.stdout.write(f"{bcolors.FAIL }{author}")

    for i in range(3):
        print()
    time.sleep(2)

    for word in disclaimer.split():
        print(f"{bcolors.WARNING} {word}", end="")
        time.sleep(0.25)
    for i in range(4):
        print()
    spin_load = ["|", "/", "-", "\\", "|"]

    animation = "|/-\\"
    idx = 0
    i = 0
    end_ = 30
    while i <= end_:
        print(
            bcolors.OKCYAN + "Initializing " + animation[idx % len(animation)], end="\r"
        )
        idx += 1
        time.sleep(0.1)
        i += 1
    os.system("cls")  # Change to clear

    while 1:
        print(f"{bcolors.OKGREEN} {instagen}")
        print(
            bcolors.OKBLUE
            + """
        [1] Create Instagram Accounts
        """
        )
        des_1 = input(bcolors.HEADER + ">>> ")

        if des_1.lower() == "1":
            print(
                """\n\nIT IS ADVICED TO NOT CREATE MORE THAN 15 ACCOUNT AT A TIME TO PREVENT IP BAN"""
            )
            print("However the choice is yours ;)\n\n\n")
            print(f"{bcolors.ENDC}NUMBER OF ACCOUNTS TO CREATE: ", end=" ")

            while 1:
                try:
                    number_of_accounts = int(input())
                except:
                    pass
                finally:
                    break
            manual_creation = input(
                f"{bcolors.WARNING}Do you want to manually enter account credentials? [y/n]: "
            ).lower()

            if manual_creation == "y":
                print("USERNAME SHOULD BE LESS THAN 30 CHARS")
                for i in range(1, number_of_accounts + 1):
                    user_name_acc = input(f"UserName For Acc [{i}]: ")
                    first_name_acc = input(f"FirstName For Acc [{i}]: ")
                    password_acc = input(f"Enter Password For Acc [{i}]: ")
                    print()
                    print("Generating Email And Verifying Account Hold On a Bit..")
                    print()
                    _create_acc()
                    email_acc = mail_addre

                    pray = _insta_gen(
                        email_acc,
                        user_name=user_name_acc,
                        first_name=first_name_acc,
                        password=password_acc,
                    )
                    print(f"{bcolors.OKBLUE}ACCOUNT GEN : PASS")
                    print(f"{bcolors.OKGREEN} ")
            elif manual_creation == "n":
                print(
                    f"\n{bcolors.OKCYAN}AUTO GENERATING {number_of_accounts} ACCOUNTS! [Sit Back And Relax..This may take some time]"
                )
                for i in range(1, number_of_accounts + 1):
                    _create_acc()
                    email_acc_a = mail_addre
                    _insta_gen(
                        email_acc_a,
                        user_name=generate_username(1)[0]
                        + str(random.randint(1, 1000)),
                        first_name=generate_username(1)[0],
                        password=str(pwo.generate())
                        + str(random.randint(1, 999999999999)),
                    )
                    print(f"{bcolors.OKGREEN}[INFO] {i} ACCOUNT GENERATED .")
            else:
                print()
                time.sleep(1)
                print(f"{bcolors.FAIL}What the fuck do you just said? huh ? BYE!")
                time.sleep(2)
                sys.exit()
            sys.exit()
        else:
            print("|ERROR | INVALID ENTRY :<, TRY AGAIN")
            time.sleep(3)
            os.system("cls")  # Change to clear
            continue
else:
    print("You have to run this tool in linux :(")
    for i in range(7, 1, -1):
        print(f"Exiting The Application in {i}", end="\r")
        time.sleep(1)
    sys.exit()
