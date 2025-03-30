---

<h1 align="center">Animix Bot</h1>

<p align="center">
Boost your productivity with Animix Bot – your friendly automation tool that handles key tasks in Animix with ease!
</p>

---

## 🚀 About the Bot

Animix Bot is your automation buddy designed to simplify various tasks in **Animix**. No more tedious manual interactions—let the bot take over and maximize your results! This bot automates a wide range of features including:

- **🎰 Auto Gacha:**  
  Automatically perform gacha pulls to maximize your rewards.

- **🏆 Auto Achievements:**  
  Claim achievements automatically to keep your bonus collection growing.

- **🧬 Auto DNA Mixing:**  
  Use a custom mix system (configured via a `dna.json` file) to automatically mix DNA while avoiding combinations with pets that have a star rating greater than 4.

- **🗺️ Auto Missions & Quests:**  
  Complete missions and quests automatically without manual intervention.

- **🎫 Auto Claim Pass:**  
  Claim pass rewards automatically for maximum benefit.

- **⚔️ Auto PvP & Defense Setup:**  
  Engage in PvP battles automatically and configure your defense team for better performance.

- **⏫ Pet Upgrade System:**  
  Automatically upgrade pets with 4 stars or higher to boost your gameplay.

- **👥 Multi-Account Support:**  
  Manage multiple accounts simultaneously with ease.

- **🔌 Proxy Support:**  
  Dynamically assign proxies for each account to support multi-account setups.

- **🧵 Thread System:**  
  (New!) Run multiple tasks concurrently to increase performance and speed up operations.

- **⏱️ Delay Loop & Account Switching:**  
  Set delays between loops and account switches to suit your workflow.

---

## 🌟 Version Updates

**Current Version: v1.3.0**

### v1.3.0 - Latest Update

- **Gacha System Optimization:**  
  The gacha process has been optimized for improved efficiency and reliability.

- **Thread System Addition:**  
  New support for a thread system allows running multiple tasks concurrently to boost performance.

---

## ⚙️ Configuration

### Main Bot Configuration (`config.json`)

```json
{
  "gacha": true,
  "achievements": true,
  "mix": true,
  "mission": true,
  "quest": true,
  "claim_pass": true,
  "pvp": true,
  "proxy": false,
  "thread": 1,
  "delay_loop": 3000,
  "delay_account_switch": 10,
  "pet_mix": [
    [122, 125],
    [125, 121],
    [124, 125],
    [118, 116],
    [119, 115],
    [120, 113]
  ],
  "defens_type": "armor",
  "defens_id": [],
  "attack_type": "damage",
  "attack_id": []
}
```

| **Setting**            | **Description**                                                      | **Default Value** |
| ---------------------- | -------------------------------------------------------------------- | ----------------- |
| `gacha`                | Enable automatic gacha pulls.                                        | `true`            |
| `achievements`         | Automatically claim achievements.                                    | `true`            |
| `mix`                  | Automate DNA mixing.                                                 | `true`            |
| `mission`              | Complete missions automatically.                                     | `true`            |
| `quest`                | Execute quests without manual intervention.                          | `true`            |
| `claim_pass`           | Automatically claim pass rewards.                                    | `true`            |
| `pvp`                  | Enable automatic PvP battles.                                        | `true`            |
| `proxy`                | Enable proxy usage for multi-account setups.                         | `false`           |
| `thread`               | Number of threads to run tasks concurrently.                         | `1`               |
| `delay_loop`           | Delay (in seconds) before the next loop begins.                      | `3000`            |
| `delay_account_switch` | Delay (in seconds) between switching accounts.                       | `10`              |
| `pet_mix`              | Custom configuration for pet mixing.                                 | See above         |
| `defens_type`          | Attribute for defense selection (e.g., armor, hp, speed, damage).    | `"armor"`         |
| `defens_id`            | Specific pet IDs for defense configuration.                          | `[]`              |
| `attack_type`          | Attribute for PvP attack selection (e.g., armor, hp, speed, damage). | `"damage"`        |
| `attack_id`            | Specific pet IDs for PvP attack configuration.                       | `[]`              |

---

## 📥 **How to Register**

Start using Animix by registering through the following link:

<div align="center">
  <a href="https://t.me/animix_game_bot?startapp=3lsLj56QYJx6" target="_blank">
    <img src="https://img.shields.io/static/v1?message=Animix&logo=telegram&label=&color=2CA5E0&logoColor=white&labelColor=&style=for-the-badge" height="25" alt="telegram logo" />
  </a>
</div>

---

## 📥 Installation Steps

### Main Bot Installation

1. **Clone the Repository**  
   Clone the repository to your local machine:

   ```bash
   git clone https://github.com/livexords-nw/Animix-bot.git
   ```

2. **Navigate to the Project Folder**  
   Change to the project directory:

   ```bash
   cd Animix-bot
   ```

3. **Install Dependencies**  
   Install all required libraries:

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Your Query**  
   Create a file named `query.txt` and add your Animix query data.

5. **Set Up Proxy (Optional)**  
   If you wish to use a proxy, create a `proxy.txt` file and add your proxies in the following format:

   ```
   http://username:password@ip:port
   ```

   > **Note:** Only HTTP and HTTPS proxies are supported.

6. **Run the Bot**  
   Execute the bot with the following command:
   ```bash
   python main.py
   ```

---

### 🔹 Need Free Proxies?

You can obtain free proxies from [Webshare.io](https://www.webshare.io/).
