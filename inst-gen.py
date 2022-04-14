from json import JSONDecodeError
import sys
import pymailtm
from pymailtm.pymailtm import CouldNotGetAccountException
from random_username.generate import generate_username
import os
import random
import time
import argparse
import requests
from password_generator import PasswordGenerator
from datetime import datetime
import platform
from gooey import Gooey, GooeyParser

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
    with requests.Session() as s:
        s.get(link)
        csrf = s.cookies["csrftoken"]
        mid = s.cookies["mid"]

        payload_creation = {
            "enc_password": f"#PWD_INSTAGRAM_BROWSER:0:{time}:{password}",
            "email": email,
            "username": user_name,
            "first_name": first_name,
            "opt_into_one_tap": "false",
            "client_id": mid,
            "seamless_login_enabled": "0",
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

        while 1:
            time.sleep(1.5)
            messages = acc_inst.get_messages()
            try:
                inst_mail = messages[0]
                verification_code = inst_mail.subject[:6]
                break
            except:
                pass
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

    print("STARTED TO CREATE AN ACCOUNT\n")
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


prog_descr = "A Tool Used To Automate Creating Instagram Accounts"


@Gooey(
    menu=[
        {
            "name": "About",
            "items": [
                {
                    "type": "AboutDialog",
                    "menuTitle": "About",
                    "name": "INST-GEN ",
                    "description": "A Program To Automate Creating Instagram Accounts",
                    "version": "v2.0.0",
                    "copyright": "2022",
                    "website": "https://github.com/Zday-X/INSTA-GEN",
                    "developer": "ZDay-X",
                    "license": "MIT",
                }
            ],
        },
        {
            "name": "Informations/Warnings",
            "items": [
                {
                    "type": "MessageDialog",
                    "menuTitle": "About Abusing The Software",
                    "message": "Guys, just because you have the power, dont abuse it :)",
                    "caption": "Do not Abuse The Power!",
                },
                {
                    "type": "MessageDialog",
                    "menuTitle": "Warning About IP Banning",
                    "message": "It is adviced not to create too many accounts continously to prevent IP-BANNING from instagram servers.\nThe recomended Accounts Creation Per day is 200.",
                    "caption": "WARNING",
                },
                {
                    "type": "MessageDialog",
                    "menuTitle": "About Spamming",
                    "message": "This software is created purely for Educational Purposes Only! That is to purely learn about how this tech/algorithm works and just playing with it to gain more knowledge.",
                    "caption": "You had heard this many times, but its my duty to add it here :)",
                },
                {
                    "type": "MessageDialog",
                    "menuTitle": "About Contributing",
                    "message": "You can Help me along with others in the community to add more features to this software!!!\nYou can find the github link in the about section or in the information/warning section.",
                    "caption": "The door is always open!",
                },
                {
                    "type": "Link",
                    "menuTitle": "I Want To Contribute This Software.",
                    "url": "https://github.com/Zday-X/INSTA-GEN",
                },
            ],
        },
    ],
    program_name="INSTA-GEN",
    program_description=prog_descr,
    disable_stop_button=True,
    monospace_display=False,
    navigation="Tabbed",
    tabbed_groups=True,
    image_dir=".",
)
def main():
    parser = GooeyParser(
        description="Automate Creating Instagram Accounts!",
    )

    parser = GooeyParser(description="Automate Creating Instagram Accounts!")

    automate = parser.add_argument_group("Automate")
    automate.add_argument(
        "--Accounts",
        action="store",
        help="Number Of Instagram Accounts You Want To Generate",
    )

    args = parser.parse_args()
    print(f"AUTO GENERATING [ {args.Accounts} ] ACCOUNTS!\n ")
    print("[Sit Back And Relax..This may take some time]\n")
    for i in range(1, int(args.Accounts) + 1):
        _create_acc()
        email_acc_a = mail_addre
        print(f"Using Email: {email_acc_a}")
        _insta_gen(
            email_acc_a,
            user_name=generate_username(1)[0] + str(random.randint(1, 1000)),
            first_name=generate_username(1)[0],
            password=str(pwo.generate()) + str(random.randint(1, 999999999999)),
        )
        print(f"------\n[✔️] {i} ACCOUNT GENERATED .\n------\n")

    print("\n Account Details Are Stored In A File Named [cred.txt]")


if __name__ == "__main__":
    main()
