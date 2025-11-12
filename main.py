import requests
import random
import string
import time

WEBHOOK_URL = "YOUR_EWBHOOK_URL_HERE"

def generate_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=18))

def check_code(code):
    url = f"https://discordapp.com/api/v9/entitlements/gift-codes/{code}?with_application=false&with_subscription_plan=true"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return True
        elif response.status_code == 429:
            retry_after = response.json().get("retry_after", 5)
            print(f"Rate limited. Sleeping for {retry_after} seconds...")
            time.sleep(retry_after)
        return False
    except requests.exceptions.RequestException as e:
        print(f"Error checking code {code}: {e}")
        return False

def send_to_webhook(code):
    data = {"content": f"Valid Nitro Code Found: https://discord.gift/{code}"}
    try:
        r = requests.post(WEBHOOK_URL, json=data, timeout=5)
        if r.status_code == 204:
            print(f"Sent valid nitro code to webhook: {code}")
        else:
            print(f"Webhook failed: {r.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending to webhook: {e}")

def main():
    while True:
        code = generate_code()
        print(f"Checking code: {code}")

        if check_code(code):
            send_to_webhook(code)

        delay = random.uniform(1.0, 3.0)
        time.sleep(delay)

if __name__ == "__main__":
    main()
