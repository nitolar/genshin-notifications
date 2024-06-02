import dotenv, os, pyttsx3, pytz, datetime, psutil
import genshinstats as gs
from win10toast import ToastNotifier
from multiprocessing import Process
from time import sleep, localtime, strftime

dotenv.load_dotenv(dotenv_path="settings.env")
toaster = ToastNotifier()
engine = pyttsx3.init()
os.system("") # To make colors in errors always work

if os.getenv('set_cookies_method') == 'auto':
    gs.set_cookie_auto()
elif os.getenv('set_cookies_method') == 'login':
    if os.getenv('ltuid') == 0 or os.getenv('ltoken') == "":
        print("\33[31mIncorrect ltuid or ltoken empty!\033[0m")
        exit()
    else:
        gs.set_cookie(ltuid=int(os.getenv('ltuid')), ltoken=os.getenv('ltoken'))
else:
    print("\33[31mIncorrect value for \"set_cookies_method\"! \n\33[93mSet it to: \"login\" or \"auto\"\033[0m")
    exit()

if os.getenv("server") not in ["eu", "us", "as"]:
    print("\33[31mIncorrect value for \"server\"! \n\33[93mSet it to on of this values: \"eu\", \"us\", \"as\"\033[0m")
    exit()

def resin():
    resin_notification_send = False
    resin_last_count = -1
    while (True):
        ac = gs.get_game_accounts()
        get_account_pos = list(map(lambda x:x['biz']=='hk4e_global', ac))
        z = 0
        pos = 0
        for i in get_account_pos:
            if i == True:
                pos = z
            else:
                z += 1
        uid = ac[pos]['uid']
        notes = gs.get_notes(uid)

        if resin_notification_send == True:
            if resin_last_count != notes['resin']:
                resin_notification_send = False

        if (os.getenv('resin_milestone')) == 'True':
            resin_milestones = os.getenv('resin_milestones').split(', ')
            if str(notes['resin']) in resin_milestones:
                if resin_notification_send == False:
                    print(f"{strftime('%H:%M:%S', localtime())} | One of your resin milestone was reached")
                    if os.getenv('tts') == 'True':
                        engine.say("One of your resin milestone was reached")
                        engine.runAndWait()
                    resin_last_count = notes['resin']
                    toaster.show_toast("One of your resin milestone was reached", f"You currently have {notes['resin']} resin out of {notes['max_resin']}", "ico/Resin.ico", 60)
                    resin_notification_send = True
            else:
                if resin_notification_send == False:
                    if notes['resin'] == notes['max_resin']:
                        print(f"{strftime('%H:%M:%S', localtime())} | Your resin is FULL")
                        if os.getenv('tts') == 'True':
                            engine.say("Your resin is FULL")
                            engine.runAndWait()
                        resin_last_count = notes['resin']
                        toaster.show_toast("Your resin is FULL", f"You currently have {notes['resin']} resin out of {notes['max_resin']}", "ico/Resin.ico", 60)
                        resin_notification_send = True
                    elif notes['resin'] >= notes['max_resin']:
                        print(f"{strftime('%H:%M:%S', localtime())} | Your resin isn't just FULL")
                        if os.getenv('tts') == 'True':
                            engine.say("Your resin isn't just FULL")
                            engine.runAndWait()
                        resin_last_count = notes['resin']
                        toaster.show_toast("Your resin isn't just FULL", f"You currently have {notes['resin']} resin out of {notes['max_resin']}", "ico/Resin.ico", 60)
                        resin_notification_send = True    
        else: 
            if resin_notification_send == False:
                if notes['resin'] == notes['max_resin']:
                    print(f"{strftime('%H:%M:%S', localtime())} | Your resin is FULL")
                    if os.getenv('tts') == 'True':
                        engine.say("Your resin is FULL")
                        engine.runAndWait()
                    resin_last_count = notes['resin']
                    toaster.show_toast("Your resin is FULL", f"You currently have {notes['resin']} resin out of {notes['max_resin']}", "ico/Resin.ico", 60)
                    resin_notification_send = True
                elif notes['resin'] >= notes['max_resin']:
                    print(f"{strftime('%H:%M:%S', localtime())} | Your resin isn't just FULL")
                    if os.getenv('tts') == 'True':
                        engine.say("Your resin isn't just FULL")
                        engine.runAndWait()
                    resin_last_count = notes['resin']
                    toaster.show_toast("Your resin isn't just FULL", f"You currently have {notes['resin']} resin out of {notes['max_resin']}", "ico/Resin.ico", 60)
                    resin_notification_send = True

        sleep(480)

def realm():
    realm_notification_send = False
    realm_last_count = -1
    while (True):
        ac = gs.get_game_accounts()
        get_account_pos = list(map(lambda x:x['biz']=='hk4e_global', ac))
        z = 0
        pos = 0
        for i in get_account_pos:
            if i == True:
                pos = z
            else:
                z += 1
        uid = ac[pos]['uid']
        notes = gs.get_notes(uid)

        if realm_notification_send == True:
            if realm_last_count != notes['realm_currency']:
                realm_notification_send = False

        if (os.getenv('realm_milestone')) == 'True':
            realm_milestones = os.getenv('realm_milestones').split(', ')
            if str(notes['realm_currency']) in realm_milestones:
                if realm_notification_send == False:
                    print(f"{strftime('%H:%M:%S', localtime())} | One of your realm currency milestone was reached")
                    if os.getenv('tts') == 'True':
                        engine.say("One of your realm currency milestone was reached")
                        engine.runAndWait()
                    realm_last_count = notes['realm_currency']
                    toaster.show_toast("One of your realm currency milestone was reached", f"You currently have {notes['realm_currency']} realm currency out of {notes['max_realm_currency']}", "ico/Realm.ico", 60)
                    realm_notification_send = True
            else:
                if realm_notification_send == False:
                    if notes['realm_currency'] == notes['max_realm_currency']:
                        print(f"{strftime('%H:%M:%S', localtime())} | Your realm currency is FULL")
                        if os.getenv('tts') == 'True':
                            engine.say("Your realm currency is FULL")
                            engine.runAndWait()
                        realm_last_count = notes['realm_currency']
                        toaster.show_toast("Your realm currency is FULL", f"You currently have {notes['realm_currency']} realm currency out of {notes['max_realm_currency']}", "ico/Realm.ico", 60)
                        realm_notification_send = True
        else: 
            if realm_notification_send == False:
                if notes['realm_currency'] == notes['max_realm_currency']:
                    print(f"{strftime('%H:%M:%S', localtime())} | Your realm currency is FULL")
                    if os.getenv('tts') == 'True':
                        engine.say("Your realm currency is FULL")
                        engine.runAndWait()
                    realm_last_count = notes['realm_currency']
                    toaster.show_toast("Your realm currency is FULL", f"You currently have {notes['realm_currency']} realm currency out of {notes['max_realm_currency']}", "ico/Realm.ico", 60)
                    realm_notification_send = True

        sleep(300)

def transformer():
    parametric_notification_send = False
    while (True):
        ac = gs.get_game_accounts()
        get_account_pos = list(map(lambda x:x['biz']=='hk4e_global', ac))
        z = 0
        pos = 0
        for i in get_account_pos:
            if i == True:
                pos = z
            else:
                z += 1
        uid = ac[pos]['uid']
        notes = gs.get_notes(uid)

        if parametric_notification_send == True:
            if notes['parametric_transformer_cooldown_ended'] == False:
                parametric_notification_send = False

        if notes['parametric_transformer_cooldown_ended'] == True:
            if parametric_notification_send == False:
                print(f"{strftime('%H:%M:%S', localtime())} | Parametric Transformer cooldown has ended")
                if os.getenv('tts') == 'True':
                    engine.say("Parametric Transformer cooldown has ended")
                    engine.runAndWait()
                toaster.show_toast("Parametric Transformer cooldown has ended", f"Parametric Transformer cooldown has ended", "ico/Transformer.ico", 60)
                parametric_notification_send = True

        sleep(600)

def expeditions():
    expeditions_notification_send = False
    expeditions_last_count = 0
    while (True):
        ac = gs.get_game_accounts()
        get_account_pos = list(map(lambda x:x['biz']=='hk4e_global', ac))
        z = 0
        pos = 0
        for i in get_account_pos:
            if i == True:
                pos = z
            else:
                z += 1
        uid = ac[pos]['uid']
        notes = gs.get_notes(uid)
        
        if expeditions_notification_send == True:
            if list(map(lambda x:x['status']=='Finished', notes['expeditions'])).count(True) != expeditions_last_count:
                expeditions_notification_send = False

        elif expeditions_notification_send == False:
            if list(map(lambda x:x['status']=='Finished', notes['expeditions'])).count(True) == notes['max_expeditions']:
                print(f"{strftime('%H:%M:%S', localtime())} | All your expeditions have completed")
                if os.getenv('tts') == 'True':
                    engine.say("All your expeditions have completed")
                    engine.runAndWait()
                expeditions_last_count = list(map(lambda x:x['status']=='Finished', notes['expeditions'])).count(True)
                toaster.show_toast("All your expeditions have completed", f"{expeditions_last_count} expeditions have completed out of {notes['max_expeditions']}", "ico/Expedition.ico", 60)
                expeditions_notification_send = True
            elif list(map(lambda x:x['status']=='Finished', notes['expeditions'])).count(True) > expeditions_last_count:
                print(f"{strftime('%H:%M:%S', localtime())} | Some of your expeditions have completed")
                if os.getenv('tts') == 'True':
                    engine.say("Some of your expeditions have completed")
                    engine.runAndWait()
                expeditions_last_count = list(map(lambda x:x['status']=='Finished', notes['expeditions'])).count(True)
                toaster.show_toast("Some of your expeditions have completed", f"{expeditions_last_count} expeditions have completed out of {notes['max_expeditions']}", "ico/Expedition.ico", 60)
                expeditions_notification_send = True

        sleep(600)

def daily():
    daily_last_day = -1
    timezone = pytz.timezone('Etc/GMT-8')
    while (True):
        day = datetime.datetime.now(timezone).strftime('%d')

        if daily_last_day != day:
            reward = gs.claim_daily_reward()
            if reward is not None:
                print(f"{strftime('%H:%M:%S', localtime())} | Claimed daily reward - {reward['cnt']}x {reward['name']}")
                if os.getenv('tts') == 'True':
                    engine.say("Collected your daily check-in reward")
                    engine.runAndWait()
                daily_last_day = day
                if os.getenv('daily_not') == 'True':
                    toaster.show_toast("Collected your daily check-in reward", f"Claimed daily reward - {reward['cnt']}x {reward['name']}", "ico/Daily.ico", 60)
            else:
                daily_last_day = day

        sleep(900)

def abyss_shop():
    timezones = {"eu": "Etc/GMT-1", "as": "Etc/GMT-8", "us": "Etc/GMT+5"}
    last_day = -1
    while(True):
        day = datetime.datetime.now(pytz.timezone(timezones[os.getenv("server")])).strftime('%d')

        if last_day != day:
            last_day = day
            if day == "01":
                if (os.getenv('abyss_not')) == 'True':
                    print(f"{strftime('%H:%M:%S', localtime())} | Abyss has been reset today")
                    if os.getenv('tts') == 'True':
                        engine.say("Abyss has been reset today")
                        engine.runAndWait()
                    toaster.show_toast("Abyss reset", f"Abyss has been reset today", "ico/Abyss.ico", 5) # Shorter duration to make next notification go off faster
                if (os.getenv('shop_not')) == 'True':
                    print(f"{strftime('%H:%M:%S', localtime())} | Shop has been reset today")
                    if os.getenv('tts') == 'True':
                        engine.say("Shop has been reset today")
                        engine.runAndWait()
                    toaster.show_toast("Shop reset", f"Shop has been reset today", "ico/Shop.ico", 5)
            if day == "16":
                if (os.getenv('abyss_not')) == 'True':
                    print(f"{strftime('%H:%M:%S', localtime())} | Abyss has been reset today")
                    if os.getenv('tts') == 'True':
                        engine.say("Abyss has been reset today")
                        engine.runAndWait()
                    toaster.show_toast("Abyss reset", f"Abyss has been reset today", "ico/Abyss.ico", 60)

        sleep(900)

def reminder():
    game_on = False
    while(True):
        name = "genshinimpact.exe" # "notepad++.exe"
        if name in (p.name().lower() for p in psutil.process_iter()):
            if game_on == False:
                game_on = True
                
                if (int(os.getenv("reminder_additional_delay")) != 0):
                    sleep(int(os.getenv("reminder_additional_delay")))

                ac = gs.get_game_accounts()
                get_account_pos = list(map(lambda x:x['biz']=='hk4e_global', ac))
                z = 0
                pos = 0
                for i in get_account_pos:
                    if i == True:
                        pos = z
                    else:
                        z += 1
                uid = ac[pos]['uid']
                notes = gs.get_notes(uid)

                if (os.getenv("reminder_transformer")) == 'True':
                    if notes['parametric_transformer_cooldown_ended'] == True:
                        print(f"REMINDER {strftime('%H:%M:%S', localtime())} | Parametric Transformer cooldown has ended")
                        if os.getenv('tts') == 'True':
                            engine.say("REMINDER Parametric Transformer cooldown has ended")
                            engine.runAndWait()
                        toaster.show_toast("Parametric Transformer cooldown has ended", f"Parametric Transformer cooldown has ended", "ico/Transformer.ico", 5)

                if (os.getenv("reminder_realm")) == 'True':
                    if (os.getenv('realm_milestone')) == 'True':
                        realm_milestones = os.getenv('realm_milestones').split(', ')
                        if str(notes['realm_currency']) in realm_milestones:
                            print(f"REMINDER {strftime('%H:%M:%S', localtime())} | One of your realm currency milestone was reached")
                            if os.getenv('tts') == 'True':
                                engine.say("REMINDER One of your realm currency milestone was reached")
                                engine.runAndWait()
                            toaster.show_toast("One of your realm currency milestone was reached", f"You currently have {notes['realm_currency']} realm currency out of {notes['max_realm_currency']}", "ico/Realm.ico", 5)
                        else:
                            if notes['realm_currency'] == notes['max_realm_currency']:
                                print(f"REMINDER {strftime('%H:%M:%S', localtime())} | Your realm currency is FULL")
                                if os.getenv('tts') == 'True':
                                    engine.say("REMINDER Your realm currency is FULL")
                                    engine.runAndWait()
                                toaster.show_toast("Your realm currency is FULL", f"You currently have {notes['realm_currency']} realm currency out of {notes['max_realm_currency']}", "ico/Realm.ico", 5)
                    else: 
                        if notes['realm_currency'] == notes['max_realm_currency']:
                            print(f"REMINDER {strftime('%H:%M:%S', localtime())} | Your realm currency is FULL")
                            if os.getenv('tts') == 'True':
                                engine.say(" REMINDERYour realm currency is FULL")
                                engine.runAndWait()
                            toaster.show_toast("Your realm currency is FULL", f"You currently have {notes['realm_currency']} realm currency out of {notes['max_realm_currency']}", "ico/Realm.ico", 5)

                timezones = {"eu": "Etc/GMT-1", "as": "Etc/GMT-8", "us": "Etc/GMT+5"}
                day = datetime.datetime.now(pytz.timezone(timezones[os.getenv("server")])).strftime('%d')
                if (os.getenv("reminder_abyss")) == 'True':
                    if day == "1" or day == "16":
                        print(f"REMINDER {strftime('%H:%M:%S', localtime())} | Abyss has been reset today")
                        if os.getenv('tts') == 'True':
                            engine.say("REMINDER Abyss has been reset today")
                            engine.runAndWait()
                        toaster.show_toast("Abyss reset", f"Abyss has been reset today", "ico/Abyss.ico", 5)
                
                if (os.getenv("reminder_shop")) == 'True':
                    if day == "1":
                        print(f"REMINDER {strftime('%H:%M:%S', localtime())} | Shop has been reset today")
                        if os.getenv('tts') == 'True':
                            engine.say("REMINDER Shop has been reset today")
                            engine.runAndWait()
                        toaster.show_toast("Shop reset", f"Shop has been reset today", "ico/Shop.ico", 5)
        else:
            if game_on == True:
                game_on = False

        sleep(int(os.getenv("reminder_time")))

if __name__ == '__main__':
    print("-----------------------------------")
    if (os.getenv('resin_not')) == 'True':
        p1 = Process(target=resin)
        p1.start()
        print("Resin turned on")
    if (os.getenv('realm_not')) == 'True':
        p2 = Process(target=realm)
        p2.start()
        print("Realm currency turned on")
    if (os.getenv('transformer_not')) == 'True':
        p3 = Process(target=transformer)
        p3.start()
        print("Parametric Transformer turned on")
    if (os.getenv('expeditions_not')) == 'True':
        p4 = Process(target=expeditions)
        p4.start()
        print('Expeditions turned on')
    if (os.getenv('daily_check_in')) == 'True':
        p5 = Process(target=daily)
        p5.start()
        print('Daily check-in turned on')
    if (os.getenv('abyss_not')) == 'True' or (os.getenv('shop_not')) == 'True':
        p6 = Process(target=abyss_shop)
        p6.start()
        print('Abyss/Shop reset turned on')
    if (os.getenv('reminder')) == 'True':
        p7 = Process(target=reminder)
        p7.start()
        print('Reminder turned on')
    print("-----------------------------------")