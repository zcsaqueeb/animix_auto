---

<h1 align="center">Animix Bot</h1>

<p align="center">Automate tasks in Animix to enhance your efficiency and maximize your results!</p>

---

## 🚀 **About the Bot**

The Animix Bot is designed to automate various tasks in **Animix**, including:

- **Automatic Gacha**
- **Automatic Achievement Claims**
- **Automatic DNA Mixing**
- **Automatic Missions**
- **Automatic Quests**
- **Pass Reward Automation**
- **PvP Automation**
- **Multi-Account Support**
- **Proxy Support**

With this bot, you can save time and maximize your outcomes without manual interactions.

---

## 🌟 Version v1.2.5

### Updates

- **Mission System Optimization:**  
  The bot now performs a two-stage pet assignment process for missions. In the first stage, it assigns pets that exactly match the mission requirements. For any missions that fail to start due to unavailable exact matches, the second stage kicks in—assigning available pets with a star rating higher than the mission’s requirement. This dual-phase approach maximizes mission completion and ensures efficient pet utilization.

---

### **Features in This Version:**

- **Auto Gacha:** Perform gacha automatically.
- **Auto Achievements:** Automatically claim achievements.
- **Custom Mix System:** Configure your pet mix using the provided `dna.json` file and avoid mixing pets with a star rating greater than 4.
- **Auto Missions:** Complete missions automatically.
- **Auto Quests:** Accomplish quests without manual intervention.
- **Auto Claim Pass:** Automatically claim pass rewards.
- **Auto PvP:** Engage in PvP battles and maximize rewards.
- **Defense Setup for PvP:** Configure your defense team for better PvP performance.
- **Pet Upgrade System:** Automatically upgrade pets with 4 stars or higher.
- **Multi-Account Support:** Manage multiple accounts simultaneously.
- **Proxy Support:** Assign different proxies for each account dynamically.
- **Delay Loop and Account Switching:** Set intervals for looping and account transitions.

---

## ⚙️ **Configuration in `config.json`**

| **Function**           | **Description**                          | **Default**                                                                  |
| ---------------------- | ---------------------------------------- | ---------------------------------------------------------------------------- |
| `gacha`                | Automate gacha pulls                     | `True`                                                                       |
| `achievements`         | Claim achievements automatically         | `True`                                                                       |
| `mix`                  | Automate DNA mixing                      | `True`                                                                       |
| `mission`              | Complete missions automatically          | `True`                                                                       |
| `quest`                | Automate quest completion                | `True`                                                                       |
| `claim_pass`           | Claim pass rewards automatically         | `True`                                                                       |
| `pvp`                  | Engage in PvP battles automatically      | `True`                                                                       |
| `pet_mix`              | Custom pet mix configuration             | `[ [125, 121], [122, 125], [124, 125], [118, 116], [119, 115], [120, 113] ]` |
| `proxy`                | Enable/Disable proxy usage               | `False`                                                                      |
| `delay_loop`           | Delay before the next loop (seconds)     | `3000`                                                                       |
| `delay_account_switch` | Delay between account switches (seconds) | `10`                                                                         |

---

## 📥 **How to Register**

Start using Animix by registering through the following link:

<div align="center">
  <a href="https://t.me/animix_game_bot?startapp=3lsLj56QYJx6" target="_blank">
    <img src="https://img.shields.io/static/v1?message=Animix&logo=telegram&label=&color=2CA5E0&logoColor=white&labelColor=&style=for-the-badge" height="25" alt="telegram logo" />
  </a>
</div>

---

## 📖 **Installation Steps**

1. **Clone the Repository**  
   Copy the project to your local machine:

   ```bash
   git clone https://github.com/livexords-nw/Animix-bot.git
   ```

2. **Navigate to the Project Folder**  
   Move to the project directory:

   ```bash
   cd Animix-bot
   ```

3. **Install Dependencies**  
   Install the required libraries:

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Query**  
   Create a `query.txt` file and add your Animix query data.

5. **Set Up Proxy (Optional)**  
   To use a proxy, create a `proxy.txt` file and add proxies in the format:

   ```
   http://username:password@ip:port
   ```

   - Only HTTP and HTTPS proxies are supported.

6. **Run the Bot**  
   Execute the bot using the following command:
   ```bash
   python main.py
   ```

---

### 🔹 Want Free Proxies? You can obtain free proxies from [Webshare.io](https://www.webshare.io/).

---

## 🛠️ **Contributing**

This project is developed by **Livexords**. If you have suggestions, questions, or would like to contribute, feel free to contact us:

<div align="center">
  <a href="https://t.me/livexordsscript" target="_blank">
    <img src="https://img.shields.io/static/v1?message=Livexords&logo=telegram&label=&color=2CA5E0&logoColor=white&labelColor=&style=for-the-badge" height="25" alt="telegram logo" />
  </a>
</div>

---
