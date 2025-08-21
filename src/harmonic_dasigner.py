import sys
from pathlib import Path

# Add data to path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from data.reducers_tables import solid_shaft_df,hollow_shaft_df

def tourqe_based_dimensioning(T,n,L_10_req,gear_set_df):
    """
        this function determine the validity of Reducer based on 
        the average cyclic load and the the opreation speed
        
        Parameters
        --------------
        T : dictionary
            {'dt' (timestamps): list,'T_cyclic': list,t_k (overload time): float ,'T_k'(overload Tourqe): float,'t_p' (Dwell time): float}.
        
        n : dictionary
            {'n_cycle': *, 'n_k' (speed at overload): *}
        
        L_10_req : float
            the required lifetime in houres
        
        gear_set_df : pandas DataFrame
            the dataset for the gear type hollow or solid shaft

        Returns
        -------------
        gear : string 
            gear model
    """

    

    T3nt = 0 # = |(T_1)^3*n_1|*t1+...+|(T_n)^3*n_n|*t_n
    nt = 0 # = n_1*t1+...+n_n*t_n
    #this loop calulate the average tourqe T_av
    for T_i,n_i,dt in zip(T['T_cycle'],n['n_cycle'],T['dt']):
        T3nt += abs(T_i**3*n_i)*dt
        nt += abs(n_i)*dt
    T_av = (T3nt/nt)**(1/3)

    # main algorithm loop
    gear_index = 0
    while 1:
        # Calculation of the average output speed
        T_A = gear_set_df.loc[gear_index,"Limit for average torque [Nm]"]
        i = gear_set_df.loc[gear_index,"Ratio"]
        
        if T_A < T_av:
            gear_index+=1
            continue
        
        # Calculation of the average output speed
        input_n_av =  i*(nt/(sum(T['dt'])+T['t_p']))
        n_av = gear_set_df.loc[gear_index,"Limit for average input speed [rpm]"]
        # Checking the permissible average Input speed nin av ≤ nav (max)
        if n_av < input_n_av:
            gear_index+=1
            continue
        
        # Determination of the maximum input speed from load cycle
        input_n_max = i*max(n['n_cycle'])
        n_max = gear_set_df.loc[gear_index,"Max. input speed [rpm]"]
        # Checking the permissible maximum input speed nin max ≤ nin (max)
        if  n_max < input_n_max:
            gear_index+=1
            continue

        # Determination of the maximum torque from load cycle
        R_T_max = max(T['T_cycle']) # repeted maximum tourqe from cycle
        T_R = gear_set_df.loc[gear_index,"Limit for repeated peak torque [Nm]"]
        # Checking the permissible repeated peak torque Tmax ≤ TR
        if R_T_max > T_R:
            gear_index+=1
            continue
        
        # Determination of the overload torque
        T_k = T['T_k']
        T_M = gear_set_df.loc[gear_index,"Limit for momentary peak torque [Nm]"]
        # Checking the permissible momentary peak torque TK ≤ TM
        if T_k > T_M:
            gear_index+=1
            continue

        # Determining the number of momentary peak torques
        N_k = 1e4/(2*n['n_k']/60*i*T['t_k'])
        if N_k > 1e4:
            gear_index+=1
            continue

        # Checking the Wave Generator bearing lifetime 
        # Calculated lifetime L10h > required lifetime L10 req.
        n_N = 2000 # speed at rated tourqe
        T_N = gear_set_df.loc[gear_index,"Rated torque at rated speed 2000 rpm [Nm]"]
        L_n = 10000 # Nominal lifetime
        L_10 = L_n*(n_N/input_n_av)*(T_N/T_av)**3
        # Checking the Wave Generator bearing lifetime
        # Calculated lifetime L10h > required lifetime L10 req.
        if L_10_req < L_10:
            gear_index+=1

        break

    print(gear_set_df.loc[gear_index])

T = {'dt': [0.3,3,0.4],'T_cycle':[400,320,200],'t_k': 0.15,'T_k':1000,'t_p': 0.2}
n = {'n_cycle': [7,14,7], 'n_k': 14}

L_req = 15000

tourqe_based_dimensioning(T,n,L_req,solid_shaft_df)
