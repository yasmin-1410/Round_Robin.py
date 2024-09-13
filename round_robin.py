import tkinter as tk
from tkinter import ttk
from queue import Queue
from operator import itemgetter
import matplotlib.pyplot as plt
fig, gnt = plt.subplots()


def roundRobin():
    maxSize = int(entry_Number.get())
    quantum = int(entry_quantam.get())

    newQueue = Queue(maxSize)
    readyQueue = Queue(maxSize)
    terminatedQueue = Queue(maxSize)

    arrival_times = [int(entry.get()) for entry in arrival_entries]
    burst_times = [int(entry.get()) for entry in burst_entries]

    total_burst = sum(burst_times)

    for i in range(maxSize):
        process = [i , arrival_times[i], burst_times[i], burst_times[i], 0, 0, 0, 0]
        newQueue.put(process)

    time = 0
    timeFirstProcess = newQueue.queue[0][1]
    count = 0
    running = False
    runningProcess = []

    # Gantt Chart
        
    # Setting Y-axis limits
    gnt.set_ylim(0, 10 * maxSize)

    # Setting X-axis limits
    gnt.set_xlim(0, total_burst + timeFirstProcess)

    # Setting labels for x-axis and y-axis
    gnt.set_xlabel('Running')
    gnt.set_ylabel('Processor')
    list =[]
    list2 =[]
    list3 =[]
    i = 0
    while i < total_burst + timeFirstProcess :
        list.append(i)
        i += quantum

    i = 1
    while i <= maxSize :
        list2.append("P"+str(i))
        i += 1

    i = 0
    count = 10
    while i < maxSize :
        list3.append(count)
        i += 1
        count += 10


    # Setting ticks on y-axis
    gnt.set_yticks(list3)
    gnt.set_xticks(list)
    # Labelling tickes of y-axis
    gnt.set_yticklabels(list2)

    # Setting graph attribute
    gnt.grid(True)


    result_output = []

    while len(newQueue.queue) > 0 or len(readyQueue.queue) > 0 or time <= (total_burst + timeFirstProcess):

        while len(newQueue.queue) > 0 and newQueue.queue[0][1] == time:
            readyQueue.put(newQueue.get())

        if running == False and len(readyQueue.queue) > 0:
            runningProcess = readyQueue.get()
            running = True
            count = 0
            result_output.append("  " + str(time))
            result_output.append(runningProcess[0])

        elif running == True:
            if count < quantum:
                runningProcess[3] -= 1
                count += 1
            elif count == quantum:
                running = False
                runningProcess[3] -= 1
                if runningProcess[3] > 0:
                    readyQueue.put(runningProcess)
                    result_output.append("  " + str(time))

        if running == True and runningProcess[3] == 0:
            running = False
            runningProcess[4] = time
            runningProcess[5] = time - runningProcess[1]
            runningProcess[6] = runningProcess[5] - runningProcess[2]
            runningProcess[7] = runningProcess[4] - runningProcess[1] - runningProcess[2]
            terminatedQueue.put(runningProcess)
            count = 0
            result_output.append("  " + str(time))
            if time == total_burst + timeFirstProcess:
                break

        if running == True and runningProcess[3] > 0 and count == quantum:
            readyQueue.put(runningProcess)
            running = False
            count = 0

        if running == False and len(readyQueue.queue) > 0:
            runningProcess = readyQueue.get()
            running = True
            count = 0
       
        gnt.broken_barh([(time, 1)], ((runningProcess[0] * 10) + 2 ,6 ),facecolors ='tab:blue')
        time += 1

    terminated_processes = []
    proc = []
    while not terminatedQueue.empty():
        proc = terminatedQueue.get()
        terminated_processes.append([proc[1],proc[2],proc[4],proc[5],proc[6],proc[7]])

    terminated_processes = sorted(terminated_processes, key=itemgetter(0))

    avrTernaroundTime = 0
    avrWaitingTime = 0
    avrResponseTime = 0
    for process in terminated_processes:
        result_output.append(str(process))
        avrTernaroundTime += process[3]
        avrWaitingTime += process[4]
        avrResponseTime += process[5]

    avrTurnaroundTime = avrTernaroundTime / maxSize
    avrWaitingTime = avrWaitingTime / maxSize
    avrResponseTime = avrResponseTime / maxSize

    # Open a new window to display the results
    result_window = tk.Toplevel(root)
    result_window.title("Round Robin Results")

    # Display the results in a table
    result_table = ttk.Treeview(result_window, columns=( "Arrival Time", "Burst Time", "Finish Time", "Turnaround Time", "Waiting Time", "Response Time"))
    result_table.heading("#0", text="Process")
    result_table.heading("Arrival Time", text="Arrival Time")
    result_table.heading("Burst Time", text="Burst Time")
    result_table.heading("Finish Time", text="Finish Time")
    result_table.heading("Turnaround Time", text="Turnaround Time")
    result_table.heading("Waiting Time", text="Waiting Time")
    result_table.heading("Response Time", text="Response Time")
    result_table.column("#0", width=75)
    result_table.column("Arrival Time", width=75)
    result_table.column("Burst Time", width=75)
    result_table.column("Finish Time", width=75)
    result_table.column("Turnaround Time", width=100)
    result_table.column("Waiting Time", width=100) 
    result_table.column("Response Time", width=100)

    for i, process in enumerate(terminated_processes):
        text = "P"+str(i+1)
        result_table.insert("", tk.END,text=text , values=process)

    result_table.grid(row=0, column=0, padx=10, pady=10)

    # Display the averages
    avg_turnaround_label = tk.Label(result_window, text="Average Turnaround time = {:.2f}".format(avrTurnaroundTime))
    avg_turnaround_label.grid(row=1, column=0, padx=10, pady=5)

    avg_waiting_label = tk.Label(result_window, text="Average Waiting time = {:.2f}".format(avrWaitingTime))
    avg_waiting_label.grid(row=2, column=0, padx=10, pady=5)

    avg_response_label = tk.Label(result_window, text="Average Response time = {:.2f}".format(avrResponseTime))
    avg_response_label.grid(row=3, column=0, padx=10, pady=5)

    
    plt.savefig("gantt1.png")
    chart = plt.imread('gantt1.png')
    plt.imshow(chart , aspect="auto")
    plt.show()

root = tk.Tk()
root.title("Round Robin")

label_quantam = tk.Label(root, text="Time Quantum:")
label_quantam.grid(row=0, column=0, padx=10, pady=10)
entry_quantam = tk.Entry(root)
entry_quantam.grid(row=0, column=1, padx=10, pady=10)

label_Number = tk.Label(root, text="Number of processes:")
label_Number.grid(row=1, column=0, padx=10, pady=10)
entry_Number = tk.Entry(root)
entry_Number.grid(row=1, column=1, padx=10, pady=10)

arrival_entries = []
burst_entries = [] 

def create_entries():
    maxSize = int(entry_Number.get())
    for i in range(maxSize):
        pros_label=tk.Label(root,text=f"P{i+1}")
        pros_label.grid(row=2, column=i+1, padx=10, pady=10)
    label_arrival = tk.Label(root, text="Arrival Time:")
    label_arrival.grid(row=3, column=0, padx=10, pady=10)
    label_burst = tk.Label(root, text="Burst Time:")
    label_burst.grid(row=4, column=0, padx=10, pady=10)
    
    for i in range(maxSize): 
        arrival_entry = tk.Entry(root)
        arrival_entry.grid(row=3, column=i+1, padx=10, pady=10)
        arrival_entries.append(arrival_entry)
        
        burst_entry = tk.Entry(root)
        burst_entry.grid(row=4, column=i+1, padx=10, pady=10)
        burst_entries.append(burst_entry)

button_Number = tk.Button(root, text="ADD", command=create_entries)
button_Number.grid(row=1, column=2, padx=10, pady=10)

button_Run = tk.Button(root, text="RESULT", command=roundRobin)
button_Run.grid(row=5, column=0, columnspan=2, padx=10, pady=10)
avg_turnaround_label = tk.Label(root, text="")

avg_waiting_label = tk.Label(root, text="")

avg_response_label = tk.Label(root, text="")
root.mainloop()