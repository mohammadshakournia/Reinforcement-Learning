from cProfile import label
from cmath import nan
from turtle import color
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
print("\n"+"-"*55)
print("Doctor A:\n"+"-"*55)
WSLS_ref=0

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
    

# #************************ Doctor B ************************
print("\n"+"-"*55)
print("Doctor B:\n"+"-"*55)
for i in range(0,doctors.shape[1]):
    doctors[B][i]=choice(medicines)
    rewards[B][i]=get_reward(doctors[B][i],student_id)
    print("    {:3d}) Medicine: {}, Reward: {:6.3f} , State (Win/Lose) = None".format(i+1,doctors[B][i],rewards[B][i]))

#************************ Doctor C ************************
#Step 1
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

del best_medicine_D_C,max_reward_D_C,i,medicine_t,Rewards_sum

# #************************ Visualization ************************
Medicine1=np.zeros((3,100),dtype=float)
Medicine2=np.zeros((3,100),dtype=float)
for i in range(doctors.shape[0]):
    for j in range(doctors.shape[1]):
        if doctors[i,j]==2:
            Medicine2[i,j]=rewards[i,j]
        else:
            Medicine2[i,j]=nan
        if doctors[i,j]==1:
            Medicine1[i,j]=rewards[i,j]
        else:
            Medicine1[i,j]=nan

plt.figure()
plt.subplot(311)
plt.plot(np.arange(1,101,1),rewards[A][:],color="black",label="Doctor A",linewidth=1)
plt.scatter(np.arange(1,101,1),Medicine1[A][:],color="red",label="Medicine 1",linewidths=0.1)
plt.scatter(np.arange(1,101,1),Medicine2[A][:],color="blue",label="Medicine 2",linewidths=0.1)
plt.title("Rewards per Trial")
plt.legend(loc='lower right')
plt.ylabel('Rewards')
plt.xticks(np.arange(0,110,10))
plt.grid()

plt.subplot(312)
plt.plot(np.arange(1,101,1),rewards[B][:],color="cornflowerblue",label="Doctor B",linewidth=1)
plt.scatter(np.arange(1,101,1),Medicine1[B][:],color="navy",label="Medicine 1",linewidths=0.1)
plt.scatter(np.arange(1,101,1),Medicine2[B][:],color="darkorange",label="Medicine 2",linewidths=0.1)
plt.legend(loc='lower right')
plt.ylabel('Rewards')
plt.xticks(np.arange(0,110,10))
plt.grid()

plt.subplot(313)
plt.plot(np.arange(1,101,1),rewards[C][:],color="grey",label="Doctor C",linewidth=1)
plt.scatter(np.arange(1,101,1),Medicine1[C][:],color="orange",label="Medicine 1",linewidths=0.1)
plt.scatter(np.arange(1,101,1),Medicine2[C][:],color="green",label="Medicine 2",linewidths=0.1)
plt.legend(loc='lower right')
plt.xlabel('Trial')
plt.ylabel('Rewards')
plt.xticks(np.arange(0,110,10))
plt.grid()

plt.show()