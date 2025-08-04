# epoch-status-webhook

Local webhook monitor for Discord that sends status updates for the Project Epoch servers (particularly Kezan and Auth) based on the status shown on [Epoch Status](https://epoch.strykersoft.us/) or [Epoch Status Info](https://epoch-status.info/).

## Quick Start

1. **Setup Discord Webhook:**
   - Go to your Discord server
   - Edit a channel → Integrations → Webhooks
   - Create a new webhook and copy the URL

2. **Configure the script:**
   - Rename `example-config.txt` to `config.txt`
   - Edit `config.txt` and set your webhook URL, role ID, and status website:
     ```
     webhook_url=https://discord.com/api/webhooks/YOUR_WEBHOOK_ID/YOUR_WEBHOOK_TOKEN
     role_id=1234567890123456789
     status_website_url=https://epoch-status.info/
     ```
   - For `status_website_url`, use one of:
     - `https://epoch-status.info/` (recommended)
     - `https://epoch.strykersoft.us/`

3. **Get Discord Role ID (optional, for @role mentions):**
   - Enable Developer Mode in Discord (User Settings → Advanced → Developer Mode)
   - Right-click on the role you want to mention (e.g., @Epoch)
   - Click "Copy ID" and paste it after `role_id=` in config.txt

4. **Run the monitor:**
   - Double-click `run.bat` to start (creates virtual environment, installs dependencies, and automatically runs the correct script based on your configured website)
   - Or run manually with venv: `venv\Scripts\activate && python epoch_webhook.py` (for epoch.strykersoft.us) or `python epoch_info_webhook.py` (for epoch-status.info)

## Files

- `epoch_webhook.py` - Monitoring script for https://epoch.strykersoft.us/
- `epoch_info_webhook.py` - Monitoring script for https://epoch-status.info/
- `example-config.txt` - Template configuration file (rename to config.txt)
- `config.txt` - Your actual configuration file (created from example-config.txt)
- `run.bat` - Easy launcher that creates venv, installs dependencies and runs the appropriate script based on configuration
- `clean.bat` - Removes the virtual environment folder
- `requirements.txt` - Python dependencies
- `venv/` - Python virtual environment (created automatically)

## Features

- ✅ Monitors Epoch server status changes automatically
- ✅ Supports both epoch.strykersoft.us and epoch-status.info websites
- ✅ Automatic script selection based on configured website
- ✅ Discord webhook integration with rich embeds
- ✅ Optional role mentions for notifications
- ✅ Automatic retry on failure
- ✅ Error handling and logging
- ✅ Virtual environment setup
- ✅ Easy configuration via text files

## Disclaimer

- Not affiliated with [@stryker2k2](https://www.reddit.com/user/stryker2k2/), the author of [Epoch Status](https://epoch.strykersoft.us/)
- Not affiliated with the maintainers of [Epoch Status Info](https://epoch-status.info/)
- Not affiliated with [Project Epoch](https://www.project-epoch.net/)
