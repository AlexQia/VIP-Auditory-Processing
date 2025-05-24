import pandas as pd
import matplotlib.pyplot as plt


def data_sort(file_path, tones_to_plot):
    df = pd.read_csv(file_path, delimiter='\t', header=None)
    time = df[0].tolist()                 # elapsed time
    Num_left_lick = df[1].tolist()        # the number of left licks
    Num_right_lick = df[2].tolist()       # the number of right licks
    trial_start = df[6].tolist()          # this list contain the symbol whether it is the start trial
    tones = df[8].tolist()                # this list tell you which tone does this trial has
    free_water_indicator = df[10].tolist()    # this list indicates whether this trial uses free water
    trials = df[7].tolist()                   # count which trial it is


    all_trials = {}  # a grand dictionary that contains four tones as its four key; each key contains two dicts
    free_water_dict = {}
    for tone in tones_to_plot:
        Num = 1             # the number of trials
        dict = {}            # i.e. collect all sections of Tone 1
        time_tone = []       # the elapsed time in the specific trial
        tone_type = []
        lick_tone_L = []
        lick_tone_R = []
        free_water_dict[tone] = []        # in the specific tone, trials with free water are counted



        for i in range(len(trials)-1):

            if  trial_start[i] == 1 and tones[i] == tone:


                if time[i] - 2 > time[i - 1]:  # There is no lick between -2s to 0s

                    time_tone.extend([time[i - 1], time[i]])          # the reason to include [i-1], because I have to check whether the lick on i is valid
                    tone_type.extend([tones[i - 1], tones[i]])
                    lick_tone_L.extend([Num_left_lick[i - 1], Num_left_lick[i]])
                    lick_tone_R.extend([Num_right_lick[i - 1], Num_right_lick[i]])

                if time[i] - 2 <= time[i - 1]:  # There are licks between -2s to 0s
                    matching_indices = [j for j, t in enumerate(time) if time[i] >= t >= time[i] - 2]

                    time_tone.append(time[matching_indices[0] - 1])    # the reason to matching_indices[0] - 1, because I have to check whether the lick on matching_indices[0] is valid
                    tone_type.append(tones[matching_indices[0] - 1])
                    lick_tone_L.append(Num_left_lick[matching_indices[0] - 1])
                    lick_tone_R.append(Num_right_lick[matching_indices[0] - 1])

                    time_tone.extend(time[j] for j in matching_indices)
                    tone_type.extend(tones[j] for j in matching_indices)
                    lick_tone_L.extend(Num_left_lick[j] for j in matching_indices)
                    lick_tone_R.extend(Num_right_lick[j] for j in matching_indices)

            if trial_start[i] == 0 and tones[i] == tone:
                time_tone.append(time[i])
                tone_type.append(tones[i])
                lick_tone_L.append(Num_left_lick[i])
                lick_tone_R.append(Num_right_lick[i])

                if free_water_indicator[i] == 1:
                    #print(i)
                    print(trials[i])
                    free_water_dict[tone].append(Num)



            elif time_tone and tones[i + 1] != tone:
                dict[Num] = time_tone, tone_type, lick_tone_L, lick_tone_R
                time_tone = []
                tone_type = []
                lick_tone_L = []
                lick_tone_R = []
                Num += 1

        #print(dict)
        # print(free_water_dict.items())
        



        N = 1                          # The number of trials
        left_licks_in_trial = {}       # a dictionary that contains all left licks with respect to different trials
        right_licks_in_trial = {}      # a dictionary that contains all right licks with respect to different trials
        time_diff_L = []
        time_diff_R = []
        for z in dict:   # iterate through trials
            for h in range(len(dict[z][0])-1):              # iterate through elapsed time
                index = dict[z][1].index(tone)              # pinpoint the index of each trial start (sound starts)
                if dict[z][0][h + 1] < dict[z][0][index]:  # if licks happen before the sound
                    if dict[z][2][h + 1] != dict[z][2][h]:  # check if the first left lick is valid, by comparing with the previous lick
                        time_diff_L.append(dict[z][0][h + 1] - dict[z][0][index])
                    if dict[z][3][h + 1] != dict[z][3][h]:  # check if the first right lick is valid
                        time_diff_R.append(dict[z][0][h + 1] - dict[z][0][index])
                if dict[z][0][h + 1] >= dict[z][0][index]:  # licks happen after the sound
                    if dict[z][2][h] != dict[z][2][h + 1]:  # check if the first left lick is valid
                        time_diff_L.append(dict[z][0][h + 1] - dict[z][0][index])
                    if dict[z][3][h] != dict[z][3][h + 1]:    # check if the first right lick is valid
                        time_diff_R.append(dict[z][0][h + 1] - dict[z][0][index])



            left_licks_in_trial[N] = time_diff_L
            right_licks_in_trial[N] = time_diff_R
            time_diff_L = []
            time_diff_R = []
            N += 1

        all_trials[tone] = (left_licks_in_trial, right_licks_in_trial)      # save those two dicts for the specific tone
    print(free_water_dict.items())

    return all_trials, free_water_dict


def plot_raster_plots(file_path, all_trials,free_water_dict, tones_to_plot):

    plt.rc('font', size=5)          # controls default text size
    plt.rc('axes', titlesize=8)     # fontsize of the subplot titles
    plt.rc('axes', labelsize=7)     # fontsize of the x and y labels
    plt.rc('xtick', labelsize=8)    # fontsize of the tick labels
    plt.rc('ytick', labelsize=5)    # fontsize of the tick labels

    fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6), (ax7, ax8)) = plt.subplots(4, 2, figsize=(16, 10))
    axes = [(ax1, ax2), (ax3, ax4),(ax5, ax6), (ax7, ax8)]


    for idx, tone in enumerate(tones_to_plot):
        left_licks_in_trial, right_licks_in_trial = all_trials[tone]
        print('\nTone Type: ' + str(tone))

        # Left licks
        ax_left = axes[idx][0]
        print('Left Side')
        #for trial, (trial_L, licks_L) in enumerate(left_licks_in_trial.items()):
        for trial_L, licks_L in left_licks_in_trial.items():
            print(trial_L)
            print(licks_L)
            if trial_L in free_water_dict[tone]:
                if file_path[-1] == '1' or file_path[-1] == '2' or file_path[-1] == '4':
                    if tone == 1 or tone == 3:
                        ax_left.plot([licks for licks in licks_L if 3 <=  licks <= 5], [trial_L] * len([licks for licks in licks_L if 3 <=  licks <= 5]), '.', color='green', markersize=3)
                    else:
                        ax_left.plot(licks_L, [trial_L] * len(licks_L), '.', color='black', markersize=1)
                else:
                    if tone == 1 or tone == 3:
                        ax_left.plot([licks for licks in licks_L if 1 <=  licks <= 3], [trial_L] * len([licks for licks in licks_L if 1 <=  licks <= 3]), '.', color='green', markersize=3)
                    else:
                        ax_left.plot(licks_L, [trial_L] * len(licks_L), '.', color='black', markersize=1)
            else:
                ax_left.plot(licks_L, [trial_L] * len(licks_L), '.', color='black', markersize=1)
        ax_left.set_xlabel("time(s)", labelpad=-1)
        ax_left.set_ylabel("trial")
        ax_left.axvline(x=0, color='r', linestyle=':')
        if file_path[-1] == '1' or file_path[-1] == '2' or file_path[-1] == '4':
            ax_left.axvline(x=3, color='b', linestyle=':')
            ax_left.set_xlim(-2, 9)
            ax_left.set_xticks(range(-2, 10, 1))
        else:
            ax_left.axvline(x=1, color='b', linestyle=':')
            ax_left.set_xlim(-2, 7)
            ax_left.set_xticks(range(-2, 8, 1))
        ax_left.set_ylim(0, 70)
        if tone == 1:
            ax_left.set_title("Left Speaker, Tar 1 - Left Licks")
        if tone == 2:
            ax_left.set_title("Right Speaker, Tar 2 - Left Licks")
        if tone == 3:
            ax_left.set_title("Left Speaker, Tar 2 - Left Licks")
        if tone == 4:
            ax_left.set_title("Right Speaker, Tar 1 - Left Licks")


        # Right licks
        ax_right = axes[idx][1]
        print('\nRight Side')
        #for trial, (trial_R, licks_R) in enumerate(right_licks_in_trial.items()):
        #    print(trial)
        for trial_R, licks_R in right_licks_in_trial.items():
            print(trial_R)
            print(licks_R)
            #if trial in free_water_dict[tone]:
            if trial_R in free_water_dict[tone]:
                if file_path[-1] == '1' or file_path[-1] == '2' or file_path[-1] == '4':
                    if tone == 2 or tone == 4:
                        ax_right.plot([licks for licks in licks_R if 3 <=  licks <= 5], [trial_R] * len([licks for licks in licks_R if 3 <=  licks <= 5]), '.', color='green', markersize=3)
                    else:
                        ax_right.plot(licks_R, [trial_R] * len(licks_R), '.', color='black', markersize=1)
                else:
                    if tone == 2 or tone == 4:
                        ax_right.plot([licks for licks in licks_R if 1 <=  licks <= 3], [trial_R] * len([licks for licks in licks_R if 1 <=  licks <= 3]), '.', color='green', markersize=3)
                    else:
                        ax_right.plot(licks_R, [trial_R] * len(licks_R), '.', color='black', markersize=1)

            else:
                ax_right.plot(licks_R, [trial_R] * len(licks_R), '.', color='black', markersize=1)
        ax_right.set_xlabel("time(s)",labelpad=-1)
        ax_right.set_ylabel("trial")
        ax_right.axvline(x=0, color='r', linestyle=':')
        if file_path[-1] == '1' or file_path[-1] == '2' or file_path[-1] == '4':
            ax_right.axvline(x=3, color='b', linestyle=':')
            ax_right.set_xlim(-2, 9)
            ax_right.set_xticks(range(-2, 10, 1))
        else:
            ax_right.axvline(x=1, color='b', linestyle=':')
            ax_right.set_xlim(-2, 7)
            ax_right.set_xticks(range(-2, 8, 1))
        ax_right.set_ylim(0, 70)

        if tone == 1:
            ax_right.set_title("Left Speaker, Tar 1 - Right Licks")
        if tone == 2:
            ax_right.set_title("Right Speaker, Tar 2 - Right Licks")
        if tone == 3:
            ax_right.set_title("Left Speaker, Tar 2 - Right Licks")
        if tone == 4:
            ax_right.set_title("Right Speaker, Tar 1 - Right Licks")



    plt.tight_layout(pad=4.0)
    plt.show()


if __name__ == "__main__":
    file_path = 'local path'
    #
    # 04252025-121736-VIP_1 VERY GOOD
    # 04212025-104008-VIP_2
    tones_to_plot = [1, 2, 3, 4]
    all_trials, free_water_dict = data_sort(file_path, tones_to_plot)
    plot_raster_plots(file_path, all_trials,free_water_dict, tones_to_plot)