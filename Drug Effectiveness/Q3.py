import numpy as np
from random import choice,choices
from BP_reward import get_reward
import matplotlib.pyplot as plt
from scipy.stats import t

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
n=5
rewards_5times=np.zeros((n,3,100))
for i in range(n):
    print("="*55+"\nStep %d\n"%(i+1)+"="*55)
    rewards_5times[i]=doctor_a()
    rewards_5times[i]=doctor_b()
    rewards_5times[i]=doctor_c()

alpha=0.05
mean_reward5=np.mean(rewards_5times,axis=0)

confidence_interval_A5 = np.abs(t.ppf(alpha/2,len(mean_reward5[A][:])-1)) * np.std(mean_reward5[A][:]) / np.sqrt(len(mean_reward5[A][:]))
confidence_interval_B5 = np.abs(t.ppf(alpha/2,len(mean_reward5[B][:])-1)) * np.std(mean_reward5[B][:]) / np.sqrt(len(mean_reward5[B][:]))
confidence_interval_C5 = np.abs(t.ppf(alpha/2,len(mean_reward5[C][:])-1)) * np.std(mean_reward5[C][:]) / np.sqrt(len(mean_reward5[C][:]))



n=20
rewards_20times=np.zeros((n,3,100))
for i in range(n):
    print("="*55+"\nStep %d\n"%(i+1)+"="*55)
    rewards_20times[i]=doctor_a()
    rewards_20times[i]=doctor_b()
    rewards_20times[i]=doctor_c()

alpha=0.05
mean_reward20=np.mean(rewards_20times,axis=0)
confidence_interval_A20 = np.abs(t.ppf(alpha/2,len(mean_reward20[A][:])-1)) * np.std(mean_reward20[A][:]) / np.sqrt(len(mean_reward20[A][:]))
confidence_interval_B20 = np.abs(t.ppf(alpha/2,len(mean_reward20[B][:])-1)) * np.std(mean_reward20[B][:]) / np.sqrt(len(mean_reward20[B][:]))
confidence_interval_C20 = np.abs(t.ppf(alpha/2,len(mean_reward20[C][:])-1)) * np.std(mean_reward20[C][:]) / np.sqrt(len(mean_reward20[C][:]))

del rewards_5times,rewards_20times
#************************ Visualization ************************
#******************************* 5 Times ***********************************
plt.figure()
plt.subplot(311)
plt.plot(np.arange(1,101,1),mean_reward5[A][:],color="black",label="Doctor A",linewidth=1)
plt.fill_between(np.arange(1,101,1), (mean_reward5[A][:]-confidence_interval_A5),
                 (mean_reward5[A][:]+confidence_interval_A5), color='r', alpha=0.2)
plt.legend(loc='lower right')
plt.ylabel('Rewards')
plt.xticks([1,10,20,30,40,50,60,70,80,90,100])
plt.title("Rewards in 5 Times Execution\n(Confidence interval with alpha = 0.05)")
plt.grid()

plt.subplot(312)
plt.plot(np.arange(1,101,1),mean_reward5[B][:],color="cornflowerblue",label="Doctor B",linewidth=1)
plt.fill_between(np.arange(1,101,1), (mean_reward5[B][:]-confidence_interval_B5),
                 (mean_reward5[B][:]+confidence_interval_B5), color='g', alpha=0.2)
plt.legend(loc='lower right')
plt.ylabel('Rewards')
plt.xticks([1,10,20,30,40,50,60,70,80,90,100])
plt.grid()

plt.subplot(313)
plt.plot(np.arange(1,101,1),mean_reward5[C][:],color="grey",label="Doctor C",linewidth=1)
plt.fill_between(np.arange(1,101,1), (mean_reward5[C][:]-confidence_interval_C5),
                 (mean_reward5[C][:]+confidence_interval_C5), color='b', alpha=0.2)
plt.legend(loc='lower right')
plt.xlabel('Trial')
plt.ylabel('Rewards')
plt.xticks([1,10,20,30,40,50,60,70,80,90,100])
plt.grid()
#******************************* 20 Times ***********************************
plt.figure()
plt.subplot(311)
plt.plot(np.arange(1,101,1),mean_reward20[A][:],color="black",label="Doctor A",linewidth=1)
plt.fill_between(np.arange(1,101,1), (mean_reward20[A][:]-confidence_interval_A20),
                 (mean_reward20[A][:]+confidence_interval_A20), color='r', alpha=0.2)
plt.legend(loc='lower right')
plt.ylabel('Rewards')
plt.xticks([1,10,20,30,40,50,60,70,80,90,100])
plt.title("Rewards in 20 Times Execution\n(Confidence interval with alpha = 0.05)")
plt.grid()

plt.subplot(312)
plt.plot(np.arange(1,101,1),mean_reward20[B][:],color="cornflowerblue",label="Doctor B",linewidth=1)
plt.fill_between(np.arange(1,101,1), (mean_reward20[B][:]-confidence_interval_B20),
                 (mean_reward20[B][:]+confidence_interval_B20), color='g', alpha=0.2)
plt.legend(loc='lower right')
plt.ylabel('Rewards')
plt.xticks([1,10,20,30,40,50,60,70,80,90,100])
plt.grid()

plt.subplot(313)
plt.plot(np.arange(1,101,1),mean_reward20[C][:],color="grey",label="Doctor C",linewidth=1)
plt.fill_between(np.arange(1,101,1), (mean_reward20[C][:]-confidence_interval_C20),
                 (mean_reward20[C][:]+confidence_interval_C20), color='b', alpha=0.2)
plt.legend(loc='lower right')
plt.xlabel('Trial')
plt.ylabel('Rewards')
plt.xticks([1,10,20,30,40,50,60,70,80,90,100])
plt.grid()

plt.show()