import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


from GetQuestionName import getQuestionName

FAST_DELAY = 0.5
SLOWER_DELAY = 1
MID_DELAY = 3
SLOWEST_DELAY = 6
THE_SLOWEST_DELAY = 8

folderPath = "./Pre-quiz Drafts/"
pq_num = 4

questions = []
answers = []

with open(folderPath + "PQ"+str(pq_num)+".txt", 'r') as f:

    lines = f.readlines()
    for line in lines:
        if line[0] == 'Q':
            line = line.replace('[RNB]', '')
            line = line.replace('[PB]', '')
            line = line.replace('[PV]', '')
            line = line.replace('[BS]', '')
            line = line.replace('[ANI]', '')
            line = line.replace('\n', '')
            questions.append(line[2:])
        elif line[0] == 'A':
            line = line.replace('\n', '')
            answers.append(line[2:])

driver = webdriver.Chrome()  # Optional argument, if not specified will search path.

driver.get('https://moodle.hochschule-rhein-waal.de/');

time.sleep(SLOWER_DELAY)  # Let the user actually see something!
login = driver.find_element(By.XPATH,"/html/body/div[2]/nav/div[2]/div[3]/div/span/a");
login.click()

time.sleep(FAST_DELAY) # Let the user actually see something!

username = driver.find_element(By.NAME,"j_username");
username.send_keys("Your username")
password = driver.find_element(By.NAME,"j_password");
password.send_keys("Your password")
password.send_keys(Keys.RETURN)
time.sleep(FAST_DELAY)

mycourses = driver.find_element(By.XPATH,"/html/body/div[2]/nav/div[1]/nav/ul/li[2]/a");\
mycourses.click()

time.sleep(SLOWEST_DELAY)
driver.find_element(By.XPATH,"/html/body/div[2]/div[3]/div[1]/div/div[2]/div/section/div/aside/section/div/div/div[1]/div[2]/div/div/div[1]/div/ul/li[1]/div/div[2]/a").click()

time.sleep(MID_DELAY);
driver.find_element(By.NAME,"setmode").click()

time.sleep(THE_SLOWEST_DELAY); #click on the triple dot
driver.find_element(By.XPATH,"/html/body/div[4]/div[5]/div[2]/div/div[3]/div/section/div/div/div/ul[2]/li[5]/div[2]/div[3]/ul/li[1]/div/div[1]/div[2]/div/div/div/div/a/i").click()

time.sleep(FAST_DELAY); #click on edit question
driver.find_element(By.XPATH,"/html/body/div[4]/div[5]/div[2]/div/div[3]/div/section/div/div/div/ul[2]/li[5]/div[2]/div[3]/ul/li[1]/div/div[1]/div[2]/div/div/div/div/div/a[1]/span").click()


time.sleep(SLOWEST_DELAY); #Click on question back
driver.find_element(By.XPATH,"/html/body/div[4]/div[5]/div[2]/div/div[2]/nav/ul/li[5]/a").click()

time.sleep(MID_DELAY); #click on the category
driver.find_element(By.XPATH,"/html/body/div[4]/div[5]/div[2]/div/div[3]/div/section/div[2]/div[2]/form/div/div[1]/select").click();

time.sleep(FAST_DELAY); #click on the category
driver.find_element(By.XPATH,"/html/body/div[4]/div[5]/div[2]/div/div[3]/div/section/div[2]/div[2]/form/div/div[1]/select/optgroup[2]/option["+str(pq_num+2)+"]").click();

for index,question in enumerate(questions):
    if("nein" in question):
        print("skipping question: " + question)
        continue;
    print("question: " + question)
    time.sleep(MID_DELAY); #click on create a new question
    driver.find_element(By.XPATH,"/html/body/div[4]/div[5]/div[2]/div/div[3]/div/section/div[2]/div[2]/div/div[1]/form/button").click();

    while True:
        try:
            time.sleep(FAST_DELAY);#click on multiple choice
            driver.find_element(By.NAME,"qtype").click();
            break;
        except:
            time.sleep(FAST_DELAY);
            print("error: stuck on multiple choice")
            continue;

    while True:
        try:
            time.sleep(FAST_DELAY);#click on add
            driver.find_element(By.NAME,"submitbutton").click();
            break;
        except:
            time.sleep(FAST_DELAY);
            print("error: stuck on add")
            continue;

    time.sleep(MID_DELAY); #add the question name
    question_name = getQuestionName(question)
    question_name_field = driver.find_element(By.NAME,"name");
    question_name_field.send_keys(question_name)

    time.sleep(FAST_DELAY); #add the question

    javascriptExe = f'document.getElementById("id_questiontext_ifr").contentDocument.querySelector("p").innerText ="{question}"'
    print(javascriptExe)
    driver.execute_script(javascriptExe)



    options = answers[index].split(";");

    for i in range(0,len(options)):
        if("(correct)" in options[i]):
            options[i] = options[i].replace("(correct)", "")
            select = Select(driver.find_element(By.NAME,f"fraction[{i}]"));
            select.select_by_value("1.0");

        javascriptExe = f'document.getElementById("id_answer_{i}_ifr").contentDocument.querySelector("p").innerText ="{options[i]}"'
        print(javascriptExe)
        driver.execute_script(javascriptExe)

    time.sleep(FAST_DELAY); #click on submit
    driver.find_element(By.NAME,"submitbutton").click();

    time.sleep(THE_SLOWEST_DELAY)
driver.quit()



