from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import numpy as np
import re

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/101.0.4951.67 Safari/537.36'}

main_url = 'https://spb.hh.ru'

def vacancies(name):
    params = {'text': name}
    response = requests.get(main_url + '/search/vacancy', params=params, headers=headers)
    soup = bs(response.text, 'html.parser')
    line = soup.find('h1', {'data-qa': 'bloko-header-3'})
    n = re.findall(r'\d+', line.get_text())
    salary = int(''.join(map(str, n)))
    salary = int(salary/20)

    list_of_vac = []
    page = 0
    while page <= salary:
        params = {'text': name, 'page': page, 'items_om_page': 20}
        response = requests.get(main_url + '/search/vacancy', params=params, headers=headers)
        soup = bs(response.text, 'html.parser')
        all_vacancies = soup.find_all('div', {'class': 'vacancy-serp-item'})
        for vacancy in all_vacancies:
            vac = {}
            pos = vacancy.find('span', {'class': 'g-user-content'})
            vac['Position'] = pos.text
            sal = vacancy.find_all('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
            for el in sal:
                vac['Salary'] = el.text.replace('\u202f', '')
            # vac['Salary'] = sal.text.replace('\u202f', '')
            vac_link = vacancy.find('a', {'data-qa': 'vacancy-serp__vacancy-title'}, href=True)
            vac['Link'] = vac_link['href']
            list_of_vac.append(vac)
        page += 1

    n = pd.DataFrame(list_of_vac)

    n['Currency'] = n['Salary'].replace('[0-9-дот]', '', regex=True)
    n['Min'] = np.select([n['Salary'].str.contains('от', na=False), n['Salary'].str.contains('до', na=False),
                          n['Salary'].str.contains('–', na=False)],
                         [n['Salary'].replace('[^\d]', '', regex=True), None,
                          n['Salary'].replace('–.*', '', regex=True)])
    n['Max'] = np.select([n['Salary'].str.contains('от', na=False), n['Salary'].str.contains('до', na=False),
                          n['Salary'].str.contains('–', na=False)],
                         [None, n['Salary'].replace('[^\d]', '', regex=True),
                          n['Salary'].replace('.*-', '', regex=True).replace('[^\d]', '', regex=True)])

    n.fillna('undefined', inplace=True)
    n.drop('Salary', axis=1, inplace=True)
    n = n.reindex(columns=['Position', 'Min', 'Max', 'Currency', 'Link'])
    # n[['Min', 'Max']] = n[['Min', 'Max']].astype('int')
    n.index += 1

    n.to_csv('vacancies.csv')

    print(n)

vacancies('математик-аналитик')