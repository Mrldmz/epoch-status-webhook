#!/usr/bin/env python3
"""
Epoch Status Webhook Monitor
A simple Python script that monitors for status changes and sends Discord webhooks.
Double-click this file to start monitoring.
"""

import os
import sys
import time
import json
import requests
from datetime import datetime
import traceback

# Configuration
WEBHOOK_FILE = 'webhook.txt'
CHECK_INTERVAL = 30  # seconds between checks
MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds

def read_webhook_url():
    """Read Discord webhook URL from webhook.txt file"""
    try:
        if not os.path.exists(WEBHOOK_FILE):
            print(f"❌ Error: {WEBHOOK_FILE} not found!")
            print(f"Please create {WEBHOOK_FILE} and put your Discord webhook URL inside.")
            return None
        
        with open(WEBHOOK_FILE, 'r', encoding='utf-8') as f:
            url = f.read().strip()
            
        if not url:
            print(f"❌ Error: {WEBHOOK_FILE} is empty!")
            return None
            
        if not url.startswith('https://discord.com/api/webhooks/'):
            print(f"❌ Error: Invalid Discord webhook URL in {WEBHOOK_FILE}")
            print("URL should start with: https://discord.com/api/webhooks/")
            return None
            
        return url
    except Exception as e:
        print(f"❌ Error reading {WEBHOOK_FILE}: {e}")
        return None

def send_discord_webhook(message, webhook_url, username="Epoch Status Bot", color=0x00ff00):
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
    TODO: Implement your condition logic here.
    
    This function should return True when you want to send a webhook message.
    Examples of what you might check:
    - Website status changes
    - File modifications
    - API responses
    - Time-based conditions
    - External service status
    
    Returns:
        bool: True if a webhook should be sent, False otherwise
    """
    # TODO: Replace this with your actual condition logic
    # For now, this is just a placeholder that returns False
    # 
    # Example implementations:
    #
    # Check if a specific file was modified:
    # return os.path.getmtime('some_file.txt') > last_check_time
    #
    # Check website status:
    # try:
    #     response = requests.get('https://epoch.strykersoft.us/', timeout=5)
    #     return response.status_code == 200
    # except:
    #     return False
    #
    # Check time-based condition:
    # return datetime.now().minute == 0  # Send every hour
    
    return True  # Placeholder, always returns True for testing

def get_webhook_message():
    """
    TODO: Customize the message content here.
    
    This function should return the message you want to send to Discord.
    You can make it dynamic based on current conditions.
    
    Returns:
        str: The message to send via webhook
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # TODO: Customize this message based on your needs
    message = f"Status update triggered at {timestamp}"
    
    # You can make this dynamic, for example:
    # - Include current status information
    # - Add relevant data from your checks
    # - Format based on what triggered the webhook
    
    return message

def main():
    """Main monitoring loop"""
    print("🚀 Epoch Status Webhook Monitor Starting...")
    print("=" * 50)
    
    # Check if webhook URL is configured
    webhook_url = read_webhook_url()
    if not webhook_url:
        print("\n📝 Setup Instructions:")
        print(f"1. Create a file named '{WEBHOOK_FILE}' in this directory")
        print("2. Put your Discord webhook URL inside the file")
        print("3. Run this script again")
        print("\n💡 To get a Discord webhook URL:")
        print("   - Go to your Discord server")
        print("   - Edit a channel → Integrations → Webhooks")
        print("   - Create a new webhook and copy the URL")
        input("\nPress Enter to exit...")
        return
    
    print(f"✅ Webhook URL loaded successfully")
    print(f"⏱️  Check interval: {CHECK_INTERVAL} seconds")
    print(f"🔄 Starting monitoring loop...")
    print("📝 Note: Implement your logic in the should_send() function")
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
                    send_discord_webhook(message, webhook_url)
            
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
