from pprint import pprint

import requests

BASE_URL = "https://api.hh.ru/"
headers = {"User-Agent": "api-test-agent"}
search_param = "Name:(python or django or drf or backend or fastapi or flask) and DESCRIPTION:(django or drf or fastapi or flask)"

response = requests.get(url=f'{BASE_URL}vacancies/?text={search_param}', headers=headers)
vacancies = response.json()["items"]

for vacancy in vacancies:
    vacancy_id = vacancy["id"]
    vacancy_url = f"{BASE_URL}vacancies/{vacancy_id}"
    vacancy_response = requests.get(url=vacancy_url, headers=headers)
    vacancy_data = vacancy_response.json()

    title = vacancy_data.get("name")
    key_skills = vacancy_data.get("key_skills")
    published_at = vacancy_data.get("published_at")


    data = {
        "vacancy_id": vacancy_id,
        "title": title,
        "key_skills": key_skills,
        "published_at": published_at
    }
    pprint(data)