import codecs
import json
import mechanicalsoup

browser = mechanicalsoup.StatefulBrowser()

# Main url to query
URL_MAIN_PAGE = 'https://veteriner.co/veteriner-klinikleri'
URL_COMPANIES = 'https://veteriner.co/hayvan-barinaklari'

def write_json(filename, obj):
	# Save 'obj' in the filename 'filename'
	with codecs.open(filename, 'w+', 'utf-8') as f:
		# make sure to write with utf-8
		f.write(json.dumps(obj, indent=1,ensure_ascii=False))


def get_companies():
	print(browser)

	print('Retrieving companies.. ')

	browser.open(URL_COMPANIES)
	page = browser.get_current_page()

	companies = []
	filename = 'COMPANIES'
	for url in page.find_all('li'):
		for a in url.find_all('a'):
			if a.get('href', None) is None:
				companies.append(a.text)

	write_json(filename, companies)

	print(f'{len(companies)} rows writed in file \'{filename}\' ')


def main():
    global browser
    browser.open(URL_MAIN_PAGE)
    page = browser.get_current_page()
    urls = page.find('div', { 'class' : 'c2'}).find_next_sibling('ul').find_all('a', href=True)
    urls = list(map(lambda x: x['href'], urls))
    result = []

    print('Retrieving rows.. ')
    print(f'{len(urls)} urls to query\n')

    i = 0   
    for url in urls:

        browser = mechanicalsoup.StatefulBrowser()
        browser.open(url)
        page = browser.get_current_page()
        city = page.find('h1', {"class": "title"}).text[:-21]

        i += 1
        print(f'{i} => {city} \t')

        for table in page.find_all('table',  {"class": "wp-table-reloaded"}):
            tag_district = table.find_previous_sibling('h2')

            if tag_district is not None:
                district = tag_district.text
                index = district.index('Veteriner')
                district = district[:index]
            else:
                district = ''

            for tr in table.find_all('tr'):

                obj = { 'category' : 'Veteriner Klinikleri', 'city' : city, 'district' : district}

                td_name = tr.find('td', {"class": "column-1"})
                name = td_name.text if td_name is not None else ''

                td_address = tr.find('td', {"class": "column-2"})
                address = td_address.text if td_address is not None else ''

                td_phone = tr.find('td', {"class": "column-3"})
                phone = td_phone.text if td_phone is not None else ''

                obj['name'] = name
                obj['address'] = address
                obj['phone'] = phone

                if name != '':
                    result.append(obj)

    filename = 'JSON'
    write_json(filename, result)
    print(f'{len(result)} rows writed in file \'{filename}\' ')


if __name__ == '__main__':
    main()
