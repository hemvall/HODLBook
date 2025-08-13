import json
import os
import sys
import time
from colorama import init, Fore, Style

# Init colorama
init(autoreset=True)

FILE = "wallet.json"

def ascii_banner():
    print(Fore.LIGHTRED_EX + Style.BRIGHT + r"""
⡶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⢶
⡇⠀⠀⠀⠀⠀⠀⠀                                                      ⡇
⡇⠀        ██████╗░██████╗░░█████╗░██╗░░██╗███████╗             ⡇⠀
⡇⠀        ██╔══██╗██╔══██╗██╔══██╗██║░██╔╝██╔════╝             ⡇⠀
⡇⠀        ██████╦╝██████╔╝██║░░██║█████═╝░█████╗░░             ⡇⠀
⡇⠀        ██╔══██╗██╔══██╗██║░░██║██╔═██╗░██╔══╝░░             ⡇
⡇⠀        ██████╦╝██║░░██║╚█████╔╝██║░╚██╗███████╗             ⡇⠀
⡇⠀        ╚═════╝░╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝╚══════╝             ⡇⠀
⡇⠀                                                            ⡇⠀
⡷⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⢶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⡾
⠀⠀⠀⠉⠉⠉⠉⣽⡿⠁⣠⣾⡿⠾⣯⣿⠿⠯⢭⣉⠉⠉⠉⠉⣉⣭⣿⡯⠽⠯⢭⣟⡫⣽⣿⣁⣠⣦⣄⠉⠳⣿⣍⠉⠉⠉⠉⠉⠁⠀
⠀⠀⠀⠀⠀⠀⢸⣿⠃⢠⣿⣿⣴⣾⠿⠛⠋⠉⠛⠲⠯⣵⣶⡯⠟⠋⢁⣀⣠⣤⣤⣬⣽⣾⣿⣿⣻⣿⣿⣷⣄⠘⣿⡄⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢸⣿⠀⢸⣿⡿⠛⢁⣤⠶⠛⠋⠉⠉⠛⠻⢿⠤⡴⠞⠛⣉⣽⠿⠛⢉⣠⣤⣤⢤⣝⣿⣿⣿⣿⡄⢸⣿⡀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢸⡇⠀⢸⡏⠀⠰⠋⠁⠀⠀⢀⣤⣶⣾⣿⣿⡤⠤⠤⣾⣋⢀⡤⠞⢫⣿⣿⣿⣷⡄⠉⠻⣿⣿⡇⠀⣿⠁⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢸⡇⠀⢸⣇⠀⠀⠀⢀⣠⠾⢋⡵⢋⣿⢻⣿⠿⣶⡄⠀⢹⠋⠀⠀⣿⣿⢿⣧⣿⣿⣀⣠⣿⣿⠁⠀⣿⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢸⡇⠀⢸⣿⠀⠀⠚⠛⣷⡞⠋⠀⢸⣿⣟⢿⣶⣿⣧⣠⡿⣤⣤⣤⣽⡿⠿⠛⠛⢉⣿⣿⣿⡿⠀⠀⣿⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢸⡇⠀⠈⣿⠀⠀⠀⣀⣀⣉⣻⣶⣤⣿⣿⠿⠟⠛⠉⠁⠀⠀⠀⠀⣀⣀⣠⣤⠾⠋⢉⣿⣿⡇⠀⠀⣿⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢸⡇⠀⠀⣿⡆⢠⣾⠋⠉⣩⣉⣉⣙⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⢛⣉⣉⣡⣤⡶⠾⣿⣿⣿⠁⠀⢠⣿⡄⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢸⣇⠀⠀⢻⡇⠈⠛⠶⣦⣬⣉⣉⣙⡛⠛⠛⠛⠛⠛⠛⠛⠛⢛⣛⣉⣉⣉⣠⣤⣶⣿⠟⠁⠀⢀⣾⡿⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢸⣿⠀⠀⠘⣿⣤⡀⠀⠀⠈⠉⠉⠉⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠋⠉⠉⠉⢁⣠⣼⣏⠀⣀⣴⡿⠋⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠈⣿⣧⠀⠀⠘⢿⣿⢷⣦⣄⣀⠀⠀⠀⠀⠀⣀⣀⣀⣀⣀⣀⣀⣠⣤⣶⠿⠛⠉⢨⣿⣿⠟⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠘⣿⣧⡀⠀⠀⣿⠀⠈⠉⠛⠛⠿⠿⠿⠿⠛⠛⠛⠛⠛⠛⠛⠋⠉⠀⠀⠀⠀⠈⠛⢾⣢⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣾⡿⢿⣦⣴⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⣿⠄⠀⠀⠀⠀
    """ + Style.RESET_ALL)
    print(Fore.YELLOW + "        HODLBook : Your Ultimate Crypto Portfolio Tracker\n" + Style.RESET_ALL)

def loading_animation(text="Loading portfolio", duration=2.5, speed=0.1):
    dots = 0
    start_time = time.time()
    sys.stdout.write(Fore.MAGENTA + Style.BRIGHT + text)
    sys.stdout.flush()
    while time.time() - start_time < duration:
        sys.stdout.write('.')
        sys.stdout.flush()
        time.sleep(speed)
        dots += 1
        if dots == 3:
            sys.stdout.write('\b\b\b   \b\b\b')
            dots = 0
    print(Style.RESET_ALL)

def load_wallet():
    if os.path.exists(FILE):
        with open(FILE, "r") as f:
            return json.load(f)
    else:
        return {"wallets": []}

def save_wallet(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=2)

def show_wallet(wallet):
    total_usd = 0
    total_eur = 0
    print(Fore.GREEN + Style.BRIGHT + "\n=== PORTFOLIO ===" + Style.RESET_ALL)

    if not wallet["wallets"]:
        print(Fore.RED + "No wallets found. Add one to get started.\n")
        return

    for w in wallet["wallets"]:
        print(Fore.CYAN + f'[{w["id"]}] ' + Fore.WHITE + f'{w["name"]} {Fore.YELLOW}({w["platform"]})')
        print(Fore.MAGENTA + f'  Address: {Fore.WHITE}{w["address"]}')
        print(Fore.GREEN + f'  Value: {Fore.WHITE}${w["value"]}\n')
        total_usd += w["value"]

    total_eur = total_usd * 0.85
    print(Fore.YELLOW + Style.BRIGHT + f"""
████████████████████████████████████████████████████████████████
█   Total USD: {Fore.WHITE}${total_usd:,.2f}                                         {Fore.YELLOW}█
█   Total EUR: {Fore.WHITE}€{total_eur:,.2f}                                         {Fore.YELLOW}█
████████████████████████████████████████████████████████████████
    \n""")

def add_wallet(wallet):
    name = input(Fore.CYAN + "Wallet Name: ")
    platform = input(Fore.CYAN + "Platform: ")
    address = input(Fore.CYAN + "Address: ")
    try:
        value = float(input(Fore.CYAN + "Value (USD): "))
    except ValueError:
        print(Fore.RED + "Invalid value, setting to 0.")
        value = 0

    new_id = len(wallet["wallets"]) + 1
    wallet["wallets"].append({
        "id": new_id,
        "name": name,
        "platform": platform,
        "address": address,
        "value": value
    })
    save_wallet(wallet)
    print(Fore.GREEN + "Wallet added successfully!")

def delete_wallet(wallet):
    try:
        wallet_id = int(input(Fore.CYAN + "Enter wallet ID to delete: "))
    except ValueError:
        print(Fore.RED + "Invalid ID.")
        return
    wallet["wallets"] = [w for w in wallet["wallets"] if w["id"] != wallet_id]
    save_wallet(wallet)
    print(Fore.GREEN + f"Wallet {wallet_id} deleted.")

def menu():
    wallet = load_wallet()
    while True:
        print(Fore.YELLOW + "\n--- MENU ---")
        print("1. Show portfolio")
        print("2. Add wallet")
        print("3. Delete wallet")
        print("4. Exit")
        choice = input(Fore.CYAN + "Choose an option: ")

        if choice == "1":
            show_wallet(wallet)
        elif choice == "2":
            add_wallet(wallet)
        elif choice == "3":
            delete_wallet(wallet)
        elif choice == "4":
            print(Fore.MAGENTA + "Goodbye!")
            break
        else:
            print(Fore.RED + "Invalid choice.")

def main():
    ascii_banner()
    loading_animation()
    menu()

if __name__ == "__main__":
    main()
