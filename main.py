from InquirerPy import inquirer
from colorama import init, Fore, Style
import json, os, time

init(autoreset=True)

WALLET_FILE = "wallet.json"
ASSET_FILE = "assets.json"


# ===== Helpers =====
def load_data(file, key):
    if os.path.exists(file):
        with open(file, "r") as f:
            return json.load(f)
    return {key: []}


def save_data(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=2)


# ===== ASCII Banner =====
def banner():
    print(Fore.LIGHTCYAN_EX + Style.BRIGHT + r"""
██████╗░██████╗░░█████╗░██╗░░██╗███████╗
██╔══██╗██╔══██╗██╔══██╗██║░██╔╝██╔════╝
██████╦╝██████╔╝██║░░██║█████═╝░█████╗░░
██╔══██╗██╔══██╗██║░░██║██╔═██╗░██╔══╝░░
██████╦╝██║░░██║╚█████╔╝██║░╚██╗███████╗
╚═════╝░╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝╚══════╝
    """ + Style.RESET_ALL)
    print(Fore.YELLOW + "HODLBook : Track Crypto & All Your Assets\n" + Style.RESET_ALL)


# ===== Loading Animation =====
def loading_animation(text="Loading", duration=1.2):
    dots = 0
    start_time = time.time()
    print(Fore.MAGENTA + text, end="", flush=True)
    while time.time() - start_time < duration:
        print('.', end='', flush=True)
        time.sleep(0.2)
        dots += 1
        if dots == 3:
            print('\b\b\b   \b\b\b', end='', flush=True)
            dots = 0
    print(Style.RESET_ALL)


# ===== Display Portfolio =====
def show_items(data, key):
    if not data[key]:
        print(Fore.RED + "No entries found.")
        return

    loading_animation()

    # Charger le total crypto si on est dans "assets"
    extra_crypto_value_eur = 0
    if key == "assets" and os.path.exists(WALLET_FILE):
        wallets_data = load_data(WALLET_FILE, "wallets")
        total_wallets_usd = sum(w["value"] for w in wallets_data["wallets"])
        extra_crypto_value_eur = total_wallets_usd * 0.85  # conversion USD → EUR
        # Ajouter une entrée fictive dans les assets pour affichage
        data[key].append({
            "id": len(data[key]) + 1,
            "name": "Crypto (total)",
            "category": "Crypto",
            "value": extra_crypto_value_eur
        })

    # Calcul du total en tenant compte des dettes
    total = 0
    for i in data[key]:
        if i.get("category", "").lower() == "debt":
            total -= i["value"]
        else:
            total += i["value"]

    print(Fore.GREEN + f"\n=== {key.upper()} ===\n" + Style.RESET_ALL)

    # Affichage détaillé
    for i in data[key]:
        is_debt = i.get("category", "").lower() == "debt"
        signed_value = -i["value"] if is_debt else i["value"]

        percentage = (abs(signed_value) / abs(total) * 100) if total != 0 else 0
        bar = "█" * int(percentage / 2)

        extra_info = i.get("platform", i.get("category", ""))
        color = Fore.RED if is_debt else Fore.CYAN
        sign = "-" if is_debt else ""

        print(color + f"[{i['id']}] {i['name']} ({extra_info})")
        print(
            Fore.WHITE
            + f"  {sign}${i['value']:,.2f}  ({percentage:.1f}%) "
            + (Fore.LIGHTRED_EX if is_debt else Fore.LIGHTYELLOW_EX)
            + bar
        )
        print(
            Fore.WHITE + f"  Wallet Address : {i['address']}\n  Private Key : {i['key']}\n\n"
        )

    print(Fore.YELLOW + Style.BRIGHT + "╔════════════════════════════╗")
    print(f"║  TOTAL : {total:,.2f}$ (={total*0.85}€)     ║")
    print(Fore.YELLOW + Style.BRIGHT + "╚════════════════════════════╝" + Style.RESET_ALL)

    # Retirer l'entrée crypto fictive pour éviter de l'ajouter en vrai au fichier
    if key == "assets":
        data[key] = [i for i in data[key] if i["name"] != "Crypto (total)"]


# ===== CRUD =====
def add_item(data, key, extra_field):
    name = input("Name: ")
    extra = input(f"{extra_field}: ")
    value = float(input("Value (USD): "))
    new_id = len(data[key]) + 1
    data[key].append({
        "id": new_id,
        "name": name,
        extra_field.lower(): extra,
        "value": value
    })
    save_data(WALLET_FILE if key == "wallets" else ASSET_FILE, data)
    print(Fore.GREEN + "Added successfully!")


def delete_item(data, key):
    item_id = int(input("Enter ID to delete: "))
    data[key] = [i for i in data[key] if i["id"] != item_id]
    save_data(WALLET_FILE if key == "wallets" else ASSET_FILE, data)
    print(Fore.RED + "Deleted.")


def edit_item(data, key, extra_field):
    item_id = int(input("Enter ID to edit: "))
    for i in data[key]:
        if i["id"] == item_id:
            i["name"] = input(f"Name [{i['name']}]: ") or i["name"]
            i[extra_field.lower()] = input(f"{extra_field} [{i[extra_field.lower()]}]: ") or i[extra_field.lower()]
            val = input(f"Value (USD) [{i['value']}]: ")
            if val:
                i["value"] = float(val)
            save_data(WALLET_FILE if key == "wallets" else ASSET_FILE, data)
            print(Fore.GREEN + "Updated!")
            return
    print(Fore.RED + "Not found.")


# ===== Submenu for wallet/assets =====
def manage_section(file, key, extra_field):
    data = load_data(file, key)
    while True:
        action = inquirer.select(
            message=f"\n\n--- Manage {key} ---",
            choices=[
                "Show all",
                f"Add {extra_field}",
                "Edit",
                "Delete",
                "⬅ Back"
            ],
        ).execute()

        if action.startswith("S"):
            show_items(data, key)
        elif action.startswith("A"):
            add_item(data, key, extra_field)
        elif action.startswith("E"):
            edit_item(data, key, extra_field)
        elif action.startswith("D"):
            delete_item(data, key)
        elif action.startswith("⬅"):
            break


# ===== Main Menu =====
def main():
    banner()
    while True:
        action = inquirer.select(
            message="--- Main Menu ---",
            choices=[
                "Assets",
                "Crypto Wallets",
                "Exit"
            ],
        ).execute()

        if action.startswith("C"):
            manage_section(WALLET_FILE, "wallets", "Platform")
        elif action.startswith("A"):
            manage_section(ASSET_FILE, "assets", "Category")
        elif action.startswith("E"):
            print(Fore.MAGENTA + "Goodbye!")
            break


if __name__ == "__main__":
    main()
