import requests
import statistics

# Get heart rate data from API
url = "http://178.79.130.53:8000/unicareservice/sensordata"
params = {
    "profileid": "2754c964-8d3b-4474-bfeb-8d93bbc6137b",
    "hours": 8
}
response = requests.get(url, params=params)
data = response.json()

# Extract heart rate values from data
heart_rates = [d["hr"] for d in data if "hr" in d and d["hr"] is not None]

# Calculate mean and standard deviation of heart rate data
mean_hr = statistics.mean(heart_rates)
std_hr = statistics.stdev(heart_rates)

# Set Z-score threshold for abnormal heart rate
z_threshold = 2  # You can adjust this value as needed

# Calculate threshold values
upper_threshold = mean_hr + z_threshold * std_hr
lower_threshold = mean_hr - z_threshold * std_hr

# Check heart rate values against threshold values
for hr in heart_rates:
    if hr > upper_threshold or hr < lower_threshold:
        # Send alert to smartwatch
        # implement the code to send the alert to the smartwatch here
        print(f"Heart rate {hr} is abnormal. Sending alert to smartwatch.")
