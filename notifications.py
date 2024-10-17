import dotenv, os, pyttsx3, pytz, datetime, psutil, genshin, asyncio, json, contextvars, functools
from win11toast import toast_async
from time import localtime, strftime

gn_path = os.path.dirname(os.path.realpath(__file__))
toast_async = functools.partial(toast_async, app_id="Genshin Notifications", on_click=lambda args: None, on_dismissed=lambda args: None, on_failed=lambda args: None)
dotenv.load_dotenv(dotenv_path=f"{gn_path}/settings.env")
engine = pyttsx3.init()
os.system("") # To make colors in errors always work
gs = genshin.Client()

if os.path.exists("cache.json"):
    pass
else: 
    with open("cache.json", "w", encoding='utf-8') as cache_f:
        data = {
            'abyss_season': 0,
            'theater_season': 0
        }
        json.dump(data, cache_f, indent=4)

if os.getenv('set_cookies_method') == 'auto':
    gs.set_browser_cookies()
elif os.getenv('set_cookies_method') == 'login':
    if os.getenv('ltuid') == 0 or os.getenv('ltoken') == "":
        print("\33[31mIncorrect ltuid or ltoken empty!\033[0m")
        exit()
    else:
        gs.set_cookies(ltuid=int(os.getenv('ltuid')), ltoken=os.getenv('ltoken'))
else:
    print("\33[31mIncorrect value for \"set_cookies_method\"! \n\33[93mSet it to: \"login\" or \"auto\"\033[0m")
    exit()

if os.getenv("server") not in ["eu", "us", "as"]:
    print("\33[31mIncorrect value for \"server\"! \n\33[93mSet it to on of this values: \"eu\", \"us\", \"as\"\033[0m")
    exit()

def margin(input, margin, milestone):
    return any(int(x) <= input <= int(x) + margin for x in milestone)

def closest(input, milestone):
    return min(milestone, key=lambda x: abs(int(x) - input))

async def to_thread(func, /, *args, **kwargs):
    loop = asyncio.get_running_loop()
    ctx = contextvars.copy_context()
    func_call = functools.partial(ctx.run, func, *args, **kwargs)
    return await loop.run_in_executor(None, func_call)

async def resin():
    resin_notification_send = False
    resin_last_count = -1
    resin_milestone_stop_notifications_until = -1
    icon = {
        'src': f'file://{gn_path}/ico/Resin.ico',
        'placement': 'appLogoOverride'
    }
    while (True):
        ac = await gs.get_game_accounts()
        uid = 0
        for account in ac:
            if genshin.Game.GENSHIN in account.game_biz:
                uid = account.uid
        notes = await gs.get_genshin_notes(uid)

        if resin_notification_send == True:
            if resin_last_count != notes.current_resin:
                resin_notification_send = False
                if (os.getenv('resin_milestone')) == 'True':
                    if notes.current_resin <= resin_milestone_stop_notifications_until:
                        resin_notification_send = True
                    else:
                        resin_milestone_stop_notifications_until = -1

        if (os.getenv('resin_milestone')) == 'True':
            resin_milestones = os.getenv('resin_milestones').split(', ')
            if margin(notes.current_resin, int(os.getenv("resin_milestones_margin")), resin_milestones):
                if resin_notification_send == False:
                    print(f"{strftime('%H:%M:%S', localtime())} | One of your resin milestone was reached")
                    if os.getenv('tts') == 'True':
                        engine.say("One of your resin milestone was reached")
                        engine.runAndWait()
                    resin_last_count = notes.current_resin
                    await toast_async("One of your resin milestone was reached", f"You currently have {notes.current_resin} resin out of {notes.max_resin}", icon=icon)
                    resin_notification_send = True
                    resin_milestone_stop_notifications_until = int(closest(notes.current_resin, resin_milestones)) + int(os.getenv("resin_milestones_margin"))
            else:
                if resin_notification_send == False:
                    if notes.current_resin == notes.max_resin:
                        print(f"{strftime('%H:%M:%S', localtime())} | Your resin is FULL")
                        if os.getenv('tts') == 'True':
                            engine.say("Your resin is FULL")
                            engine.runAndWait()
                        resin_last_count = notes.current_resin
                        await toast_async("Your resin is FULL", f"You currently have {notes.current_resin} resin out of {notes.max_resin}", icon=icon)
                        resin_notification_send = True
                    elif notes.current_resin >= notes.max_resin:
                        print(f"{strftime('%H:%M:%S', localtime())} | Your resin isn't just FULL")
                        if os.getenv('tts') == 'True':
                            engine.say("Your resin isn't just FULL")
                            engine.runAndWait()
                        resin_last_count = notes.current_resin
                        await toast_async("Your resin isn't just FULL", f"You currently have {notes.current_resin} resin out of {notes.max_resin}", icon=icon)
                        resin_notification_send = True    
        else: 
            if resin_notification_send == False:
                if notes.current_resin == notes.max_resin:
                    print(f"{strftime('%H:%M:%S', localtime())} | Your resin is FULL")
                    if os.getenv('tts') == 'True':
                        engine.say("Your resin is FULL")
                        engine.runAndWait()
                    resin_last_count = notes.current_resin
                    await toast_async("Your resin is FULL", f"You currently have {notes.current_resin} resin out of {notes.max_resin}", icon=icon)
                    resin_notification_send = True
                elif notes.current_resin >= notes.max_resin:
                    print(f"{strftime('%H:%M:%S', localtime())} | Your resin isn't just FULL")
                    if os.getenv('tts') == 'True':
                        engine.say("Your resin isn't just FULL")
                        engine.runAndWait()
                    resin_last_count = notes.current_resin
                    await toast_async("Your resin isn't just FULL", f"You currently have {notes.current_resin} resin out of {notes.max_resin}", icon=icon)
                    resin_notification_send = True

        await asyncio.sleep(480)

async def realm():
    realm_notification_send = False
    realm_last_count = -1
    realm_milestone_stop_notifications_until = -1
    icon = {
        'src': f'file://{gn_path}/ico/Realm.ico',
        'placement': 'appLogoOverride'
    }
    while (True):
        ac = await gs.get_game_accounts()
        uid = 0
        for account in ac:
            if genshin.Game.GENSHIN in account.game_biz:
                uid = account.uid
        notes = await gs.get_genshin_notes(uid)

        if realm_notification_send == True:
            if realm_last_count != notes.current_realm_currency:
                realm_notification_send = False
                if (os.getenv('realm_milestone')) == 'True':
                    if notes.current_resin <= realm_milestone_stop_notifications_until:
                        realm_notification_send = True
                    else:
                        realm_milestone_stop_notifications_until = -1

        if (os.getenv('realm_milestone')) == 'True':
            realm_milestones = os.getenv('realm_milestones').split(', ')
            if margin(notes.current_realm_currency, int(os.getenv("realm_milestones_margin")), realm_milestones):
                if realm_notification_send == False:
                    print(f"{strftime('%H:%M:%S', localtime())} | One of your realm currency milestone was reached")
                    if os.getenv('tts') == 'True':
                        engine.say("One of your realm currency milestone was reached")
                        engine.runAndWait()
                    realm_last_count = notes.current_realm_currency
                    await toast_async("One of your realm currency milestone was reached", f"You currently have {notes.current_realm_currency} realm currency out of {notes.max_realm_currency}", icon=icon)
                    realm_notification_send = True
                    realm_milestone_stop_notifications_until = int(closest(notes.current_resin, realm_milestones)) + int(os.getenv("realm_milestones_margin"))
            else:
                if realm_notification_send == False:
                    if notes.current_realm_currency == notes.max_realm_currency:
                        print(f"{strftime('%H:%M:%S', localtime())} | Your realm currency is FULL")
                        if os.getenv('tts') == 'True':
                            engine.say("Your realm currency is FULL")
                            engine.runAndWait()
                        realm_last_count = notes.current_realm_currency
                        await toast_async("Your realm currency is FULL", f"You currently have {notes.current_realm_currency} realm currency out of {notes.max_realm_currency}", icon=icon)
                        realm_notification_send = True
        else: 
            if realm_notification_send == False:
                if notes.current_realm_currency == notes.max_realm_currency:
                    print(f"{strftime('%H:%M:%S', localtime())} | Your realm currency is FULL")
                    if os.getenv('tts') == 'True':
                        engine.say("Your realm currency is FULL")
                        engine.runAndWait()
                    realm_last_count = notes.current_realm_currency
                    await toast_async("Your realm currency is FULL", f"You currently have {notes.current_realm_currency} realm currency out of {notes.max_realm_currency}", icon=icon)
                    realm_notification_send = True

        await asyncio.sleep(300)

async def transformer():
    parametric_notification_send = False
    icon = {
        'src': f'file://{gn_path}/ico/Transformer.ico',
        'placement': 'appLogoOverride'
    }
    while (True):
        ac = await gs.get_game_accounts()
        uid = 0
        for account in ac:
            if genshin.Game.GENSHIN in account.game_biz:
                uid = account.uid
        notes = await gs.get_genshin_notes(uid)

        if parametric_notification_send == True:
            if notes.transformer_recovery_time != datetime.datetime.now().astimezone():
                parametric_notification_send = False

        if notes.transformer_recovery_time == datetime.datetime.now().astimezone():
            if parametric_notification_send == False:
                print(f"{strftime('%H:%M:%S', localtime())} | Parametric Transformer cooldown has ended")
                if os.getenv('tts') == 'True':
                    engine.say("Parametric Transformer cooldown has ended")
                    engine.runAndWait()
                await toast_async("Parametric Transformer cooldown has ended", f"Parametric Transformer cooldown has ended", icon=icon)
                parametric_notification_send = True

        await asyncio.sleep(600)

async def expeditions():
    expeditions_notification_send = False
    expeditions_last_count = 0
    icon = {
        'src': f'file://{gn_path}/ico/Expedition.ico',
        'placement': 'appLogoOverride'
    }
    while (True):
        ac = await gs.get_game_accounts()
        uid = 0
        for account in ac:
            if genshin.Game.GENSHIN in account.game_biz:
                uid = account.uid
        notes = await gs.get_genshin_notes(uid)
        
        completed = 0
        for expedition in notes.expeditions:
            if expedition.finished == True:
                completed += 1
        
        if expeditions_notification_send == True:
            if completed != expeditions_last_count:
                expeditions_notification_send = False

        elif expeditions_notification_send == False:
            if completed == notes.max_expeditions:
                print(f"{strftime('%H:%M:%S', localtime())} | All your expeditions have completed")
                if os.getenv('tts') == 'True':
                    engine.say("All your expeditions have completed")
                    engine.runAndWait()
                expeditions_last_count = completed
                await toast_async("All your expeditions have completed", f"{expeditions_last_count} expeditions have completed out of {notes.max_expeditions}", icon=icon)
                expeditions_notification_send = True
            elif completed > expeditions_last_count:
                print(f"{strftime('%H:%M:%S', localtime())} | Some of your expeditions have completed")
                if os.getenv('tts') == 'True':
                    engine.say("Some of your expeditions have completed")
                    engine.runAndWait()
                expeditions_last_count = completed
                await toast_async("Some of your expeditions have completed", f"{expeditions_last_count} expeditions have completed out of {notes.max_expeditions}", icon=icon)
                expeditions_notification_send = True

        await asyncio.sleep(600)

async def daily():
    daily_last_day = -1
    timezone = pytz.timezone('Etc/GMT-8')
    icon = {
        'src': f'file://{gn_path}/ico/Daily.ico',
        'placement': 'appLogoOverride'
    }
    while (True):
        day = datetime.datetime.now(timezone).strftime('%d')

        if daily_last_day != day:
            try:
                reward = await gs.claim_daily_reward(game=genshin.Game.GENSHIN)
            except genshin.AlreadyClaimed:
                daily_last_day = day
            else:
                print(f"{strftime('%H:%M:%S', localtime())} | Claimed daily reward - {reward.amount}x {reward.name}")
                if os.getenv('tts') == 'True':
                    engine.say("Collected your daily check-in reward")
                    engine.runAndWait()
                daily_last_day = day
                if os.getenv('daily_not') == 'True':
                    await toast_async("Collected your daily check-in reward", f"Claimed daily reward - {reward.amount}x {reward.name}", icon=icon)

        await asyncio.sleep(900)

abyss_reset = False

async def abyss():
    global abyss_reset
    icon = {
        'src': f'file://{gn_path}/ico/Abyss.ico',
        'placement': 'appLogoOverride'
    }
    while(True):    
        ac = await gs.get_game_accounts()
        uid = 0
        for account in ac:
            if genshin.Game.GENSHIN in account.game_biz:
                uid = account.uid
        abyss = await gs.get_genshin_spiral_abyss(uid)
        
        with open("cache.json", "r", encoding='utf-8') as cache_f:
            cache = json.load(cache_f)
            season = cache['abyss_season']
            cache_f.close()

        if season != abyss.season:
            with open("cache.json", "w", encoding='utf-8') as cache_f:
                abyss_reset = True
                cache['abyss_season'] = abyss.season
                json.dump(cache, cache_f, indent=4)
                cache_f.close()
            print(f"{strftime('%H:%M:%S', localtime())} | Abyss has been reset")
            if os.getenv('tts') == 'True':
                engine.say("Abyss has been reset")
                engine.runAndWait()
            await toast_async("Abyss reset", f"Abyss has been reset", icon=icon)
                    
        await asyncio.sleep(900)

theater_reset = False
 
async def theater():
    global theater_reset
    icon = {
        'src': f'file://{gn_path}/ico/Theater.ico',
        'placement': 'appLogoOverride'
    }
    while(True):    
        ac = await gs.get_game_accounts()
        uid = 0
        for account in ac:
            if genshin.Game.GENSHIN in account.game_biz:
                uid = account.uid
        theater = await gs.get_imaginarium_theater(uid)
        
        with open("cache.json", "r", encoding='utf-8') as cache_f:
            cache = json.load(cache_f)
            season = cache['theater_season']
            cache_f.close()

        if season != theater.datas[0].schedule.id:
            with open("cache.json", "w", encoding='utf-8') as cache_f:
                theater_reset = True
                cache['theater_season'] = theater.datas[0].schedule.id
                json.dump(cache, cache_f, indent=4)
                cache_f.close()
            print(f"{strftime('%H:%M:%S', localtime())} | Imaginarium Theater has been reset")
            if os.getenv('tts') == 'True':
                engine.say("Imaginarium Theater has been reset")
                engine.runAndWait()
            await toast_async("Imaginarium Theater reset", f"Imaginarium Theater has been reset", icon=icon)
                    
        await asyncio.sleep(900)

async def shop():
    timezones = {"eu": "Etc/GMT-1", "as": "Etc/GMT-8", "us": "Etc/GMT+5"}
    last_day = -1
    icon = {
        'src': f'file://{gn_path}/ico/Shop.ico',
        'placement': 'appLogoOverride'
    }
    while(True):
        day = int(datetime.datetime.now(pytz.timezone(timezones[os.getenv("server")])).strftime('%d'))

        if last_day != day:
            last_day = day
            if day == 1:
                print(f"{strftime('%H:%M:%S', localtime())} | Shop has been reset today")
                if os.getenv('tts') == 'True':
                    engine.say("Shop has been reset today")
                    engine.runAndWait()
                await toast_async("Shop reset", f"Shop has been reset today", icon=icon)

        await asyncio.sleep(900)

async def reminder():
    game_on = False
    global abyss_reset
    global theater_reset
    icon_t = {
        'src': f'file://{gn_path}/ico/Transformer.ico',
        'placement': 'appLogoOverride'
    }
    icon_r = {
        'src': f'file://{gn_path}/ico/Realm.ico',
        'placement': 'appLogoOverride'
    }
    icon_a = {
        'src': f'file://{gn_path}/ico/Abyss.ico',
        'placement': 'appLogoOverride'
    }
    icon_it = {
        'src': f'file://{gn_path}/ico/Theater.ico',
        'placement': 'appLogoOverride'
    }
    icon_s = {
        'src': f'file://{gn_path}/ico/Shop.ico',
        'placement': 'appLogoOverride'
    }
    while(True):
        name = "genshinimpact.exe" # "notepad++.exe"
        if name in (p.name().lower() for p in psutil.process_iter()):
            if game_on == False:
                game_on = True
                
                if (int(os.getenv("reminder_additional_delay")) != 0):
                    await asyncio.sleep(int(os.getenv("reminder_additional_delay")))

                ac = await gs.get_game_accounts()
                uid = 0
                for account in ac:
                    if genshin.Game.GENSHIN in account.game_biz:
                        uid = account.uid
                notes = await gs.get_genshin_notes(uid)

                if (os.getenv("reminder_transformer")) == 'True':
                    if notes.transformer_recovery_time == datetime.datetime.now().astimezone():
                        print(f"REMINDER {strftime('%H:%M:%S', localtime())} | Parametric Transformer cooldown has ended")
                        if os.getenv('tts') == 'True':
                            engine.say("REMINDER Parametric Transformer cooldown has ended")
                            engine.runAndWait()
                        await toast_async("Parametric Transformer cooldown has ended", f"Parametric Transformer cooldown has ended", icon=icon_t)

                if (os.getenv("reminder_realm")) == 'True':
                    if (os.getenv('realm_milestone')) == 'True':
                        realm_milestones = os.getenv('realm_milestones').split(', ')
                        if margin(notes.current_realm_currency, int(os.getenv("realm_milestones_margin")), realm_milestones):
                            print(f"REMINDER {strftime('%H:%M:%S', localtime())} | One of your realm currency milestone was reached")
                            if os.getenv('tts') == 'True':
                                engine.say("REMINDER One of your realm currency milestone was reached")
                                engine.runAndWait()
                            await toast_async("One of your realm currency milestone was reached", f"You currently have {notes.current_realm_currency} realm currency out of {notes.max_realm_currency}", icon=icon_r)
                        else:
                            if notes.current_realm_currency == notes.max_realm_currency:
                                print(f"REMINDER {strftime('%H:%M:%S', localtime())} | Your realm currency is FULL")
                                if os.getenv('tts') == 'True':
                                    engine.say("REMINDER Your realm currency is FULL")
                                    engine.runAndWait()
                                await toast_async("Your realm currency is FULL", f"You currently have {notes.current_realm_currency} realm currency out of {notes.max_realm_currency}", icon=icon_r)
                    else: 
                        if notes.current_realm_currency == notes.max_realm_currency:
                            print(f"REMINDER {strftime('%H:%M:%S', localtime())} | Your realm currency is FULL")
                            if os.getenv('tts') == 'True':
                                engine.say("REMINDER Your realm currency is FULL")
                                engine.runAndWait()
                            await toast_async("Your realm currency is FULL", f"You currently have {notes.current_realm_currency} realm currency out of {notes.max_realm_currency}", icon=icon_r)

                if (os.getenv("reminder_abyss")) == 'True':
                    if abyss_reset:
                        print(f"REMINDER {strftime('%H:%M:%S', localtime())} | Abyss has been reset")
                        if os.getenv('tts') == 'True':
                            engine.say("REMINDER Abyss has been reset")
                            engine.runAndWait()
                        await toast_async("Abyss reset", f"Abyss has been reset", icon=icon_a)
                
                if (os.getenv("reminder_theater")) == 'True':
                    if theater_reset:
                        print(f"REMINDER {strftime('%H:%M:%S', localtime())} | Imaginarium Theater has been reset")
                        if os.getenv('tts') == 'True':
                            engine.say("REMINDER Imaginarium Theater has been reset")
                            engine.runAndWait()
                        await toast_async("Imaginarium Theater reset", f"Imaginarium Theater has been reset", icon=icon_it)
                
                timezones = {"eu": "Etc/GMT-1", "as": "Etc/GMT-8", "us": "Etc/GMT+5"}
                day = int(datetime.datetime.now(pytz.timezone(timezones[os.getenv("server")])).strftime('%d'))
                if (os.getenv("reminder_shop")) == 'True':
                    if day == 1:
                        print(f"REMINDER {strftime('%H:%M:%S', localtime())} | Shop has been reset today")
                        if os.getenv('tts') == 'True':
                            engine.say("REMINDER Shop has been reset today")
                            engine.runAndWait()
                        await toast_async("Shop reset", f"Shop has been reset today", icon=icon_s)
        else:
            if game_on == True:
                game_on = False

        await asyncio.sleep(int(os.getenv("reminder_time")))

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    print("-----------------------------------")
    if (os.getenv('resin_not')) == 'True':
        task1 = asyncio.ensure_future(resin())
        print("Resin turned on")
    if (os.getenv('realm_not')) == 'True':
        task2 = asyncio.ensure_future(realm())
        print("Realm currency turned on")
    if (os.getenv('transformer_not')) == 'True':
        task3 = asyncio.ensure_future(transformer())
        print("Parametric Transformer turned on")
    if (os.getenv('expeditions_not')) == 'True':
        task4 = asyncio.ensure_future(expeditions())
        print('Expeditions turned on')
    if (os.getenv('daily_check_in')) == 'True':
        task5 = asyncio.ensure_future(daily())
        print('Daily check-in turned on')
    if (os.getenv('abyss_not')) == 'True':
        task6 = asyncio.ensure_future(abyss())
        print('Abyss reset turned on')
    if (os.getenv('theater_not')) == 'True':
        task7 = asyncio.ensure_future(theater())
        print('Imaginarium Theater reset turned on')
    if (os.getenv('shop_not')) == 'True':
        task8 = asyncio.ensure_future(shop())
        print('Shop reset turned on')
    if (os.getenv('reminder')) == 'True':
        task9 = asyncio.ensure_future(reminder())
        print('Reminder turned on')
    print("-----------------------------------")
    loop.run_forever()