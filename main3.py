import requests
from urllib.parse import unquote
import time
# input: 7700 words, inputedit, and output
# output: word, def, sentence

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"}

# scrape definition
def naversearch(word):
    url = f"https://korean.dict.naver.com/api3/koen/search?query={word}&m=mobile&range=meaning&page=1&lang=en&hid=162545087939236350"
    response = requests.get(url, headers=headers)
    json_response = response.json()
    result_num = json_response['pagerInfo']["totalRows"]
    if result_num != 0:
        definition = json_response['searchResultMap']['searchResultListMap']['MEANING']['items'][0]['expEntry']
        return f"{definition}\n"
    else:
        return f"NO RESULTS FOR {word}\n"


def output(naversearched, filename):
    with open(filename, 'a', encoding='utf-8') as f:
        f.writelines(naversearched)


def main():
    with open("7700 alpha.txt", encoding='utf8') as f:
        for line in f:
            output(naversearch(line.strip()), "definitions.txt")

main()