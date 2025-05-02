import random
import time
import json
import os
import sys
from datetime import datetime, timedelta
import platform
import re
import select
import requests


if platform.system().lower() == 'windows':
    os.system('color')
    
rarity = {
    "Comum": 3,
    "\033[32mIncomum\033[0m": 5,
    "\033[34mRaro\033[0m": 15,
    "\033[35mEpico\033[0m": 50,
    "\033[33mLendário\033[0m": 100,
    "\033[36mMítico\033[0m": 500,
    "\x1b[38;2;255;0;8mA\x1b[38;2;255;0;8mr\x1b[38;2;255;0;8mc\x1b[38;2;255;0;8ma\x1b[38;2;255;0;8mn\x1b[38;2;255;0;8mo\x1b[0m": 750, # Arcano
    "\x1b[38;2;255;0;30mE\x1b[38;2;252;42;25mx\x1b[38;2;250;85;20mo\x1b[38;2;248;127;15mt\x1b[38;2;246;170;10mi\x1b[38;2;244;212;5mc\x1b[38;2;242;255;0mo\x1b[0m": 2250, # Exotico
    "\x1b[38;2;245;245;181mD\x1b[38;2;246;246;145mi\x1b[38;2;247;247;109mv\x1b[38;2;248;248;73mi\x1b[38;2;249;249;37mn\x1b[38;2;250;250;2mo\x1b[0m": 5000, # Divino
    "\x1b[38;2;255;255;255mC\x1b[38;2;223;255;255me\x1b[38;2;191;255;255ml\x1b[38;2;159;255;255me\x1b[38;2;127;255;255ms\x1b[38;2;95;255;255mt\x1b[38;2;63;255;255mi\x1b[38;2;31;255;255ma\x1b[38;2;0;255;255ml\x1b[0m": 10000, # Celestial
    "\x1b[38;2;103;39;214mA\x1b[38;2;119;62;218mc\x1b[38;2;136;86;223me\x1b[38;2;153;110;227mn\x1b[38;2;170;134;232md\x1b[38;2;186;158;236me\x1b[38;2;203;182;241mn\x1b[38;2;220;206;245mt\x1b[38;2;237;230;250me\x1b[0m": 50000, # Acendente
    "\x1b[38;2;29;179;141mE\x1b[38;2;44;149;148mt\x1b[38;2;59;119;156me\x1b[38;2;74;89;163mr\x1b[38;2;89;59;171mn\x1b[38;2;104;29;179mo\x1b[0m": 100000, # Eterno
    "\x1b[38;2;255;100;0mA\x1b[38;2;255;120;30mn\x1b[38;2;255;140;60mt\x1b[38;2;255;160;90mi\x1b[38;2;255;180;120mg\x1b[38;2;255;200;150mo\x1b[0m": 200000, # Antigo
    "\x1b[38;2;255;253;0mF\x1b[38;2;229;245;8ma\x1b[38;2;203;237;16mb\x1b[38;2;177;229;24mu\x1b[38;2;152;221;32ml\x1b[38;2;126;213;40mo\x1b[38;2;100;205;48ms\x1b[38;2;75;198;57mo\x1b[0m": 400000, # Fabuloso
    "\x1b[38;2;0;200;255mI\x1b[38;2;50;180;240ml\x1b[38;2;100;160;225mu\x1b[38;2;150;140;210ms\x1b[38;2;200;120;195mt\x1b[38;2;250;100;180mr\x1b[38;2;255;80;165me\x1b[0m": 800000, # Ilustre
    "\x1b[38;2;255;215;0mG\x1b[38;2;255;200;30ml\x1b[38;2;255;185;60mo\x1b[38;2;255;170;90mr\x1b[38;2;255;155;120mi\x1b[38;2;255;140;150mo\x1b[38;2;255;125;180ms\x1b[38;2;255;110;210mo\x1b[0m": 1600000, # Glorioso
    "\x1b[38;2;0;255;0mS\x1b[38;2;30;230;30mu\x1b[38;2;60;205;60mp\x1b[38;2;90;180;90mr\x1b[38;2;120;155;120me\x1b[38;2;150;130;150mm\x1b[38;2;180;105;180mo\x1b[0m": 3200000, # Supremo
    "\x1b[38;2;139;69;19mP\x1b[38;2;150;80;30mr\x1b[38;2;161;91;41mi\x1b[38;2;172;102;52mm\x1b[38;2;183;113;63me\x1b[38;2;194;124;74mv\x1b[38;2;205;135;85mo\x1b[0m": 6400000, # Primevo
    "\x1b[38;2;255;0;255mS\x1b[38;2;255;0;170ma\x1b[38;2;255;0;85mg\x1b[38;2;255;0;0mr\x1b[38;2;255;84;0ma\x1b[38;2;255;170;0md\x1b[38;2;255;255;0mo\x1b[0m": 12800000, # Sagrado
    "\x1b[38;2;119;0;255mR\x1b[38;2;127;72;196me\x1b[38;2;136;145;137ml\x1b[38;2;145;218;78mi\x1b[38;2;165;233;42mq\x1b[38;2;195;190;28mu\x1b[38;2;225;147;15mi\x1b[38;2;255;105;2ma\x1b[0m": 25600000, # Reliquia
    "\x1b[38;2;255;255;255mI\x1b[38;2;212;211;212mm\x1b[38;2;169;167;169mo\x1b[38;2;127;124;126mr\x1b[38;2;169;167;169mt\x1b[38;2;212;211;212ma\x1b[38;2;255;255;255ml\x1b[0m": 51200000, # Imortal
    "\x1b[38;2;0;229;0mO\x1b[38;2;85;152;53mn\x1b[38;2;170;76;106mi\x1b[38;2;255;0;160mr\x1b[38;2;233;62;106mi\x1b[38;2;212;126;53mc\x1b[38;2;191;189;0mo\x1b[0m": 102400000, #Onírico
    "\x1b[38;2;0;121;0mA\x1b[38;2;26;90;62ml\x1b[38;2;52;60;124mq\x1b[38;2;78;30;186mu\x1b[38;2;105;0;248mi\x1b[38;2;142;30;249mm\x1b[38;2;180;61;251mi\x1b[38;2;217;92;253mc\x1b[38;2;255;123;255mo\x1b[0m": 204800000, #alquimico
    "\x1b[38;2;255;0;255mI\x1b[38;2;204;27;255mn\x1b[38;2;153;54;255mi\x1b[38;2;102;82;255mg\x1b[38;2;51;109;255mu\x1b[38;2;0;137;255ma\x1b[38;2;27;109;232ml\x1b[38;2;54;82;209ma\x1b[38;2;82;54;186mv\x1b[38;2;109;27;163me\x1b[38;2;137;0;140ml\x1b[0m": 409600000, #Inigualavel
    "\x1b[38;2;73;247;102mI\x1b[38;2;109;238;111mn\x1b[38;2;145;230;121me\x1b[38;2;182;222;130ms\x1b[38;2;218;214;140mt\x1b[38;2;255;206;150mi\x1b[38;2;255;215;120mm\x1b[38;2;255;225;90ma\x1b[38;2;255;235;59mv\x1b[38;2;255;245;30me\x1b[38;2;255;255;0ml\x1b[0m": 819200000, #Inestimavel
    "\x1b[38;2;234;43;102mA\x1b[38;2;238;75;92mr\x1b[38;2;242;108;82mq\x1b[38;2;246;140;72mu\x1b[38;2;250;173;62me\x1b[38;2;255;206;53mt\x1b[38;2;212;186;90mi\x1b[38;2;169;166;127mp\x1b[38;2;125;146;165mi\x1b[38;2;83;126;202mc\x1b[38;2;40;107;240mo\x1b[0m": 1638400000, #Arquetipico
    "\x1b[38;2;71;43;234mA\x1b[38;2;132;113;241mb\x1b[38;2;193;184;248mi\x1b[38;2;255;255;255ms\x1b[38;2;255;205;250ms\x1b[38;2;255;156;245ma\x1b[38;2;255;107;240ml\x1b[0m": 3276800000, #Abissal
    "\x1b[38;2;175;43;183mT\x1b[38;2;145;68;195mr\x1b[38;2;116;94;207ma\x1b[38;2;87;120;219mn\x1b[38;2;58;145;231ms\x1b[38;2;29;171;243mc\x1b[38;2;0;197;255me\x1b[38;2;25;206;212mn\x1b[38;2;50;216;170md\x1b[38;2;76;226;127me\x1b[38;2;102;235;84mn\x1b[38;2;127;245;42mt\x1b[38;2;153;255;0me\x1b[0m": 6553600000, #Trancendente
    "\x1b[38;2;255;255;58mU\x1b[38;2;168;249;67mt\x1b[38;2;81;244;76mo\x1b[38;2;108;173;114mp\x1b[38;2;192;69;166mi\x1b[38;2;218;32;209ma\x1b[38;2;128;128;232mn\x1b[38;2;38;225;255mo\x1b[0m": 13107200000, #Utopiano
    "\x1b[38;2;255;255;58mE\x1b[38;2;255;145;142ms\x1b[38;2;255;36;226mt\x1b[38;2;255;43;182mr\x1b[38;2;255;107;72me\x1b[38;2;242;129;36ml\x1b[38;2;206;64;145ma\x1b[38;2;170;0;255mr\x1b[0m": 26214400000, #Estelar
    "\x1b[38;2;107;109;255mG\x1b[38;2;170;171;255ma\x1b[38;2;233;234;255ml\x1b[38;2;255;255;255ma\x1b[38;2;255;255;255mt\x1b[38;2;234;255;255mi\x1b[38;2;172;255;255mc\x1b[38;2;110;255;255mo\x1b[0m": 52428800000, #Galatico
    "\x1b[38;2;109;0;202mC\x1b[38;2;97;72;223mo\x1b[38;2;85;144;244ms\x1b[38;2;81;195;239mm\x1b[38;2;85;225;207mo\x1b[38;2;89;255;175ms\x1b[0m": 104857600000, #Cosmos
    "\x1b[38;2;161;204;40mM\x1b[38;2;173;178;87mo\x1b[38;2;186;153;135mn\x1b[38;2;199;128;183mu\x1b[38;2;212;103;231mm\x1b[38;2;215;109;232me\x1b[38;2;208;145;187mn\x1b[38;2;201;182;142mt\x1b[38;2;194;218;97ma\x1b[38;2;188;255;52ml\x1b[0m": 419430400000, #Monumental
    "\x1b[38;2;255;0;255mC\x1b[38;2;170;0;232me\x1b[38;2;85;0;209ml\x1b[38;2;0;0;187me\x1b[38;2;0;61;209ms\x1b[38;2;0;124;232mt\x1b[38;2;0;186;255me\x1b[0m": 838860800000, #Celeste
    "\x1b[38;2;62;62;63mO\x1b[38;2;98;100;101mb\x1b[38;2;135;138;139ml\x1b[38;2;172;176;177mi\x1b[38;2;200;203;204mv\x1b[38;2;218;220;221mi\x1b[38;2;236;237;238mo\x1b[38;2;255;255;255mn\x1b[0m": 1677721600000, #Oblivion
    "\x1b[38;2;201;186;126mS\x1b[38;2;201;144;130mu\x1b[38;2;201;103;134mp\x1b[38;2;201;62;139mr\x1b[38;2;201;20;143me\x1b[38;2;189;20;136mm\x1b[38;2;165;61;118ma\x1b[38;2;141;103;99mc\x1b[38;2;117;144;81mi\x1b[38;2;93;186;63ma\x1b[0m": 3355443200000, #Supermacia
    "\x1b[38;2;255;62;63mA\x1b[38;2;210;88;89ms\x1b[38;2;165;115;116mc\x1b[38;2;120;141;142me\x1b[38;2;75;168;169mn\x1b[38;2;31;195;196md\x1b[38;2;45;207;161ma\x1b[38;2;59;219;127mn\x1b[38;2;73;231;92mc\x1b[38;2;87;243;58mi\x1b[38;2;102;255;24ma\x1b[0m": 6710886400000, #Ascendancia
}

raritys = {}
__version__ = "1.8.4" 
upd = "Github no way"
Gamestarts = [0]
raritys = {cat: [0] for cat in rarity}
Rolls = [0]
delay = 0.00001
manual_rolls = 0
auto_rolls = [0]
lucky_event_active = False
lucky_event_end = 0
lucky_event_start = 0
roll_time_history = []
max_history_size = 15
autoclick_detected = False
tolerance = 0.01
debug = False
CheatT = [0]
noprintar = True
mrar = 600
Dhelp = """cl: cheat count reset\nardebug: auto roll no delay mode\nardemodebug: ardebug but you can turn it off by pressing enter"""
multiroll = False
cont = [0]
mod = False
autosave = False
KEY = 42
save_file_path = None
rarity_history = []
login_streak = [0] 
last_login_date = [None]
auto_bet_threshold = 0



def check_for_updates():
    GITHUB_RAW_URL = "https://raw.githubusercontent.com/Shall12eds/Gum/main/gamev1.8.3%20github.py"
    
    try:
        print("\nChecking for updates...")
        
        response = requests.get(GITHUB_RAW_URL)
        response.raise_for_status()
        latest_code = response.text
        
        with open(__file__, 'r', encoding='utf-8') as f:
            local_code = f.read()
            
        if latest_code == local_code:
            print("You already have the latest version!")
            return False
            
        print("\nNew update available!")
        print("Would you like to update now? (Y/N)")
        
        while True:
            choice = input("> ").strip().lower()
            if choice in ['y', 'yes']:
                backup_file = __file__ + ".bak"
                with open(backup_file, 'w', encoding='utf-8') as f:
                    f.write(local_code)
                print(f"Backup created: {backup_file}")
                
                with open(__file__, 'w', encoding='utf-8') as f:
                    f.write(latest_code)
                
                print("Update successful! Restarting...")
                os.execv(sys.executable, [sys.executable] + sys.argv)
                return True
                
            elif choice in ['n', 'no']:
                print("Update cancelled by user.")
                return False
            else:
                print("Please answer with Y (Yes) or N (No):")
                
    except requests.exceptions.RequestException as e:
        print(f"Connection error: {str(e)}")
    except Exception as e:
        print(f"Update failed: {str(e)}")
        print("Please download the update manually from GitHub")
    return False

def xor_encrypt_decrypt(data, key):
    return ''.join(chr(ord(char) ^ key) for char in data)

def show_stats():
    print(f"Rolls: {Rolls[0]}")
    print(f"Automatic Rolls: {auto_rolls[0]}")
    
    for cat, count in raritys.items():
        if count[0] > 0: 
            print(f"{cat}: {count[0]}")
    
    print(f"Cheats detected: {CheatT[0]}")
    print(f"Game starts: {Gamestarts[0]}")

def get_program_directory():
    if getattr(sys, 'frozen', False):  
        return os.path.dirname(sys.executable)
    else: 
        return os.path.dirname(os.path.abspath(__file__))

def ardemodebugstats():
    print("\nAuto roll debug mode with live stats - Press Enter to stop")
    global running_ardemodebug
    running_ardemodebug = True
    clear_line = "\033[K"
    move_up = "\033[F"
    
    try:
        while running_ardemodebug:
            roll()
            
            for _ in range(20):
                print(clear_line, end="")
                print(move_up, end="")
            
            
            show_stats()
            
            while sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                line = sys.stdin.readline()
                if line:
                    running_ardemodebug = False
                    break
                    
    except KeyboardInterrupt:
        running_ardemodebug = False
    
    for _ in range(20):
        print(clear_line, end="")
        print(move_up, end="")
    
    print("Auto roll debug mode stopped\n")

def attempt_auto_bet(rarity_name):
    global auto_bet_threshold
    
    if raritys[rarity_name][0] < auto_bet_threshold:
        return False
    
    next_rarity = get_next_rarity(rarity_name)
    if not next_rarity:
        return False
    
    bet_amount = auto_bet_threshold
    success_chance = (bet_amount / 10) * 100
    
    if random.uniform(0, 100) <= success_chance:
        raritys[rarity_name][0] -= bet_amount
        raritys[next_rarity][0] += 1
        clean_current = re.sub(r'\033\[[0-9;]+m', '', rarity_name)
        clean_next = re.sub(r'\033\[[0-9;]+m', '', next_rarity)
        print(f"\nAuto-bet successful! Converted {bet_amount} {clean_current} to 1 {clean_next}!")
        return True
    else:
        raritys[rarity_name][0] -= bet_amount
        clean_current = re.sub(r'\033\[[0-9;]+m', '', rarity_name)
        print(f"\nAuto-bet failed! Lost {bet_amount} {clean_current}.")
        return False

def save_player_data(filename="player_stats.sav"):
    global save_file_path
    program_dir = get_program_directory()
    save_path = os.path.join(program_dir, filename)
    
    serializable_raritys = {cat: count[0] for cat, count in raritys.items()}
    
    player_data = {
        "Rolls": Rolls[0],
        "Raritys": serializable_raritys,  
        "Manual Rolls": manual_rolls,
        "Cheating": CheatT[0],
        "Auto Rolls": auto_rolls[0],
        "Converted": True,
        "Gamestarts": Gamestarts[0], 
    }
    
    json_data = json.dumps(player_data)
    encrypted_data = xor_encrypt_decrypt(json_data, KEY)
    
    with open(save_path, "w") as file:
        file.write(encrypted_data)
    
    save_file_path = save_path
    print(f"Data saved securely in {save_path}.")

def load_player_data(filename="player_stats.sav"):
    global Rolls, raritys, manual_rolls, auto_rolls, Gamestarts
    
    program_dir = get_program_directory()
    save_path = os.path.join(program_dir, filename)
    
    if os.path.exists(save_path):
        with open(save_path, "r") as file:
            data = file.read()
        
        try:
            decrypted_data = xor_encrypt_decrypt(data, KEY)
            player_data = json.loads(decrypted_data)
            print("Loaded encrypted save file.")
            
            Rolls[0] = player_data.get("Rolls", 0)
            
            saved_rarities = player_data.get("Raritys", {})
            raritys.clear() 
            
            for cat, count in saved_rarities.items():
                if count > 0:  
                    raritys[cat] = [count]
            
            manual_rolls = player_data.get("Manual Rolls", 0)
            auto_rolls[0] = player_data.get("Auto Rolls", 0)
            CheatT[0] = player_data.get("Cheating", 0)
            Gamestarts[0] = player_data.get("Gamestarts", 0)
            
            print(f"Data loaded from {save_path}.")
        except Exception as e:
            print(f"Error loading save file: {e}")
    else:
        print(f"{save_path} not found. No data loaded.")

def delete_player_data(filename="player_stats.sav"):
    global save_file_path
    program_dir = get_program_directory()
    save_path = os.path.join(program_dir, filename)
    
    if os.path.exists(save_path):
        try:
            os.remove(save_path)
            save_file_path = None
            print(f"Save file '{save_path}' deleted successfully.")
        except OSError as e:
            print(f"Error deleting save file: {e}")
    else:
        print(f"Save file '{save_path}' not found. Nothing to delete.")

def show_rarity_distribution():
    obtained = [(re.sub(r'\033\[[0-9;]+m', '', cat), count[0]) 
               for cat, count in raritys.items() if count[0] > 0]
    
    if not obtained:
        print("\nNo rarities obtained yet!")
        return
    
    obtained.sort(key=lambda x: -x[1])
    total = sum(count for _, count in obtained)
    max_name_len = max(len(name) for name, _ in obtained)
    max_count_len = len(str(max(count for _, count in obtained)))
    
    print("\n" + "=" * (max_name_len + max_count_len + 15))
    print(f"RARITY DISTRIBUTION (Total: {total})".center(max_name_len + max_count_len + 15))
    print("=" * (max_name_len + max_count_len + 15))
    
    max_count = obtained[0][1]
    scale = 50 / max_count if max_count > 0 else 1
    
    for name, count in obtained:
        pct = (count / total) * 100
        bar = '#' * int(count * scale)
        print(f"{name:<{max_name_len}} | {count:>{max_count_len}} | {pct:5.1f}% | {bar}")
    
    print("=" * (max_name_len + max_count_len + 15) + "\n")

def get_current_time():
    return datetime.now().strftime("%H:%M:%S")

def is_next_available_rarity(cat):
    clean_rarities = []
    for r in rarity.keys():
        clean_name = re.sub(r'\033\[[0-9;]+m', '', r)
        clean_rarities.append(clean_name)
    
    current_clean = re.sub(r'\033\[[0-9;]+m', '', cat)
    
    if current_clean in clean_rarities:
        current_index = clean_rarities.index(current_clean)
        if current_index > 0:
            previous_rarity = list(rarity.keys())[current_index - 1]
            return previous_rarity in raritys and raritys[previous_rarity][0] > 0
    return False

def redeem():
    program_dir = get_program_directory()
    voucher_file = os.path.join(program_dir, "extra.sav")
    
    if not os.path.exists(voucher_file):
        print("No voucher file found")
        return

    try:
        with open(voucher_file, "r") as f:
            encrypted_data = f.read()
        os.remove(voucher_file)

        decrypted_data = xor_encrypt_decrypt(encrypted_data, KEY)
        voucher = json.loads(decrypted_data)

        rarity_name = voucher["raridade"]
        if rarity_name not in rarity:
            rarity[rarity_name] = voucher["valor"]
            raritys[rarity_name] = [1]  
            print(f"Exclusive rarity unlocked: {rarity_name}!")
        else:
            raritys[rarity_name][0] += 1
            print(f"You already have {rarity_name}. +1 added.")

    except Exception as e:
        print("Error redeeming voucher:", e)
        
def show_save_path():
    if save_file_path:
        print(f"Save file located at: {save_file_path}")
    else:
        print("No save file created yet.")

def calculate_finish_time(added_time, unit):
    now = datetime.now()
    h, m, s = now.hour, now.minute, now.second
    
    if unit == 'h':
        total_h = h + added_time
        h = total_h % 24
    elif unit == 'm':
        total_m = m + added_time
        h += total_m // 60
        m = total_m % 60
        h = h % 24
    elif unit == 's':
        total_s = s + added_time
        m += total_s // 60
        s = total_s % 60
        h += m // 60
        m = m % 60
        h = h % 24
    
    return f"{h:02d}:{m:02d}:{s:02d}"

def show_rarity_percentages():
    print("")
    
    rarity_factor = 0.5 if lucky_event_active else 1
    pet_bonus = pets[active_pet]["bonus"] if active_pet else 0
    
    for cat, value in rarity.items():
        if cat in raritys and (raritys[cat][0] > 0 or is_next_available_rarity(cat)):
            adjusted_value = value * rarity_factor
            if active_pet:
                adjusted_value = adjusted_value / (1 + pet_bonus)
            
            percentage = (1 / adjusted_value) * 100
            
            modifiers_note = ""
            if lucky_event_active or active_pet:
                base_percentage = (1 / value) * 100
                modifiers_note = f" (base: {base_percentage:.19f}%)"
                
                if lucky_event_active:
                    modifiers_note += " + Lucky Event"
                if active_pet:
                    modifiers_note += f" + {active_pet} pet"
            
            print(f"{cat}: {percentage:.19f}%{modifiers_note}")
    
    if lucky_event_active:
        time_left = lucky_event_end - time.time()
        print(f"\nLucky Event active! Time remaining: {time_left:.1f} seconds")
    if active_pet:
        print(f"\nPet active: {active_pet} (+{pet_bonus*100:.0f}% rarity boost)")
    print(" ")

def is_next_available_rarity(cat):
    clean_rarities = []
    for r in rarity.keys():
        clean_name = re.sub(r'\033\[[0-9;]+m', '', r)
        clean_rarities.append(clean_name)
    
    current_clean = re.sub(r'\033\[[0-9;]+m', '', cat)
    
    if current_clean in clean_rarities:
        current_index = clean_rarities.index(current_clean)
        if current_index > 0:
            previous_rarity = list(rarity.keys())[current_index - 1]
            return raritys[previous_rarity][0] > 0
    return False

def roll():
    if autoclick_detected:
        return

    global multiroll, Rolls, db, auto_bet_threshold
    Rolls[0] += 1
    unlock_pets()
    rarity_found = []

    rarity_factor = 0.5 if lucky_event_active else 1
    roll_count = db if multiroll else 1 

    for _ in range(roll_count):
        for cat, max_val in rarity.items():
            adjusted_chance = apply_pet_bonus(max_val * rarity_factor)
            if random.randint(1, int(adjusted_chance)) == 1:
                rarity_found.append(cat)
                if cat not in raritys:
                    raritys[cat] = [0]
                raritys[cat][0] += 1
                rarity_history.append((cat, time.time()))
                
                if auto_bet_threshold > 0 and raritys[cat][0] >= auto_bet_threshold:
                    attempt_auto_bet(cat)
    
    if rarity_found and noprintar:
        print("\n".join(rarity_found))
        
def oroll():

    global multiroll, Rolls, db
    Rolls[0] += 1
    rarity_found = []

    rarity_factor = 1

    for _ in range(1):
        for cat, max_val in rarity.items():
            adjusted_chance = apply_pet_bonus(max_val * rarity_factor)
            if random.randint(1, int(adjusted_chance)) == 1:
                rarity_found.append(cat)
                if cat not in raritys:
                    raritys[cat] = [0]
                raritys[cat][0] += 1
                rarity_history.append((cat, time.time()))

def show_performance_stats(minutes=99999999999999999999):
    global rarity_history

    current_time = time.time()
    recent_rarities = [rarity for rarity, timestamp in rarity_history if current_time - timestamp <= minutes * 60]

    if not recent_rarities:
        print(f"No rarity colected on this game launch yet")
        return

    max_rarity = max(recent_rarities, key=lambda x: list(rarity.keys()).index(x))

    total_rarities = len(recent_rarities)
    print(f"Highest rarity obtained: {max_rarity}")

pets = {
    "Dolly": {"bonus": 0.05, "required_rolls": 5000},  #5%
    "Haru": {"bonus": 0.10, "required_rolls": 7500},  #10%
    "Mel": {"bonus": 0.15, "required_rolls": 10000},  #15%
    "Nego": {"bonus": 0.20, "required_rolls": 20000},  # 20%
    "Mih": {"bonus": 0.50, "required_rolls": 50000},  # 50%
    "Zeeee": {"bonus": 1.00, "required_rolls": 100000},  # 100%
    "Fran": {"bonus": 2.00, "required_rolls": 200000},  # 200%
}


unlocked_pets = []
active_pet = None




def remove_extra_rarity():
    rarity_name = input("Type the name of the extra rarity")
    
    if rarity_name in rarity:
        del rarity[rarity_name]
        del raritys[rarity_name]
        print("Done")
    else:
        print("Error, the rarity doesnt exist in game")
        
def add_pet():

    pet_name = input("New pet name: ")
    pet_bonus = float(input("Pet bonus (ex: 0.05 to 5%): "))
    required_rolls = int(input("Requires rolls: "))

    pets[pet_name] = {"bonus": pet_bonus, "required_rolls": required_rolls}
    print(f"New pet added: {pet_name} bonus: {pet_bonus * 100 - 100}% rarity boost and {required_rolls} rolls for unlock.")

def print_animated_gradient(text, gradient_code):
    print("\033[F\033[K", end="")
    colored_text = ""
    for i, char in enumerate(text):
        colored_text += gradient_code[i] + char + "\x1b[0m"
        print(colored_text + text[i+1:], end='\r')
        time.sleep(0.11)

def ardemodebug():
    print("Auto roll debug mode started. Press Enter to stop.")
    global running_ardemodebug
    running_ardemodebug = True
    
    try:
        while running_ardemodebug:
            oroll()
            
            try:
                if platform.system() == 'Windows':
                    import msvcrt
                    if msvcrt.kbhit():
                        if msvcrt.getch() == b'\r':
                            running_ardemodebug = False
                            break
                else:
                    import sys, select
                    if select.select([sys.stdin], [], [], 0)[0]:
                        if sys.stdin.readline().strip() == '':
                            running_ardemodebug = False
                            break
            except:
                pass
                
    except KeyboardInterrupt:
        running_ardemodebug = False
    
    print("Auto roll debug mode stopped\n")

def unlock_pets():
    for pet, data in pets.items():
        if Rolls[0] >= data["required_rolls"] and pet not in unlocked_pets:
            unlocked_pets.append(pet)
            print(f"Pet unlocked: {pet}")

def apply_pet_bonus(base_chance):
    if active_pet:
        bonus = pets[active_pet]["bonus"]
        return base_chance / (1 + bonus)
    return base_chance

def choose_pet():
    if not unlocked_pets:
        print("No pets unlocked yet")
        return

    print("Pets:")
    for index, pet in enumerate(unlocked_pets, start=1):
        print(f"{index}. {pet}")

    choice = int(input("Chose a pet by number (or 0 para cancel): "))
    if 0 < choice <= len(unlocked_pets):
        global active_pet
        active_pet = unlocked_pets[choice - 1]
        print(f"Pet activated: {active_pet}")

def aroll():
    auto_rolls[0] += 1
    rarity_found = []

    rarity_factor = 0.5 if lucky_event_active else 1

    for cat, max_val in rarity.items():
        adjusted_chance = apply_pet_bonus(max_val * rarity_factor)
        result = random.randint(1, int(adjusted_chance))

        if result == 1:
            rarity_found.append(cat)
            raritys[cat][0] += 1
            
    if rarity_found:
        if noprintar == True:
            print("\n".join(rarity_found))
        else:
            pass
    else:
        pass



    if rarity_found:
        if noprintar == True:
            print("\n".join(rarity_found))
        else:
            pass
    else:
        pass

def show_stats():
    print(f"Rolls: {Rolls[0]}")
    print(f"Automatic Rolls: {auto_rolls[0]}")
    
    obtained_rarities = {cat: count for cat, count in raritys.items() if count[0] > 0}
    
    if not obtained_rarities:
        print("No rarities obtained yet!")
    else:
        for cat, count in obtained_rarities.items():
            print(f"{cat}: {count[0]}")
    
    print(f"Cheats detected: {CheatT[0]}")
    print(f"Game starts: {Gamestarts[0]}")
    
def start_lucky_event():
    global lucky_event_active, lucky_event_start, lucky_event_end
    lucky_event_active = True
    lucky_event_start = time.time()
    print("Lucky time!!!")
    lucky_event_end = lucky_event_start + random.randint(8, 12)

def get_next_rarity(current_rarity):
    all_rarities = list(rarity.keys())
    
    try:
        current_index = all_rarities.index(current_rarity)
        if current_index + 1 < len(all_rarities):
            return all_rarities[current_index + 1]
    except ValueError:
        pass
    
    return None

def mini_bet():
    print("You can trade lower rarities for a chance to get a higher rarity.")
    print("Requirements: 10 of the same rarity to guarantee the upgrade, or fewer for lower chances.")
    
    available_rarities = []
    print("\nAvailable rarities for betting:")
    
    rarity_mapping = {}
    for i, (original_name, count) in enumerate(raritys.items(), start=1):
        if count[0] > 0:
            clean_name = re.sub(r'\033\[[0-9;]+m', '', original_name)
            rarity_mapping[str(i)] = original_name
            print(f"{i}. {clean_name}: {count[0]} available")
    
    if not rarity_mapping:
        print("You don't have any rarities to bet!")
        return
    
    try:
        choice = input("\nEnter the number of the rarity you want to bet: ")
        if choice not in rarity_mapping:
            print("Invalid number.")
            return
            
        chosen_rarity = rarity_mapping[choice]
        clean_name = re.sub(r'\033\[[0-9;]+m', '', chosen_rarity)
        current_count = raritys[chosen_rarity][0]
        
        bet_amount = int(input(f"How much {clean_name} want to bet? (Max: 10): "))
        if bet_amount <= 0 or bet_amount > 10 or bet_amount > current_count:
            print("Invalid amount.")
            return

        success_chance = (bet_amount / 10) * 100
        print(f"\nYou will have {success_chance:.2f}% chance to obtain a better rarity")
        
        confirm = input("Continue? (Yes/No): ").lower()
        if confirm != "yes":
            print("Bet cancelled")
            return
        
        raritys[chosen_rarity][0] -= bet_amount
        if random.uniform(0, 100) <= success_chance:
            next_rarity = get_next_rarity(chosen_rarity)
            if next_rarity:
                if next_rarity not in raritys:
                    raritys[next_rarity] = [0]
                raritys[next_rarity][0] += 1
                clean_next = re.sub(r'\033\[[0-9;]+m', '', next_rarity)
                print(f"\nCongratulations! You now have a {clean_next}!")
            else:
                print("\nYou already have the highest rarity!")
                raritys[chosen_rarity][0] += bet_amount
        else:
            print("\nHow unfortunate... You lost your bet.")
            
    except ValueError:
        print("Please enter a valid number.")

lucky_event_active = False
lucky_event_start = 0
lucky_event_end = 0
manual_rolls = 0

def start_lucky_event():
    global lucky_event_active, lucky_event_start, lucky_event_end
    if lucky_event_active:
        return
    
    lucky_event_active = True
    lucky_event_start = time.time()
    lucky_event_end = lucky_event_start + random.randint(8, 12)

    print("Lucky time!!!")
    print("Go!!!!")

def calculate_event_chance():
    base_chance = 1000
    reduction = (manual_rolls // 10) * 50 
    current_chance = max(base_chance - reduction, 100)  
    return current_chance

def auto_start_lucky_event():
    global lucky_event_active
    if not lucky_event_active:  
        current_chance = calculate_event_chance()
        if random.randint(1, current_chance) == 1:
            start_lucky_event()

def check_lucky_event():
    global lucky_event_active
    if lucky_event_active and time.time() > lucky_event_end:
        lucky_event_active = False
        print("Lucky ran out!")

def encrypt_decrypt(data, key):
    encrypted = ''.join(chr(ord(char) ^ key) for char in data)
    return encrypted

def backup_rarities(filename="rarity_backup.sav"):
    program_dir = get_program_directory()
    backup_path = os.path.join(program_dir, filename)
    
    backup_data = {cat: count[0] for cat, count in raritys.items() if count[0] > 0}
    
    if not backup_data:
        print("No rarities to backup!")
        return
    
    json_data = json.dumps(backup_data)
    encrypted_data = xor_encrypt_decrypt(json_data, KEY)
    
    with open(backup_path, "w") as file:
        file.write(encrypted_data)
    
    print(f"Rarities backed up to {backup_path}")

def restore_backup(filename="rarity_backup.sav"):
    """Restore rarity counts from backup file"""
    program_dir = get_program_directory()
    backup_path = os.path.join(program_dir, filename)
    
    if not os.path.exists(backup_path):
        print(f"No backup file found at {backup_path}")
        return
    
    with open(backup_path, "r") as file:
        data = file.read()
    
    try:
        decrypted_data = xor_encrypt_decrypt(data, KEY)
        backup_data = json.loads(decrypted_data)
        
        for cat in raritys:
            raritys[cat][0] = 0
            
        for cat, count in backup_data.items():
            if cat in raritys:
                raritys[cat][0] = count
            else:
                raritys[cat] = [count]
                if cat not in rarity:
                    rarity[cat] = 100
                    print(f"Restored unknown rarity: {cat}")
        
        print("Rarities restored from backup!")
        print(f"Total rarities restored: {sum(count for count in backup_data.values())}")
        
    except Exception as e:
        print(f"Error restoring backup: {e}")

def auto_backup():
    """Automatically create backup if significant changes detected"""
    global last_backup_time
    
    current_time = time.time()
    if 'last_backup_time' not in globals() or current_time:
        backup_rarities()
        last_backup_time = current_time

def detect_regular_intervals():
    global autoclick_detected, CheatT
    if len(roll_time_history) < max_history_size:
        return False

    intervals = [roll_time_history[i+1] - roll_time_history[i] for i in range(len(roll_time_history) - 1)]
    
    first_interval = intervals[0]
    if all(abs(interval - first_interval) <= tolerance for interval in intervals):
        autoclick_detected = True
        print("Autoclick pattern detected! No more rolls allowed. Program will now terminate.")
        CheatT[0] += 1
        save_player_data()
        time.sleep(2)
        sys.exit()
    return False

def detect_autoclick():
    global roll_time_history, autoclick_detected, CheatT

    current_time = time.time()
    roll_time_history.append(current_time)

    if len(roll_time_history) > max_history_size:
        roll_time_history.pop(0)

    if len(roll_time_history) >= max_history_size:
        intervals = [roll_time_history[i+1] - roll_time_history[i] for i in range(len(roll_time_history) - 1)]
        first_interval = intervals[0]

        if all(abs(interval - first_interval) <= tolerance for interval in intervals):
            autoclick_detected = True
            print("Autoclick pattern detected! No more rolls allowed. Program will now terminate.")
            CheatT[0] += 1
            save_player_data()
            time.sleep(2)
            sys.exit()

def mega_bet():
    print("\n=== MEGA BET ===")
    print("Will automatically bet ALL available rarities at once")
    print("You choose how many items to use per bet (chance = items×10%)")
    
    try:
        items_per_bet = int(input("How many items per bet? (1-10): "))
        if items_per_bet < 1 or items_per_bet > 10:
            print("Please enter a number between 1 and 10")
            return
    except ValueError:
        print("Invalid input. Please enter a number.")
        return
    
    print(f"\nEach bet will use {items_per_bet} items with {items_per_bet*10}% chance")
    print("Continue? (yes/no)")
    
    confirm = input().lower()
    if confirm != 'yes':
        print("Mega Bet cancelled!")
        return
    
    upgrades_made = 0
    total_bets = 0
    
    sorted_rarities = sorted(rarity.keys(), key=lambda x: list(rarity.keys()).index(x))
    
    for current_rarity in sorted_rarities:
        if current_rarity not in raritys or raritys[current_rarity][0] < items_per_bet:
            continue
            
        next_rarity = get_next_rarity(current_rarity)
        if not next_rarity:
            continue
            
        max_bets = raritys[current_rarity][0] // items_per_bet
        if max_bets < 1:
            continue
            
        clean_name = re.sub(r'\033\[[0-9;]+m', '', current_rarity)
        print(f"\nProcessing {clean_name}...")
        
        for _ in range(max_bets):
            total_bets += 1
            raritys[current_rarity][0] -= items_per_bet
            if random.uniform(0, 100) <= (items_per_bet * 10):
                raritys[next_rarity][0] += 1
                upgrades_made += 1
                clean_next = re.sub(r'\033\[[0-9;]+m', '', next_rarity)
                print(f"Success! Converted {items_per_bet} {clean_name} to 1 {clean_next}")
            else:
                print(f"Failed! Lost {items_per_bet} {clean_name}")
    
    print("\n=== Mega Bet Results ===")
    print(f"Items used per bet: {items_per_bet}")
    print(f"Success chance per bet: {items_per_bet*10}%")
    print(f"Total bets made: {total_bets}")
    print(f"Successful upgrades: {upgrades_made}")
    print(f"Failed bets: {total_bets - upgrades_made}")
    print(f"Total items consumed: {total_bets * items_per_bet}")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    
def auto_save(filename="player_stats.sav"):
    if Rolls[0] % 5 == 0 and autosave == "True":
        auto_backup()
        player_data = {
            "Rolls": Rolls[0],
            "Raritys": {cat: count[0] for cat, count in raritys.items()},
            "Manual Rolls": manual_rolls,
            "Cheating": CheatT[0],
            "Auto Rolls": auto_rolls[0]
        }
        json_data = json.dumps(player_data)
        encrypted_data = xor_encrypt_decrypt(json_data, KEY)
    
        with open(filename, "w") as file:
            file.write(encrypted_data)
    
        save_file_path = os.path.abspath(filename)
    



def check_for_updates():
    GITHUB_RAW_URL = "https://raw.githubusercontent.com/Shall12eds/Gum/refs/heads/main/gamev1.8.3%20github.py?token=GHSAT0AAAAAADDHE7U7VSRYXDHXCCXJTUJE2AVH7CA"
    
    try:
        print("\Checking for updates...")
        
        response = requests.get(GITHUB_RAW_URL)
        response.raise_for_status()
        latest_code = response.text
        
        with open(__file__, 'r', encoding='utf-8') as f:
            local_code = f.read()
            
        if latest_code == local_code:
            print("You already have the latest version!")
            return False
            
        print("NEW UPDATE AVAILABLE!")
        print("Would you like to update now? (Y/N)")
        
        while True:
            choice = input("> ").strip().lower()
            if choice in ['y', 'yes']:
                print("Downloading update...")
                backup_path = f"{__file__}.bak"
                with open(backup_path, 'w', encoding='utf-8') as f:
                    f.write(local_code)
                
                with open(__file__, 'w', encoding='utf-8') as f:
                    f.write(latest_code)
                
                print("Update complete! Restarting...")
                os.execv(sys.executable, [sys.executable] + sys.argv)
                return True
                
            elif choice in ['n', 'no']:
                print("Update cancelled by user.")
                return False
            else:
                print("Please answer with Y (Yes) or N (No):")
                
    except requests.exceptions.RequestException as e:
        print(f"Failed to check for updates: {str(e)}")
        return False
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False


# elif RNG.lower() == "update":
#     check_for_updates()

print(r"""

 __                       __                _             
/__  _. ._ _    |_       (_  |_   _. | | /|  )  _   _|  _ 
\_| (_| | | |   |_) \/   __) | | (_| | |  | /_ (/_ (_| _> 
                    /                                     
                    enter for start
""")
o = input("")
if o.lower() == "shall12eds":
    time.sleep(1.5)
    print("\033[F\033[K", end="")
    
    gradient_options = [
        ["\x1b[38;2;255;0;255m", "\x1b[38;2;232;0;255m", "\x1b[38;2;209;0;255m", 
         "\x1b[38;2;187;0;255m", "\x1b[38;2;164;0;255m", "\x1b[38;2;164;17;226m",
         "\x1b[38;2;187;51;170m", "\x1b[38;2;209;86;113m", "\x1b[38;2;232;120;56m",
         "\x1b[38;2;255;155;0m"],
        
        ["\x1b[38;2;0;0;255m", "\x1b[38;2;0;28;226m", "\x1b[38;2;0;56;198m",
        "\x1b[38;2;0;85;170m", "\x1b[38;2;0;113;141m", "\x1b[38;2;0;141;113m",
        "\x1b[38;2;0;170;85m", "\x1b[38;2;0;198;56m", "\x1b[38;2;0;226;28m",
        "\x1b[38;2;0;255;0m"],

        ["\x1b[38;2;65;27;204m", "\x1b[38;2;83;26;201m", "\x1b[38;2;101;25;198m",
        "\x1b[38;2;119;24;195m", "\x1b[38;2;137;23;192m", "\x1b[38;2;155;22;189m",
        "\x1b[38;2;173;21;186m", "\x1b[38;2;191;20;183m", "\x1b[38;2;209;19;180m",
        "\x1b[38;2;227;18;178m"],

        ["\x1b[38;2;255;0;0m", "\x1b[38;2;255;153;0m", "\x1b[38;2;203;255;0m",
        "\x1b[38;2;51;255;0m", "\x1b[38;2;0;255;102m", "\x1b[38;2;0;255;255m",
        "\x1b[38;2;0;102;255m", "\x1b[38;2;50;0;255m", "\x1b[38;2;204;0;255m",
        "\x1b[38;2;255;0;152m"],

    ]
    
    selected_gradient = random.choice(gradient_options)
    
    print_animated_gradient("shall12eds", selected_gradient)
    debug = True
    time.sleep(1)
    print("Welcome to debug mode")
    print("Type Dhelp for Debug commands\n")
    mod = True
    noprintar = True
    autosave = True
    load_player_data(filename="player_stats.sav")
    for cat in list(raritys.keys()):
        if cat not in rarity:
            rarity[cat] = 100
    Gamestarts[0] += 1
else:
    print("Let's go Gambling!!!!")
    print("Type Help for commands")
while True:
    
    if CheatT[0] >= 3:
        print("You cheated 3 times deleting save file....\n")
        delete_player_data()
        sys.exit()
    time.sleep (0.000001)
    RNG = input("")
    time.sleep (0.000001)
    if RNG == "":
        detect_autoclick()
        auto_start_lucky_event()
        roll()
        check_lucky_event()
        auto_save()
    elif RNG.lower() == "stats":
        print(" ")
        show_stats()
    elif RNG.lower() == "redeem":
        redeem()
        
    elif RNG.lower() == "clear":
        clear_screen()
        
        
    elif RNG.lower() == "ar":
        if Rolls[0] >= mrar:
            tm = int(input("time in minutes: "))
            tm = tm * 60
            start_time = time.time()
            print(f"Started at {get_current_time()}") 
            while time.time() - start_time < tm:
                RNG = ""
                time.sleep(delay)
                delay += 0.00002
                aroll()
                auto_save()
        else:
            print(f"Need more {mrar - Rolls[0]} manual rolls for auto roll")


    elif RNG == "ardebug":
        if debug:
            while True:
                ttm = input("seg, min or h? ").lower()
                if ttm == "seg":
                    tm = float(input("How many seconds?\n "))
                    start_time = time.time()
                    print(f"Started at {get_current_time()}")
                    if not autosave:
                        while time.time() - start_time < tm:
                            oroll()
                    else:
                        while time.time() - start_time < tm:
                            oroll()
                            auto_save()
                    break
                elif ttm == "min":
                    tm = float(input("How many minutes?\n ")) * 60
                    start_time = time.time()
                    print(f"Started at {get_current_time()}")
                    if not autosave:
                        while time.time() - start_time < tm:
                            oroll()
                    else:
                        while time.time() - start_time < tm:
                            oroll()
                            auto_save()
                    break
                elif ttm == "h":
                    tm = float(input("How many hours?\n ")) * 3600
                    start_time = time.time()
                    print(f"Started at {get_current_time()}")
                    if not autosave:
                        while time.time() - start_time < tm:
                            oroll()
                    else:
                        while time.time() - start_time < tm:
                            oroll()
                            auto_save()
                    break
                else:
                    print("Error")
                    break
                break
                print("Error")

    elif RNG.lower() == "rarity":
        print(" ")
        show_rarity_percentages()
        print(" ")

    elif RNG.lower() == "rdelayar":
        delay = 0.0001
        print("Auto roll delay reseted")

    elif RNG.lower() == "save":
        save_player_data()

    elif RNG.lower() == "load":
        load_player_data()
        
    elif RNG.lower() == "backup":
        backup_rarities()
    
    elif RNG.lower() == "restore":
        restore_backup()
    
    elif RNG.lower() == "delete":
        delete_player_data()

    elif RNG.lower() == "statistics":
        show_rarity_distribution()
        show_performance_stats()
    
    elif RNG.lower() == "dhelp":
        if debug == True:
            print(Dhelp)
    elif RNG.lower() == "cl":
        if debug == True:
            CheatT.clear()
            CheatT = [0]
            print("Cheat count reset")
    elif RNG.lower() == "upd":
        print("")
        print(upd)
    elif RNG.lower() == "ardemodebug":
        if debug:
            ardemodebug()
    elif RNG.lower() == "savepath":
        show_save_path()
        
    elif RNG.lower() == "ardemodebugstats":
        if debug:
            ardemodebugstats()
    elif RNG.lower() == "bet":
        mini_bet()
        
    elif RNG.lower() == "addpet":
        if debug == True:
            add_pet()
            
    elif RNG.lower() == "pets":
        choose_pet()
        
    elif RNG.lower() == "eredeem":
        remove_extra_rarity()
        
    elif RNG.lower() == "megabet":
        mega_bet()
    elif RNG.lower() == "multiroll":
        if debug == True:
            multiroll = True
            db = int(input("Enter roll per enter:\n"))
    elif RNG.lower() == "update":
        check_for_updates()
    elif RNG.lower() == "disablemultiroll":
        if multiroll:
            multiroll = False
            print("Multi-roll mode deactivated.")
        else:
            print("Multi-roll mode is not active.")
            
    elif RNG.lower() == "activepet":
        if active_pet:
            print(f"Active Pet:: {active_pet}")
        else:
            print("No pet active")
            
    elif RNG.lower() == "config":
        while True:
            print("Options\n1:Display rarity\n2:Autosave\n3:Auto-bet")
            configopt = int(input("\n"))
            if configopt == 1:
                performode = input("(12% roll boost) Display rarity for auto Roll\n True\n False\n\n")
                if performode.lower() == "true":
                    noprintar = True
                    print("Roll display enabled")
                    break
                elif performode.lower() == "false":
                    noprintar = False
                    print("Auto roll display disabled")
                    break
                else:
                    print("Error")
                    break
            elif configopt == 2:
                savi = input("Auto-save \nTrue \nFalse\n\n")
                if savi.lower() == "false":
                    autosave = False
                    print("Auto-save disabled")
                    break
                elif savi.lower() == "true":
                    autosave = True
                    print("Auto-save enabled")
                    break
                else:
                    print("Error")
                    break
            elif configopt == 3:
                print("Auto-betting will automatically attempt to upgrade rarities when you have enough")
                threshold = input("Set threshold (1-10, 0 to disable): ")
                try:
                    threshold = int(threshold)
                    if 0 <= threshold <= 10:
                        auto_bet_threshold = threshold
                        if threshold > 0:
                            print(f"Auto-betting enabled with threshold {threshold}")
                        else:
                            print("Auto-betting disabled")
                        break
                    else:
                        print("Please enter a number between 0 and 10")
                except ValueError:
                    print("Please enter a valid number")
                
    elif RNG.lower() == "help":
        print(f"""
Available commands:

enter: performs a roll

stats: displays roll and rarity statistics

clear: clears the screen

ar: activates auto roll

rarity: shows the percentage chance for each rarity

save: saves the player's data

load: loads saved player data

delete: deletes saved player data

help: displays this list of commands

upd: displays last update

config: game config options
  1: Display rarity settings
  2: Auto-save settings
  3: Auto-betting (automatically bet when you have X of a rarity)

pets: show pets

activatepet: activate a pet

rdelayar: reset auto-roll delay

savepath: show where the save is located

bet: bet your rarity

statistics: show the best rarity rolled afeter the game launch

redeem: get a new rarity if you recieved a rarity file by the dev

backup: make a second save for your progress

restore: load the backup save

megabet: bet all at once

""")
    
    
    
