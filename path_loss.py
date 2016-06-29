import numpy as np

h_bs = 50   # height of Basestation Antenna(m)
h_m = 1.5   # Height of Mobile(m)
freq_a = 860    # Alpha Sector
freq_b = 865    # Beta Sector

# calculate fading for alpha and beta sectors
fading_a = np.random.rayleigh(1, 10)
fading_b = np.random.rayleigh(1, 10)
# Take the second lowest value as the fading loss and convert to db
fading_db_a = 10*np.log10(sorted(fading_a)[1])
fading_db_b = 10*np.log10(sorted(fading_b)[1])
# Calculate a_hm for both sectors
a_hm_a = 0.8 + (1.1*np.log10(freq_a)-0.7)*h_m - 1.56*np.log10(freq_a)
a_hm_b = 0.8 + (1.1*np.log10(freq_b)-0.7)*h_m - 1.56*np.log10(freq_b)


def path_loss(dist):
    # calculate the distance from base station (pythagoras theorem)
    # the dist here is calculated in kms
    e_dist = np.sqrt((dist/1000.0)**2 + 0.020**2)
    # Propagation loss for alpha and beta
    prop_loss_a = 69.55 + (26.16 * np.log10(freq_a)) - (13.82 * np.log10(h_bs)) - a_hm_a + (44.9-(6.55*np.log10(h_bs))) * np.log10(e_dist)
    prop_loss_b = 69.55 + (26.16 * np.log10(freq_b)) - (13.82 * np.log10(h_bs)) - a_hm_b + (44.9-(6.55*np.log10(h_bs))) * np.log10(e_dist)
    loss_a = prop_loss_a - fading_db_a
    loss_b = prop_loss_b - fading_db_b
    # return the loss to the function call
    return loss_a, loss_b
