from datetime import datetime,timezone
from dateutil import parser,tz
from collections import Counter
#now = datetime.now()

def utc_to_lt(match_time_utc):

    to_zone = tz.tzlocal()
    match_time_utc = parser.parse(match_time_utc)
    match_time_lt = match_time_utc.astimezone(to_zone)
    return match_time_lt

def is_previous_war_day(match_time_utc):
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    now = datetime.now()
    match_time_utc = parser.parse(match_time_utc)
    two_thirty_pm = parser.parse('14:30:00')
    two_thirty_pm = two_thirty_pm.replace(tzinfo=to_zone)  # speciff time is in localtime
    today_230 = two_thirty_pm.replace(day=now.day)
    previous_230 = two_thirty_pm.replace(day=now.day-1)
    yesterday_230 = two_thirty_pm.replace(day=now.day+1)


    # Convert time zone
    match_time_lt = match_time_utc.astimezone(to_zone)
    return previous_230 < match_time_lt < today_230

def is_today_war_day(match_time_utc):
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    now = datetime.now()
    match_time_utc = parser.parse(match_time_utc)
    two_thirty_pm = parser.parse('14:40:00')
    two_thirty_pm = two_thirty_pm.replace(tzinfo=to_zone)  # speciff time is in localtime
    today_230 = two_thirty_pm.replace(day=now.day)
    previous_230 = two_thirty_pm.replace(day=now.day-1)
    nextday_230 = two_thirty_pm.replace(day=now.day+1)


    # Convert time zone
    match_time_lt = match_time_utc.astimezone(to_zone)
    if  datetime.strptime('00:00:00', '%H:%M:%S').time() < now.time() < datetime.strptime('14:40:00', '%H:%M:%S').time():
        return previous_230 < match_time_lt < today_230
    else:
        return today_230 < match_time_lt < nextday_230

def cal_win_defeat(victory, defeat, game_mode,outcome,opp_clan_name):

    if game_mode == 'Duel':
        if outcome == 'Victory':
            if len(opp_clan_name) == 2:
                victory = victory + opp_clan_name
            elif len(opp_clan_name) == 3:
                victory = victory + opp_clan_name[:2]
                defeat = defeat + [opp_clan_name[2]]
            else:
                print(f"Error in length of clan name: {opp_clan_name}")

        elif outcome == 'Defeat':
            if len(opp_clan_name) == 2:
                defeat = defeat + opp_clan_name
            elif len(opp_clan_name) == 3:
                defeat = defeat + opp_clan_name[:2]
                victory = victory + [opp_clan_name[2]]
            else:
                print(f"Error in length of clan name: {opp_clan_name}")
        else:
            print(f"error in Outcome string: {outcome}")
    else:
        if outcome == 'Victory':
            victory = victory + opp_clan_name
        elif outcome == 'Defeat':
            defeat = defeat + opp_clan_name
        else:
            print(f"error in Outcome string: {outcome}")

    return victory, defeat

def cal_win_defeat_single(victory, defeat,draw, game_mode,outcome,opp_clan_name):
    print(f"{opp_clan_name}Goes in cal_win_defeat_single")
    if game_mode == 'Duel':
        if outcome == 'Victory':
            if len(opp_clan_name) == 2:
                victory = victory + opp_clan_name
            elif len(opp_clan_name) == 3:
                victory = victory + opp_clan_name[:2]
                defeat = defeat + [opp_clan_name[2]]
            else:
                print(f"Error in length of clan name: {opp_clan_name}")

        elif outcome == 'Defeat':
            if len(opp_clan_name) == 2:

                defeat = defeat + opp_clan_name
            elif len(opp_clan_name) == 3:
                defeat = defeat + opp_clan_name[:2]
                victory = victory + [opp_clan_name[2]]
            else:
                print(f"Error in length of clan name: {opp_clan_name}")
        else:
            print(f"error in Outcome string: {outcome}")
    else:
        if outcome == 'Victory':
            victory = victory + opp_clan_name
        elif outcome == 'Defeat':
            defeat = defeat + opp_clan_name
        elif outcome == 'Draw':
            draw = draw + opp_clan_name
        else:
            print(f"error in Outcome string: {outcome}")

    return victory, defeat, draw
def cal_percentage(victory,defeat):
    total_matches = len(victory) + len(defeat)
    total_win_per = round(len(victory) / total_matches * 100, 1)
    def_per = (len(defeat) / total_matches) * 100
    win_count = Counter(victory)
    def_count = Counter(defeat)

    only_def = {k: 0 for k, v in def_count.items() if k not in win_count}

    all_match_count = {key: win_count[key] + def_count[key] for key in win_count} | {key: win_count[key] + def_count[key] for key in only_def}
    win_per = {key: round(win_count[key] / all_match_count[key] * 100, 1) for key in win_count} | only_def
    # win_per_sort = dict(sorted(win_per.items(), key=lambda x: x[1], reverse=True))
    all_match_count_sort = dict(sorted(all_match_count.items(), key=lambda x: x[1], reverse=True))

    return all_match_count_sort, win_count, win_per, total_win_per, total_matches


def is_match_diff_less_then_40sec(t1,t2):
    t3 = parser.parse(t1) - parser.parse(t2)
    t4 = parser.parse('00:06:00') - parser.parse('00:05:20') #40sec
    return t4 > t3

# match_time_utc = parser.parse('2023-03-02 03:41:11 UTC')
print(is_today_war_day("2023-03-04 11:36:35+05:00"))

print(is_match_diff_less_then_40sec('2023-03-03 21:02:55+05:00','2023-03-03 21:02:54+05:00'))

if is_match_diff_less_then_40sec('2023-03-03 21:02:55+05:00','2023-03-03 21:02:54+05:00'):
    print("hey")
#print(utc_to_lt("2023-02-26 13:22:08 UTC"))

print(datetime.strptime('00:00:00', '%H:%M:%S').time() <datetime.now().time() < datetime.strptime('15:00:00', '%H:%M:%S').time() )

to_zone = tz.tzlocal()
usa_zone = tz.gettz("America/New_York")
pk_zone = tz.gettz('Asia/Karachi')
time = now = datetime.now(pk_zone)
print(time)

# local = now.replace(tzinfo=to_zone)
# usa =now.replace(tzinfo=usa_zone)
# pk = usa.replace(tzinfo=pk_zone)
# print(local)
# print(usa)
# print(pk)

