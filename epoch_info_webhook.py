#!/usr/bin/env python3
"""
Epoch Status Webhook Monitor
A simple Python script that monitors for status changes and sends Discord webhooks.
Double-click this file to start monitoring or run the batch file named run.bat.
"""

import os
import sys
import time
import json
import requests
from datetime import datetime
import traceback

# Configuration
CONFIG_FILE = 'config.txt'
CHECK_INTERVAL = 30  # seconds between checks
MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds
EPOCH_STATUS_URL = 'https://epoch-status.info/'
# EPOCH_STATUS_URL = 'http://localhost:8000/' # Testing with local server
AUTH_STATUS = 'Login'
KEZAN_STATUS = 'Kezan'

# Status Data
status_data = {
    "previous_auth": None,
    "previous_kezan": None
}

current_message_content = ""

def read_config():
    """Read configuration from config.txt file"""
    try:
        if not os.path.exists(CONFIG_FILE):
            print(f"❌ Error: {CONFIG_FILE} not found!")
            print(f"Please create {CONFIG_FILE} and configure your webhook URL and role ID.")
            return None, None
        
        webhook_url = None
        role_id = None
        
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith('webhook_url='):
                    webhook_url = line.split('=', 1)[1].strip()
                elif line.startswith('role_id='):
                    role_id = line.split('=', 1)[1].strip()
        
        # Validate webhook URL
        if not webhook_url:
            print(f"❌ Error: webhook_url is empty in {CONFIG_FILE}!")
            return None, None
            
        if not webhook_url.startswith('https://discord.com/api/webhooks/'):
            print(f"❌ Error: Invalid Discord webhook URL in {CONFIG_FILE}")
            print("URL should start with: https://discord.com/api/webhooks/")
            return None, None
        
        # Validate role ID (optional)
        if role_id and not role_id.isdigit():
            print(f"⚠️  Warning: Invalid role ID in {CONFIG_FILE}! Should be numbers only. Role mentions will be disabled.")
            role_id = None
        
        if not role_id:
            print(f"⚠️  Warning: role_id is empty in {CONFIG_FILE}. Role mentions will be disabled.")
            
        return webhook_url, role_id
    except Exception as e:
        print(f"❌ Error reading {CONFIG_FILE}: {e}")
        return None, None

def send_discord_webhook(message, webhook_url, role_id=None, username="Epoch Status Bot", color=0x00ff00):
    """Send message to Discord via webhook"""
    try:
        embed = {
            "title": "🚀 Epoch Status Update",
            "description": message,
            "color": color,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "footer": {
                "text": "Epoch Status Monitor",
                "icon_url": "https://cdn.discordapp.com/embed/avatars/0.png"
            }
        }
        
        payload = {
            "username": username,
            "embeds": [embed]
        }
        
        # Add role mention if role ID is available
        if role_id and "DOWN" not in message:
            payload["content"] = f"<@&{role_id}>"
        
        for attempt in range(MAX_RETRIES):
            try:
                response = requests.post(webhook_url, json=payload, timeout=10)
                response.raise_for_status()
                print(f"✅ Message sent successfully: {message}")
                return True
            except requests.exceptions.RequestException as e:
                if attempt < MAX_RETRIES - 1:
                    print(f"⚠️  Attempt {attempt + 1} failed, retrying in {RETRY_DELAY}s...")
                    time.sleep(RETRY_DELAY)
                else:
                    print(f"❌ Failed to send webhook after {MAX_RETRIES} attempts: {e}")
                    return False
        
        return False
    except Exception as e:
        print(f"❌ Unexpected error sending webhook: {e}")
        traceback.print_exc()
        return False

def should_send():
    """
    Check Epoch status page for server status changes using the API.
    Returns True when both Auth and Kezan servers change status and are equal.
    
    Returns:
        bool: True if a webhook should be sent, False otherwise
    """
    global status_data, current_message_content
    
    try:
        # Use the tRPC API endpoint to get server status
        api_url = "https://epoch-status.info/api/trpc/post.getStatus,post.getUptimeHistory"
        params = {
            "batch": "1",
            "input": '{"0":{"json":null,"meta":{"values":["undefined"]}},"1":{"json":null,"meta":{"values":["undefined"]}}}'
        }
        
        print(f"🌐 Fetching server status from API...")
        response = requests.get(api_url, params=params, timeout=10)
        response.raise_for_status()
        
        # Parse the JSON response
        api_data = response.json()
        
        # Extract the status data from the first result
        if (isinstance(api_data, list) and len(api_data) > 0 and 
            "result" in api_data[0] and "data" in api_data[0]["result"] and 
            "json" in api_data[0]["result"]["data"]):
            
            status_json = api_data[0]["result"]["data"]["json"]
            
            # Extract auth and world1 (Kezan) status
            current_auth = "UP" if status_json.get("auth", False) else "DOWN"
            current_kezan = "UP" if status_json.get("world1", False) else "DOWN"
            
        else:
            print("⚠️  Unexpected API response structure")
            return False
        
        current_time = datetime.now().strftime("%H:%M:%S")
        print(f"🔍 [{current_time}] Current status - Auth: {current_auth}, Kezan: {current_kezan}")
        
        # Check if we could parse both statuses
        if current_auth is None or current_kezan is None:
            print("⚠️  Could not parse server status from API")
            return False
        
        # Initialize previous values if they're None
        if status_data["previous_auth"] is None or status_data["previous_kezan"] is None:
            print("📝 Initializing status tracking...")
            status_data["previous_auth"] = current_auth
            status_data["previous_kezan"] = current_kezan
            return False
        
        # Check for status change with different conditions for UP vs DOWN
        auth_changed = current_auth != status_data["previous_auth"]
        kezan_changed = current_kezan != status_data["previous_kezan"]
        
        should_notify = False
        
        if current_auth == "UP" and current_kezan == "UP":
            # For UP status: both servers must be UP AND both must have changed
            should_notify = auth_changed or kezan_changed
        else:
            # For DOWN status: either server went DOWN from previously being UP
            auth_went_down = (status_data["previous_auth"] == "UP" and current_auth == "DOWN")
            kezan_went_down = (status_data["previous_kezan"] == "UP" and current_kezan == "DOWN")
            should_notify = auth_went_down or kezan_went_down
        
        if should_notify:
            # Prepare message content based on current status
            if current_auth == "UP" and current_kezan == "UP":
                current_message_content = "✅ Both Auth and Kezan servers are UP"
            else:
                if current_auth == "DOWN" and current_kezan == "DOWN":
                    current_message_content = "❌ Both Auth and Kezan servers are DOWN"
                elif current_auth == "DOWN":
                    current_message_content = "❌ Auth Server is DOWN"
                elif current_kezan == "DOWN":
                    current_message_content = "❌ Kezan Server is DOWN"
                else:
                    current_message_content = "⚠️ Server status changed"
            
            print(f"🚨 Status change detected! Auth: {current_auth}, Kezan: {current_kezan}")
        
        # Update stored values regardless of outcome
        status_data["previous_auth"] = current_auth
        status_data["previous_kezan"] = current_kezan
        
        return should_notify
        
    except requests.exceptions.RequestException as e:
        print(f"🌐 Error fetching status page: {e}")
        return False
    except Exception as e:
        print(f"❌ Error checking status: {e}")
        traceback.print_exc()
        return False

def get_webhook_message():
    """
    Get the webhook message content from current_message_content variable.
    
    Returns:
        str: The message to send via webhook with timestamp
    """
    global current_message_content
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if current_message_content:
        message = f"{current_message_content}\n\n🕐 Detected at: {timestamp}"
    else:
        message = f"Status update triggered at {timestamp}"
    
    return message

def main():
    """Main monitoring loop"""
    print("🚀 Epoch Status Webhook Monitor Starting...")
    print("=" * 50)
    
    # Check if configuration is set up
    webhook_url, role_id = read_config()
    if not webhook_url:
        print("\n📝 Setup Instructions:")
        print(f"1. Create a file named '{CONFIG_FILE}' in this directory")
        print("2. Add your Discord webhook URL and role ID in this format:")
        print("   webhook_url=https://discord.com/api/webhooks/YOUR_WEBHOOK_ID/YOUR_WEBHOOK_TOKEN")
        print("   role_id=1234567890123456789")
        print("3. Run this script again")
        print("\n💡 To get a Discord webhook URL:")
        print("   - Go to your Discord server")
        print("   - Edit a channel → Integrations → Webhooks")
        print("   - Create a new webhook and copy the URL")
        print("\n💡 To get a Discord role ID (optional):")
        print("   - Enable Developer Mode in Discord")
        print("   - Right-click on the role and copy ID")
        input("\nPress Enter to exit...")
        return
    
    print(f"✅ Webhook URL loaded successfully")
    print(f"⏱️  Check interval: {CHECK_INTERVAL} seconds")
    print(f"🔄 Starting monitoring loop...")
    print("⏹️  Press Ctrl+C to stop monitoring")
    print("-" * 50)
    
    try:
        check_count = 0
        while True:
            check_count += 1
            current_time = datetime.now().strftime("%H:%M:%S")
            
            try:
                # Check if we should send a webhook
                if should_send():
                    message = get_webhook_message()
                    send_discord_webhook(message, webhook_url, role_id)
            
            except Exception as e:
                print(f"❌ Error during check: {e}")
                traceback.print_exc()
            
            # Wait before next check
            time.sleep(CHECK_INTERVAL)
            
    except KeyboardInterrupt:
        print("\n\n⏹️  Stopping monitor...")
        print("👋 Monitor stopped successfully!")
        
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        traceback.print_exc()
        input("Press Enter to exit...")

if __name__ == '__main__':
    main()
