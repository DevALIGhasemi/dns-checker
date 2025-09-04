# DNS Optimizer for Linux

A simple Python tool to automatically **find the fastest DNS servers** for your network and apply them to your chosen interface.  
It also allows you to **revert DNS settings** back to automatic (via DHCP).

---

## 🖥️ Supported Distributions
This script works on Linux distributions that use **systemd-resolved**, such as:
- Ubuntu (18.04+)
- Debian (10+)
- Fedora
- Arch Linux
- Manjaro
- Pop!_OS

> ⚠️ It will not work on minimal distros without `systemd`.

---

## 📂 Project Structure
```
dns-checker/
├── run.py        # Main script
├── list.txt      # DNS server list (one IP per line)
└── README.md     # Project documentation
```

---

## 🚀 Installation & Usage

1. Clone the repository:
   ```bash
   git clone https://github.com/DEVALIGhasemi/dns-checker.git
   cd dns-checker/
   ```

2. Install dependencies:
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip -y
   pip install dnspython
   ```

3. Edit `list.txt` and add your preferred DNS servers (one IP per line).

4. Run the script:
   ```bash
   python3 run.py
   ```

---

## 📋 Menu Options
When you start the program, you’ll see:

```
       Welcome
----------------------
[1] Set     DNS
[2] Clean   DNS
[9] About Me
[0] Exit
----------------------
```

- **[1] Set DNS** → Tests all DNS servers (with Google + Soft98) and applies the fastest ones to your chosen interface.  
- **[2] Clean DNS** → Reverts DNS settings to default (automatic via DHCP).  
- **[9] About Me** → Author information.  
- **[0] Exit** → Exit the program.  

---

## 📌 Example Run
```bash
python3 run.py

Enter Number: 1

Best DNS list: ['178.22.122.100', '185.51.200.2']
<-------------------------------------->
[1] eno1
[2] wlp3s0
<-------------------------------------->
Enter number of interface: 2
DNS applied on wlp3s0: 178.22.122.100, 185.51.200.2
```

---

## ✨ Features
- Tests DNS servers against both local and global domains.  
- Automatically selects the fastest DNS servers.  
- Supports multiple network interfaces.  
- One-click revert to automatic DNS (DHCP).  
- Handles errors gracefully and supports `CTRL+C` exit.

---

## 👨‍💻 Author
Created by **ALI Ghasemi**
