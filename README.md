# DNS Manager v2.0 (Linux)

A powerful and clean Python tool to **test, optimize, and manage DNS servers on Linux systems**.  
This tool automatically benchmarks DNS servers, selects the fastest ones, and applies them to your chosen network interface using `systemd-resolved`.

---

## 🖥️ Supported Systems

This project works on **Linux distributions that use `systemd-resolved`**, including:

- Ubuntu 18.04+
- Debian 10+
- Fedora
- Arch Linux
- Manjaro
- Pop!_OS

⚠️ **Not supported** on systems without `systemd-resolved` or `resolvectl`.

---

## ✨ Features

- 🚀 Automatic DNS speed testing
- 📊 Benchmarks DNS servers using real domain queries
- ⚡ Selects the fastest DNS servers automatically
- 🌐 Supports IPv4 and IPv6
- 🧠 Clean OOP-based architecture
- 🔌 Interface selection (Ethernet / Wi-Fi)
- ♻️ One-command DNS revert (back to DHCP)
- 🛑 Robust error handling
- 🧪 Standalone DNS speed test mode

---

## 📂 Project Structure

```
dns-manager/
├── run.py        # Main application
├── list.txt      # DNS servers list (IPv4 / IPv6)
└── README.md     # Documentation
```

---

## 📦 Requirements

- Python 3.8+
- systemd-resolved
- sudo access

### Python Dependencies

```bash
pip install dnspython
```

---

## 🚀 Installation

```bash
git clone https://github.com/DEVALIGhasemi/dns-checker.git
cd dns-checker
```

Edit `list.txt` and add DNS servers (one per line):

```txt
1.1.1.1
8.8.8.8
178.22.122.100
2606:4700:4700::1111
```

---

## ▶️ Usage

```bash
python3 run.py
```

Menu:

```
DNS Manager
----------------------
[1] Set DNS
[2] Clean DNS
[3] Test DNS Speed
[9] About
[0] Exit
----------------------
```

---

## 📋 Menu Options

### [1] Set DNS
Tests all DNS servers and applies the 2 fastest ones to the selected interface.

### [2] Clean DNS
Reverts DNS settings to automatic (DHCP).

### [3] Test DNS Speed
Tests DNS servers without applying changes.

---

## 🔐 Permissions

DNS modification requires sudo privileges.

```bash
sudo python3 run.py
```

---

## 👨‍💻 Author

**ALI Ghasemi**  

---

## 📄 License

MIT License
