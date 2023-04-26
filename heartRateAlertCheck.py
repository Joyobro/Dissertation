import requests
import statistics

# Define the API endpoint and parameters
url = "http://178.79.130.53:8000/unicareservice/sensordata"
params = {"profileid": "2754c964-8d3b-4474-bfeb-8d93bbc6137b", "hours": 8}

# Make a GET request to the API and extract the heart rate and step count data
response = requests.get(url, params=params)
data = response.json()
hr_data = [d["hr"] for d in data if d["hr"] is not None]
step_data = [d["step"] for d in data if d["step"] is not None]

# Calculate the moving average of heart rate and step count
n = len(hr_data)
if n > 0:
    hr_avg = statistics.mean(hr_data)
    step_avg = statistics.mean(step_data)
    hr_stdev = statistics.stdev(hr_data)
    step_stdev = statistics.stdev(step_data)
    hr_threshold = hr_avg - 2*hr_stdev + 0.1*step_avg
    hr_max = hr_avg + 2*hr_stdev + 0.1*step_avg
    hr_min = hr_avg - 2*hr_stdev - 0.1*step_avg

    # Check if the current heart rate is outside the threshold
    current_hr = hr_data[-1]
    if current_hr is not None and (current_hr > hr_max or current_hr < hr_min):
        print("Heart rate anomaly detected:", current_hr)
        # Send alert to smart watch + website
else:
    print("No heart rate data available.")
# 888