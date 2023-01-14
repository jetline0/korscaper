import requests
from urllib.parse import unquote
import time

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"}


def naversearch(word):
    url = f"https://korean.dict.naver.com/api3/koen/search?query={word}&m=mobile&range=example&page=1&lang=en&shouldSearchVlive=false&exampleLevel=exist:1&haveTrans=exist:1"
    response = requests.get(url, headers=headers)
    json_response = response.json()
    result_num = json_response['searchResultMap']["searchResultListMap"]["EXAMPLE"]["total"]
    if result_num != 0:
        eng_sent = [x["expExample1"] for x in
                    json_response['searchResultMap']['searchResultListMap']['EXAMPLE']['items']]
        print(eng_sent)
        index_of_cap = checkupper(eng_sent)
        if index_of_cap is not None:
            kor_sent = json_response['searchResultMap']['searchResultListMap']['EXAMPLE']['items'][index_of_cap][
                "translationEncode"]
            kor_sent = unquote(kor_sent).split("+")
            kor_sent = ' '.join(kor_sent)
            return f'{word}\t{eng_sent[index_of_cap]}\t{kor_sent}\n'
        else:
            return f"ERROR 1: NO FULL SENTENCE FOR {word}!\n"
    else:
        return f"ERROR 2: NO RESULTS FOR {word}!\n"


"""
checks
are there examples for level 1 + have translations? (searchResultMap.searchResultListMap.EXAMPLE.total != 0)
    YES:
        run separate first letter loop function... did the loop return anything? (lettersearch(word) is not NoneType)
            YES: return word (Tab) Korean Sentence (Tab) English Sentence
            NO: MANUAL SENTENCE
    NO:
        do it for the All Level"
            run separate first letter loop function... did the loop return anything? (lettersearch(word) is not NoneType)
                YES: return word (Tab) Korean Sentence (Tab) English Sentence
                NO: MANUAL SENTENCE
"""


def checkupper(listname):  # listname should be an array of english sentences
    for sent in listname:
        if sent[0].isupper():
            return listname.index(sent)


def output(naversearched, filename):
    with open(filename, 'a', encoding='utf-8') as f:
        f.writelines(naversearched)


def main():
    with open("InputEdit.txt", encoding='utf8') as f:
        for line in f:
            output(naversearch(line.strip()), "Output.txt")


t0 = time.time()
main()
t1 = time.time()
time_taken = t1 - t0
print(f"Scraping took {str(time_taken)} seconds")
