import dotenv, os, pyttsx3, pytz, datetime
import genshinstats as gs
from win10toast import ToastNotifier
from multiprocessing import Process
from time import sleep, localtime, strftime

dotenv.load_dotenv(dotenv_path="settings.env")
toaster = ToastNotifier()
engine = pyttsx3.init()

if os.getenv('set_cookies_method') == 'auto':
    gs.set_cookie_auto()
else:
    gs.set_cookie(ltuid=int(os.getenv('ltuid')), ltoken=os.getenv('ltoken'))

def resin():
    resin_notification_send = False
    resin_last_count = -1
    while (True):
        notes = gs.get_notes(gs.get_game_accounts()[0]['uid'])
        
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
                        toaster.show_toast("Your resin is FULL", f"You currently have {notes['resin']} resin out of {notes['max_resin']}", "ico/Resin.ico", 10)
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
                    toaster.show_toast("Your resin is FULL", f"You currently have {notes['resin']} resin out of {notes['max_resin']}", "ico/Resin.ico", 10)
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
        notes = gs.get_notes(gs.get_game_accounts()[0]['uid'])
        
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
        notes = gs.get_notes(gs.get_game_accounts()[0]['uid'])
        
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
        notes = gs.get_notes(gs.get_game_accounts()[0]['uid'])
        
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
        
if __name__ == '__main__':
    if (os.getenv('resin_not')) == 'True':
        p1 = Process(target=resin)
        p1.start()
        print("Resin turnd on")
    if (os.getenv('realm_not')) == 'True':
        p2 = Process(target=realm)
        p2.start()
        print("Realm currency turnd on")
    if (os.getenv('transformer_not')) == 'True':
        p3 = Process(target=transformer)
        p3.start()
        print("Parametric Transformer turnd on")
    if (os.getenv('expeditions_not')) == 'True':
        p4 = Process(target=expeditions)
        p4.start()
        print('Expeditions turned on')
    if (os.getenv('daily_check_in')) == 'True':
        p5 = Process(target=daily)
        p5.start()
        print('Daily check-in turned on')
    print("-----------------------------------")