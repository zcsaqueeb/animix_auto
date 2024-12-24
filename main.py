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
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0" 
    }
    
    def __init__(self):
        self.query_list = self.load_query("query.txt")
        self.token = None
        self.gacha_point = 0

    def banner(self):
            print("     Animix Free Bot")
            print("     This Bot Created By LIVEXORDS\n")
            print("     Channel: t.me/livexordsscript")

    def log(self, message, color=Fore.RESET):
            print(Fore.LIGHTBLACK_EX + datetime.now().strftime("[%Y:%m:%d:%H:%M:%S] |") + " " + color + message + Fore.RESET)

    def load_config(self):
            """Membaca konfigurasi dari file config.json"""
            try:
                with open("config.json", "r") as config_file:
                    config_data = json.load(config_file)
                    return config_data
            except FileNotFoundError:
                print("File config.json tidak ditemukan!")
                return {}
            except json.JSONDecodeError:
                print("Terjadi kesalahan dalam membaca config.json!")
                return {}

    def load_query(self, path_file="query.txt"):
            self.banner()
            
            try:
                with open(path_file, 'r') as file:
                    queries = [line.strip() for line in file if line.strip()]    
                
                if not queries:
                    self.log(f"Warning: {path_file} is empty.", Fore.YELLOW)
                
                self.log(f"Data Load : {len(queries)} queries loaded.", Fore.GREEN)
                return queries

            except FileNotFoundError:
                self.log(f"File not found: {path_file}", Fore.RED)
                return []
            except Exception as e:
                self.log(f"Error while loading queries from file: {e}", Fore.RED)
                return []

    def login(self, index: int) -> None:
        self.log("🔐 Mencoba login...", Fore.GREEN)

        if index >= len(self.query_list):
            self.log("❌ Indeks login tidak valid. Silakan cek kembali.", Fore.RED)
            return

        req_url = f"{self.BASE_URL}user/info"
        token = self.query_list[index]

        self.log(f"📋 Token yang digunakan: {token[:10]}... (dipotong untuk keamanan)", Fore.CYAN)

        headers = {**self.HEADERS, "Tg-Init-Data": token}

        try:
            self.log("📡 Mengirim permintaan untuk mendapatkan informasi pengguna...", Fore.CYAN)
            response = requests.get(req_url, headers=headers)
            response.raise_for_status()
            data = response.json()

            if "result" in data:
                user_info = data["result"]
                username = user_info.get("telegram_username", "Tidak diketahui")
                gacha_point = user_info.get("god_power", 0)

                self.gacha_point = int(gacha_point) if isinstance(gacha_point, (int, str)) and str(gacha_point).isdigit() else 0
                self.token = token

                self.log("✅ Login berhasil!", Fore.GREEN)
                self.log(f"👤 Username: {username}", Fore.LIGHTGREEN_EX)
                self.log(f"💎 Point Gacha: {self.gacha_point}", Fore.CYAN)
            else:
                self.log("⚠️ Respons tidak sesuai struktur yang diharapkan.", Fore.YELLOW)

        except requests.exceptions.RequestException as e:
            self.log(f"❌ Gagal mengirim permintaan login: {e}", Fore.RED)
        except ValueError as e:
            self.log(f"❌ Data error (kemungkinan JSON): {e}", Fore.RED)
        except KeyError as e:
            self.log(f"❌ Kesalahan key: {e}", Fore.RED)
        except Exception as e:
            self.log(f"❌ Kesalahan tidak terduga: {e}", Fore.RED)

    def gacha(self) -> None:
        while True:
            if self.gacha_point > 0:
                req_url = f"{self.BASE_URL}pet/dna/gacha"

                headers = {**self.HEADERS, "Tg-Init-Data": self.token}
                payload = {"amount": 1}

                self.log(f"🎲 Memulai gacha! Point gacha tersisa: {self.gacha_point}", Fore.CYAN)

                try:
                    response = requests.post(req_url, headers=headers, json=payload)
                    response.raise_for_status()  
                    data = response.json()

                    if 'result' in data and 'dna' in data['result']:
                        dna = data['result']['dna']

                        if isinstance(dna, list):
                            self.log(f"🎉 Kamu mendapatkan beberapa DNA!", Fore.GREEN)
                            for dna_item in dna:
                                name = dna_item.get('name', 'Tidak diketahui')
                                dna_class = dna_item.get('class', 'Tidak diketahui')
                                star = dna_item.get('star', 'Tidak diketahui')
                                remaining_points = str(data['result']['god_power'])

                                self.log(f"🧬 Nama: {name}", Fore.LIGHTGREEN_EX)
                                self.log(f"🏷️  Class: {dna_class}", Fore.YELLOW)
                                self.log(f"⭐ Star: {star}", Fore.MAGENTA)
                                self.log(f"💎 Point Gacha Tersisa: {remaining_points}", Fore.CYAN)

                        else: 
                            name = dna.get('name', 'Tidak diketahui')
                            dna_class = dna.get('class', 'Tidak diketahui')
                            star = dna.get('star', 'Tidak diketahui')
                            remaining_points = str(data['result']['god_power'])

                            self.log(f"🎉 Kamu mendapatkan DNA baru!", Fore.GREEN)
                            self.log(f"🧬 Nama: {name}", Fore.LIGHTGREEN_EX)
                            self.log(f"🏷️  Class: {dna_class}", Fore.YELLOW)
                            self.log(f"⭐ Star: {star}", Fore.MAGENTA)
                            self.log(f"💎 Point Gacha Tersisa: {remaining_points}", Fore.CYAN)

                        self.gacha_point = int(remaining_points) if isinstance(remaining_points, (int, str)) and remaining_points.isdigit() else 0
                    else:
                        self.log("⚠️ Data gacha tidak sesuai dengan struktur yang diharapkan.", Fore.RED)
                        break

                except requests.exceptions.RequestException as e:
                    self.log(f"❌ Gagal mengirim permintaan gacha: {e}", Fore.RED)
                    break
                except ValueError as e:
                    self.log(f"❌ Data error (kemungkinan JSON): {e}", Fore.RED)
                    break
                except KeyError as e:
                    self.log(f"❌ Kesalahan key: {e}", Fore.RED)
                    break
                except Exception as e:
                    self.log(f"❌ Kesalahan tidak terduga: {e}", Fore.RED)
                    break
            else:
                self.log("🚫 Point gacha habis. Tidak dapat melanjutkan gacha.", Fore.RED)
                break

    def mix(self) -> None:
        dad_ids = [] 
        mom_ids = [] 
        req_url = f"{self.BASE_URL}pet/dna/list"  
        headers = {**self.HEADERS, "Tg-Init-Data": self.token}

        self.log("\U0001F50D Mengambil daftar DNA...", Fore.CYAN)

        try:
            response = requests.get(req_url, headers=headers)
            response.raise_for_status()
            data = response.json()

            if "result" in data and isinstance(data["result"], list):
                for dna in data["result"]:
                    item_id = dna.get("item_id")
                    if item_id:
                        if dna.get("can_mom"):
                            mom_ids.append(item_id)
                            self.log(f"\u2705 DNA Mom ditemukan: {dna['name']} (ID: {item_id})", Fore.GREEN)
                        else:
                            dad_ids.append(item_id)
                            self.log(f"\u2705 DNA Dad ditemukan: {dna['name']} (ID: {item_id})", Fore.GREEN)
            else:
                self.log("\u26A0\uFE0F Tidak ada DNA ditemukan dalam respons.", Fore.YELLOW)

            if not dad_ids or not mom_ids:
                self.log("\u274C Daftar DNA tidak mencukupi untuk penggabungan.", Fore.RED)
                return

            self.log(f"\U0001F4CB ID DNA Dad: {dad_ids}", Fore.CYAN)
            self.log(f"\U0001F4CB ID DNA Mom: {mom_ids}", Fore.CYAN)

            mix_url = f"{self.BASE_URL}pet/mix"
            self.log("\U0001F504 Menggabungkan DNA...", Fore.CYAN)

            for dad_id in dad_ids:
                for mom_id in mom_ids:
                    payload = {"dad_id": dad_id, "mom_id": mom_id}
                    max_retries = 3
                    retries = 0

                    while retries < max_retries:
                        try:
                            mix_response = requests.post(mix_url, headers=headers, json=payload)
                            if mix_response.status_code == 400:
                                retries += 1
                                self.log(f"\u26A0\uFE0F Respons 400 diterima, mencoba ulang ({retries}/{max_retries})...", Fore.YELLOW)
                                continue

                            mix_response.raise_for_status()
                            mix_data = mix_response.json()

                            if "result" in mix_data and "pet" in mix_data["result"]:
                                pet_info = mix_data["result"]["pet"]
                                self.log(f"\U0001F389 Pet baru berhasil dibuat: {pet_info['name']} (ID: {pet_info['pet_id']})", Fore.GREEN)
                                break  
                            else:
                                message = mix_data.get("message", "Tidak ada pesan.")
                                self.log(f"\u26A0\uFE0F Gagal menggabungkan: Dad {dad_id}, Mom {mom_id}. Pesan: {message}", Fore.YELLOW)
                                break

                        except requests.exceptions.RequestException as e:
                            retries += 1
                            self.log(f"\u274C Request mix gagal untuk Dad {dad_id}, Mom {mom_id} (percobaan {retries}/{max_retries}): {e}", Fore.RED)

                        except ValueError as e:
                            self.log(f"\u274C Data error untuk Dad {dad_id}, Mom {mom_id}: {e}", Fore.RED)
                            break

                        except Exception as e:
                            self.log(f"\u274C Unexpected error untuk Dad {dad_id}, Mom {mom_id}: {e}", Fore.RED)
                            break

                        if retries == max_retries:
                            self.log(f"\u274C Gagal setelah {max_retries} percobaan untuk Dad {dad_id}, Mom {mom_id}.", Fore.RED)
                            
        except requests.exceptions.RequestException as e:
            self.log(f"\u274C Request gagal: {e}", Fore.RED)
        except ValueError as e:
            self.log(f"\u274C Data error: {e}", Fore.RED)
        except Exception as e:
            self.log(f"\u274C Unexpected error: {e}", Fore.RED)

    def achievements(self) -> None:
        req_url_list = f"{self.BASE_URL}achievement/list"
        req_url_claim = f"{self.BASE_URL}achievement/claim"
        headers = {**self.HEADERS, "tg-init-data": self.token}
        claimable_ids = []  

        try:
            # Step 1: Ambil daftar achievement
            self.log("⏳ Mengambil daftar achievements...", Fore.CYAN)
            response = requests.get(req_url_list, headers=headers)
            response.raise_for_status()
            data = response.json()

            # Filter achievement dengan status true dan claimed false
            if "result" in data and isinstance(data["result"], dict):
                for key, value in data["result"].items():
                    if isinstance(value, dict) and "achievements" in value:
                        for achievement in value["achievements"]:
                            if achievement.get("status") is True and achievement.get("claimed") is False:
                                claimable_ids.append(achievement.get("quest_id"))
                                self.log(f"✅ Achievement siap diklaim: {achievement['title']} (ID: {achievement.get('quest_id')})", Fore.GREEN)

            if not claimable_ids:
                self.log("🚫 Tidak ada achievement yang dapat diklaim.", Fore.YELLOW)
                return

            # Step 2: Klaim setiap achievement yang ditemukan
            for quest_id in claimable_ids:
                self.log(f"🔄 Mencoba klaim achievement dengan ID {quest_id}...", Fore.CYAN)
                response = requests.post(req_url_claim, headers=headers, json={"quest_id": quest_id})
                response.raise_for_status()
                claim_result = response.json()

                if claim_result.get("error_code") is None:
                    self.log(f"🎉 Berhasil klaim achievement dengan ID {quest_id}!", Fore.GREEN)
                else:
                    self.log(f"⚠️ Gagal klaim achievement dengan ID {quest_id}. Pesan: {claim_result.get('message')}", Fore.RED)

        except requests.exceptions.RequestException as e:
            self.log(f"❌ Gagal memproses request: {e}", Fore.RED)
        except ValueError as e:
            self.log(f"❌ Kesalahan data: {e}", Fore.RED)
        except Exception as e:
            self.log(f"❌ Kesalahan tidak terduga: {e}", Fore.RED)

    def mission(self):
        headers = {**self.HEADERS, "Tg-Init-Data": self.token}

        try:
            mission_url = f"{self.BASE_URL}mission/list"
            self.log("🔄 Mengambil daftar misi...", Fore.CYAN)
            mission_response = requests.get(mission_url, headers=headers)
            mission_response.raise_for_status()
            
            try:
                mission_data = mission_response.json()
            except ValueError:
                self.log("❌ Data respons misi bukan JSON yang valid.", Fore.RED)
                return
            
            missions = mission_data.get("result", [])
            if not isinstance(missions, list):
                self.log("❌ Format data misi tidak valid (diharapkan list).", Fore.RED)
                return
            
            self.log("✅ Berhasil mengambil daftar misi", Fore.GREEN)
            pet_url = f"{self.BASE_URL}pet/list"
            self.log("🔄 Mengambil daftar pet...", Fore.CYAN)
            pet_response = requests.get(pet_url, headers=headers)
            pet_response.raise_for_status()

            try:
                pet_data = pet_response.json()  
            except ValueError:
                self.log("❌ Data respons pet bukan JSON yang valid.", Fore.RED)
                return

            pets = pet_data.get('result', [])
            if not isinstance(pets, list):
                self.log("❌ Format data pet tidak valid (diharapkan list).", Fore.RED)
                return

            self.log("✅ Berhasil mengambil daftar pet", Fore.GREEN)
            
            self.log("🔍 Mulai klaim semua misi...", Fore.CYAN)
            for mission in missions:
                if mission.get("is_disabled") or mission.get("is_deleted") or mission.get("status"):
                    self.log(
                        f"⚠️ Misi {mission.get('mission_id')} dilewati (disabled/deleted/sudah selesai).", 
                        Fore.YELLOW
                    )
                    continue

                claim_url = f"{self.BASE_URL}mission/claim"
                claim_payload = {
                    "mission_id": mission.get("mission_id") 
                }

                claim_response = requests.post(claim_url, headers=headers, json=claim_payload)

                if claim_response.status_code == 200:
                    self.log(f"✅ Misi {mission.get('mission_id')} berhasil diklaim", Fore.GREEN)
                else:
                    self.log(
                        f"❌ Gagal mengklaim misi {mission.get('mission_id')} (Error: {claim_response.status_code})",
                        Fore.RED,
                    )
                    self.log(f"🔍 Detail respons klaim: {claim_response.text}", Fore.RED)

            self.log("🔍 Memfilter misi yang dapat diselesaikan dan mengirim pet...", Fore.CYAN)
            for mission in missions:
                if mission.get("is_disabled") or mission.get("is_deleted") or mission.get("status"):
                    self.log(
                        f"⚠️ Misi {mission.get('mission_id')} dilewati (disabled/deleted/sudah selesai).", 
                        Fore.YELLOW
                    )
                    continue

                required_pets = [
                    {
                        "class": mission.get(f"pet_{i}_class"),
                        "star": mission.get(f"pet_{i}_star"),
                    }
                    for i in range(1, 4)
                ]

                pet_ids = []
                for req in required_pets:
                    for pet in pets:
                        if (
                            pet.get("class") == req["class"]
                            and pet.get("star", 0) >= req["star"]
                            and pet.get("id") not in pet_ids
                        ):
                            pet_ids.append(pet["pet_id"])
                            break

                if len(pet_ids) == 3:
                    self.log(f"➡️ Mengirim pet ke misi {mission.get('mission_id')}...", Fore.CYAN)

                    enter_url = f"{self.BASE_URL}mission/enter"
                    payload = {
                        "mission_id": mission.get("mission_id"),  
                        **{f"pet_{i+1}_id": pet_id for i, pet_id in enumerate(pet_ids)}  
                    }
                    enter_response = requests.post(enter_url, headers=headers, json=payload)

                    if enter_response.status_code == 200:
                        self.log(f"✅ Misi {mission.get('mission_id')} berhasil dijalankan", Fore.GREEN)
                    else:
                        self.log(
                            f"❌ Gagal menjalankan misi {mission.get('mission_id')} (Error: {enter_response.status_code})",
                            Fore.RED,
                        )
                else:
                    self.log(f"❌ Misi {mission.get('mission_id')} tidak memenuhi syarat pet", Fore.RED)

        except requests.exceptions.RequestException as e:
            self.log(f"❌ Terjadi kesalahan saat memproses: {e}", Fore.RED)

    def quest(self):
        headers = {**self.HEADERS, "Tg-Init-Data": self.token}

        try:
            quest_url = f"{self.BASE_URL}quest/list"
            self.log("🔄 Mengambil daftar quest...", Fore.CYAN)
            quest_response = requests.get(quest_url, headers=headers)
            quest_response.raise_for_status()
            quest_data = quest_response.json()

            quests = quest_data.get("result", {}).get("quests", [])
            if not quests:
                self.log("⚠️ Tidak ada quest yang tersedia.", Fore.YELLOW)
                return

            self.log("✅ Berhasil mengambil daftar quest", Fore.GREEN)

            for quest in quests:
                if quest.get("is_disabled") or quest.get("is_deleted") or quest.get("status"):
                    self.log(f"⚠️ Quest {quest.get('quest_code')} dilewati (disabled/deleted/selesai).", Fore.YELLOW)
                    continue

                quest_code = quest.get("quest_code")
                self.log(f"➡️ Melakukan check atau claim untuk quest {quest_code}...", Fore.CYAN)

                check_url = f"{self.BASE_URL}quest/check"
                payload = {"quest_code": quest_code}
                check_response = requests.post(check_url, headers=headers, json=payload)

                if check_response.status_code == 200:
                    self.log(f"✅ Quest {quest_code} berhasil di-claim", Fore.GREEN)
                else:
                    self.log(f"❌ Gagal meng-claim quest {quest_code} (Error: {check_response.status_code})", Fore.RED)
        except requests.exceptions.RequestException as e:
            self.log(f"❌ Terjadi kesalahan saat memproses quest: {e}", Fore.RED)

    def claim_pass(self):
        headers = {**self.HEADERS, "Tg-Init-Data": self.token}

        try:
            pass_url = f"{self.BASE_URL}season-pass/list"
            self.log("🔄 Mengambil daftar season pass...", Fore.CYAN)
            pass_response = requests.get(pass_url, headers=headers)
            pass_response.raise_for_status()
            passes = pass_response.json().get("result", [])

            if not passes:
                self.log("⚠️ Tidak ada season pass yang tersedia.", Fore.YELLOW)
                return

            self.log("✅ Berhasil mengambil daftar season pass", Fore.GREEN)

            for season in passes:
                season_id = season.get("season_id")
                try:
                    current_step = int(season.get("current_step", 0))
                except ValueError:
                    self.log(f"❌ Nilai current_step untuk season {season_id} tidak valid, melewati season ini.", Fore.RED)
                    continue

                free_rewards = season.get("free_rewards", [])
                for reward in free_rewards:
                    step = reward.get("step")
                    is_claimed = reward.get("is_claimed", True)

                    try:
                        step = int(step)
                    except (ValueError, TypeError):
                        self.log(f"❌ Nilai step untuk reward free di season {season_id} tidak valid, melewati reward ini.", Fore.RED)
                        continue

                    if not is_claimed and step <= current_step:
                        self.log(f"➡️ Mengklaim reward gratis untuk season {season_id}, step {step}...", Fore.CYAN)

                        claim_url = f"{self.BASE_URL}season-pass/claim"
                        payload = {"season_id": season_id, "step": step, "type": "free"}
                        claim_response = requests.post(claim_url, headers=headers, json=payload)

                        if claim_response.status_code == 200:
                            self.log(f"✅ Reward gratis step {step} berhasil diklaim", Fore.GREEN)
                        else:
                            self.log(f"❌ Gagal klaim reward step {step} (Error: {claim_response.status_code})", Fore.RED)

                premium_rewards = season.get("premium_rewards", [])
                for reward in premium_rewards:
                    step = reward.get("step")
                    is_claimed = reward.get("is_claimed", True)

                    try:
                        step = int(step)
                    except (ValueError, TypeError):
                        self.log(f"❌ Nilai step untuk reward premium di season {season_id} tidak valid, melewati reward ini.", Fore.RED)
                        continue

                    if not is_claimed and step <= current_step:
                        self.log(f"➡️ Mengklaim reward premium untuk season {season_id}, step {step}...", Fore.CYAN)

                        claim_url = f"{self.BASE_URL}season-pass/claim"
                        payload = {"season_id": season_id, "step": step, "type": "premium"}
                        claim_response = requests.post(claim_url, headers=headers, json=payload)

                        if claim_response.status_code == 200:
                            self.log(f"✅ Reward premium step {step} berhasil diklaim", Fore.GREEN)
                        else:
                            self.log(f"❌ Gagal klaim reward step {step} (Error: {claim_response.status_code})", Fore.RED)
        except requests.exceptions.RequestException as e:
            self.log(f"❌ Terjadi kesalahan saat memproses season pass: {e}", Fore.RED)

if __name__ == "__main__":
    ani = animix()
    index = 0
    max_index = len(ani.query_list)
    config = ani.load_config()

    while True:
        ani.log(f"{Fore.GREEN}[LIVEXORDS]===== {index + 1}/{len(ani.query_list)} =====[LIVEXORDS]{Fore.RESET}")
        ani.login(index)
            
        if config.get("achievements", False):
            ani.log(f"{Fore.YELLOW}[CONFIG] achievements: True{Fore.RESET},")
            ani.achievements()
        else:
            ani.log(f"{Fore.RED}[CONFIG] achievements: False{Fore.RESET},")
        
        if config.get("mission", False):
            ani.log(f"{Fore.YELLOW}[CONFIG] mission: True{Fore.RESET},")
            ani.mission()
        else:
            ani.log(f"{Fore.RED}[CONFIG] mission: False{Fore.RESET},")
        
        if config.get("quest", False):
            ani.log(f"{Fore.YELLOW}[CONFIG] quest: True{Fore.RESET},")
            ani.quest()
        else:
            ani.log(f"{Fore.RED}[CONFIG] quest: False{Fore.RESET},")
        
        if config.get("gacha", False):
            ani.log(f"{Fore.YELLOW}[CONFIG] gacha: True{Fore.RESET},")
            ani.gacha()
        else:
            ani.log(f"{Fore.RED}[CONFIG] gacha: False{Fore.RESET},")
            
        if config.get("mix", False):
            ani.log(f"{Fore.YELLOW}[CONFIG] mix: True{Fore.RESET},")
            ani.mix()
        else:
            ani.log(f"{Fore.RED}[CONFIG] mix: False{Fore.RESET},")
            
        if config.get("claim_pass", False):
            ani.log(f"{Fore.YELLOW}[CONFIG] claim_pass: True{Fore.RESET},")
            ani.claim_pass()
        else:
            ani.log(f"{Fore.RED}[CONFIG] claim_pass: False{Fore.RESET},")
            
        if index == max_index - 1:
            ani.log(f"Berhenti untuk loop selanjutnya{Fore.CYAN},")
            ani.log(f"Tidur selama {config.get("delay_loop")} detik{Fore.CYAN},")
            time.sleep(config.get("delay_loop"))
            index = 0
        else:
            ani.log(f"Tidur selama {config.get("delay_pergantian_akun")} detik ,sebelum melanjutkan ke akun berikutnya")
            time.sleep(config.get("delay_pergantian_akun"))
            index += 1