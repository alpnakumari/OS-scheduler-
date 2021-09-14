# whenever a task is scheduled a process is created and it knows which job is running and
# it will be used when we have to free the cpu and memory when the job is over
class Process:
    def __init__(self, jobId, node, cpu_taken, memory_taken, endTime):
        self.jobId = jobId
        self.node = node
        self.cpu_taken = cpu_taken
        self.memory_taken = memory_taken
        self.endTime = endTime

    def getJobId(self):
        return self.jobId

    def getNode(self):
        return self.node

    def getCpuTaken(self):
        return self.cpu_taken

    def getMemTaken(self):
        return self.memory_taken

    def getEndTime(self):
        return self.endTime