import requests

# Fetch heart rate data from API
url = "http://178.79.130.53:8000/unicareservice/sensordata"
params = {
    "profileid": "2754c964-8d3b-4474-bfeb-8d93bbc6137b",
    "hours": 8
}
response = requests.get(url, params=params)
data = response.json()

# Extract heart rate and step count values
heart_rates = []
step_counts = []
for entry in data:
    if entry["hr"] is not None:
        heart_rates.append(entry["hr"])
    if entry["step"] is not None:
        step_counts.append(entry["step"])

# Calculate heart rate statistics
average_heart_rate = sum(heart_rates) / len(heart_rates)
step_count = max(step_counts)

# Define threshold values (expected heart rate for an 18-21 y/o male)
heart_rate_upper_threshold = 200
heart_rate_lower_threshold = 50
step_count_threshold = 10000

# Compare heart rate data with threshold values
is_abnormal_heart_rate = False
if average_heart_rate > heart_rate_upper_threshold or average_heart_rate < heart_rate_lower_threshold:
    is_abnormal_heart_rate = True

is_low_step_count = False
if step_count < step_count_threshold:
    is_low_step_count = True

# Trigger alert or notification if abnormal heart rate or low step count
if is_abnormal_heart_rate or is_low_step_count:
    #trigger alert or notification
    print("Abnormal heart rate or low step count detected! Alert triggered.")
    #*send alert to webpage*
else:
    print("Heart rate and step count within normal range.")
