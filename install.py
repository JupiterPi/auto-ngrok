#!./.venv/bin/python3
import os
import ngrok
import shutil
import subprocess

def main():

    # check if user is sudo
    if os.geteuid() != 0:
        print("Please run as root")
        exit(1)

    # prompt for install dir, create it
    install_dir = os.path.expanduser(input("Enter install directory: (default: /usr/local/bin/auto-ngrok) "))
    if install_dir == "":
        install_dir = "/usr/local/bin/auto-ngrok"
    if not os.path.isdir(install_dir):
        os.makedirs(install_dir, exist_ok=True)
    
    # prompt for ngrok authtoken and domain
    authtoken = input("Enter ngrok authtoken: ")
    http_domain = input("Enter ngrok domain: ")
    if authtoken == "" or http_domain == "":
        print("ngrok authtoken and domain required")
        exit(1)

    # test ngrok
    try:
        ngrok.forward(8000, domain=http_domain, authtoken=authtoken)
    except Exception as e:
        print(f"Error trying to start ngrok tunnel to port 8000: {e}")
        exit(1)
    print("ngrok test tunnel works...")
    

    # generate start.sh file
    with open("start.sh", "w") as f:
        f.write(
            "#!/bin/bash\n"
            f"export AUTO_NGROK_DOMAIN={http_domain}\n"
            f"export NGROK_AUTHTOKEN={authtoken}\n"
            f"{install_dir}/.venv/bin/python3 {install_dir}/server.py"
        )
    os.chmod("./start.sh", 0o755)
    
    # install source files
    shutil.copytree('.', install_dir, dirs_exist_ok=True)

    print(f"auto_ngrok installed at {install_dir}...")

    # generate auto_ngrok.service file
    with open(f"/etc/systemd/system/auto-ngrok.service", "w") as f:
        f.write(
            "[Unit]\n"
            "Description=auto_ngrok\n"
            "After=network-online.target\n"
            "\n"
            "[Service]\n"
            f"ExecStart=/bin/bash {install_dir}/start.sh\n"
            "Restart=always\n"
            "RestartSec=3\n"
            "Type=simple\n"
            "\n"
            "[Install]\n"
            "WantedBy=multi-user.target\n"
        )

    # enable and restart the service
    subprocess.run(["sudo", "systemctl", "enable", "auto-ngrok.service"], check=True)
    subprocess.run(["sudo", "systemctl", "restart", "auto-ngrok.service"], check=True)

    print("Service installed and started (`systemctl disable auto-ngrok.service` to remove)")

if __name__ == "__main__":
    main()