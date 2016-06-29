import numpy as np

EIRP = 56   # (43-1+15 in the direction of the unit vectors)
antenna_pattern = open("antenna_pattern.txt", "r")
input_string = antenna_pattern.read()
antenna_pattern_raw = input_string.split()
antenna_pattern.close()

antenna_loss = []
# store the antenna discrimination losses into an array
for i in range(0, len(antenna_pattern_raw), 2):
    antenna_loss.append(float(antenna_pattern_raw[i+1]))
unit_vector_a = [0, 1]
unit_vector_b = [np.sqrt(3)/2.0, -1/2]
mag_a = 1
mag_b = 1


def rad_power(location):
    mobile_position = [20, location]    # Location of mobile from the reference point
    mag_mob = np.sqrt(400 + location**2)
    dot_p_a = np.dot(mobile_position, unit_vector_a)
    dot_p_b = np.dot(mobile_position, unit_vector_b)
    # Find θ
    theta_a = np.arccos(dot_p_a/(mag_mob*mag_a))
    theta_b = np.arccos(dot_p_b/(mag_mob*mag_b))
    # Convert from radians to degrees
    theta_d_a = int((theta_a*180)/np.pi)
    theta_d_b = int((theta_b*180)/np.pi)
    # Return the EIRP in the given location
    return EIRP - antenna_loss[theta_d_a], EIRP - antenna_loss[theta_d_b]
