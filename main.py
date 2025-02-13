from datetime import datetime
import json
import time
from colorama import Fore
import requests
import random

class animix:

    BASE_URL = "https://pro-api.animix.tech/public/"
    HEADERS = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en-GB,en;q=0.9,en-US;q=0.8",
        "origin": "https://tele-game.animix.tech",
        "priority": "u=1, i",
        "referer": "https://tele-game.animix.tech/",
        "sec-ch-ua": '"Microsoft Edge";v="131", "Chromium";v="131", "Not_A Brand";v="24", "Microsoft Edge WebView2";v="131"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
    }

    def __init__(self):
        self.query_list = self.load_query("query.txt")
        self.token = None
        self.token_reguler = 0
        self.token_super = 0
        self.premium_user = False
        self._original_requests = {
            "get": requests.get,
            "post": requests.post,
            "put": requests.put,
            "delete": requests.delete
        }
        self.proxy_session = None
        self.config = self.load_config()

    def banner(self) -> None:
        """Displays the banner for the bot."""
        self.log("🎉 Animix Free Bot", Fore.CYAN)
        self.log("🚀 Created by LIVEXORDS", Fore.CYAN)
        self.log("📢 Channel: t.me/livexordsscript\n", Fore.CYAN)

    def log(self, message, color=Fore.RESET):
        print(
            Fore.LIGHTBLACK_EX
            + datetime.now().strftime("[%Y:%m:%d ~ %H:%M:%S] |")
            + " "
            + color
            + message
            + Fore.RESET
        )

    def load_config(self) -> dict:
        """Loads configuration from config.json."""
        try:
            with open("config.json", "r") as config_file:
                return json.load(config_file)
        except FileNotFoundError:
            self.log("❌ File config.json not found!", Fore.RED)
            return {}
        except json.JSONDecodeError:
            self.log("❌ Error reading config.json!", Fore.RED)
            return {}

    def load_query(self, path_file="query.txt") -> list:
        self.banner()

        try:
            with open(path_file, "r") as file:
                queries = [line.strip() for line in file if line.strip()]

            if not queries:
                self.log(f"⚠️ Warning: {path_file} is empty.", Fore.YELLOW)

            self.log(f"✅ Loaded: {len(queries)} queries.", Fore.GREEN)
            return queries

        except FileNotFoundError:
            self.log(f"❌ File not found: {path_file}", Fore.RED)
            return []
        except Exception as e:
            self.log(f"❌ Error loading queries: {e}", Fore.RED)
            return []

    def login(self, index: int) -> None:
        self.log("🔐 Attempting to log in...", Fore.GREEN)

        if index >= len(self.query_list):
            self.log("❌ Invalid login index. Please check again.", Fore.RED)
            return

        req_url = f"{self.BASE_URL}user/info"
        token = self.query_list[index]

        self.log(
            f"📋 Using token: {token[:10]}... (truncated for security)",
            Fore.CYAN,
        )

        headers = {**self.HEADERS, "Tg-Init-Data": token}

        try:
            self.log(
                "📡 Sending request to fetch user information...",
                Fore.CYAN,
            )
            response = requests.get(req_url, headers=headers)
            response.raise_for_status()
            data = response.json()

            if "result" in data:
                user_info = data["result"]
                username = user_info.get("telegram_username", "Unknown")
                balance = user_info.get("token", 0)

                self.balance = (
                    int(balance)
                    if isinstance(balance, (int, str))
                    and str(balance).isdigit()
                    else 0
                )
                self.token = token
                self.premium_user = user_info.get("is_premium", False)

                self.log("✅ Login successful!", Fore.GREEN)
                self.log(f"👤 Username: {username}", Fore.LIGHTGREEN_EX)
                self.log(f"💰 Balance: {self.balance}", Fore.CYAN)

                inventory = user_info.get("inventory", [])
                token_reguler = next((item for item in inventory if item["id"] == 1), None)
                token_super = next((item for item in inventory if item["id"] == 3), None)

                if token_reguler:
                    self.log(f"💵 Regular Token: {token_reguler['amount']}", Fore.LIGHTBLUE_EX)
                    self.token_reguler = token_reguler['amount']
                else:
                    self.log(f"💵 Regular Token: 0", Fore.LIGHTBLUE_EX)

                if token_super:
                    self.log(f"💸 Super Token: {token_super['amount']}", Fore.LIGHTBLUE_EX)
                    self.token_super = token_super['amount']
                else:
                    self.log(f"💸 Super Token: 0", Fore.LIGHTBLUE_EX)

            else:
                self.log(
                    "⚠️ Unexpected response structure.", Fore.YELLOW
                )

        except requests.exceptions.RequestException as e:
            self.log(f"❌ Failed to send login request: {e}", Fore.RED)
        except ValueError as e:
            self.log(f"❌ Data error (possible JSON issue): {e}", Fore.RED)
        except KeyError as e:
            self.log(f"❌ Key error: {e}", Fore.RED)
        except Exception as e:
            self.log(f"❌ Unexpected error: {e}", Fore.RED)

    def gacha(self) -> None:
        # Main gacha process
        while True:
            if self.token_reguler > 0:
                req_url = f"{self.BASE_URL}pet/dna/gacha"
                headers = {**self.HEADERS, "Tg-Init-Data": self.token}
                payload = {"amount": 1, "is_super": False}
            elif self.token_super > 0:
                req_url = f"{self.BASE_URL}pet/dna/gacha"
                headers = {**self.HEADERS, "Tg-Init-Data": self.token}
                payload = {"amount": 1, "is_super": True}
            else:
                self.log("🚫 No gacha points remaining. Unable to continue.", Fore.RED)
                break

            self.log(
                f"🎲 Starting {'super' if payload['is_super'] else 'regular'} gacha! Remaining gacha points: {self.token_super if payload['is_super'] else self.token_reguler}",
                Fore.CYAN,
            )

            try:
                response = requests.post(req_url, headers=headers, json=payload)
                if response is None or response.status_code != 200:
                    self.log("⚠️ Gacha response is None or invalid. Skipping this attempt.", Fore.YELLOW)
                    continue

                data = response.json() if response.text else {}
                if not data:
                    self.log("⚠️ Empty or invalid JSON response for gacha.", Fore.YELLOW)
                    continue

                if "result" in data and "dna" in data["result"]:
                    dna = data["result"]["dna"]

                    if isinstance(dna, list):
                        self.log(f"🎉 You received multiple DNA items!", Fore.GREEN)
                        for dna_item in dna:
                            name = dna_item.get("name", "Unknown")
                            dna_class = dna_item.get("class", "Unknown")
                            star = dna_item.get("star", "Unknown")
                            remaining_points = str(data["result"].get("god_power", 0))

                            self.log(f"🧬 Name: {name}", Fore.LIGHTGREEN_EX)
                            self.log(f"🏷️  Class: {dna_class}", Fore.YELLOW)
                            self.log(f"⭐ Star: {star}", Fore.MAGENTA)
                            self.log(f"💎 Remaining Gacha Points: {remaining_points}", Fore.CYAN)
                            if payload['is_super']:
                                self.token_super = data['result'].get("god_power", 0)
                            else: 
                                self.token_reguler = data['result'].get("god_power", 0)
                    else:
                        name = dna.get("name", "Unknown") if dna else "Unknown"
                        dna_class = dna.get("class", "Unknown") if dna else "Unknown"
                        star = dna.get("star", "Unknown") if dna else "Unknown"
                        remaining_points = str(data["result"].get("god_power", 0))

                        self.log(f"🎉 You received a new DNA item!", Fore.GREEN)
                        self.log(f"🧬 Name: {name}", Fore.LIGHTGREEN_EX)
                        self.log(f"🏷️  Class: {dna_class}", Fore.YELLOW)
                        self.log(f"⭐ Star: {star}", Fore.MAGENTA)
                        self.log(f"💎 Remaining Gacha Points: {remaining_points}", Fore.CYAN)
                        if payload['is_super']:
                            self.token_super = data['result'].get("god_power", 0)
                        else: 
                            self.token_reguler = data['result'].get("god_power", 0)

                    self.gacha_point = (
                        int(remaining_points)
                        if isinstance(remaining_points, (int, str)) and str(remaining_points).isdigit()
                        else 0
                    )
                else:
                    self.log("⚠️ Gacha data does not match the expected structure.", Fore.RED)
                    continue

            except requests.exceptions.RequestException as e:
                self.log(f"❌ Failed to send gacha request: {e}", Fore.RED)
                continue
            except ValueError as e:
                self.log(f"❌ Data error (likely JSON): {e}", Fore.RED)
                continue
            except KeyError as e:
                self.log(f"❌ Key error: {e}", Fore.RED)
                continue
            except Exception as e:
                self.log(f"❌ Unexpected error: {e}", Fore.RED)
                continue

            time.sleep(1)
            if self.token_reguler == 0 or self.token_super == 0:
                self.log("🔄 Refreshing gacha points after spinning gacha...", Fore.CYAN)
                req_url = f"{self.BASE_URL}user/info"
                headers = {**self.HEADERS, "Tg-Init-Data": self.token}

                try:
                    response = requests.get(req_url, headers=headers)
                    response.raise_for_status()
                    data = response.json()

                    if "result" in data:
                        user_info = data["result"]
                        username = user_info.get("telegram_username", "Unknown")
                        balance = user_info.get("token", 0)

                        inventory = user_info.get("inventory", [])
                        token_reguler = next((item for item in inventory if item["id"] == 1), None)
                        token_super = next((item for item in inventory if item["id"] == 3), None)

                        if token_reguler:
                            self.log(f"💵 Regular Token: {token_reguler['amount']}", Fore.LIGHTBLUE_EX)
                            self.token_reguler = token_reguler['amount']
                        else:
                            self.log(f"💵 Regular Token: 0", Fore.LIGHTBLUE_EX)

                        if token_super:
                            self.log(f"💸 Super Token: {token_super['amount']}", Fore.LIGHTBLUE_EX)
                            self.token_super = token_super['amount']
                        else:
                            self.log(f"💸 Super Token: 0", Fore.LIGHTBLUE_EX)

                    else:
                        self.log(
                            "⚠️ Unexpected response structure.", Fore.YELLOW
                        )

                except requests.exceptions.RequestException as e:
                    self.log(f"❌ Failed to send Refresh request: {e}", Fore.RED)
                except ValueError as e:
                    self.log(f"❌ Data error (possible JSON issue): {e}", Fore.RED)
                except KeyError as e:
                    self.log(f"❌ Key error: {e}", Fore.RED)
                except Exception as e:
                    self.log(f"❌ Unexpected error: {e}", Fore.RED)
                    
        # Adding requests to the new API for bonus claims
        for reward_no in [1, 2]:
            bonus_url = f"{self.BASE_URL}pet/dna/gacha/bonus/claim"
            headers = {**self.HEADERS, "Tg-Init-Data": self.token}
            payload = {"reward_no": reward_no}

            self.log(f"🎁 Claiming bonus reward {reward_no}...", Fore.CYAN)

            try:
                response = requests.post(bonus_url, headers=headers, json=payload)
                if response is None or response.status_code != 200:
                    self.log(
                        f"⚠️ Response for bonus reward {reward_no} is None or invalid.",
                        Fore.YELLOW,
                    )
                    continue

                bonus_data = response.json() if response.text else {}
                if not bonus_data:
                    self.log(
                        f"⚠️ Empty or invalid JSON response for bonus reward {reward_no}.",
                        Fore.YELLOW,
                    )
                    continue

                if bonus_data.get("error_code") is None:
                    result = bonus_data.get("result", {})
                    name = result.get("name", "Unknown")
                    description = result.get("description", "No description")
                    amount = result.get("amount", 0)

                    self.log(f"✅ Successfully claimed bonus reward {reward_no}!", Fore.GREEN)
                    self.log(f"📦 Name: {name}", Fore.LIGHTGREEN_EX)
                    self.log(f"ℹ️ Description: {description}", Fore.YELLOW)
                    self.log(f"🔢 Amount: {amount}", Fore.MAGENTA)
                else:
                    self.log(
                        f"⚠️ Failed to claim bonus reward {reward_no}: {bonus_data.get('message', 'Unknown error')}",
                        Fore.YELLOW,
                    )
            except requests.exceptions.RequestException as e:
                self.log(f"❌ Failed to send claim request for bonus reward {reward_no}: {e}", Fore.RED)
                continue
            except ValueError as e:
                self.log(f"❌ JSON error while claiming bonus reward {reward_no}: {e}", Fore.RED)
                continue
            except Exception as e:
                self.log(f"❌ Unexpected error while claiming bonus reward {reward_no}: {e}", Fore.RED)
                continue

    def mix(self) -> None:
        """Combines DNA to create new pets based on star level and can_mom constraints."""
        req_url = f"{self.BASE_URL}pet/dna/list"
        mix_url = f"{self.BASE_URL}pet/mix"
        headers = {**self.HEADERS, "Tg-Init-Data": self.token}

        self.log("🔍 Fetching DNA list...", Fore.CYAN)

        try:
            response = requests.get(req_url, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()

            dna_list = []

            if "result" in data and isinstance(data["result"], list):
                for dna in data["result"]:
                    if dna.get("star") and dna.get("can_mom") is not None:
                        dna_list.append(dna)
                        self.log(
                            f"✅ DNA found: {dna['name']} (Star: {dna['star']}, Can Mom: {dna['can_mom']})",
                            Fore.GREEN
                        )
            else:
                self.log("⚠️ No DNA found in the response.", Fore.YELLOW)
                return

            if len(dna_list) < 2:
                self.log("❌ Not enough DNA data for mixing. At least two entries are required.", Fore.RED)
                return

            self.log(f"📋 Filtered DNA list: {[(dna['name'], dna['star'], dna['can_mom']) for dna in dna_list]}", Fore.CYAN)

            used_ids = set()
            self.log("🔄 Mixing DNA...", Fore.CYAN)

            for i, dad in enumerate(dna_list):
                if dad["item_id"] in used_ids:
                    continue

                for j, mom in enumerate(dna_list):
                    if (
                        mom["item_id"] in used_ids 
                        or dad["item_id"] == mom["item_id"] 
                        or not mom["can_mom"]
                    ):
                        continue

                    if (dad["star"] <= 5 and mom["star"] <= 5) or (dad["star"] > 5 and mom["star"] > 5):
                        payload = {"dad_id": dad["item_id"], "mom_id": mom["item_id"]}

                        while True:
                            try:
                                mix_response = requests.post(mix_url, headers=headers, json=payload, timeout=10)
                                if mix_response.status_code == 200:
                                    mix_data = mix_response.json()

                                    if "result" in mix_data and "pet" in mix_data["result"]:
                                        pet_info = mix_data["result"]["pet"]
                                        self.log(
                                            f"🎉 New pet created: {pet_info['name']} (ID: {pet_info['pet_id']})",
                                            Fore.GREEN
                                        )
                                        used_ids.add(dad["item_id"])
                                        used_ids.add(mom["item_id"])
                                        break
                                    else:
                                        message = mix_data.get("message", "No message provided.")
                                        self.log(
                                            f"⚠️ Mixing failed for Dad {dad['item_id']}, Mom {mom['item_id']}: {message}",
                                            Fore.YELLOW
                                        )
                                        break
                                elif mix_response.status_code == 429:
                                    self.log("⏳ Too many requests (429). Retrying in 5 seconds...", Fore.YELLOW)
                                    time.sleep(5)
                                else:
                                    self.log(
                                        f"❌ Request failed for Dad {dad['item_id']}, Mom {mom['item_id']} (Status: {mix_response.status_code})",
                                        Fore.RED
                                    )
                                    break
                            except requests.exceptions.RequestException as e:
                                self.log(
                                    f"❌ Request failed for Dad {dad['item_id']}, Mom {mom['item_id']}: {e}",
                                    Fore.RED
                                )
                                break

        except requests.exceptions.RequestException as e:
            self.log(f"❌ Request failed while fetching DNA list: {e}", Fore.RED)
        except ValueError as e:
            self.log(f"❌ Data error while fetching DNA list: {e}", Fore.RED)
        except Exception as e:
            self.log(f"❌ Unexpected error while fetching DNA list: {e}", Fore.RED)

    def achievements(self) -> None:
        """Handles fetching and claiming achievements."""
        req_url_list = f"{self.BASE_URL}achievement/list"
        req_url_claim = f"{self.BASE_URL}achievement/claim"
        headers = {**self.HEADERS, "tg-init-data": self.token}
        claimable_ids = []

        try:
            # Step 1: Fetch the list of achievements
            self.log("⏳ Fetching the list of achievements...", Fore.CYAN)
            response = requests.get(req_url_list, headers=headers)
            response.raise_for_status()
            data = response.json()

            if "result" in data and isinstance(data["result"], dict):
                for achievement_type, achievement_data in data["result"].items():
                    if isinstance(achievement_data, dict) and "achievements" in achievement_data:
                        self.log(f"📌 Checking achievements type: {achievement_type}", Fore.BLUE)
                        for achievement in achievement_data["achievements"]:
                            if (
                                achievement.get("status") is True
                                and achievement.get("claimed") is False
                            ):
                                claimable_ids.append(achievement.get("quest_id"))
                                self.log(
                                    f"✅ Achievement ready to claim: {achievement_data['title']} (ID: {achievement.get('quest_id')})",
                                    Fore.GREEN,
                                )

            if not claimable_ids:
                self.log("🚫 No achievements available for claiming.", Fore.YELLOW)
                return

            # Step 2: Claim each achievement found
            for quest_id in claimable_ids:
                self.log(f"🔄 Attempting to claim achievement with ID {quest_id}...", Fore.CYAN)
                response = requests.post(req_url_claim, headers=headers, json={"quest_id": quest_id})
                response.raise_for_status()
                claim_result = response.json()

                if claim_result.get("error_code") is None:
                    self.log(f"🎉 Successfully claimed achievement with ID {quest_id}!", Fore.GREEN)
                else:
                    self.log(
                        f"⚠️ Failed to claim achievement with ID {quest_id}. Message: {claim_result.get('message')}",
                        Fore.RED,
                    )

        except requests.exceptions.RequestException as e:
            self.log(f"❌ Request processing failed: {e}", Fore.RED)
        except ValueError as e:
            self.log(f"❌ Data error: {e}", Fore.RED)
        except Exception as e:
            self.log(f"❌ Unexpected error: {e}", Fore.RED)

    def mission(self) -> None:
        """List missions from API, claim finished missions, then assign pets
        using mission.json definitions for missions that are not in progress."""
        import time, json, requests

        headers = {**self.HEADERS, "Tg-Init-Data": self.token}
        current_time = int(time.time())

        try:
            # === STEP 1: Fetch mission list from API ===
            mission_url = f"{self.BASE_URL}mission/list"
            self.log("🔄 Fetching the current mission list...", Fore.CYAN)
            mission_response = requests.get(mission_url, headers=headers)
            mission_response.raise_for_status()
            mission_data = mission_response.json()
            missions = mission_data.get("result", [])
            if not isinstance(missions, list):
                self.log("❌ Invalid mission data format (expected a list).", Fore.RED)
                return

            # Siapkan set untuk mission ID yang masih in progress
            in_progress_ids = set()
            # Siapkan dictionary untuk pet yang sedang digunakan (busy)
            busy_pets = {}

            for mission in missions:
                mission_id = mission.get("mission_id")
                mission_end_time = mission.get("end_time")
                if not mission_id or not mission_end_time:
                    continue

                if current_time < mission_end_time:
                    in_progress_ids.add(mission_id)
                    # Catat pet yang sudah tergabung pada misi ini (jika ada)
                    pet_joined = mission.get("pet_joined", [])
                    if isinstance(pet_joined, list):
                        for pet_info in pet_joined:
                            pet_id = pet_info.get("pet_id")
                            if pet_id:
                                busy_pets[pet_id] = busy_pets.get(pet_id, 0) + 1
                    self.log(f"⚠️ Mission {mission_id} is still in progress.", Fore.YELLOW)
                else:
                    # Claim misi yang sudah selesai
                    claim_url = f"{self.BASE_URL}mission/claim"
                    claim_payload = {"mission_id": mission_id}
                    claim_response = requests.post(claim_url, headers=headers, json=claim_payload)
                    if claim_response.status_code == 200:
                        self.log(f"✅ Mission {mission_id} successfully claimed.", Fore.GREEN)
                    else:
                        self.log(f"❌ Failed to claim mission {mission_id} (Error: {claim_response.status_code}).", Fore.RED)
                        self.log(f"🔍 Claim response details: {claim_response.text}", Fore.RED)

            # === STEP 2: Baca definisi misi dari file lokal mission.json ===
            self.log("🔄 Reading mission definitions from mission.json...", Fore.CYAN)
            try:
                with open("mission.json", "r") as f:
                    static_data = json.load(f)
            except Exception as e:
                self.log(f"❌ Failed to read mission.json: {e}", Fore.RED)
                return

            static_missions = static_data.get("result", [])
            if not isinstance(static_missions, list):
                self.log("❌ Invalid mission.json format (expected a list).", Fore.RED)
                return

            # Buat dictionary definisi misi berdasarkan mission_id (pastikan tipe data konsisten)
            mission_defs = {str(m_def["mission_id"]): m_def for m_def in static_missions}

            # === STEP 3: Fetch pet list from API untuk assignment ===
            pet_url = f"{self.BASE_URL}pet/list"
            self.log("🔄 Fetching the list of pets...", Fore.CYAN)
            pet_response = requests.get(pet_url, headers=headers)
            pet_response.raise_for_status()
            pet_data = pet_response.json()
            pets = pet_data.get("result", [])
            if not isinstance(pets, list):
                self.log("❌ Invalid pet data format (expected a list).", Fore.RED)
                return
            self.log("✅ Successfully fetched the list of pets.", Fore.GREEN)

            # === STEP 4: Assignment pet untuk misi yang TIDAK in progress ===
            self.log("🔍 Filtering missions for pet assignment...", Fore.CYAN)
            for mission_def in static_missions:
                mission_id = str(mission_def.get("mission_id"))
                # Lewati misi yang masih in progress (belum waktunya claim)
                if mission_id in in_progress_ids:
                    self.log(f"⚠️ Mission {mission_id} skipped (still in progress).", Fore.YELLOW)
                    continue

                # Bangun daftar requirement pet dari mission.json
                required_pets = []
                for i in range(1, 4):
                    pet_class = mission_def.get(f"pet_{i}_class")
                    pet_star = mission_def.get(f"pet_{i}_star")
                    if pet_class is not None and pet_star is not None:
                        required_pets.append({"class": pet_class, "star": pet_star})

                # Lakukan assignment jika misi belum memiliki pet (diasumsikan setelah claim, pet_joined kosong)
                # Jika ternyata pet sudah pernah diassign, kamu bisa menambahkan pengecekan tambahan di sini.
                while True:
                    # Filter pet yang masih memiliki slot penggunaan (amount)
                    available_pets = [
                        pet for pet in pets
                        if busy_pets.get(pet.get("pet_id"), 0) < pet.get("amount", 1)
                    ]
                    pet_ids = []
                    # Cari pet yang sesuai untuk tiap requirement (EXACT match)
                    for req in required_pets:
                        for pet in available_pets:
                            if (
                                pet.get("class") == req["class"]
                                and pet.get("star", 0) == req["star"]
                                and pet.get("pet_id") not in pet_ids
                            ):
                                pet_ids.append(pet["pet_id"])
                                available_pets.remove(pet)
                                break

                    if len(pet_ids) == 3:
                        self.log(f"➡️ Assigning pets to mission {mission_id}...", Fore.CYAN)
                        enter_url = f"{self.BASE_URL}mission/enter"
                        payload = {"mission_id": mission_id}
                        for i, pet_id in enumerate(pet_ids):
                            payload[f"pet_{i+1}_id"] = pet_id
                        enter_response = requests.post(enter_url, headers=headers, json=payload)
                        if enter_response.status_code == 200:
                            self.log(f"✅ Mission {mission_id} successfully started.", Fore.GREEN)
                            # Update busy_pets untuk pet yang telah digunakan
                            for pet_id in pet_ids:
                                busy_pets[pet_id] = busy_pets.get(pet_id, 0) + 1
                            break
                        else:
                            self.log(f"❌ Failed to start mission {mission_id} (Error: {enter_response.status_code}).", Fore.RED)
                            self.log(f"🔍 Mission start response details: {enter_response.text}", Fore.RED)
                            if "PET_BUSY" in enter_response.text:
                                self.log(f"🔄 Retrying with different pets for mission {mission_id}...", Fore.YELLOW)
                                continue
                            else:
                                break
                    else:
                        self.log(f"❌ Mission {mission_id} does not meet pet requirements.", Fore.RED)
                        break

        except requests.exceptions.RequestException as e:
            self.log(f"❌ An error occurred while processing: {e}", Fore.RED)

    def quest(self) -> None:
        """Handles fetching and claiming quests."""
        headers = {**self.HEADERS, "Tg-Init-Data": self.token}

        try:
            # Step 1: Fetch the list of quests
            quest_url = f"{self.BASE_URL}quest/list"
            self.log("🔄 Fetching the list of quests...", Fore.CYAN)
            quest_response = requests.get(quest_url, headers=headers)
            quest_response.raise_for_status()

            try:
                quest_data = quest_response.json()
            except ValueError:
                self.log("❌ Quest response is not valid JSON.", Fore.RED)
                return

            quests = quest_data.get("result", {}).get("quests", [])
            if not quests:
                self.log("⚠️ No quests available.", Fore.YELLOW)
                return

            self.log("✅ Successfully fetched the list of quests.", Fore.GREEN)

            # Step 2: Process each quest
            for quest in quests:
                if (
                    quest.get("is_disabled")
                    or quest.get("is_deleted")
                    or quest.get("status")
                ):
                    self.log(
                        f"⚠️ Quest {quest.get('quest_code')} skipped (disabled/deleted/completed).",
                        Fore.YELLOW,
                    )
                    continue

                quest_code = quest.get("quest_code")
                self.log(
                    f"➡️ Checking or claiming quest {quest_code}...",
                    Fore.CYAN,
                )

                # Step 3: Claim the quest
                check_url = f"{self.BASE_URL}quest/check"
                payload = {"quest_code": quest_code}
                check_response = requests.post(check_url, headers=headers, json=payload)

                if check_response.status_code == 200:
                    self.log(f"✅ Quest {quest_code} successfully claimed.", Fore.GREEN)
                else:
                    self.log(
                        f"❌ Failed to claim quest {quest_code} (Error: {check_response.status_code}).",
                        Fore.RED,
                    )
                    self.log(f"🔍 Claim response details: {check_response.text}", Fore.RED)

        except requests.exceptions.RequestException as e:
            self.log(f"❌ An error occurred while processing quests: {e}", Fore.RED)

    def claim_pass(self) -> None:
        """Handles claiming rewards from season passes."""
        headers = {**self.HEADERS, "Tg-Init-Data": self.token}

        try:
            # Step 1: Fetch the list of season passes
            pass_url = f"{self.BASE_URL}season-pass/list"
            self.log("🔄 Fetching the list of season passes...", Fore.CYAN)
            pass_response = requests.get(pass_url, headers=headers)
            pass_response.raise_for_status()

            try:
                passes = pass_response.json().get("result", [])
            except ValueError:
                self.log("❌ Season pass response is not valid JSON.", Fore.RED)
                return

            if not passes:
                self.log("⚠️ No season passes available.", Fore.YELLOW)
                return

            self.log("✅ Successfully fetched the list of season passes.", Fore.GREEN)

            # Step 2: Process each season pass
            for season in passes:
                season_id = season.get("season_id")
                try:
                    current_step = int(season.get("current_step", 0))
                except ValueError:
                    self.log(
                        f"❌ Invalid `current_step` value for season {season_id}, skipping this season.",
                        Fore.RED,
                    )
                    continue

                # Step 3: Claim free rewards
                free_rewards = season.get("free_rewards", [])
                for reward in free_rewards:
                    step = reward.get("step")
                    is_claimed = reward.get("is_claimed", True)

                    try:
                        step = int(step)
                    except (ValueError, TypeError):
                        self.log(
                            f"❌ Invalid `step` value for free reward in season {season_id}, skipping this reward.",
                            Fore.RED,
                        )
                        continue

                    if not is_claimed and step <= current_step:
                        self.log(
                            f"➡️ Claiming free reward for season {season_id}, step {step}...",
                            Fore.CYAN,
                        )

                        claim_url = f"{self.BASE_URL}season-pass/claim"
                        payload = {"season_id": season_id, "step": step, "type": "free"}
                        claim_response = requests.post(
                            claim_url, headers=headers, json=payload
                        )

                        if claim_response.status_code == 200:
                            self.log(
                                f"✅ Successfully claimed free reward at step {step}.",
                                Fore.GREEN,
                            )
                        else:
                            self.log(
                                f"❌ Failed to claim reward at step {step} (Error: {claim_response.status_code}).",
                                Fore.RED,
                            )

                # Step 4: Claim premium rewards if the user is premium
                if getattr(self, "premium_user", False):
                    premium_rewards = season.get("premium_rewards", [])
                    for reward in premium_rewards:
                        step = reward.get("step")
                        is_claimed = reward.get("is_claimed", True)

                        try:
                            step = int(step)
                        except (ValueError, TypeError):
                            self.log(
                                f"❌ Invalid `step` value for premium reward in season {season_id}, skipping this reward.",
                                Fore.RED,
                            )
                            continue

                        if not is_claimed and step <= current_step:
                            self.log(
                                f"➡️ Claiming premium reward for season {season_id}, step {step}...",
                                Fore.CYAN,
                            )

                            claim_url = f"{self.BASE_URL}season-pass/claim"
                            payload = {
                                "season_id": season_id,
                                "step": step,
                                "type": "premium",
                            }
                            claim_response = requests.post(
                                claim_url, headers=headers, json=payload
                            )

                            if claim_response.status_code == 200:
                                self.log(
                                    f"✅ Successfully claimed premium reward at step {step}.",
                                    Fore.GREEN,
                                )
                            else:
                                self.log(
                                    f"❌ Failed to claim reward at step {step} (Error: {claim_response.status_code}).",
                                    Fore.RED,
                                )

        except requests.exceptions.RequestException as e:
            self.log(f"❌ An error occurred while processing season passes: {e}", Fore.RED)

    def upgrade_pets(self, req_url_pets: str, req_url_upgrade_check: str, req_url_upgrade: str, headers: dict) -> None:
        """
        Mengecek dan meng-upgrade pet yang memenuhi syarat.
        Fungsi ini akan terus melakukan pengecekan ulang selama terdapat pet yang diupgrade.
        """
        upgraded_any = True
        while upgraded_any:
            upgraded_any = False
            self.log("⚙️ Checking for pets eligible for upgrade...", Fore.CYAN)
            response = requests.get(req_url_pets, headers=headers)
            response.raise_for_status()
            pets_data = response.json()
            
            if "result" in pets_data and isinstance(pets_data["result"], list):
                pets = pets_data["result"]
                for pet in pets:
                    # Cek pet dengan star minimal 4 dan amount lebih dari 1
                    if pet.get("star", 0) >= 4 and pet.get("amount", 0) > 1:
                        pet_id = pet.get("pet_id")
                        payload = {"pet_id": pet_id}
                        # Cek kelengkapan upgrade untuk pet tersebut
                        response = requests.get(f"{req_url_upgrade_check}?pet_id={pet_id}", headers=headers, json=payload)
                        response.raise_for_status()
                        upgrade_data = response.json()
                        
                        if "result" in upgrade_data and isinstance(upgrade_data["result"], dict):
                            # Ambil data requirement dan material (diasumsikan dalam list dan ambil elemen pertama)
                            required = upgrade_data["result"].get("required", [])[0]
                            materials = upgrade_data["result"].get("materials", [])[0]
                            
                            if (required["available"] >= required["amount"] and
                                materials["available"] >= materials["amount"]):
                                
                                self.log(f"🔧 Upgrading pet ID {pet_id}...", Fore.CYAN)
                                response = requests.post(req_url_upgrade, headers=headers, json=payload)
                                response.raise_for_status()
                                upgrade_result = response.json()
                                
                                if ("result" in upgrade_result and 
                                    upgrade_result["result"].get("status", False)):
                                    new_level = upgrade_result["result"].get("level")
                                    self.log(f"✅ Pet ID {pet_id} upgraded to Level {new_level}", Fore.GREEN)
                                    upgraded_any = True
                                else:
                                    self.log(f"🚫 Failed to upgrade pet ID {pet_id}", Fore.RED)
            else:
                self.log("🚫 No pets found for upgrade check.", Fore.RED)

    def pvp(self) -> None:
        """Handles fetching and displaying PvP user information."""
        req_url_info = f"{self.BASE_URL}battle/user/info"
        req_url_opponents = f"{self.BASE_URL}battle/user/opponents"
        req_url_pets = f"{self.BASE_URL}pet/list"
        req_url_attack = f"{self.BASE_URL}battle/attack"
        req_url_set_defense = f"{self.BASE_URL}battle/user/defense-team"
        req_url_upgrade_check = f"{self.BASE_URL}battle/pet/level-up/required"
        req_url_upgrade = f"{self.BASE_URL}battle/pet/level-up"
        headers = {**self.HEADERS, "tg-init-data": self.token}

        # === Upgrade Pets di luar loop PvP ===
        try:
            self.upgrade_pets(req_url_pets, req_url_upgrade_check, req_url_upgrade, headers)
        except requests.exceptions.RequestException as e:
            self.log(f"❌ Upgrade process failed: {e}", Fore.RED)
        except Exception as e:
            self.log(f"❌ Unexpected error during upgrade: {e}", Fore.RED)

        try:
            while True:
                # Step 1: Fetch PvP user info
                self.log("⏳ Fetching PvP user information...", Fore.CYAN)
                response = requests.get(req_url_info, headers=headers)
                response.raise_for_status()
                data = response.json()

                if "result" in data and isinstance(data["result"], dict):
                    result = data["result"]

                    # Extracting important details
                    season_id = result.get("season_id", "N/A")
                    tier_name = result.get("tier_name", "N/A")
                    tier = result.get("tier", "N/A")
                    score = result.get("score", 0)
                    matches = result.get("match", 0)
                    win_matches = result.get("win_match", 0)
                    tickets = result.get("ticket", {}).get("amount", 0)
                    defense_team = result.get("defense_team", [])

                    # Logging the extracted details
                    self.log(f"🌟 Season ID: {season_id}", Fore.GREEN)
                    self.log(f"🏆 Tier: {tier_name} (Level {tier})", Fore.GREEN)
                    self.log(f"📊 Score: {score}", Fore.GREEN)
                    self.log(f"⚔️ Matches Played: {matches} | Wins: {win_matches}", Fore.GREEN)
                    self.log(f"🎟️ Tickets Available: {tickets}", Fore.GREEN)

                    if tickets <= 0:
                        self.log("🎟️ No tickets remaining. PvP session ending.", Fore.YELLOW)
                        break

                    if defense_team:
                        self.log("🛡️ Defense Team:", Fore.BLUE)
                        for idx, pet in enumerate(defense_team, start=1):
                            pet_id = pet.get("pet_id", "Unknown")
                            level = pet.get("level", 0)
                            self.log(f"   {idx}. Pet ID: {pet_id} | Level: {level}", Fore.BLUE)
                    else:
                        self.log("🛡️ Defense Team: None", Fore.YELLOW)

                    # Step 2: Fetch user's pet list (tanpa upgrade, karena sudah dilakukan di luar loop)
                    self.log("🔍 Fetching user pet list...", Fore.CYAN)
                    response = requests.get(req_url_pets, headers=headers)
                    response.raise_for_status()
                    pets_data = response.json()

                    best_pets = []
                    if "result" in pets_data and isinstance(pets_data["result"], list):
                        pets = pets_data["result"]

                        # Step 2.2: Determine the 3 best pets based on total attribute scores
                        best_pets = sorted(
                            pets,
                            key=lambda pet: (
                                pet.get("hp", 0) +
                                pet.get("damage", 0) +
                                pet.get("speed", 0) +
                                pet.get("armor", 0)
                            ),
                            reverse=True
                        )[:3]

                        if best_pets:
                            self.log("🐾 Best Pets Found:", Fore.GREEN)
                            for idx, pet in enumerate(best_pets, start=1):
                                pet_id = pet.get("pet_id", "Unknown")
                                name = pet.get("name", "Unknown")
                                hp = pet.get("hp", 0)
                                damage = pet.get("damage", 0)
                                speed = pet.get("speed", 0)
                                armor = pet.get("armor", 0)

                                self.log(
                                    f"   {idx}. {name} (ID: {pet_id}) - "
                                    f"HP: {hp}, Damage: {damage}, Speed: {speed}, Armor: {armor}",
                                    Fore.GREEN
                                )

                            # Step 2.3: Set Defense Team using the best pets
                            self.log("🛡️ Setting defense team with the best pets...", Fore.CYAN)
                            payload = {
                                "pet_id_1": best_pets[0].get("pet_id"),
                                "pet_id_2": best_pets[1].get("pet_id"),
                                "pet_id_3": best_pets[2].get("pet_id")
                            }

                            response = requests.post(req_url_set_defense, headers=headers, json=payload)
                            response.raise_for_status()
                            defense_result = response.json()

                            if "result" in defense_result and isinstance(defense_result["result"], dict):
                                self.log("✅ Defense team successfully updated!", Fore.GREEN)
                            else:
                                self.log("🚫 Failed to update defense team.", Fore.RED)
                        else:
                            self.log("🚫 No pets found in the list.", Fore.RED)
                    else:
                        self.log("🚫 Failed to fetch pet list properly.", Fore.RED)

                    # Step 3: If tickets are available, fetch opponent information
                    if tickets > 0:
                        self.log("🎯 Tickets available. Fetching opponent information...", Fore.CYAN)
                        response = requests.get(req_url_opponents, headers=headers)
                        response.raise_for_status()
                        opponent_data = response.json()

                        if "result" in opponent_data and isinstance(opponent_data["result"], dict):
                            opponent = opponent_data["result"].get("opponent", {})

                            # Extract opponent details
                            opponent_id = opponent.get("telegram_id", "Unknown")
                            opponent_name = opponent.get("full_name", "Unknown")
                            opponent_username = opponent.get("telegram_username", "Unknown")
                            opponent_score = opponent.get("score", 0)
                            opponent_pets = opponent.get("pets", [])

                            # Log opponent details
                            self.log(f"🎮 Opponent Found: {opponent_name} (@{opponent_username}) id: {opponent_id}", Fore.MAGENTA)
                            self.log(f"📊 Opponent Score: {opponent_score}", Fore.MAGENTA)

                            if opponent_pets:
                                self.log("🐾 Opponent's Pets:", Fore.BLUE)
                                for idx, pet in enumerate(opponent_pets, start=1):
                                    pet_id = pet.get("pet_id", "Unknown")
                                    level = pet.get("level", 0)
                                    self.log(f"   {idx}. Pet ID: {pet_id} | Level: {level}", Fore.BLUE)
                            else:
                                self.log("🐾 Opponent's Pets: None", Fore.YELLOW)

                            # Step 4: Execute attack if opponent and best pets are available
                            if opponent_id != "Unknown" and len(best_pets) == 3:
                                self.log("⚔️ Executing attack...", Fore.CYAN)
                                payload = {
                                    "opponent_id": opponent_id,
                                    "pet_id_1": best_pets[0].get("pet_id"),
                                    "pet_id_2": best_pets[1].get("pet_id"),
                                    "pet_id_3": best_pets[2].get("pet_id")
                                }
                                response = requests.post(req_url_attack, headers=headers, json=payload)
                                response.raise_for_status()
                                attack_result = response.json()

                                if "result" in attack_result and isinstance(attack_result["result"], dict):
                                    result = attack_result["result"]
                                    is_win = result.get("is_win", False)
                                    score_gained = result.get("score", 0)
                                    tickets = result.get("ticket", {}).get("amount", 0)

                                    self.log("🏅 Attack Results:", Fore.GREEN)
                                    for idx, round_info in enumerate(result.get("rounds", []), start=1):
                                        attacker_id = round_info.get("attacker_pet_id", "Unknown")
                                        defender_id = round_info.get("defender_pet_id", "Unknown")
                                        round_result = "Win" if round_info.get("result", False) else "Lose"
                                        self.log(f"   Round {idx}: Attacker {attacker_id} vs Defender {defender_id} - {round_result}", Fore.GREEN)

                                    if is_win:
                                        self.log(f"🎉 Victory! Gained Score: {score_gained}", Fore.GREEN)
                                    else:
                                        self.log("💔 Defeat!", Fore.RED)
                                    self.log(f"🎟️ Tickets Remaining: {tickets}", Fore.GREEN)

                                    if tickets <= 0:
                                        self.log("🎟️ No tickets remaining. PvP session ending.", Fore.YELLOW)
                                        break
                                else:
                                    self.log("🚫 Failed to process attack results.", Fore.RED)
                        else:
                            self.log("🚫 Failed to fetch opponent information.", Fore.RED)

                else:
                    self.log("🚫 Failed to retrieve PvP information. No result found.", Fore.RED)

        except requests.exceptions.RequestException as e:
            self.log(f"❌ Request processing failed: {e}", Fore.RED)
        except ValueError as e:
            self.log(f"❌ Data error: {e}", Fore.RED)
        except Exception as e:
            self.log(f"❌ Unexpected error: {e}", Fore.RED)

    def load_proxies(self, filename="proxy.txt"):
        """
        Reads proxies from a file and returns them as a list.
        
        Args:
            filename (str): The path to the proxy file.
        
        Returns:
            list: A list of proxy addresses.
        """
        try:
            with open(filename, "r", encoding="utf-8") as file:
                proxies = [line.strip() for line in file if line.strip()]
            if not proxies:
                raise ValueError("Proxy file is empty.")
            return proxies
        except Exception as e:
            self.log(f"❌ Failed to load proxies: {e}", Fore.RED)
            return []

    def set_proxy_session(self, proxies: list) -> requests.Session:
        """
        Creates a requests session with a working proxy from the given list.
        
        If a chosen proxy fails the connectivity test, it will try another proxy
        until a working one is found. If no proxies work or the list is empty, it
        will return a session with a direct connection.

        Args:
            proxies (list): A list of proxy addresses (e.g., "http://proxy_address:port").
        
        Returns:
            requests.Session: A session object configured with a working proxy,
                            or a direct connection if none are available.
        """
        # If no proxies are provided, use a direct connection.
        if not proxies:
            self.log("⚠️ No proxies available. Using direct connection.", Fore.YELLOW)
            self.proxy_session = requests.Session()
            return self.proxy_session

        # Copy the list so that we can modify it without affecting the original.
        available_proxies = proxies.copy()

        while available_proxies:
            proxy_url = random.choice(available_proxies)
            self.proxy_session = requests.Session()
            self.proxy_session.proxies = {"http": proxy_url, "https": proxy_url}

            try:
                test_url = "https://httpbin.org/ip"
                response = self.proxy_session.get(test_url, timeout=5)
                response.raise_for_status()
                origin_ip = response.json().get("origin", "Unknown IP")
                self.log(f"✅ Using Proxy: {proxy_url} | Your IP: {origin_ip}", Fore.GREEN)
                return self.proxy_session
            except requests.RequestException as e:
                self.log(f"❌ Proxy failed: {proxy_url} | Error: {e}", Fore.RED)
                # Remove the failed proxy and try again.
                available_proxies.remove(proxy_url)
        
        # If none of the proxies worked, use a direct connection.
        self.log("⚠️ All proxies failed. Using direct connection.", Fore.YELLOW)
        self.proxy_session = requests.Session()
        return self.proxy_session
    
    def override_requests(self):
        """Override requests functions globally when proxy is enabled."""
        if self.config.get("proxy", False):
            self.log("[CONFIG] 🛡️ Proxy: ✅ Enabled", Fore.YELLOW)
            proxies = self.load_proxies()
            self.set_proxy_session(proxies)

            # Override request methods
            requests.get = self.proxy_session.get
            requests.post = self.proxy_session.post
            requests.put = self.proxy_session.put
            requests.delete = self.proxy_session.delete
        else:
            self.log("[CONFIG] proxy: ❌ Disabled", Fore.RED)
            # Restore original functions if proxy is disabled
            requests.get = self._original_requests["get"]
            requests.post = self._original_requests["post"]
            requests.put = self._original_requests["put"]
            requests.delete = self._original_requests["delete"]

if __name__ == "__main__":
    ani = animix()
    index = 0
    max_index = len(ani.query_list)
    config = ani.load_config()
    if config.get("proxy", False):
        proxies = ani.load_proxies()

    ani.log("🎉 [LIVEXORDS] === Welcome to AniMix Automation === [LIVEXORDS]", Fore.YELLOW)
    ani.log(f"📂 Loaded {max_index} accounts from query list.", Fore.YELLOW)

    while True:
        # Format current_account: Show only the first 10 characters, rest hidden
        current_account = ani.query_list[index]
        display_account = current_account[:10] + "..." if len(current_account) > 10 else current_account

        ani.log(f"👤 [ACCOUNT] Processing account {index + 1}/{max_index}: {display_account}", Fore.YELLOW)

        if config.get("proxy", False):
            ani.override_requests()
        else:
            ani.log("[CONFIG] Proxy: ❌ Disabled", Fore.RED)

        # Perform login for the current account
        ani.login(index)

        # Task execution with clear log messages
        ani.log("🛠️ Starting task execution...")
        tasks = {
            "achievements": "🏆 Achievements",
            "mission": "📜 Missions",
            "quest": "🗺️ Quests",
            "gacha": "🎰 Gacha",
            "mix": "🧬 DNA Mixing",
            "claim_pass": "🎟️ Claiming Pass Rewards",
            "pvp": "⚔️ PvP Battles",
        }

        for task_key, task_name in tasks.items():
            task_status = config.get(task_key, False)
            ani.log(f"[CONFIG] {task_name}: {'✅ Enabled' if task_status else '❌ Disabled'}", Fore.YELLOW if task_status else Fore.RED)

            if task_status:
                ani.log(f"🔄 Executing {task_name}...")
                getattr(ani, task_key)()

        # Handle account switching and loop delay
        if index == max_index - 1:
            ani.log("🔁 All accounts processed. Restarting loop.")
            ani.log(f"⏳ Sleeping for {config.get('delay_loop', 30)} seconds before restarting.")
            time.sleep(config.get("delay_loop", 30))
            index = 0
        else:
            ani.log(f"➡️ Switching to the next account in {config.get('delay_account_switch', 10)} seconds.")
            time.sleep(config.get("delay_account_switch", 10))
            index += 1