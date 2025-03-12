import numpy as np
import pandas as pd

df = pd.read_csv("NFL Play by Play 2009-2018 (v7).csv", low_memory=False)

print('** Welcome to Our Football Play Call Model **')
print()

def prompt():
    """
    Prompts the user and returns the command number

    Parameters
    ----------
    None

    Returns
    -------
    Command number entered by user (0, 1)
    """
    print()
    print(">> Enter a command:")
    print("   0 => exit")
    print("   1 => new play")

    cmd = int(input())
    return cmd


def play_call():
    try:

        down = int(input("What down is it? \n"))
        yards_to_go = int(input("How many yards to first down? \n"))
        yards_to_td = int(input("How many yards to touchdown? \n"))
        quarter = int(input("Which quarter is it? (Overtime is 5)\n"))
        time_remaining = input("How much time left in quarter? (format as mm:ss) \n")
        score = input("What is the score? (format as xx-yy with your score first and opponent's score second) \n")

        if type(down) != int or down > 4:
            raise Exception("Invalid down entered")

        minutes, seconds = map(int, time_remaining.split(":"))
        time_remaining_secs = 0
        if quarter == 1:
            time_remaining_secs = 2700 + seconds + (minutes * 60)
        elif quarter == 2:
            time_remaining_secs = 1800 + seconds + (minutes * 60)
        elif quarter == 3:
            time_remaining_secs = 900 + seconds + (minutes * 60)
        elif quarter == 4 or quarter == 5:
            time_remaining_secs = seconds + (minutes * 60)

        if (time_remaining_secs < 240) | (1800 < time_remaining_secs <= 2000):
            drilling = 1
        else:
            drilling = 0

        yourscore, oppscore = map(int, score.split('-'))

        score_dif = yourscore - oppscore

        if time_remaining_secs > 3600 or time_remaining_secs < 0:
            raise Exception("Invalid time entered")

        within_three = 0
        within_eight = 0
        blowout = 0
        winning = 0

        if (score_dif >= -8) and (score_dif < -3):
            within_eight = 1
        elif (score_dif >= -3) and (score_dif <= 0):
            within_three = 1
        elif score_dif < -8:
            blowout = 1
        else:
            winning = 1

        backed_up = 0
        own_terr = 0
        midfield = 0
        opp_terr = 0
        red_zone = 0
        goal_to_go = 0

        if (yards_to_td >= 90) and (yards_to_td <= 100):
            backed_up = 1
        elif (yards_to_td >= 61) and (yards_to_td <= 89):
            own_terr = 1
        elif (yards_to_td >= 43) and (yards_to_td <= 60):
            midfield = 1
        elif (yards_to_td >= 21) and (yards_to_td <= 42):
            opp_terr = 1
        elif (yards_to_td >= 11) and (yards_to_td <= 20):
            red_zone = 1
        else:
            goal_to_go = 1



        rp = df[(df["down"] == down) &
                (df["ydstogo"] >= yards_to_go - 1) &
                (df["ydstogo"] <= yards_to_go + 1) &
                (df['backed_up'] == backed_up) &
                (df['own_terr'] == own_terr) &
                (df['midfield'] == midfield) &
                (df['opp_terr'] == opp_terr) &
                (df['red_zone'] == red_zone) &
                (df['goal_to_go'] == goal_to_go) &
                (df['drilling'] == drilling) &
                (df['within_three'] == within_three) &
                (df['within_eight'] == within_eight) &
                (df['blowout'] == blowout) &
                (df['winning'] == winning)
                ]

        # Filter out rows where EPA is not NaN
        rp_filtered = rp.dropna(subset=['epa'])

        pass_plays = rp_filtered[rp_filtered['play_type'] == 'pass']
        run_plays = rp_filtered[rp_filtered['play_type'] == 'run']
        punt_plays = rp_filtered[rp_filtered['play_type'] == 'punt']
        fg_plays = rp_filtered[rp_filtered['play_type'] == 'field_goal']

        pass_avg_epa = np.mean(pass_plays['epa'])
        run_avg_epa = np.mean(run_plays['epa'])
        punt_avg_epa = np.mean(punt_plays['epa'])
        fg_avg_epa = np.mean(fg_plays['epa'])

        # Build a dictionary with play types and their average EPAs
        plays = {'pass': pass_avg_epa, 
                 'run': run_avg_epa, 
                 'punt': punt_avg_epa, 
                 'field_goal': fg_avg_epa}

        # Remove play types with NaN EPAs from consideration
        plays = {play_type: avg_epa for play_type, avg_epa in plays.items() if not np.isnan(avg_epa)}

        # Choose the play type with the highest average EPA
        chosen_play = max(plays, key=plays.get)
        print(f"You should run the following play: {chosen_play}")
        print("Data Set Instances: " + str(rp.shape[0]))
        print("Here are the EPAs based on the different play types:")
        print(f"Run EPA: {run_avg_epa}")
        print(f"Pass EPA: {pass_avg_epa}")
        print(f"Field Goal EPA: {fg_avg_epa}")
        print(f"Punt EPA: {punt_avg_epa}")

    except Exception as e:
        print(e)


cmd = prompt()
while cmd != 0:
    if cmd == 1:
        play_call()
    else:
        print("** Unknown command, try again...")
    cmd = prompt()

print()
print('** done **')



