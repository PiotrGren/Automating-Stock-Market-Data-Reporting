import schedule
import time
import subprocess
import os

# Sprawdź, czy istnieje plik blokujący
def is_previous_run_finished():
    return not os.path.exists("lockfile.txt")

def create_lockfile():
    with open("lockfile.txt", "w") as file:
        file.write("")

def remove_lockfile():
    os.remove("lockfile.txt")

def run_script():
    if is_previous_run_finished():
        create_lockfile()
        print("STARTING SCRIPT...\n")
        with open(os.devnull, 'w') as null:
            subprocess.run(["python", "WEBSCRAPPING/scraper.py"], stdout=null, stderr = null)  # Zastąp 'nazwa_twojego_skryptu.py' nazwą twojego skryptu
        remove_lockfile()
        print("\nWEBSCRAPPING FINISHED")

schedule.every(15).seconds.do(run_script)

while True:
    schedule.run_pending()
    time.sleep(1)
