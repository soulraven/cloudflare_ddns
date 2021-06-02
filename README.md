## 🌤 Cloudflare DDNS client
Linux client that update the Cloudflare DNS records for domains hosted on Cloudflare account.

This Python script is using [CloudFlare's client API](https://api.cloudflare.com/) to automatically and periodically
update the A and the AAAA records present on Cloudflare domains DNS records with host external IP or specific IP


### 🔧 Installation
The installation is very simple. 
```bash
git clone https://github.com/soulraven/cloudflare_ddns.git
cd cloudflare_ddns
ln -s cfddns.service /lib/systemd/system/cfddns.service
systemctl daemon-reload
systemctl enable cfddns
systemctl start cfddns
```
Keep in mind that the client will not work without settings.py configuration file.
Rename the settings_example.py to settings.py and change the default values with your own API credentials

### 🔑 Authentication methods

You can choose to use either the newer API tokens, or the traditional API keys

To generate a new API tokens, go to your [Cloudflare Profile](https://dash.cloudflare.com/profile/api-tokens) 
and create a token capable of **Edit DNS**.

### 🌍 Contributions

Contributions of all forms are welcome :)

## 🗒 License

This repository is licensed under the GNU General Public License, version 3 (GPLv3).

## 👀 Author

Zaharia Constantin

[View my GitHub profile 💡](https://github.com/soulraven)
