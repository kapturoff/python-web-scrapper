import requests
from bs4 import BeautifulSoup
from collections import namedtuple

URL = 'https://python.org'
UpcomingEvents = namedtuple('UpcomingEvents', ['href', 'title'])

# Function for processing of the parsed data
format_output = lambda tag: UpcomingEvents(
    # We need to concatenate href with an URL, because there're relative links presented
    href=URL + tag['href'],
    title=tag.text
)

print('Loading the main page...')
page = requests.get(URL)

print('Parsing the page...')
soup = BeautifulSoup(page.content, 'html.parser')

print('Getting the "Upcoming Events" widget...')
events_widget = soup.find(text='Upcoming Events').parent.parent
announcements = events_widget.select('ul.menu > li > a')  # Getting only its links

print('Processing the parsed data...')
events_formatted = map(format_output, announcements)

print('Compiling output to string...')
compiled_string = '\n'.join(
    f'----\ntitle: { event.title }\nhref: { event.href }\n----\n' for event in events_formatted
)

print('\nDone! Here is the Upcoming Events list:\n\n' + compiled_string)
