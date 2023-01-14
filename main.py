from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--headless")
options.add_argument("--window-size=1920,1200")
DRIVER_PATH = 'chromedriver.exe'


def naversearch(word):
    driver = webdriver.Chrome(executable_path=DRIVER_PATH, options=options)
    url = "https://korean.dict.naver.com/koendict/#/search?range=example&shouldSearchVlive=false&query=" + word + "&exampleLevel=exist:1&haveTrans=exist:1"
    driver.get(url)
    # print(driver.page_source)
    # ids: level2, translation2
    try:
        ignored_exceptions = (NoSuchElementException, StaleElementReferenceException)
        wait = WebDriverWait(driver, 10, ignored_exceptions=ignored_exceptions).until(
            EC.presence_of_element_located((By.CLASS_NAME, "row"))
        )
    finally:
        korsent = driver.find_elements_by_class_name("row")
        for sent in korsent:
            sent = sent.text
            sent = sent.split("\n")[0:2]  # sent[0] is kor, sent[1] is eng
            if sent[1][0].isupper():
                return sent[0] + " / " + sent[1]
                break
            else:
                pass
        driver.quit()


def output(original, naversearched, filename):
    with open(filename, 'a', encoding='utf-8') as f:
        try:
            f.write(original + ": " + naversearched + "\n")
        except TypeError:
            f.write("MANUAL SENTENCE FOR " + original + "\n")
            print("error for " + original)


def main():
    with open("test.txt", encoding='utf8') as f:
        for line in f:
            output(line.strip(), naversearch(line.strip()), "Output.txt")


main()
