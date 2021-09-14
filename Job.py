# This class simulate the work of a Job.
# It contains all the data related to a job

class Job:

    def __init__(self, id, arrivalDay, hourTime, memReq, cpuReq, exeTime):
        self.id = id
        self.arrivalDay = arrivalDay
        self.hourTime = hourTime
        self.memReq = memReq
        self.cpuReq = cpuReq
        self.exeTime = exeTime

    def getArrivalDay(self):
        return self.arrivalDay

    def getId(self):
        return self.id

    def getHourTime(self):
        return self.hourTime

    def getMemReq(self):
        return self.memReq

    def getCpuReq(self):
        return self.cpuReq

    def getExeTime(self):
        return self.exeTime
