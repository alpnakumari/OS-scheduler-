from Job import Job
from Process import Process
import matplotlib.pyplot as plt

#plot graph-----------------------------------------------------------------------
def plotGraphs():
    list1 = ['FCFS', 'Shortest job', 'Shortest job duration']
    list2 = ['First Fit + ', 'Worst Fit + ', 'Best Fit + ']
    a = 0
    for i in range(3):
        for j in range(3):
            plt.figure(a + 1)
            plt.plot(monthlyAvgMem[a], 'b', label='memory')
            plt.plot(monthlyAvgCpu[a], 'orange', label='cpu')
            plt.xlabel("days")
            plt.ylabel("memory and cpu % utilization")
            plt.title(list2[i] + list1[j])
            plt.grid()
            a += 1
    plt.legend()
    plt.show()


# alocating the mem and cpu using first fit------------------------------------
def nodeAllocatedFirstFit(currJob):
    cpuReq = int(currJob.getCpuReq())
    memReq = int(currJob.getMemReq())
    exeTime = int(currJob.getExeTime())
    for i1 in range(128):
        if cores[i1] >= cpuReq:
                # found the core now check for the cores memory
            if  memory[i1] >= memReq:
                # core and memory both found at i1 node
                # allocate the memory and core by subtracting it from total
                cores[i1] = cores[i1] - cpuReq
                memory[i1] = memory[i1] - memReq
                end_time = (exeTime + currentTime)%24
                if end_time == 0:
                    end_time = 24
                # create process(put the required info) and put it in runningProcessList
                p = Process(currJob.getId(),i1,cpuReq,memReq,end_time)
                runningProcessList.append(p)
                return True
    else:
        return

# alocating the mem and cpu using worst fit-------------------------------
def nodeAllocatedWorstFit(currJob):
    cpuReq = int(currJob.getCpuReq())
    memReq = int(currJob.getMemReq())
    exeTime = int(currJob.getExeTime())
	
    # used to select those memories which are worst fit but core not avalaible so we again search for worst fit ignoring the values
    remMax = []
    while(True):
        l = list(set(memory) - set(remMax))
        if len(l) == 0:
            return False
        worstFit = max(l)
        if (worstFit > memReq):
            index = memory.index(worstFit)
            # check if core available
            if cores[index] > cpuReq:
                # corefound
                cores[index] = cores[index] - cpuReq
                memory[index] = memory[index] - memReq
                end_time = (exeTime + currentTime) % 24
                if end_time == 0:
                    end_time = 24
                # create process(put the required info) and put it in runningProcessList
                p = Process(currJob.getId(), index, cpuReq, memReq, end_time)
                runningProcessList.append(p)
                return True
            else:
                remMax.append(worstFit)
        else:
            return False

# alocating the mem and cpu using best fit----------------------------------------------
def nodeAllocatedBestFit(currJob):
    cpuReq = int(currJob.getCpuReq())
    memReq = int(currJob.getMemReq())
    exeTime = int(currJob.getExeTime())
    # used to select those memories which are best fit but core not avalaible or lower than mem required
   
    remMax = []
    while(True):
        l = list(set(memory) - set(remMax))
        if len(l) == 0:
            return False
        bestFit = min(l)
        if (bestFit >= memReq):
            index = memory.index(bestFit)
            # check if core available
            if cores[index] > cpuReq:
                # corefound
                cores[index] = cores[index] - cpuReq
                memory[index] = memory[index] - memReq
                end_time = (exeTime + currentTime) % 24
                if end_time == 0:
                    end_time = 24
                # create process(put the required info) and put it in runningProcessList
                p = Process(currJob.getId(), index, cpuReq, memReq, end_time)
                runningProcessList.append(p)
                return True
            else:
                remMax.append(bestFit)
        else:
            remMax.append(bestFit)

#open the given file
f = open("JobArrival.txt", "r")
jobList = []
for x in f:
    x = x.split()
    job = Job(x[1],x[4],x[7],x[9],x[11],x[13])
    jobList.append(job)
# we have populated all the jobs in list - jobList


#----------------------------------------------------------------------------------


# variables required
currentTime = 0
currentJobId = 0
currentDay = 0
Q = [jobList[currentJobId]]
currentJobId = currentJobId + 1
runningProcessList = []
cores = [24 for _ in range(128)]
memory =  [64 for _ in range(128)]
totalMemDay = 0
totalCpuDay = 0
monthlyAvgMem = [[] for _ in range(9)]
monthlyAvgCpu = [[] for _ in range(9)]

# code for first come first serve with First Fit
while len(Q)!=0 or len(runningProcessList)!=0:
    while (currentJobId < len(jobList) and jobList[currentJobId].getArrivalDay() == str(currentDay)) \
            or len(Q)!=0 or len(runningProcessList)!=0:
        # filling the queue for present time using FCFS
        while currentJobId < len(jobList) and jobList[currentJobId].getHourTime() == str(currentTime):
            Q.append(jobList[currentJobId])
            currentJobId = currentJobId + 1
        # allocate jobs, if the job is allocated remove it from the que
        if len(Q) != 0:
            currJob = Q[0]
            # finding the core and memory to allocate
            while (nodeAllocatedFirstFit(currJob)):
                Q.pop(0)
                if len(Q) > 0:
                    currJob = Q[0]
                else:
                    break
        # all memory and cpu which can be allocated are completed
        # calculaion is done by getting the used memory and cpu
        totalCpuDay = totalCpuDay + 128*24 - sum(cores)
        totalMemDay = totalMemDay + 128*64 - sum(memory)
        currentTime = currentTime + 1
        # free jobs which got completed after the current time is increased
        # destroy the process by removing it from the runningProcessList
        newRPL = runningProcessList.copy()
        if len(runningProcessList) != 0:
            for p1 in runningProcessList:
                if (p1.getEndTime() == currentTime):
                    # freeing resources
                    cores[p1.getNode()] = cores[p1.getNode()] + p1.getCpuTaken()
                    memory[p1.getNode()] = memory[p1.getNode()] + p1.getMemTaken()
                    newRPL.remove(p1)
        runningProcessList = newRPL
        #if present time goes to 24
        # reset time, increase day, reset variables after adding them in a list appropriately
        if currentTime == 24:
            # we counted cpu and mem 24 times so to get the average we divide by 24
            totalCpuDay = totalCpuDay/24
            totalMemDay = totalMemDay/24
            currentTime = 0
            currentDay = currentDay + 1
            monthlyAvgCpu[0].append(round((totalCpuDay/(128*24))*100,2))
            monthlyAvgMem[0].append(round((totalMemDay/(128*64))*100,2))
            totalMemDay,totalCpuDay = 0,0

			
#-----------------------------------------------

# variables required
currentTime,currentJobId,currentDay = 0,0,0
Q = [jobList[currentJobId]]
currentJobId = currentJobId + 1
runningProcessList = []
cores = [24 for _ in range(128)]
memory =  [64 for _ in range(128)]
totalMemDay = 0
totalCpuDay = 0

# code for shortest job first serve with First Fit
while len(Q)!=0 or len(runningProcessList)!=0:
    while (currentJobId < len(jobList) and jobList[currentJobId].getArrivalDay() == str(currentDay)) \
            or len(Q)!=0 or len(runningProcessList)!=0:
        # filling the queue for present time using shortest job first
        while currentJobId < len(jobList) and jobList[currentJobId].getHourTime() == str(currentTime):
            newJob = jobList[currentJobId]
            for index in range(len(Q)):
                if int(newJob.getExeTime()) * int(newJob.getCpuReq()) * int(newJob.getMemReq()) < \
                        int(Q[index].getExeTime()) + int(Q[index].getCpuReq()) + int(Q[index].getMemReq()):
                    Q.insert(index, newJob)
                    break
            else:
                Q.append(newJob)
            currentJobId = currentJobId + 1
        # allocate jobs, if the job is allocated remove it from the que
        if len(Q) != 0:
            currJob = Q[0]
            # finding the core and memory to allocate
            while (nodeAllocatedFirstFit(currJob)):
                Q.pop(0)
                if len(Q) > 0:
                    currJob = Q[0]
                else:
                    break
        # all memory and cpu which can be allocated are completed
        # calculaion is done by getting the used memory and cpu
        totalCpuDay = totalCpuDay + 128*24 - sum(cores)
        totalMemDay = totalMemDay + 128*64 - sum(memory)
        currentTime = currentTime + 1

        # free jobs which got completed after the current time is increased
        # destroy the process by removing it from the runningProcessList
        newRPL = runningProcessList.copy()
        if len(runningProcessList) != 0:
            for p1 in runningProcessList:
                if (p1.getEndTime() == currentTime):
                    # freeing resources
                    cores[p1.getNode()] = cores[p1.getNode()] + p1.getCpuTaken()
                    memory[p1.getNode()] = memory[p1.getNode()] + p1.getMemTaken()
                    newRPL.remove(p1)
        runningProcessList = newRPL
		
        #if present time goes to 24
        # reset time, increase day, reset variables after adding them in a list appropriately
        if currentTime == 24:
            # we counted cpu and mem 24 times so to get the average we divide by 24
            totalCpuDay = totalCpuDay/24
            totalMemDay = totalMemDay/24
            currentTime = 0
            currentDay = currentDay + 1
            monthlyAvgCpu[1].append(round((totalCpuDay/(128*24))*100,2))
            monthlyAvgMem[1].append(round((totalMemDay/(128*64))*100,2))
            totalMemDay,totalCpuDay = 0,0


#------------------------------------------------------------------------


# variables required
currentTime,currentJobId,currentDay = 0,0,0
Q = [jobList[currentJobId]]
currentJobId = currentJobId + 1
runningProcessList = []
cores = [24 for _ in range(128)]
memory =  [64 for _ in range(128)]
totalMemDay = 0
totalCpuDay = 0

# code for shortest job duration serve with First Fit
while len(Q)!=0 or len(runningProcessList)!=0:
    while (currentJobId < len(jobList) and jobList[currentJobId].getArrivalDay() == str(currentDay)) \
            or len(Q)!=0 or len(runningProcessList)!=0:
        # filling the queue for present time using shortest job duration
        while currentJobId < len(jobList) and jobList[currentJobId].getHourTime() == str(currentTime):
            newJob = jobList[currentJobId]
            for index in range(len(Q)):
                if int(newJob.getExeTime()) < int(Q[index].getExeTime()):
                    Q.insert(index, newJob)
                    break
            else:
                Q.append(newJob)
            currentJobId = currentJobId + 1

        # allocate jobs, if the job is allocated remove it from the que
        if len(Q) != 0:
            currJob = Q[0]
            # finding the core and memory to allocate
            while (nodeAllocatedFirstFit(currJob)):
                Q.pop(0)
                if len(Q) > 0:
                    currJob = Q[0]
                else:
                    break
        # all memory and cpu which can be allocated are completed
        # calculaion is done by getting the used memory and cpu
        totalCpuDay = totalCpuDay + 128*24 - sum(cores)
        totalMemDay = totalMemDay + 128*64 - sum(memory)
        currentTime = currentTime + 1
        # free jobs which got completed after the current time is increased
        # destroy the process by removing it from the runningProcessList
        newRPL = runningProcessList.copy()
        if len(runningProcessList) != 0:
            for p1 in runningProcessList:
                if (p1.getEndTime() == currentTime):
                    # freeing resources
                    cores[p1.getNode()] = cores[p1.getNode()] + p1.getCpuTaken()
                    memory[p1.getNode()] = memory[p1.getNode()] + p1.getMemTaken()
                    newRPL.remove(p1)

        runningProcessList = newRPL
        #if present time goes to 24
        # reset time, increase day, reset variables after adding them in a list appropriately
        if currentTime == 24:
            # we counted cpu and mem 24 times so to get the average we divide by 24
            totalCpuDay = totalCpuDay/24
            totalMemDay = totalMemDay/24
            currentTime = 0
            currentDay = currentDay + 1
            monthlyAvgCpu[2].append(round((totalCpuDay/(128*24))*100,2))
            monthlyAvgMem[2].append(round((totalMemDay/(128*64))*100,2))
            totalMemDay,totalCpuDay = 0,0


#------------------

# variables required
currentTime = 0
currentJobId = 0
currentDay = 0
Q = [jobList[currentJobId]]
currentJobId = currentJobId + 1
runningProcessList = []
cores = [24 for _ in range(128)]
memory =  [64 for _ in range(128)]
totalMemDay = 0
totalCpuDay = 0
# code for first come first serve with worst fit
while len(Q)!=0 or len(runningProcessList)!=0:
    while (currentJobId < len(jobList) and jobList[currentJobId].getArrivalDay() == str(currentDay)) \
            or len(Q)!=0 or len(runningProcessList)!=0:
        # filling the queue for present time using FCFS
        while currentJobId < len(jobList) and jobList[currentJobId].getHourTime() == str(currentTime):
            Q.append(jobList[currentJobId])
            currentJobId = currentJobId + 1
        # allocate jobs, if the job is allocated remove it from the que
        if len(Q) != 0:
            currJob = Q[0]
            # finding the core and memory to allocate
            while (nodeAllocatedWorstFit(currJob)):
                Q.pop(0)
                if len(Q) > 0:
                    currJob = Q[0]
                else:
                    break
					
        # all memory and cpu which can be allocated are completed
        totalCpuDay = totalCpuDay + 128*24 - sum(cores)
        totalMemDay = totalMemDay + 128*64 - sum(memory)

        # increase the current time
        currentTime = currentTime + 1
        # free jobs which got completed after the current time is increased
        # destroy the process by removing it from the runningProcessList
        newRPL = runningProcessList.copy()
        if len(runningProcessList) != 0:
            for p1 in runningProcessList:
                if (p1.getEndTime() == currentTime):
                    # freeing resources
                    cores[p1.getNode()] = cores[p1.getNode()] + p1.getCpuTaken()
                    memory[p1.getNode()] = memory[p1.getNode()] + p1.getMemTaken()
                    newRPL.remove(p1)

        runningProcessList = newRPL
        #if present time goes to 24
        # reset time, increase day, reset variables after adding them in a list appropriately
        if currentTime == 24:
            # we counted cpu and mem 24 times so to get the average we divide by 24
            totalCpuDay = totalCpuDay/24
            totalMemDay = totalMemDay/24
            currentTime = 0
            currentDay = currentDay + 1
            monthlyAvgCpu[3].append(round((totalCpuDay/(128*24))*100,2))
            monthlyAvgMem[3].append(round((totalMemDay/(128*64))*100,2))
            totalMemDay,totalCpuDay = 0,0


#--------------------------------------------------------------

# variables required
currentTime,currentJobId,currentDay = 0,0,0
Q = [jobList[currentJobId]]
currentJobId = currentJobId + 1
runningProcessList = []
cores = [24 for _ in range(128)]
memory =  [64 for _ in range(128)]
totalMemDay = 0
totalCpuDay = 0

# code for shortest job first serve with worst fit
while len(Q)!=0 or len(runningProcessList)!=0:
    while (currentJobId < len(jobList) and jobList[currentJobId].getArrivalDay() == str(currentDay)) \
            or len(Q)!=0 or len(runningProcessList)!=0:
        # filling the queue for present time using shortest job first
        while currentJobId < len(jobList) and jobList[currentJobId].getHourTime() == str(currentTime):
            newJob = jobList[currentJobId]
            for index in range(len(Q)):
                if int(newJob.getExeTime()) * int(newJob.getCpuReq()) * int(newJob.getMemReq()) < \
                        int(Q[index].getExeTime()) + int(Q[index].getCpuReq()) + int(Q[index].getMemReq()):
                    Q.insert(index, newJob)
                    break
            else:
                Q.append(newJob)
            currentJobId = currentJobId + 1
        # allocate jobs, if the job is allocated remove it from the que
        if len(Q) != 0:
            currJob = Q[0]

            # finding the core and memory to allocate
            while (nodeAllocatedWorstFit(currJob)):
                Q.pop(0)
                if len(Q) > 0:
                    currJob = Q[0]
                else:
                    break

        # all memory and cpu which can be allocated are completed
        # calculaion is done by getting the used memory and cpu
        totalCpuDay = totalCpuDay + 128*24 - sum(cores)
        totalMemDay = totalMemDay + 128*64 - sum(memory)
		
        # increase the current time
        currentTime = currentTime + 1
        # free jobs which got completed after the current time is increased
        # destroy the process by removing it from the runningProcessList
        newRPL = runningProcessList.copy()
        if len(runningProcessList) != 0:
            for p1 in runningProcessList:
                if (p1.getEndTime() == currentTime):
                    # freeing resources
                    cores[p1.getNode()] = cores[p1.getNode()] + p1.getCpuTaken()
                    memory[p1.getNode()] = memory[p1.getNode()] + p1.getMemTaken()
                    newRPL.remove(p1)

        runningProcessList = newRPL
        #if present time goes to 24
        # reset time, increase day, reset variables after adding them in a list appropriately
        if currentTime == 24:
            # we counted cpu and mem 24 times so to get the average we divide by 24
            totalCpuDay = totalCpuDay/24
            totalMemDay = totalMemDay/24
            currentTime = 0
            currentDay = currentDay + 1
            monthlyAvgCpu[4].append(round((totalCpuDay/(128*24))*100,2))
            monthlyAvgMem[4].append(round((totalMemDay/(128*64))*100,2))
            totalMemDay,totalCpuDay = 0,0

#------------------------------------------------------------------------

# variables required
currentTime,currentJobId,currentDay = 0,0,0
Q = [jobList[currentJobId]]
currentJobId = currentJobId + 1
runningProcessList = []
cores = [24 for _ in range(128)]
memory =  [64 for _ in range(128)]
totalMemDay = 0
totalCpuDay = 0

# code for shortest job duration serve with worst fit
while len(Q)!=0 or len(runningProcessList)!=0:
    while (currentJobId < len(jobList) and jobList[currentJobId].getArrivalDay() == str(currentDay)) \
            or len(Q)!=0 or len(runningProcessList)!=0:

        # filling the queue for present time using shortest job duration
        while currentJobId < len(jobList) and jobList[currentJobId].getHourTime() == str(currentTime):
            newJob = jobList[currentJobId]
            for index in range(len(Q)):
                if int(newJob.getExeTime()) < int(Q[index].getExeTime()):
                    Q.insert(index, newJob)
                    break
            else:
                Q.append(newJob)
            currentJobId = currentJobId + 1

        # allocate jobs, if the job is allocated remove it from the que
        if len(Q) != 0:
            currJob = Q[0]
            # finding the core and memory to allocate
            while (nodeAllocatedWorstFit(currJob)):
                Q.pop(0)
                if len(Q) > 0:
                    currJob = Q[0]
                else:
                    break
					
        # all memory and cpu which can be allocated are completed
        # calculaion is done by getting the used memory and cpu
        totalCpuDay = totalCpuDay + 128*24 - sum(cores)
        totalMemDay = totalMemDay + 128*64 - sum(memory)
        currentTime = currentTime + 1
		
        # free jobs which got completed after the current time is increased
        # destroy the process by removing it from the runningProcessList
        newRPL = runningProcessList.copy()
        if len(runningProcessList) != 0:
            for p1 in runningProcessList:
                if (p1.getEndTime() == currentTime):
                    # freeing resources
                    cores[p1.getNode()] = cores[p1.getNode()] + p1.getCpuTaken()
                    memory[p1.getNode()] = memory[p1.getNode()] + p1.getMemTaken()
                    newRPL.remove(p1)
        runningProcessList = newRPL
        #if present time goes to 24
        # reset time, increase day, reset variables after adding them in a list appropriately
        if currentTime == 24:
            # we counted cpu and mem 24 times so to get the average we divide by 24
            totalCpuDay = totalCpuDay/24
            totalMemDay = totalMemDay/24
            currentTime = 0
            currentDay = currentDay + 1
            monthlyAvgCpu[5].append(round((totalCpuDay/(128*24))*100,2))
            monthlyAvgMem[5].append(round((totalMemDay/(128*64))*100,2))
            totalMemDay,totalCpuDay = 0,0

			
#------------------------------------------------------------------


# variables required
currentTime = 0
currentJobId = 0
currentDay = 0
Q = [jobList[currentJobId]]
currentJobId = currentJobId + 1
runningProcessList = []
cores = [24 for _ in range(128)]
memory =  [64 for _ in range(128)]
totalMemDay = 0
totalCpuDay = 0

# code for first come first serve with  Best Fit
while len(Q)!=0 or len(runningProcessList)!=0:
    while (currentJobId < len(jobList) and jobList[currentJobId].getArrivalDay() == str(currentDay)) \
            or len(Q)!=0 or len(runningProcessList)!=0:
        # filling the queue for present time using FCFS
        while currentJobId < len(jobList) and jobList[currentJobId].getHourTime() == str(currentTime):
            Q.append(jobList[currentJobId])
            currentJobId = currentJobId + 1
        # allocate jobs, if the job is allocated remove it from the que
        if len(Q) != 0:
            currJob = Q[0]
            # finding the core and memory to allocate
            while (nodeAllocatedBestFit(currJob)):
                Q.pop(0)
                if len(Q) > 0:
                    currJob = Q[0]
                else:
                    break
        # all memory and cpu which can be allocated are completed
        # calculaion is done by getting the used memory and cpu
        totalCpuDay = totalCpuDay + 128*24 - sum(cores)
        totalMemDay = totalMemDay + 128*64 - sum(memory)
        currentTime = currentTime + 1
        # free jobs which got completed after the current time is increased
        # destroy the process by removing it from the runningProcessList
        newRPL = runningProcessList.copy()
        if len(runningProcessList) != 0:
            for p1 in runningProcessList:
                if (p1.getEndTime() == currentTime):
                    # freeing resources
                    cores[p1.getNode()] = cores[p1.getNode()] + p1.getCpuTaken()
                    memory[p1.getNode()] = memory[p1.getNode()] + p1.getMemTaken()
                    newRPL.remove(p1)

        runningProcessList = newRPL

        #if present time goes to 24
        # reset time, increase day, reset variables after adding them in a list appropriately
        if currentTime == 24:
            # we counted cpu and mem 24 times so to get the average we divide by 24
            totalCpuDay = totalCpuDay/24
            totalMemDay = totalMemDay/24
            currentTime = 0
            currentDay = currentDay + 1
            monthlyAvgCpu[6].append(round((totalCpuDay/(128*24))*100,2))
            monthlyAvgMem[6].append(round((totalMemDay/(128*64))*100,2))
            totalMemDay,totalCpuDay = 0,0


#--------------------------------------------------------------

# variables required
currentTime,currentJobId,currentDay = 0,0,0
Q = [jobList[currentJobId]]
currentJobId = currentJobId + 1
runningProcessList = []
cores = [24 for _ in range(128)]
memory =  [64 for _ in range(128)]
totalMemDay = 0
totalCpuDay = 0

# code for shortest job first serve with  Best Fit
while len(Q)!=0 or len(runningProcessList)!=0:
    while (currentJobId < len(jobList) and jobList[currentJobId].getArrivalDay() == str(currentDay)) \
            or len(Q)!=0 or len(runningProcessList)!=0:
        # filling the queue for present time using shortest job first
        while currentJobId < len(jobList) and jobList[currentJobId].getHourTime() == str(currentTime):
            newJob = jobList[currentJobId]
            for index in range(len(Q)):
                if int(newJob.getExeTime()) * int(newJob.getCpuReq()) * int(newJob.getMemReq()) < \
                        int(Q[index].getExeTime()) + int(Q[index].getCpuReq()) + int(Q[index].getMemReq()):
                    Q.insert(index, newJob)
                    break
            else:
                Q.append(newJob)
            currentJobId = currentJobId + 1
        # allocate jobs, if the job is allocated remove it from the que
        if len(Q) != 0:
            currJob = Q[0]
            # finding the core and memory to allocate
            while (nodeAllocatedBestFit(currJob)):
                Q.pop(0)
                if len(Q) > 0:
                    currJob = Q[0]
                else:
                    break

        # all memory and cpu which can be allocated are completed
        # calculaion is done by getting the used memory and cpu
        totalCpuDay = totalCpuDay + 128*24 - sum(cores)
        totalMemDay = totalMemDay + 128*64 - sum(memory)
        currentTime = currentTime + 1

        # free jobs which got completed after the current time is increased
        # destroy the process by removing it from the runningProcessList
        newRPL = runningProcessList.copy()
        if len(runningProcessList) != 0:
            for p1 in runningProcessList:
                if (p1.getEndTime() == currentTime):
                    # freeing resources
                    cores[p1.getNode()] = cores[p1.getNode()] + p1.getCpuTaken()
                    memory[p1.getNode()] = memory[p1.getNode()] + p1.getMemTaken()
                    newRPL.remove(p1)

        runningProcessList = newRPL
        #if present time goes to 24
        # reset time, increase day, reset variables after adding them in a list appropriately
        if currentTime == 24:
            # we counted cpu and mem 24 times so to get the average we divide by 24
            totalCpuDay = totalCpuDay/24
            totalMemDay = totalMemDay/24
            currentTime = 0
            currentDay = currentDay + 1
            monthlyAvgCpu[7].append(round((totalCpuDay/(128*24))*100,2))
            monthlyAvgMem[7].append(round((totalMemDay/(128*64))*100,2))
            totalMemDay,totalCpuDay = 0,0

#------------------------------------------------------------------------

# variables required
currentTime,currentJobId,currentDay = 0,0,0
Q = [jobList[currentJobId]]
currentJobId = currentJobId + 1
runningProcessList = []
cores = [24 for _ in range(128)]
memory =  [64 for _ in range(128)]
totalMemDay = 0
totalCpuDay = 0

# code for shortest job duration serve with Best Fit
while len(Q)!=0 or len(runningProcessList)!=0:
    while (currentJobId < len(jobList) and jobList[currentJobId].getArrivalDay() == str(currentDay)) \
            or len(Q)!=0 or len(runningProcessList)!=0:
        # filling the queue for present time using shortest job duration
        while currentJobId < len(jobList) and jobList[currentJobId].getHourTime() == str(currentTime):
            newJob = jobList[currentJobId]
            for index in range(len(Q)):
                if int(newJob.getExeTime()) < int(Q[index].getExeTime()):
                    Q.insert(index, newJob)
                    break
            else:
                Q.append(newJob)
            currentJobId = currentJobId + 1
        # allocate jobs, if the job is allocated remove it from the que
        if len(Q) != 0:
            currJob = Q[0]
            # finding the core and memory to allocate
            while (nodeAllocatedBestFit(currJob)):
                Q.pop(0)
                if len(Q) > 0:
                    currJob = Q[0]
                else:
                    break

        # all memory and cpu which can be allocated are completed
        # calculaion is done by getting the used memory and cpu
        totalCpuDay = totalCpuDay + 128*24 - sum(cores)
        totalMemDay = totalMemDay + 128*64 - sum(memory)
        currentTime = currentTime + 1
		
        # free jobs which got completed after the current time is increased
        # destroy the process by removing it from the runningProcessList
        newRPL = runningProcessList.copy()
        if len(runningProcessList) != 0:
            for p1 in runningProcessList:
                if (p1.getEndTime() == currentTime):
                    # freeing resources
                    cores[p1.getNode()] = cores[p1.getNode()] + p1.getCpuTaken()
                    memory[p1.getNode()] = memory[p1.getNode()] + p1.getMemTaken()
                    newRPL.remove(p1)

        runningProcessList = newRPL
        #if present time goes to 24
        # reset time, increase day, reset variables after adding them in a list appropriately
        if currentTime == 24:
            # we counted cpu and mem 24 times so to get the average we divide by 24
            totalCpuDay = totalCpuDay/24
            totalMemDay = totalMemDay/24
            currentTime = 0
            currentDay = currentDay + 1
            monthlyAvgCpu[8].append(round((totalCpuDay/(128*24))*100,2))
            monthlyAvgMem[8].append(round((totalMemDay/(128*64))*100,2))
            totalMemDay,totalCpuDay = 0,0


print("plot the graphs")
plotGraphs()

