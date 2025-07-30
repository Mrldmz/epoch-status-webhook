# epoch-status-webhook

Local webhook monitor for Discord that sends status updates based on custom conditions.

## Quick Start

1. **Setup Discord Webhook:**
   - Go to your Discord server
   - Edit a channel → Integrations → Webhooks
   - Create a new webhook and copy the URL

2. **Configure the script:**
   - Edit `webhook.txt` and replace the placeholder with your Discord webhook URL
   - Edit the `should_send()` function in `epoch_webhook.py` to implement your condition logic
   - Customize the `get_webhook_message()` function for your message content

3. **Run the monitor:**
   - Double-click `run.bat` to start (creates virtual environment and installs dependencies automatically)
   - Or run manually with venv: `venv\Scripts\activate && python epoch_webhook.py`

## Files

- `epoch_webhook.py` - Main monitoring script
- `webhook.txt` - Contains your Discord webhook URL (create from webhook.txt.template)
- `webhook.txt.template` - Template for webhook configuration
- `run.bat` - Easy launcher that creates venv, installs dependencies and runs the script
- `clean.bat` - Removes the virtual environment folder
- `requirements.txt` - Python dependencies
- `venv/` - Python virtual environment (created automatically)

## Customization

### Implementing your condition logic

Edit the `should_send()` function in `epoch_webhook.py`:

```python
def should_send():
    # Example: Check website status
    try:
        response = requests.get('https://epoch.strykersoft.us/', timeout=5)
        return response.status_code != 200  # Send if site is down
    except:
        return True  # Send if can't reach site
```

### Customizing messages

Edit the `get_webhook_message()` function:

```python
def get_webhook_message():
    return "Custom status message here!"
```

## Features

- ✅ Continuous monitoring loop
- ✅ Discord webhook integration with rich embeds
- ✅ Automatic retry on failure
- ✅ Startup/shutdown notifications
- ✅ Error handling and logging
- ✅ Easy to customize and extend

## Disclaimer

- Not affiliated with the user [@stryker2k2](https://www.reddit.com/user/stryker2k2/)
- Not affiliated with [Project Epoch](https://www.project-epoch.net/)
