import json
from bs4 import BeautifulSoup
import requests


def medicines_scraper():
    url = 'https://apteka911.ua/ua/shop/lekarstvennyie-preparatyi/ot_diabeta'
    medicines = []
    for i in range(1, 5):
        url_page = url + f'/page={i}'
        page = requests.get(url_page)
        soup = BeautifulSoup(page.text, "html.parser")
        filtered_medicines_list = []
        all_medicines_list = soup.findAll('div', class_='b-prod__bottom')
        for medicine in all_medicines_list:
            if medicine.find('p', class_='prod__header'):
                filtered_medicines_list.append(medicine.text.replace('\n', '').replace('грн.', ':'))

        for medicine in filtered_medicines_list:
            medicine_info = medicine.split(' :')[1].split(' ')
            m_i = medicine_info.copy()
            m_i.pop(0)
            dose = ['']
            for i in m_i:
                if 'г' in i or 'мл' in i:
                    dose.append(i)
                    break
            medicines.append(
                {
                    'title': medicine_info[0],
                    'dose': ''.join(dose)
                }
            )

    # convert to encode json
    json_medicines_encode = json.dumps(medicines, indent=2)

    # decode json but to list
    data = json.loads(json_medicines_encode)

    # convert decoded data to json
    json_medicines = json.dumps(data, indent=2, ensure_ascii=False)

    return medicines
