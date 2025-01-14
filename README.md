# auto-ngrok

Installs a Linux `systemd` service that opens an SSH tunnel using [ngrok](https://ngrok.com) (see [here](https://ngrok.com/docs/using-ngrok-with/ssh)), and opens a webserver that returns the SSH connection URL. **Why so complicated?** ngrok's free tier supports static domains only for HTTP tunnels. This way, the SSH tunnel can be opened on boot and discovered without the need for another connection (besides the HTTP request to the static domain). 


## Installation

Clone the Git repository:
```console
git clone https://github.com/JupiterPi/auto-ngrok
```

In `auto-ngrok`, create a Python virtual environment and install the `ngrok` dependency:
```console
cd auto-ngrok
python3 -m venv .venv
source .venv/bin/activate
pip install ngrok
```

Execute `install.py` (you will be asked for an install location and your ngrok Authtoken):
```console
chmod +x install.py
sudo ./install.py
```
It will install the files at the specified location and install a `systemd` system service that will start auto-ngrok on startup.

You can remove auto-ngrok by deleting the service (`systemctl disable auto-ngrok.service`) and optionally removing the installed files (e. g. `rm -r /usr/lib/bin/auto-ngrok`).
