""" --------------------ENTS 656  Introduction to Cellular Communication Networks--------------
    ------------------------------Sectored Base Station simulation project---------------------
    ---------------------------Done by: Rohith Prabha Krishnan---------------------------------
    ------------------------------------UID: 114203274-------------------------------------"""
# import all relevant modules
import path_loss as pl
import eirp_calculator as ec
import numpy as np

# seed function to generate the same random numbers for every simulation
# np.random.seed(20)

total_time = 0  # Time counter which will keep track of the total time of simulation
time_step = 1   # in seconds
RSL_threshold = -102    # Mobile Rx Threshold
road_length = 6000  # length of road in meters
num_users = 160     # Total number of users at any given point of time
HOm = 3     # Handoff Margin
dir_choice = [1, -1]    # 1 for North, -1 for South
channel_unused_a = 15   # Number of traffic channels Alpha
channel_unused_b = 15   # Number of traffic channels Beta
call_rate = 2.0/3600    # Number of calls made in one second
prob_making_call = call_rate * time_step

active_call_details = []    # List which will hold the details of active calls during the simulation
caller_list = []    # List which will have the user number having active calls
# List of variables which will hold the system parameters
call_attempts_a = 0
call_attempts_b = 0
dropped_call_capacity_a = 0
dropped_call_capacity_b = 0
call_blocked_capacity_a = 0
call_blocked_capacity_b = 0
dropped_call_signal_strength_a = 0
dropped_call_signal_strength_b = 0
call_completed_successfully_a = 0
call_completed_successfully_b = 0
handoff_attempt_a = 0
handoff_attempt_b = 0
successful_handoff_a_out = 0
successful_handoff_b_out = 0
failed_handoff_out_a = 0
failed_handoff_out_b = 0
hourly_stats = []   # Hourly stats
cum_stats = []  # Final stats
hour = 0
shadowing_values = np.random.normal(0.0, 2, (road_length/10) + 1)

sim_end = False     # End the simulation when the timer reaches the total simulation time

# Start of simulation
print("--------Initial Conditions:------ \nRoad Length:{0} kms\nNumber of users:{1}\nHOm:{2} db\n"
      "Number of channels/sector:{3}".format(road_length/1000, num_users, HOm, channel_unused_a))
while sim_end is False:
    total_time += time_step     # Increment the time counter in counts of 1 second
    call_id = 0
    # Go through active caller List
    for j in active_call_details:
        call_id += 1
        if j[3] == 1:  # heading north
            j[1] += 15
            if j[1] > (road_length/2):      # If user moves out North of Alpha sector
                if j[4] is "Alpha":
                    call_completed_successfully_a += 1
                    channel_unused_a += 1
                else:
                    call_completed_successfully_b += 1
                    channel_unused_b += 1
                caller_list.remove(j[0])    # Remove the caller from active caller list
                del active_call_details[call_id-1]
                continue
        else:
            j[1] -= 15  # heading south
            if j[1] < -(road_length/2):
                if j[4] is "Alpha":
                    call_completed_successfully_a += 1
                    channel_unused_a += 1
                else:
                    call_completed_successfully_b += 1
                    channel_unused_b += 1
                caller_list.remove(j[0])
                del active_call_details[call_id-1]
                continue
        j[2] -= 1   # Decrement total duration of call by 1 second
        if j[2] <= 0:   # If the user has completed the call duration
            if j[4] is 'Alpha':
                channel_unused_a += 1
                call_completed_successfully_a += 1
            else:
                channel_unused_b += 1
                call_completed_successfully_b += 1
            caller_list.remove(j[0])
            del active_call_details[call_id-1]
            continue
        # For users who still have an active call
        (path_loss_a, path_loss_b) = pl.path_loss(j[1])
        EIRP_a, EIRP_b = ec.rad_power(j[1])
        temp = int(((j[1]+(road_length/2))/10))     # Calculate which part of the road the user
        shadowing_loss = shadowing_values[temp]
        RSL_a = EIRP_a - path_loss_a + shadowing_loss
        RSL_b = EIRP_b - path_loss_b + shadowing_loss
        if j[4] == "Alpha":  # If serving sector is Alpha
            if RSL_a >= RSL_threshold:
                if RSL_b >= RSL_a + HOm:
                    handoff_attempt_a += 1
                    if channel_unused_b > 0:
                        channel_unused_b -= 1
                        channel_unused_a += 1
                        j[4] = 'Beta'
                        successful_handoff_a_out += 1
                    else:
                        failed_handoff_out_a += 1
            else:
                dropped_call_signal_strength_a += 1
                channel_unused_a += 1
                caller_list.remove(j[0])
                del active_call_details[call_id-1]
        else:
            if RSL_b >= RSL_threshold:
                if RSL_a >= RSL_b + HOm:
                    handoff_attempt_b += 1
                    if channel_unused_a > 0:
                        channel_unused_a -= 1
                        channel_unused_b += 1
                        j[4] = "Alpha"
                        successful_handoff_b_out += 1
                    else:
                        failed_handoff_out_b += 1
            else:
                dropped_call_signal_strength_b += 1
                channel_unused_b += 1
                caller_list.remove(j[0])
                del active_call_details[call_id-1]
    # serve the rest of the users who do not have an active call
    for i in range(num_users):
        temp = np.random.uniform(0, 1)
        if i+1 in caller_list:  # Active users are already taken care of
            continue
        if temp < prob_making_call:
            user_location = np.random.uniform(-(road_length/2), (road_length/2))
            direction = np.random.choice(dir_choice)
            (path_loss_a, path_loss_b) = pl.path_loss(user_location)
            EIRP_a, EIRP_b = ec.rad_power(user_location)
            temp = int(((user_location+(road_length/2))/10))
            shadowing_loss = shadowing_values[temp]
            RSL_a = EIRP_a - path_loss_a - shadowing_loss
            RSL_b = EIRP_b - path_loss_b - shadowing_loss
            if RSL_a > RSL_b:
                call_attempts_a += 1
                if RSL_a >= RSL_threshold:
                    if channel_unused_a > 0:
                        # call is made and connected.
                        channel_unused_a -= 1
                        caller_list.append(i+1)
                        active_call_details.append([i+1, user_location, np.random.exponential(180), direction, 'Alpha'])
                    else:
                        call_blocked_capacity_a += 1
                        if RSL_b >= RSL_threshold:
                            if channel_unused_b > 0:
                                channel_unused_b -= 1
                                caller_list.append(i+1)
                                active_call_details.append([i+1, user_location, np.random.exponential(180), direction,
                                                            'Beta'])
                            else:
                                dropped_call_capacity_a += 1
                else:
                    dropped_call_signal_strength_a += 1
            else:
                call_attempts_b += 1
                if RSL_b >= RSL_threshold:
                    if channel_unused_b > 0:
                        # call is made and connected.
                        channel_unused_b -= 1
                        caller_list.append(i+1)
                        active_call_details.append([i+1, user_location, np.random.exponential(180), direction, 'Beta'])
                    else:
                        call_blocked_capacity_b += 1
                        if RSL_a >= RSL_threshold:
                            if channel_unused_a > 0:
                                caller_list.append(i+1)
                                channel_unused_a -= 1
                                active_call_details.append([i+1, user_location, np.random.exponential(180), direction,
                                                            'Alpha'])
                            else:
                                dropped_call_capacity_b += 1
                else:
                    dropped_call_signal_strength_b += 1

    if total_time % 3600 is 0:  # Generate a report for every hour
        cum_stats.append([[channel_unused_a, call_attempts_a, call_completed_successfully_a, handoff_attempt_a,
                           successful_handoff_a_out, failed_handoff_out_a, dropped_call_capacity_a,
                           dropped_call_signal_strength_a, call_blocked_capacity_a],
                          [channel_unused_b, call_attempts_b, call_completed_successfully_b, handoff_attempt_b,
                           successful_handoff_b_out, failed_handoff_out_b, dropped_call_signal_strength_b,
                           dropped_call_capacity_b, call_blocked_capacity_b]])
        if hour > 0:
            hourly_stats[0][0][0] = cum_stats[hour][0][0]
            hourly_stats[0][1][0] = cum_stats[hour][1][0]
            for j in range(1, 9):
                hourly_stats[0][0][j] = cum_stats[hour][0][j] - cum_stats[hour-1][0][j]
                hourly_stats[0][1][j] = cum_stats[hour][1][j] - cum_stats[hour-1][1][j]
        else:
            hourly_stats.append([cum_stats[0][0], cum_stats[0][1]])
        print(str(hour+1) + " Hour")
        print("Sector Alpha\n--------------------------------------------------------------------------")
        print(" Unused_Ch  Call_A  Call_C   HO_A    HO_S    HO_F    DR_S    DR_C    BL_C")
        for i in hourly_stats[0][0]:
            print("{0:=8}".format(i), end='')
        # print(cum_stats[hour][0])

        print("\nSector Beta\n--------------------------------------------------------------------------")
        print(" Unused_Ch  Call_A  Call_C   HO_A    HO_S    HO_F    DR_S     DR_C    BL_C")
        for i in hourly_stats[0][1]:
            print("{0:=8}".format(i), end='')
        print('\n')
        # print(cum_stats[hour][1])
        hour += 1
    if total_time == 3600*6:    # 3600 seconds * 6 i.e for 6 hours
        sim_end = True
print("------------------------Total simulation Report (Alpha)-------------------")
print(" Unused_Ch  Call_A  Call_C   HO_A    HO_S    HO_F    DR_S     DR_C    BL_C")
for i in cum_stats[hour-1][0]:
    print("{0:=8}".format(i), end='')
print("\n------------------------Total simulation Report (Beta)--------------------")
print(" Unused_Ch  Call_A  Call_C   HO_A    HO_S    HO_F    DR_S     DR_C    BL_C")
for i in cum_stats[hour-1][1]:
    print("{0:=8}".format(i), end='')
