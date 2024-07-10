import schedule
import time

# Assuming this is your list of values
values = [1, 2, 3, 4, 5]
# Global list to store results
results = []
# Global iterator
current_index = 0

def job(arg, jobs):
    global current_index
    print("job:", jobs)
    # Perform operations and return a value  # Example operation
    results.append(values[current_index] + 1)
    print(results)
    print(len(values))
    current_index += 1  
    print(current_index)# Move to the next value
    

# Start the scheduling with the first value
schedule.every(2).seconds.do(job, values[current_index], "first")

while True:
    schedule.run_pending()
    time.sleep(1)
    if current_index >= len(values):  # Break the loop when all values are processed
        print("All values processed. Results:", results)
        break
