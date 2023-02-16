from math import nan
from turtle import color
import numpy as np
from random import choice,choices
from BP_reward import get_reward
import matplotlib.pyplot as plt
from scipy import stats

student_id=810100064

medicines=[1,2]
doctors=np.zeros(shape=(3,100),dtype=int)
rewards=np.zeros(shape=(3,100),dtype=float)
A,B,C=0,1,2
#************************ Doctor A ************************
def doctor_a():
    WSLS_ref=0
    doctors[A][0]=choice(medicines)
    def WSLS(doctors,medicines,medicine_t,i,p):
        if i==doctors.shape[1]:
            return 0
        else:
            weights=np.array(medicines,dtype=float)
            weights[weights==medicine_t]=p
            weights[weights!=p]=1-p
            doctors[A][i]=choices(medicines, weights=weights, k=1)[0]

    doctors[A][0]=choice(medicines)           
    for i in range(0,doctors.shape[1]):
        medicine_t=doctors[A][i]
        rewards[A][i]=get_reward(medicine_t,student_id)
    
        if rewards[A][i]>=WSLS_ref:
            WSLS(doctors,medicines,medicine_t,i+1,0.8)
        else:
            WSLS(doctors,medicines,medicine_t,i+1,0.7)

    del i,medicine_t
    return rewards,doctors

#************************ Doctor B ************************
def doctor_b():
    for i in range(0,doctors.shape[1]):
        doctors[B][i]=choice(medicines)
        rewards[B][i]=get_reward(doctors[B][i],student_id)
    return rewards,doctors
#************************ Doctor C ************************
#Step 1
def doctor_c():
    print("\n"+"-"*55)
    print("Doctor C:\n"+"-"*55) 
    doctors[C][:10]=medicines[0]
    doctors[C][10:20]=medicines[1]
    Rewards_sum=[0,0]
    for i in range(20):
        rewards[C][i]=get_reward(doctors[C][i],student_id)
        Rewards_sum[doctors[C][i]-1]+=rewards[C][i]
        print("    {:3d}) Medicine: {}, Reward: {:6.3f} , State (Win/Lose) = None".format(i+1,doctors[C][i],rewards[C][i]))
    #Step 2
    for i in range(20,doctors.shape[1]):
        if i%10==0:
            max_reward_D_C=max(Rewards_sum)
            best_medicine_D_C=Rewards_sum.index(max_reward_D_C)+1     
        if i%10 in range(0,7):
            doctors[C,i]=best_medicine_D_C
            rewards[C][i]=get_reward(doctors[C][i],student_id)
            Rewards_sum[doctors[C][i]-1]+=rewards[C][i]
        else:
            doctors[C,i]=choice(medicines)
            rewards[C][i]=get_reward(doctors[C][i],student_id)
            Rewards_sum[doctors[C][i]-1]+=rewards[C][i]

        print("    {:3d}) Medicine: {}, Reward: {:6.3f} , State (Win/Lose) = None".format(i+1,doctors[C][i],rewards[C][i]))

    del best_medicine_D_C,max_reward_D_C,i,Rewards_sum   
    return rewards,doctors
#************************ Multi Execution **********************
n=20
rewards_20times=np.zeros((n,3,100))
doctors_20times=np.zeros((n,3,100))
for i in range(n):
    rewards_20times[i],doctors_20times[i]=doctor_a()
    rewards_20times[i],doctors_20times[i]=doctor_b()
    rewards_20times[i],doctors_20times[i]=doctor_c()


Medicine1=np.zeros((n,3,100),dtype=float)
Medicine2=np.zeros((n,3,100),dtype=float)
for x in range(n):
    for i in range(doctors_20times.shape[1]):
        for j in range(doctors_20times.shape[2]):
            if doctors_20times[x,i,j]==2:
                Medicine2[x,i,j]=rewards_20times[x,i,j]
            
            if doctors_20times[x,i,j]==1:
                Medicine1[x,i,j]=rewards_20times[x,i,j]
            
                
mean_reward_medicine1=np.nanmean(Medicine1,axis=(1,2))
mean_reward_medicine2=np.nanmean(Medicine2,axis=(1,2))
alpha=0.05

#************************ Hypothesis Testing **********************
def Hypothesis_testing(data1,data2):
    res=""
    ttest,p_value = stats.ttest_ind(data1, data2)
    if p_value/2 < alpha:
        res="Since {:.2e} < {} then:\n    Null Hypothesis [H₀] is Rejected\n\n".format(p_value/2,alpha)
    else:
        res="Since {:.2e} > {}} then:\n    Null Hypothesis [H₀] is  Not Rejected\n\n".format(p_value/2,alpha)

    return res

res=Hypothesis_testing(mean_reward_medicine1,mean_reward_medicine2)

#************************ Report **********************

print("="*70)
print("Hypothesis Testing")
print("="*70)
print('''Defining Hypothesis:\n
    H₀: mean_reward_medicine_1 <= mean_reward_medicine_2
    H₁: mean_reward_medicine_1 > mean_reward_medicine_2\n''')
print("-"*70)
print(res)
