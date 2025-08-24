import sys
from pathlib import Path

# Add data to path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from data.reducers_tables import reducers_df,resonance_frequency,torsional_data
from math import pi

gear_index = 0

def average(load_data):
    '''
    this function calculates the average based on the load cycle
    Parameters
    --------------
    load_data : dictionary
        Combined dictionary containing:
        {'dt': list, 'T_cycle': list, 't_k': float, 'T_k': float, 't_p': float, 'n_cycle': list, 'n_k': float}

    Returns
    -------------
    T_av : float
        the average torque in Nm 
    nt : float
        the average angular speed in rpm     
    '''
    # Combined T and n into load_data
    T3nt = 0 # = |(T_1)^3*n_1|*t1+...+|(T_n)^3*n_n|*t_n
    nt = 0 # = n_1*t1+...+n_n*t_n
    for T_i, n_i, dt in zip(load_data['T_cycle'], load_data['n_cycle'], load_data['dt']):
        T3nt += abs(T_i**3 * n_i) * dt
        nt += abs(n_i) * dt
    T_av = (T3nt / nt) ** (1/3)
    return T_av, nt

def torque_based_dimensioning(type,load_data,L_10_req,first_selection = {'Series': "HFUS",'Size': 11,'Ratio': 50}):
    """
        This function determines the validity of Reducer based on 
        the average cyclic load and the operation speed
        
        Parameters
        --------------
        type : str
            type of reducer you need

        load_data : dictionary
            Combined dictionary containing:
            {'dt': list, 'T_cycle': list, 't_k': float, 'T_k': float, 't_p': float, 'n_cycle': list, 'n_k': float}
            # Combined T and n into load_data
        
        L_10_req : float
            the required lifetime in hours

        first_selection : dict
            {"Series": str, "Size": int, "Ratio": int}

        Returns
        -------------
        gear : string 
            gear model
    """

    #find the first selection index in table
    try:
        result = reducers_df[(reducers_df["Series"] == first_selection["Series"]) & (reducers_df["Size"] == first_selection['Size']) & (reducers_df["Ratio"] == first_selection["Ratio"])]
        first_index = (result.index.values[0])
    except Exception as e:
        raise Exception("your first selection is not in the table!")

    if first_selection == {'Series': "HFUS",'Size': 11,'Ratio': 50} and type != "HFUS":
        # Condition: column 'Series' equal type of gear
        condition = reducers_df["Series"] == type
        # Get first index satisfying the condition
        first_index = reducers_df[condition].index[0]
    else:
        if type != first_selection["Series"]:
            raise Exception("type of gear should be the same as your first selection!")

    # Use combined load_data for average calculation
    T_av, nt = average(load_data)

    # main algorithm loop
    global gear_index
    gear_index = first_index
    while 1:
        
        if gear_index >= len(reducers_df):
            return ("no suitable gear found, try to change your first selection or the type of gear")
        # Calculation of the average output speed
        T_A = reducers_df.loc[gear_index,"Limit for average torque [Nm]"]
        
        if T_A < T_av:
            gear_index+=1
            continue
        
        # Calculation of the average output speed
        i = reducers_df.loc[gear_index,"Ratio"]
        input_n_av = i * (nt / (sum(load_data['dt']) + load_data['t_p']))
        n_av = reducers_df.loc[gear_index,"Limit for average input speed [rpm]"]
        # Checking the permissible average Input speed nin av ≤ nav (max)
        if n_av < input_n_av:
            gear_index+=1
            continue
        
        # Determination of the maximum input speed from load cycle
        input_n_max = i * max(load_data['n_cycle'])
        n_max = reducers_df.loc[gear_index,"Max. input speed [rpm]"]
        # Checking the permissible maximum input speed nin max ≤ nin (max)
        if  n_max < input_n_max:
            gear_index+=1
            continue

        # Determination of the maximum torque from load cycle
        R_T_max = max(load_data['T_cycle']) # repeated maximum torque from cycle
        T_R = reducers_df.loc[gear_index, "Limit for repeated peak torque [Nm]"]
        # Checking the permissible repeated peak torque Tmax ≤ TR
        if R_T_max > T_R:
            gear_index += 1
            continue
        
        # Determination of the overload torque
        T_k = load_data['T_k']
        T_M = reducers_df.loc[gear_index,"Limit for momentary peak torque [Nm]"]
        # Checking the permissible momentary peak torque TK ≤ TM
        if T_k > T_M:
            gear_index+=1
            continue

        # Determining the number of momentary peak torques
        N_k = 1e4 / (2 * load_data['n_k'] / 60 * i * load_data['t_k'])
        if N_k > 1e4:
            gear_index+=1
            continue

        # Checking the Wave Generator bearing lifetime 
        # Calculated lifetime L10h > required lifetime L10 req.
        n_N = 2000 # speed at rated torque
        T_N = reducers_df.loc[gear_index,"Rated torque at rated speed 2000 rpm [Nm]"]
        L_n = 10000 # Nominal lifetime
        L_10 = L_n*(n_N/input_n_av)*(T_N/T_av)**3
        # Checking the Wave Generator bearing lifetime
        # Calculated lifetime L10h > required lifetime L10 req.
        if L_10_req > L_10:
            gear_index+=1

        
        # the last index for SHG table
        result = reducers_df[(reducers_df["Series"] == "SHG") & (reducers_df["Size"] == 65) & (reducers_df["Ratio"] == 160)]
        last_shg_index = (result.index.values[0])
        if gear_index == last_shg_index:
            raise Exception("no suitable gear found for SHG, try to change your type of gear")

        break

    return str(reducers_df.loc[gear_index,"Series"])+"-"+str(reducers_df.loc[gear_index,'Size'])+"-"+str(reducers_df.loc[gear_index,'Ratio'])+"-"+"2UH"


def stiffness_based_dimensioning(application,J):
    '''
    evaluates the ratio of the load moment of inertial to the stiffness of the
    gear and compares it to the application requirements.

    Parameters
    --------------
    application : str
        type of application you use the gear for
    J : float
        load moment of inertia in kg.m^2    

    Returns
    -------------
    gear : string 
        gear model
    '''
    global gear_index
    # calculation of the resonance frequency of the drive
    while 1:
        gear_series = reducers_df.loc[gear_index, "Series"]
        gear_size = int(reducers_df.loc[gear_index, 'Size'])
        gear_ratio = int(reducers_df.loc[gear_index, 'Ratio'])
        f_res = resonance_frequency[application]
        # selecting the right column based on the gear ratio
        ratio = lambda x: 30 if x <= 30 else (50 if x <= 50 else 80)
        K_1 = torsional_data[gear_series].loc[torsional_data[gear_series]["Size"] == gear_size, "K1_i" + str(ratio(gear_ratio)) + " [x10^4 Nm/rad]"].values[0] * 1e4 #Nm/rad
        f_n = (1 / (2 * pi)) * ((K_1 / J) ** 0.5) # working resonance frequency in Hz
        # Checking the permissible resonance frequency fn ≥ fres
        if f_n < f_res:
            gear_index += 1
            continue

        # the last index for SHG table
        result = reducers_df[(reducers_df["Series"] == "SHG") & (reducers_df["Size"] == 65) & (reducers_df["Ratio"] == 160)]
        last_shg_index = (result.index.values[0])
        if gear_index == last_shg_index:
            raise Exception("no suitable gear found for SHG, try to change your type of gear")
        break
    
    return str(reducers_df.loc[gear_index, "Series"]) + "-" + str(reducers_df.loc[gear_index, 'Size']) + "-" + str(reducers_df.loc[gear_index, 'Ratio']) + "-" + "2UH"

def torsional_angel(load):
    '''
    this function determine the tortional angle based on the gear selected and the load applied
    
    Parameters
    --------------
    load : float
        the load applied on the gear in Nm
    
    Returns
    -------------
    angle : float
        the tortional angle in armin    
    '''
    gear_series = load.split("-")[0]
    gear_size = int(load.split("-")[1])
    gear_ratio = int(load.split("-")[2])
    #compute the tortional angle
    T_1 = torsional_data[gear_series].loc[torsional_data[gear_series]["Size"] == gear_size,"T1 [Nm]"].values[0]
    T_2 = torsional_data[gear_series].loc[torsional_data[gear_series]["Size"] == gear_size,"T2 [Nm]"].values[0]
    ratio = lambda x: 30 if x <= 30 else (50 if x <= 50 else 80)
    K_1 = torsional_data[gear_series].loc[torsional_data[gear_series]["Size"] == gear_size, "K1_i"+str(ratio(gear_ratio))+" [x10^4 Nm/rad]"].values[0]*1e4 #Nm/rad
    K_2 = torsional_data[gear_series].loc[torsional_data[gear_series]["Size"] == gear_size, "K2_i"+str(ratio(gear_ratio))+" [x10^4 Nm/rad]"].values[0]*1e4 #Nm/rad
    K_3 = torsional_data[gear_series].loc[torsional_data[gear_series]["Size"] == gear_size, "K3_i"+str(ratio(gear_ratio))+" [x10^4 Nm/rad]"].values[0]*1e4 #Nm/rad
    
    if load <= T_1:
        angle = (load/K_1) #armin
    elif load <= T_2:
        angle = (load/K_2)+((T_1/K_1)-(T_1/K_2)) #armin
    else:
        angle = (load/K_3)+((T_1/K_1)-(T_1/K_3))+((T_2/K_2)-(T_2/K_3)) #armin   
    
    return angle

def output_bearing_dimensioning(F_tilting,L_r,L_a,R):
    '''
    this function determine the validity of output bearing based on the gear selected
    '''
    Fr_max = F_tilting['Fr_max'] #N
    Fa_max = F_tilting['Fa_max'] #N
    M_max = Fr_max*(L_r+R) + Fa_max*L_a #Nm
    B = 10.0/3.0 #only for crossed roller bearing
    # If you want to use average for combined data, update accordingly
    # Fr_av = average(F_tilting) #N
    


    
    

load_data = {
    'dt': [0.3, 3, 0.4],
    'T_cycle': [400, 320, 200],
    't_k': 0.15,
    'T_k': 1000,
    't_p': 0.2,
    'n_cycle': [7, 14, 7],
    'n_k': 14
}

# Combined T and n into load_data
L_req = 15000

print(torque_based_dimensioning("CSG", load_data, L_req, first_selection={'Series': "CSG", 'Size': 40, 'Ratio': 120}))
print(stiffness_based_dimensioning("Milling heads for woodworking (hardwood etc.)", 7))
