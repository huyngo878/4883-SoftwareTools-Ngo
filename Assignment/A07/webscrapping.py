import PySimpleGUI as sg
from selenium import webdriver
from bs4 import BeautifulSoup

def buildWeatherURL(month, day, year, airport, filter):
    base_url = "https://www.wunderground.com/history"
    url = f"{base_url}/{filter}/{airport}/date/{year}-{month}-{day}"
    return url

def retrieveWeatherData(url):
    driver = webdriver.Chrome()
    driver.get(url)
    page_source = driver.page_source
    driver.quit()
    return page_source

def parseWeatherData(page_source):
    soup = BeautifulSoup(page_source, 'html.parser')

    # find the table in the webpage
    table = soup.find('table')

    # get the column names from the table headers
    column_names = [th.text for th in table.find_all('th')]

    # get the table rows
    rows = table.find_all('tr')

    parsed_data = []
    for row in rows:
        columns = row.find_all('td')
        # get the values in each column for this row
        values = [td.text for td in columns]
        # create a dictionary for this row
        row_dict = dict(zip(column_names, values))
        parsed_data.append(row_dict)

    return parsed_data

def displayWeatherData(data):
    data_list = [list(d.values()) for d in data]  # Convert each dictionary to a list
    layout = [
        [sg.Table(values=data_list, headings=list(data[0].keys()), display_row_numbers=True, auto_size_columns=True)]
    ]
    window = sg.Window('Weather Data', layout)
    event, values = window.read()
    window.close()


def main():
    layout = [
        [sg.Text('Month'), sg.Input(key='month')],
        [sg.Text('Day'), sg.Input(key='day')],
        [sg.Text('Year'), sg.Input(key='year')],
        [sg.Text('Airport'), sg.Input(key='airport')],
        [sg.Text('Filter'), sg.Input(key='filter')],
        [sg.Submit(), sg.Cancel()]
    ]

    window = sg.Window('Weather Data Entry', layout)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == 'Cancel':
            break

        month = values['month']
        day = values['day']
        year = values['year']
        airport = values['airport']
        filter = values['filter']

        url = buildWeatherURL(month, day, year, airport, filter)
        page_source = retrieveWeatherData(url)
        weather_data = parseWeatherData(page_source)
        displayWeatherData(weather_data)

    window.close()

if __name__ == '__main__':
    main()
