import numpy as np

# de målte R-verdiene. [R1, R2, theta, krystallplan (kun for print)]        
# >>>> resultater

# [100]
R = np.array([4.94, 6.98, np.pi*45.5/180, 100, [0,0,-4]]) # R1, R2, theta in      
# >>> [2,0,0] og [2,2,0]  >>> P = [0,0,-4] -> {100}

# [110]
# R = np.array([4.23, 4.91, np.pi*54.2/180, 110, [2,2,0]]) # R1, R2, theta      
# >>> [0,0,2] og [-1,1,1] >>> P = [2,2,0]

# [110]
# R = np.array([6.92, 4.23, np.pi*35.5/180, 110, [2,2,0]]) # R1, R2, theta         
# >>> [-2,2,0] og [-1,1,1]  >>> P = [-2,-2,0] -> {110}


# boolean values to skip certain if statements. they skip when the boolean is TRUE
skip_zone_axis_filter = False


R_ratio = (R[0]/R[1])**2 # ratio mellom R1 og R2
maks_hkl = 4 # maksverdien-1 for hkl-tallene
min_hkl = -3
ratio_threshold = 0.05 # terskel for ratio, likning 10 i TEM-labinfo
angle_threshold = 0.1 # terskel for cos-ratio, likning 13 i TEM-labinfo


# regner ut kvadratroten av verdiene til h, k og l
def hkl_sqare(list): 
        return (list[0]**2 + list[1]**2 + list[2]**2)

# regner ut venstresiden av cos-likningen
def cos_check(l1,l2):
    return ( l1[0]*l2[0] + l1[1]*l2[1] + l1[2]*l2[2] )/(np.sqrt(hkl_sqare(l1))*np.sqrt(hkl_sqare(l2)))

# denne funksjonen sjekker vel om siste bit er 1 eller 0
def is_odd(num):
    return num & 0x1

# samme som over, bare for partall
def is_even(num):
    return is_odd(num+1)


# lage listen med alle mulige hkl-kombinasjoner fra 0 til maks_hkl.
# sjekker at hkl ikke er [0,0,0].
# gjør FCC-sjekken, altså kun odde- eller partall i én hkl
def make_hkl():
    hkl = []
    hkl_sum = []
    for h in range (min_hkl, maks_hkl):
            for k in range(min_hkl, maks_hkl):
                    for l in range(min_hkl, maks_hkl):
                        midlertidig = [h, k, l]
                        if midlertidig != [0,0,0]:
                            summen = hkl_sqare(midlertidig)
                            # print(summen)
                            # denne fjerner alle duplikater, i.e. [2,0,0] og [0,2,0] og [0,0,2] er ekvivalente
                            # if summen not in hkl_sum: 
                                # denne gjør FCC-sjekken, i.e. alle tall i én hkl er oddetall eller partall
                            if (is_odd(h) and is_odd(k) and is_odd(l)) or (is_even(h) and is_even(k) and is_even(l)):
                                # print(h, k, l)
                                hkl.append(midlertidig)
                                hkl_sum.append(summen)
    # print(hkl)
    # print(len(hkl))
    return hkl, hkl_sum

hkl_list, hkl_sum = make_hkl()
# print(hkl)
# print(len(hkl))


# sjekker først om ratio R_1 / R_2 er innenfor ratio_threshold
# sjekker så om vinkelen er innenfor angle_threshold
# skriver ut mulige hkl-kombinasjoner
# OBS: bruker må selv anvende ekskluderingsprinsippet for fcc (alle oddetall eller alle partall)

def possible_hkl_check(hkl, hkl_sum, ratio_threshold, angle_threshold):
    possbile_hkl = []
    for i in range (len(hkl)):
        for j in range (len(hkl)):
            ratio = hkl_sum[i]/hkl_sum[j]
            if abs(R_ratio-ratio) < ratio_threshold:
                if abs(np.cos(R[2])-(cos_check((hkl[i]), (hkl[j])))) < angle_threshold:
                    # print(str(hkl[i]) + " / " + str(hkl[j]))
                    if (str(np.cross(hkl[i],hkl[j])) == str(np.array(R[4])) or skip_zone_axis_filter):
                        print(f"[{int(R[3])}]: hkl(1) = {hkl[i]} & hkl(2) = {hkl[j]}, crossproduct: {np.cross(hkl[i],hkl[j])}")
                        # print(f"& & {hkl[i][0]}, {hkl[i][1]}, {hkl[i][2]} & & {hkl[j][0]}, {hkl[j][1]}, {hkl[j][2]} ")

                    # print((cos_check((hkl[i]), (hkl[j])))-np.cos(R[2]))
                    possbile_hkl.append([hkl[i], hkl[j]])
    return possbile_hkl

possibilities = possible_hkl_check(hkl_list, hkl_sum, ratio_threshold, angle_threshold)

# print(possibilities)
print(len(possibilities))




