from data.reducers_tables import solid_shaft_df,hollow_shaft_df

def tourqe_based_dimensioning(T,n,i,gear_set_df):
    """
        this function determine the validity of Reducer based on 
        the average cyclic load and the the opreation speed
        
        Parameters
        --------------
        T : dictionary
            {'dt': *,'T_cyclic': *,t_k (overload time): * ,'T_k'(overload Tourqe): *}.
        
        n : list 
            rotational speeds in (rpm)
        
        i : int
            the reduction ratio input_speed/out_speed

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
    for T,n_i in zip(T.T_cyclic,n):
        T3nt += abs(T**3*n_i)*T.dt
        nt += abs(n_i)*T.dt
    T_av = (T3nt/nt)**(1/3)

    T_A = gear_set_df.loc[0,"Limit for average torque [Nm]"]

    # this loop check and stop for the reducer with the appropriat average load
    while 1:
        if T_A < T_av:
            gear_index+=1
            T_A = gear_set_df.loc[gear_index,"Limit for average torque [Nm]"]
            continue
        break
    
    input_n_av =  i*(nt/sum(T.dt))
    
    n_av = gear_set_df.loc[0,"Limit for average input speed [rpm]"]
    while 1:
        if n_av < input_n_av:
            gear_index+=1
            n_av = gear_set_df.loc[gear_index,"Limit for average input speed [rpm]"]
            continue
        break


tourqe_based_dimensioning()