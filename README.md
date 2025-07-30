# epoch-status-webhook

Local webhook monitor for Discord that sends status updates based on custom conditions.

## Quick Start

1. **Setup Discord Webhook:**
   - Go to your Discord server
   - Edit a channel → Integrations → Webhooks
   - Create a new webhook and copy the URL

2. **Configure the script:**
   - Edit `webhook.txt` and replace the placeholder with your Discord webhook URL
   - Edit `role-id.txt` and replace the placeholder with your Discord role ID (optional)

3. **Get Discord Role ID (optional, for @role mentions):**
   - Enable Developer Mode in Discord (User Settings → Advanced → Developer Mode)
   - Right-click on the role you want to mention (e.g., @Epoch)
   - Click "Copy ID" and paste it in `role-id.txt`

4. **Run the monitor:**
   - Double-click `run.bat` to start (creates virtual environment and installs dependencies automatically)
   - Or run manually with venv: `venv\Scripts\activate && python epoch_webhook.py`

## Files

- `epoch_webhook.py` - Main monitoring script
- `webhook.txt` - Contains your Discord webhook URL (create from webhook.txt.template)
- `webhook.txt.template` - Template for webhook configuration
- `role-id.txt` - Contains Discord role ID for mentions (create from role-id.txt.template)
- `role-id.txt.template` - Template for role ID configuration
- `run.bat` - Easy launcher that creates venv, installs dependencies and runs the script
- `clean.bat` - Removes the virtual environment folder
- `requirements.txt` - Python dependencies
- `venv/` - Python virtual environment (created automatically)

## Features

- ✅ Monitors Epoch server status changes automatically
- ✅ Discord webhook integration with rich embeds
- ✅ Optional role mentions for notifications
- ✅ Automatic retry on failure
- ✅ Error handling and logging
- ✅ Virtual environment setup
- ✅ Easy configuration via text files

## Disclaimer

- Not affiliated with the user [@stryker2k2](https://www.reddit.com/user/stryker2k2/)
- Not affiliated with [Project Epoch](https://www.project-epoch.net/)
