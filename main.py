import os
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from GetQuestionName import getQuestionName

# Define constants
DELAY_FAST = 0.5
DELAY_SLOWER = 1
DELAY_MID = 3
DELAY_SLOWEST = 6
DELAY_THE_SLOWEST = 8


folderPath = "./Pre-quiz Drafts/"
PQ_NUM = 6

questions = []
answers = []

with open(os.path.join(folderPath, f"PQ{PQ_NUM}.txt"), 'r') as f:
    lines = f.readlines()
    for line in lines:
        line = line.replace('[RNB]', '').replace('[PB]', '').replace('[PV]', '').replace('[BS]', '').replace('[ANI]', '').strip()
        
        if line.startswith('Q'):
            if(("?" not in line) or (":" not in line)):
                line = line + "?"
            questions.append(line[2:].capitalize())
        elif line.startswith('A'):
            answers.append(line[2:].capitalize())

driver = webdriver.Chrome()

def wait_for_element(by, value, timeout=10):
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, value)))

def click_element(by, value):
    element = wait_for_element(by, value)
    element.click()

def set_text(by, value, text):
    element = wait_for_element(by, value)
    element.send_keys(text)

driver.get('https://moodle.hochschule-rhein-waal.de/')
time.sleep(DELAY_SLOWER)

click_element(By.XPATH, "/html/body/div[2]/nav/div[2]/div[3]/div/span/a")

set_text(By.NAME, "j_username", "NiceTry@youremail.com")
set_text(By.NAME, "j_password", "NiceTryPassword")
driver.find_element(By.NAME, "j_password").send_keys(Keys.RETURN)
time.sleep(DELAY_FAST)

click_element(By.XPATH, "/html/body/div[2]/nav/div[1]/nav/ul/li[2]/a")
time.sleep(DELAY_SLOWEST)
click_element(By.XPATH, "/html/body/div[2]/div[3]/div[1]/div/div[2]/div/section/div/aside/section/div/div/div[1]/div[2]/div/div/div[1]/div/ul/li[1]/div/div[2]/a")
time.sleep(DELAY_MID)
click_element(By.NAME, "setmode")
time.sleep(DELAY_SLOWEST)#click on the triple dot
click_element(By.XPATH, "/html/body/div[4]/div[5]/div[2]/div/div[3]/div/section/div/div/div/ul[2]/li[5]/div[2]/div[3]/ul/li[1]/div/div[1]/div[2]/div/div/div/div/a/i")
time.sleep(DELAY_FAST)#click on edit question
click_element(By.XPATH, "/html/body/div[4]/div[5]/div[2]/div/div[3]/div/section/div/div/div/ul[2]/li[5]/div[2]/div[3]/ul/li[1]/div/div[1]/div[2]/div/div/div/div/div/a[1]/span")
time.sleep(DELAY_SLOWEST)#Click on question back
click_element(By.XPATH, "/html/body/div[4]/div[5]/div[2]/div/div[2]/nav/ul/li[5]/a")
time.sleep(DELAY_MID)#click on the category
click_element(By.XPATH, "/html/body/div[4]/div[5]/div[2]/div/div[3]/div/section/div[2]/div[2]/form/div/div[1]/select")
time.sleep(DELAY_FAST)#click on the category
click_element(By.XPATH, f"/html/body/div[4]/div[5]/div[2]/div/div[3]/div/section/div[2]/div[2]/form/div/div[1]/select/optgroup[2]/option[{PQ_NUM+2}]")

for index, question in enumerate(questions):
    if "nein" in question:
        print("Skipping question: " + question)
        continue
    print("Question: " + question)
    time.sleep(DELAY_MID); #click on create a new question
    click_element(By.XPATH, "/html/body/div[4]/div[5]/div[2]/div/div[3]/div/section/div[2]/div[2]/div/div[1]/form/button")

    while True:
        try:
            click_element(By.NAME, "qtype")
            break
        except:
            time.sleep(DELAY_FAST)
            print("Error: Stuck on multiple choice")
            continue

    while True:
        try:
            click_element(By.NAME, "submitbutton")
            break
        except:
            time.sleep(DELAY_FAST)
            print("Error: Stuck on add")
            continue

    time.sleep(DELAY_SLOWER)
    question_name = getQuestionName(question)
    set_text(By.NAME, "name", question_name)

    javascript_exe = f'document.getElementById("id_questiontext_ifr").contentDocument.querySelector("p").innerText ="{question}"'
    print(javascript_exe)
    driver.execute_script(javascript_exe)

    options = answers[index].split(";")

    for i in range(len(options)):
        if "(correct)" in options[i]:
            options[i] = options[i].replace("(correct)", "")
            select = Select(wait_for_element(By.NAME, f"fraction[{i}]"))
            select.select_by_value("1.0")
            print("(correct)",end="")

        javascript_exe = f'document.getElementById("id_answer_{i}_ifr").contentDocument.querySelector("p").innerText ="{options[i]}"'
        print(javascript_exe)
        driver.execute_script(javascript_exe)

    click_element(By.NAME, "submitbutton")
    time.sleep(DELAY_SLOWER)

driver.quit()
