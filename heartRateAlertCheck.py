import requests
import statistics

# Get sensor data from API
url = "http://178.79.130.53:8000/unicareservice/sensordata"
params = {
    "profileid": "2754c964-8d3b-4474-bfeb-8d93bbc6137b",
    "hours": 8
}
response = requests.get(url, params=params)
data = response.json()

# Extract heart rate and step count values from data
heart_rates = [d["hr"] for d in data if "hr" in d and d["hr"] is not None]
step_counts = [d["step"] for d in data if "step" in d and d["step"] is not None]

# Calculate mean and standard deviation of heart rate and step count data
mean_hr = statistics.mean(heart_rates)
std_hr = statistics.stdev(heart_rates)
mean_step = statistics.mean(step_counts)
std_step = statistics.stdev(step_counts)

# Set Z-score threshold for abnormal heart rate and step count
z_threshold_hr = 2  # You can adjust this value as needed for heart rate
z_threshold_step = 2  # You can adjust this value as needed for step count

# Calculate threshold values for heart rate and step count
upper_threshold_hr = mean_hr + z_threshold_hr * std_hr
lower_threshold_hr = mean_hr - z_threshold_hr * std_hr
upper_threshold_step = mean_step + z_threshold_step * std_step
lower_threshold_step = mean_step - z_threshold_step * std_step

# Check heart rate and step count values against threshold values
for d in data:
    hr = d["hr"]
    step = d["step"]
    if hr is not None and (hr > upper_threshold_hr or hr < lower_threshold_hr):
        # Send alert to smartwatch for abnormal heart rate
        # You can implement the code to send the alert to the smartwatch here
        print(f"Heart rate {hr} is abnormal. Sending alert to smartwatch.")
    if step is not None and (step > upper_threshold_step or step < lower_threshold_step):
        # Send alert to smartwatch for abnormal step count
        # You can implement the code to send the alert to the smartwatch here
        print(f"Step count {step} is abnormal. Sending alert to smartwatch.")
