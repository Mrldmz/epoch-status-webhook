# epoch-status-webhook

Local webhook monitor for Discord that sends status updates for the Project Epoch servers (particularly Kezan and Auth) based on the status shown on [Epoch Status](https://epoch.strykersoft.us/).

## Quick Start

1. **Setup Discord Webhook:**
   - Go to your Discord server
   - Edit a channel → Integrations → Webhooks
   - Create a new webhook and copy the URL

2. **Configure the script:**
   - Rename `example-config.txt` to `config.txt`
   - Edit `config.txt` and set your webhook URL and role ID:
     ```
     webhook_url=https://discord.com/api/webhooks/YOUR_WEBHOOK_ID/YOUR_WEBHOOK_TOKEN
     role_id=1234567890123456789
     ```

3. **Get Discord Role ID (optional, for @role mentions):**
   - Enable Developer Mode in Discord (User Settings → Advanced → Developer Mode)
   - Right-click on the role you want to mention (e.g., @Epoch)
   - Click "Copy ID" and paste it after `role_id=` in config.txt

4. **Run the monitor:**
   - Double-click `run.bat` to start (creates virtual environment and installs dependencies automatically)
   - Or run manually with venv: `venv\Scripts\activate && python epoch_webhook.py`

## Files

- `epoch_webhook.py` - Main monitoring script
- `example-config.txt` - Template configuration file (rename to config.txt)
- `config.txt` - Your actual configuration file (created from example-config.txt)
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

- Not affiliated with [@stryker2k2](https://www.reddit.com/user/stryker2k2/), the author of [Epoch Status](https://epoch.strykersoft.us/)
- Not affiliated with [Project Epoch](https://www.project-epoch.net/)
