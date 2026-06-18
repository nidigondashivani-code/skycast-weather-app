import smtplib
from email.message import EmailMessage
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

def send_email_alert(subject, body):
    """Sends an email alert using SMTP."""
    sender_email = config.SENDER_EMAIL
    sender_password = config.SENDER_PASSWORD
    recipients = config.ALERT_RECIPIENTS

    if not sender_email or not sender_password or sender_email == "your_email@gmail.com":
        print("Alert triggered, but email credentials are not configured. Printing to console instead.")
        print(f"--- ALERT ---\nSubject: {subject}\nBody: {body}\n-------------")
        return

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = ", ".join(recipients)
    msg.set_content(body)

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.send_message(msg)
        print(f"Alert email sent to {recipients}")
    except Exception as e:
        print(f"Failed to send email alert: {e}")

def check_and_send_alerts(weather_data):
    """Checks weather data against thresholds and sends alerts if necessary."""
    city = weather_data['city']
    temp = weather_data['temperature']
    condition = weather_data['weather_condition']

    alerts = []

    if temp > config.TEMP_UPPER_THRESHOLD:
        alerts.append(f"High Temperature Alert! Current temperature is {temp}°C.")
    
    if temp < config.TEMP_LOWER_THRESHOLD:
        alerts.append(f"Low Temperature Alert! Current temperature is {temp}°C.")
    
    if condition in config.ALERT_CONDITIONS:
        alerts.append(f"Severe Weather Alert! Current condition is {condition}.")

    if alerts:
        subject = f"Weather Alert for {city}"
        body = "\n".join(alerts)
        send_email_alert(subject, body)
