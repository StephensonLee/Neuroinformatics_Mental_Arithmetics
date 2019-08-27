import pyedflib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv
#
# transfor part of data into csv
split = 2
length = 1000

# from porportion_f
# select = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1]
# from porportion_c
select = [1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1]
# from time domain
# select = [1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0]
# from std
# select = [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1]
# select = (np.ones(21,int))
print(select)

# print(tar)
for i in range(36):
    if i < 10:
        s1 = 'PHY/Subject0' + str(i) + '_1.edf'
        s2 = 'PHY/Subject0' + str(i) + '_2.edf'
    else:
        s1 = 'PHY/Subject' + str(i) + '_1.edf'
        s2 = 'PHY/Subject' + str(i) + '_2.edf'
    name1 = 'sam' + str(i + 1) + '.csv'
    name2 = 'sam' + str(i + 37) + '.csv'
    print(s1, s2,name1,name2)
    s=s2
    name=name1
    # for s,name in ([s1,name1],[s2,name2]):
    signum = int(np.sum(select))
    # print(signum)
    f = pyedflib.EdfReader(s)
    n = f.signals_in_file
    m = int(f.getNSamples()[0])
    signal_labels = f.getSignalLabels()
    start=int(m/20)*10
    # start=10000
    # length=m
    sigbufs = np.zeros((int(length / split), signum))

    col=0
    for j in range(n):
        if select[j]==1:
            y = []
            x = f.readSignal(j)
            sum=0
            for k in range(1,length+1):
                sum = sum + x[start + k - 1]
                if (k %split == 0):
                    y.append(sum / split)
                    sum=0
            min1=min(y)
            max1=max(y)
            # y = (y-min1)/(max1-min1)
            sigbufs[:, col] = y
            # print(y)
            col+=1
    pd.DataFrame(sigbufs).to_csv(name, index=False, header=None)

#write coordinates to EEG_channels_mapping
coordinates = pd.read_csv("Coordinates.csv",header=None)
coout = np.zeros((np.sum(select),3))
ord = 0
for i in range(np.size(coordinates, 0)):
    if select[i] == 1:
        coout[ord,:]=coordinates.iloc[i]
        ord+=1
pd.DataFrame(coout).to_csv("EEG_channels_mapping.csv",index=False,header=None)

#write lables
fopen = open("labels1.csv")
file1 = csv.reader(fopen)
labelout = []
fwrite = open("labels.txt", 'w')
for i, s in enumerate(file1):
    if select[i] == 1:
        labelout.append(s)
        fwrite = open("labels.txt", 'a')
        fwrite.write(s[0]+'\n')
        fwrite.close()

# #variance
# tar=pd.read_csv("tar.csv",header=None,index_col=False)
# samples=36
# signals=21
# tar=tar[0]
# num1=0
# num2=sum(tar-1)
# num1=samples-num2
# print(num1,num2)
# data_1=np.zeros((num1,signals))
# data_2=np.zeros((num2,signals))
# order1=0
# order2=0
# # for i,label in enumerate(tar):
# #     print(i,label)
# #     name = 'Mental/sam' + str(i+1) + '.csv'
# #     table = pd.read_csv(name, header=None, index_col=False)
# #     if label==1:
# #         for j in range(signals):
# #             data_1[order1,j]=np.std(table[j])
# #         order1+=1
# #     else:
# #         for j in range(signals):
# #             print(np.std(table[j]))
# #             data_2[order2, j] = np.std(table[j])
# #         order2 += 1
# # np.save("data_1.npy",data_1)
# # np.save("data_2.npy",data_2)
#
# data_1out=np.zeros((signals))
# data_2out=np.zeros((signals))
# data_1=np.load("data_1.npy")
# data_2=np.load("data_2.npy")
# for i in range(signals):
#     data_1out[i]=np.average(data_1[:,i])
#     data_2out[i]=np.average(data_2[:,i])
# # plt.plot(data_1out,label='Rest')
# # plt.plot(data_2out,label='Arithmetic')
# plt.plot(np.arange(1,22,1),data_1out-data_2out)
# plt.scatter(np.arange(1,22,1),data_1out-data_2out,label='Difference')
# plt.title('Variance')
# plt.legend()
# plt.show()


# # difference
# samples=36
# signals=21
# data_1=np.zeros((27000,signals))
# data_2=np.zeros((27000,signals))
# tar=pd.read_csv("tar.csv",header=None,index_col=False)
# tar=tar[0]
# for i, label in enumerate(tar):
#     name = 'Mental/sam' + str(i+1) + '.csv'
#     table = pd.read_csv(name, header=None, index_col=False)
#     temp = table[i]
#     if label ==1:
#         data_1[:,i]+=abs(temp[0:27000])
#     else:
#         data_2[:,i]+=abs(temp[0:27000])
# np.save("data_re1.npy",data_1)
# np.save("data_mt1.npy",data_2)
#
# data_re=np.load("data_re1.npy")
# data_mt=np.load("data_mt1.npy")
# split=500
# for i in range (signals):
#     data_reout = []
#     data_mtout = []
#     sum1 = 0
#     sum2 = 0
#     for j in range(1,30001):
#         sum1+=data_re[j-1,i]
#         sum2+=data_mt[j-1,i]
#         if j%split == 0:
#             data_reout.append(sum1/split)
#             data_mtout.append(sum2/split)
#             sum1=0
#             sum2=0
#
#     # print(data_reout)
#     plt.figure(i)
#     plt.title(str(i))
#     plt.plot(data_reout)
#     plt.plot(data_mtout)
#     plt.show()

# data_re=np.load("data_re1.npy")
# data_mt=np.load("data_mt1.npy")
# split=500
# for i in range (signals):
#     data_reout = []
#     data_mtout = []
#     sum1 = 0
#     sum2 = 0
#     for j in range(1,30001):
#         sum1+=data_re[j-1,i]
#         sum2+=data_mt[j-1,i]
#         if j%split == 0:
#             data_reout.append(sum1/split)
#             data_mtout.append(sum2/split)
#             sum1=0
#             sum2=0
#
#     # print(data_reout)
#     plt.figure(i)
#     plt.title(str(i))
#     plt.plot(data_reout)
#     plt.plot(data_mtout)
#     plt.show()

# # plot the variance between rest and mental signals
# samples=36
# signals=21
# # data_re=np.zeros((signals,samples))
# # data_mt=np.zeros((signals,samples))
# # for i in range(samples):
# #     name1= 'E:/AUT Study/Neuroinformatics/Assignment 2/Discard/rest full/sam' + str(i+1) + '.csv'
# #     name2= 'E:/AUT Study/Neuroinformatics/Assignment 2/Discard/mental full/sam' + str(i+37) + '.csv'
# #     rest=pd.read_csv(name1,header=None,index_col=False)
# #     mental=pd.read_csv(name2, header=None, index_col=False)
# #     for j in range (signals):
# #         data_re[j,i]=np.std(rest[j])
# #         data_mt[j,i]=np.std(mental[j])
# # np.save("data_re.npy",data_re)
# # np.save("data_mt.npy",data_mt)
#
# data_reout=np.zeros((signals))
# data_mtout=np.zeros((signals))
# data_re=np.load("data_re.npy")
# data_mt=np.load("data_mt.npy")
# for i in range(signals):
#     data_reout[i]=np.sum(data_re[i,:])
#     data_mtout[i]=np.sum(data_mt[i, :])
# # plt.plot(data_reout,label='Rest')
# # plt.plot(data_mtout,label='Arithmetic')
# plt.plot(data_mtout-data_reout,label='Difference')
# plt.title('Variance')
# plt.legend()
# plt.show()

# for i in range(signals):
#     plt.figure(i)
#     plt.title(str(i))
#     plt.plot(data_re[i,:])
#     plt.plot(data_mt[i,:])
#     plt.show()

# # plot the difference between rest and mental signals
# samples=36
# signals=21
# data_re=np.zeros((30000,signals))
# data_mt=np.zeros((30000,signals))
#
# # for i in range(1,samples+1):
# #     name1= 'E:/AUT Study/Neuroinformatics/Assignment 2/Discard/rest full/sam' + str(i) + '.csv'
# #     name2= 'E:/AUT Study/Neuroinformatics/Assignment 2/Discard/mental full/sam' + str(i+36) + '.csv'
# #     rest=pd.read_csv(name1,header=None,index_col=False)
# #     mental=pd.read_csv(name2, header=None, index_col=False)
# #     for j in range (signals):
# #         restemp=rest[j]
# #         mentemp=mental[j]
# #         data_re[:,j]+=abs(restemp[0:30000])
# #         data_mt[:,j] += abs(mentemp[0:30000])
# # np.save("data_re1.npy",data_re)
# # np.save("data_mt1.npy",data_mt)
#
# data_re=np.load("data_re1.npy")
# data_mt=np.load("data_mt1.npy")
# split=500
# for i in range (signals):
#     data_reout = []
#     data_mtout = []
#     sum1 = 0
#     sum2 = 0
#     for j in range(1,30001):
#         sum1+=data_re[j-1,i]
#         sum2+=data_mt[j-1,i]
#         if j%split == 0:
#             data_reout.append(sum1/split)
#             data_mtout.append(sum2/split)
#             sum1=0
#             sum2=0
#
#     # print(data_reout)
#     plt.figure(i)
#     plt.title(str(i))
#     plt.plot(data_reout)
#     plt.plot(data_mtout)
#     plt.show()

# print(f.ix[:,:])
# plt.subplot(5,6,order)
# plt.plot(f1.ix[14000:15000,0])
# plt.subplot(5,6,order)
# plt.plot(f2.ix[14000:15000, 0])
# split=1
# x2=[]
# sum1=np.zeros(len(f.ix[0, :]))
# sum1=0
# for i in range(1,len(f.ix[:, 0])):
#     if i%split == 0:
#         x2.append(sum1/split)
#         sum1=0
#     x1 = f.ix[i, :]
#     for j in f.ix[i, :]:
#         sum1=sum1+abs(j)
# print(x2)
# plt.plot(x2)
# plt.show()