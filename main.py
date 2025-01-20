from datetime import datetime
import json
import time
from colorama import Fore
import requests

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

    def mix(self) -> None:
        """Combines DNA to create new pets without delay and ensuring unique DNA usage."""
        req_url = f"{self.BASE_URL}pet/dna/list/all"
        mix_url = f"{self.BASE_URL}pet/mix"
        headers = {**self.HEADERS, "Tg-Init-Data": self.token}

        self.log("🔍 Fetching DNA list...", Fore.CYAN)

        try:
            response = requests.get(req_url, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()

            dna_ids = []

            if "result" in data and isinstance(data["result"], list):
                for dna in data["result"]:
                    dna_id = dna.get("dna_id")
                    if dna_id:
                        dna_ids.append(dna_id)
                        self.log(f"✅ DNA found: {dna['name']} (ID: {dna_id})", Fore.GREEN)
            else:
                self.log("⚠️ No DNA found in the response.", Fore.YELLOW)
                return

            if len(dna_ids) < 2:
                self.log("❌ Not enough DNA data for mixing. At least two IDs are required.", Fore.RED)
                return

            self.log(f"📋 DNA IDs: {dna_ids}", Fore.CYAN)

            used_ids = set()

            self.log("🔄 Mixing DNA...", Fore.CYAN)
            for i, dad_id in enumerate(dna_ids):
                if dad_id in used_ids:
                    continue
                for j, mom_id in enumerate(dna_ids):
                    if mom_id in used_ids or dad_id == mom_id:
                        continue

                    payload = {"dad_id": dad_id, "mom_id": mom_id}
                    while True:
                        try:
                            mix_response = requests.post(mix_url, headers=headers, json=payload, timeout=10)
                            if mix_response.status_code == 200:
                                mix_data = mix_response.json()

                                if "result" in mix_data and "pet" in mix_data["result"]:
                                    pet_info = mix_data["result"]["pet"]
                                    self.log(f"🎉 New pet created: {pet_info['name']} (ID: {pet_info['pet_id']})", Fore.GREEN)
                                    # Mark the IDs as used
                                    used_ids.add(dad_id)
                                    used_ids.add(mom_id)
                                    break
                                else:
                                    message = mix_data.get("message", "No message provided.")
                                    self.log(f"⚠️ Mixing failed for Dad {dad_id}, Mom {mom_id}: {message}", Fore.YELLOW)
                                    break
                            elif mix_response.status_code == 429:
                                self.log("⏳ Too many requests (429). Retrying in 5 seconds...", Fore.YELLOW)
                                time.sleep(5)
                            else:
                                self.log(f"❌ Request failed for Dad {dad_id}, Mom {mom_id} (Status: {mix_response.status_code})", Fore.RED)
                                break
                        except requests.exceptions.RequestException as e:
                            self.log(f"❌ Request failed for Dad {dad_id}, Mom {mom_id}: {e}", Fore.RED)
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
        """Handles fetching and completing missions."""
        headers = {**self.HEADERS, "Tg-Init-Data": self.token}

        try:
            # Step 1: Fetch the list of missions
            mission_url = f"{self.BASE_URL}mission/list"
            self.log("🔄 Fetching the list of missions...", Fore.CYAN)
            mission_response = requests.get(mission_url, headers=headers)
            mission_response.raise_for_status()

            try:
                mission_data = mission_response.json()
            except ValueError:
                self.log("❌ Mission response is not valid JSON.", Fore.RED)
                return

            missions = mission_data.get("result", [])
            if not isinstance(missions, list):
                self.log("❌ Invalid mission data format (expected a list).", Fore.RED)
                return

            self.log("✅ Successfully fetched the list of missions.", Fore.GREEN)

            # Step 2: Fetch the list of pets
            pet_url = f"{self.BASE_URL}pet/list"
            self.log("🔄 Fetching the list of pets...", Fore.CYAN)
            pet_response = requests.get(pet_url, headers=headers)
            pet_response.raise_for_status()

            try:
                pet_data = pet_response.json()
            except ValueError:
                self.log("❌ Pet response is not valid JSON.", Fore.RED)
                return

            pets = pet_data.get("result", [])
            if not isinstance(pets, list):
                self.log("❌ Invalid pet data format (expected a list).", Fore.RED)
                return

            self.log("✅ Successfully fetched the list of pets.", Fore.GREEN)

            # Step 3: Claim available missions
            self.log("🔍 Claiming all available missions...", Fore.CYAN)
            for mission in missions:
                if (
                    mission.get("is_disabled")
                    or mission.get("is_deleted")
                    or mission.get("status")
                ):
                    self.log(
                        f"⚠️ Mission {mission.get('mission_id')} skipped (disabled/deleted/already completed).",
                        Fore.YELLOW,
                    )
                    continue

                claim_url = f"{self.BASE_URL}mission/claim"
                claim_payload = {"mission_id": mission.get("mission_id")}
                claim_response = requests.post(claim_url, headers=headers, json=claim_payload)

                if claim_response.status_code == 200:
                    self.log(
                        f"✅ Mission {mission.get('mission_id')} successfully claimed.",
                        Fore.GREEN,
                    )
                else:
                    self.log(
                        f"❌ Failed to claim mission {mission.get('mission_id')} (Error: {claim_response.status_code}).",
                        Fore.RED,
                    )
                    self.log(f"🔍 Claim response details: {claim_response.text}", Fore.RED)

            # Step 4: Send pets to complete eligible missions
            self.log("🔍 Filtering missions and assigning pets...", Fore.CYAN)
            for mission in missions:
                if (
                    mission.get("is_disabled")
                    or mission.get("is_deleted")
                    or mission.get("status")
                ):
                    self.log(
                        f"⚠️ Mission {mission.get('mission_id')} skipped (disabled/deleted/already completed).",
                        Fore.YELLOW,
                    )
                    continue

                required_pets = [
                    {
                        "class": mission.get(f"pet_{i}_class"),
                        "star": mission.get(f"pet_{i}_star"),
                    }
                    for i in range(1, 4)
                ]

                available_pets = pets.copy()
                while True:
                    pet_ids = []
                    for req in required_pets:
                        for pet in available_pets:
                            if (
                                pet.get("class") == req["class"]
                                and pet.get("star", 0) >= req["star"]
                                and pet.get("id") not in pet_ids
                            ):
                                pet_ids.append(pet["pet_id"])
                                available_pets.remove(pet)
                                break

                    if len(pet_ids) == 3:
                        self.log(
                            f"➡️ Assigning pets to mission {mission.get('mission_id')}...",
                            Fore.CYAN,
                        )

                        enter_url = f"{self.BASE_URL}mission/enter"
                        payload = {
                            "mission_id": mission.get("mission_id"),
                            **{f"pet_{i+1}_id": pet_id for i, pet_id in enumerate(pet_ids)},
                        }
                        enter_response = requests.post(enter_url, headers=headers, json=payload)

                        if enter_response.status_code == 200:
                            self.log(
                                f"✅ Mission {mission.get('mission_id')} successfully started.",
                                Fore.GREEN,
                            )
                            break
                        else:
                            self.log(
                                f"❌ Failed to start mission {mission.get('mission_id')} (Error: {enter_response.status_code}).",
                                Fore.RED,
                            )
                            self.log(
                                f"🔍 Mission start response details: {enter_response.text}",
                                Fore.RED,
                            )

                            if "PET_BUSY" in enter_response.text:
                                self.log(
                                    f"🔄 Retrying with different pets for mission {mission.get('mission_id')}...",
                                    Fore.YELLOW,
                                )
                                continue
                            else:
                                break
                    else:
                        self.log(
                            f"❌ Mission {mission.get('mission_id')} does not meet pet requirements.",
                            Fore.RED,
                        )
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

                # Step 4: Claim premium rewards
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

if __name__ == "__main__":
    ani = animix()
    index = 0
    max_index = len(ani.query_list)
    config = ani.load_config()

    ani.log("🎉 [LIVEXORDS] === Welcome to AniMix Automation === [LIVEXORDS]", Fore.YELLOW)
    ani.log(f"📂 Loaded {max_index} accounts from query list.", Fore.YELLOW)

    while True:
        # Format current_account: Show only the first 10 characters, rest hidden
        current_account = ani.query_list[index]
        display_account = current_account[:10] + "..." if len(current_account) > 10 else current_account

        ani.log(f"👤 [ACCOUNT] Processing account {index + 1}/{max_index}: {display_account}", Fore.YELLOW)

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