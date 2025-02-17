import sys
import random
import math
import heapq

# class for events
class event:
    eventType = ""
    time = 0
    length = 0

    def __init__(self, eventType, time , length = 0):
        self.eventType = eventType
        self.time = time
        self.length = length

    def __lt__(self, other):
        return self.time < other.time

    def __str__(self):
        return f'Event: {self.eventType} Time: {self.time} Length: {self.length}'

# generate a set of random values according to a Poisson distribution
def random_num_gen(rate):
    ln = math.log(1-random.uniform(0,1))
    return (-1/rate)*ln

def main():
    # QUESTION 1 (exponential random variable generator):
    exp_random_var = []

    rate = 75 # lambda -> average number of packets generated/arrived (packets/seconds)

    # generate 1000 exponential random variables w/ rate of 75
    for i in range(1000):
        exp_random_var.append(random_num_gen(rate))

    mean_val = sum(exp_random_var)/len(exp_random_var) # calculate the mean of the gernerated variables

    # calculate the variance of the generated variables
    expected_val = float(1/75)
    expected_var = float(1/(75**2))
    variance = 0
    for j in exp_random_var:
        variance += ((j-expected_val)**2)/1000

    print('Mean: ', mean_val)
    print('Expected value: ', expected_val)
    print('Variance: ', variance)
    print('Expected variance: ', expected_var)

    # QUESTION 2, 3 & 4 (M/M/1 Queue):
    L = 2000 # average packet length (2000bits)
    C = 1000000 # transmission/link rate (1Mbps)

    for i in range(0, 8):
        numArrivals = 0 # number of packet arrivals
        numDepartures = 0 # number of packets departure
        numObservers = 0 # number of observations
        idleCounter = 0 # idle counter
        totalPackets = 0 # number of packets in the queue (observer event)

        des = [] # Discrete Event Scheduler

        execTime = 1000 # experiment run time (T = 1000s)
        #execTime = 2000 # experiment run time (2T)
        #execTime = 3000 # experiment run time (3T)
        lambdaVal = (125 + i*50) # lambda -> average number of packets generated/arrived (packets/seconds)

        serviceTime = 0 # determines when we can start servicing an arrival event
        arrivalAccumulate = 0 # sum of inter-arrival times
        lastDeparture = 0 # timestamp of last departure

        # generate arrivals and departures
        while(arrivalAccumulate < execTime):
            arrivalTime = random_num_gen(lambdaVal) # generate a set of packet arrival times (parameter: lambda)
            packetLength = random_num_gen(1/L) # generate corresponding packet lengths (parameter: 1/L)

            serviceTime = max(lastDeparture, arrivalAccumulate + arrivalTime) # handles case if during departure event, another arrival event arrives
            arrivalAccumulate += arrivalTime

            departureTime = (serviceTime + packetLength/C) # calculate departure times

            des.append(event("Arrival", arrivalAccumulate, packetLength))
            des.append(event("Departure", departureTime))

            lastDeparture = departureTime

        serviceTime = 0

        # generate observers
        while(serviceTime < execTime):
            serviceTime += random_num_gen(5*lambdaVal) # generate a set of random observation times (parameter: 5*rate of arrival elements)
            des.append(event("Observer" , serviceTime))

        # sort the DES according to time
        des.sort()

        # process events & update counters
        for events in des:
            if(events.eventType == "Arrival"):
                numArrivals = (numArrivals + 1)
            elif(events.eventType == "Departure"):
                numDepartures = (numDepartures + 1)
            else:
                totalPackets = (totalPackets + (numArrivals - numDepartures)) # calculate number of packets in the queue
                idleCounter = (idleCounter + (numArrivals == numDepartures)) # count number of times queue is idle/empty
                numObservers = (numObservers + 1)

        # calculating parameters
        packetsExpected = (totalPackets/numObservers) # time-average number of packets in the queue (E[N])
        p_idle = (idleCounter/numObservers) # proportion of time the server is idle (P_idle)

        print('PIdle: ',  p_idle)
        print('ExpectedPackets: ', packetsExpected)

    # QUESTION 5 & 6 (M/M/1/K Queue):
    Kvals = [10, 25 ,50] # the size of the buffer in number of packets.

    for K in Kvals:
        for i in range(0, 9):
            numArrivals = 0 # number of packet arrivals
            numDepartures = 0 # number of packets departure
            numObservers = 0 # number of observations

            totalPackets = 0 # number of packets in the queue (observer event)
            totalPacketsGenerated = 0 # number of packets generated
            lostPackets = 0 # number of packets lost

            des = [] # Discrete Event Scheduler

            execTime = 1000 # experiment run time (T = 1000s)
            # execTime = 2000 # experiment run time (2T)
            # execTime = 3000 # experiment run time (3T)
            lambdaVal = (300 + i*50) # lambda -> average number of packets generated/arrived (packets/seconds)

            serviceStart = 0  # determines when we can start servicing an arrival event
            arrivalAccumulate = 0 # sum of inter-arrival times
            lastDeparture = 0  # timestamp of last departure

            # generate arrivals
            while(arrivalAccumulate < execTime):
                arrivalTime = random_num_gen(lambdaVal) # generate a set of packet arrival times (parameter: lambda)
                packetLength = random_num_gen(1/L) # generate corresponding packet lengths (parameter: 1/L)

                arrivalAccumulate += arrivalTime
                totalPacketsGenerated += 1

                des.append(event("Arrival", arrivalAccumulate, packetLength))

            arrivalAccumulate = 0

            # generate observers
            while(arrivalAccumulate < execTime):
                arrivalAccumulate += random_num_gen(5*lambdaVal) # generate a set of random observation times (parameter: 5*rate of arrival elements)
                des.append(event("Observer" , arrivalAccumulate))

            des.sort() #sort the DES

            departures = []
            heapq.heapify(departures) # store departure events in a heap

            for events in des:
                # while current time is greater then smallest departure time in heap, pop from the heap
                while(len(departures) > 0 and events.time >= departures[0]):
                    heapq.heappop(departures)
                    numDepartures += 1

                if(events.eventType == "Arrival"):
                    # if we have room in the heap, we can add the departure of the current event
                    if(len(departures) < K):
                        serviceStart = max(lastDeparture, events.time) # max determines when we can start servicing
                        departureTime = (serviceStart + events.length/C) # calculate departure times

                        heapq.heappush(departures, departureTime) # populate the heap

                        lastDeparture = departureTime
                        numArrivals += 1
                    # if no room, mark lost packet
                    else:
                        lostPackets += 1
                else:
                    totalPackets += numArrivals - numDepartures # calculate number of packets in the queue
                    numObservers += 1

            # calculating parameters
            packetsExpected = (totalPackets/numObservers) # time-average number of packets in the queue (E[N])
            p_loss = (lostPackets/totalPacketsGenerated) # proportion of lost packets (P_loss)

            print('P_loss: '  + str(p_loss), "| K = ", K, "| P = ", lambdaVal/500)
            print('ExpectedPackets: ', packetsExpected, "| K = ", K, "| P = ", lambdaVal/500)

if __name__ == "__main__":
    main()
