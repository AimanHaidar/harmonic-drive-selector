import sys
from pathlib import Path

# Add data to path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from data.reducers_tables import solid_shaft_df,hollow_shaft_df

def tourqe_based_dimensioning(T,n,gear_set_df):
    """
        this function determine the validity of Reducer based on 
        the average cyclic load and the the opreation speed
        
        Parameters
        --------------
        T : dictionary
            {'dt': *,'T_cyclic': *,t_k (overload time): * ,'T_k'(overload Tourqe): *}.
        
        n : list 
            rotational speeds in (rpm)
        
        gear_set_df : pandas DataFrame
            the dataset for the gear type hollow or solid shaft

        Returns
        -------------
        gear : string 
            gear model
    """

    gear_index = 0

    T3nt = 0 # = |(T_1)^3*n_1|*t1+...+|(T_n)^3*n_n|*t_n
    nt = 0 # = n_1*t1+...+n_n*t_n
    #this loop calulate the average tourqe T_av
    for T_i,n_i in zip(T['T_cycle'],n):
        T3nt += abs(T_i**3*n_i)*T['dt']
        nt += abs(n_i)*T['dt']
    T_av = (T3nt/nt)**(1/3)

    # Calculation of the average output speed
    T_A = gear_set_df.loc[0,"Limit for average torque [Nm]"]
    i = gear_set_df.loc[gear_index,"Ratio"]
    input_n_av =  i*(nt/(len(T['T_cycle']*T['dt'])))
    n_av = gear_set_df.loc[0,"Limit for average input speed [rpm]"]

    # Determination of the maximum input speed from load cycle
    input_n_max = i*max(n)
    n_max = gear_set_df.loc[0,"Max. input speed [rpm]"]

    #Determination of the maximum torque from load cycle
    R_T_max = max(T['T_cycle']) # repeted maximum tourqe from cycle
    T_R = gear_set_df.loc[0,"Limit for repeated peak torque [Nm]"]

    # Determination of the overload torque
    T_k = T['T_k']
    T_M = gear_set_df.loc[0,"Limit for momentary peak torque [Nm]"]

    # main algorithm loop
    while 1:
        if T_A < T_av:
            gear_index+=1
            T_A = gear_set_df.loc[gear_index,"Limit for average torque [Nm]"]
            continue

        if n_av < input_n_av:
            gear_index+=1
            n_av = gear_set_df.loc[gear_index,"Limit for average input speed [rpm]"]
            continue

        if  n_max < input_n_max:
            gear_index+=1
            n_max = gear_set_df.loc[gear_index,"Max. input speed [rpm]"]
            continue

        if R_T_max > T_R:
            gear_index+=1
            T_R = gear_set_df.loc[gear_index,"Limit for repeated peak torque [Nm]"]
            continue
        
        if T_k > T_M:
            gear_index+=1
            T_M = gear_set_df.loc[gear_index,"Limit for momentary peak torque [Nm]"]
            continue

        break
    print(gear_set_df.loc[gear_index])
