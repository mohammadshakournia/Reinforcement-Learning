import numpy as np
from random import choice,choices
from BP_reward import get_reward
import matplotlib.pyplot as plt

student_id=810100064

medicines=[1,2]
doctors=np.zeros(shape=(3,100),dtype=int)
rewards=np.zeros(shape=(3,100),dtype=float)
A,B,C=0,1,2
#************************ Doctor A ************************
def doctor_a():
    print("\n"+"-"*55)
    print("Doctor A:\n"+"-"*55)
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
            print("    {:3d}) Medicine: {}, Reward: {:6.3f} , State (Win/Lose) = Win".format(i+1,medicine_t,rewards[A][i]))
            WSLS(doctors,medicines,medicine_t,i+1,0.8)
        else:
            print("    {:3d}) Medicine: {}, Reward: {:6.3f} , State (Win/Lose) = Lose".format(i+1,medicine_t,rewards[A][i]))
            WSLS(doctors,medicines,medicine_t,i+1,0.7)

    del i,medicine_t
    return rewards

#************************ Doctor B ************************
def doctor_b():
    print("\n"+"-"*55)
    print("Doctor B:\n"+"-"*55)
    for i in range(0,doctors.shape[1]):
        doctors[B][i]=choice(medicines)
        rewards[B][i]=get_reward(doctors[B][i],student_id)
        print("    {:3d}) Medicine: {}, Reward: {:6.3f} , State (Win/Lose) = None".format(i+1,doctors[B][i],rewards[B][i]))
    return rewards
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
    return rewards
#************************ Multi Execution **********************
n=10
rewards_10times=np.zeros((n,3,100))
for i in range(n):
    print("="*55+"\nStep %d\n"%(i+1)+"="*55)
    rewards_10times[i]=doctor_a()
    rewards_10times[i]=doctor_b()
    rewards_10times[i]=doctor_c()
    
Box_plot=np.zeros((3,10))
Box_plot[0]=rewards_10times[:,A,doctors.shape[1]-1]
Box_plot[1]=rewards_10times[:,B,doctors.shape[1]-1]
Box_plot[2]=rewards_10times[:,C,doctors.shape[1]-1]
Box_plot=Box_plot.T
#************************ Visualization ************************
plt.figure()
plt.boxplot(Box_plot)
plt.title("Box Plot for last Trial after 10 Execution")
plt.xticks(range(1,4),["Doctor A","Doctor B","Doctor C"])
plt.ylabel('Rewards')
plt.xlabel('Strategies')
plt.grid()
plt.show()