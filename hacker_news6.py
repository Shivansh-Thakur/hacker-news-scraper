import requests
from bs4 import BeautifulSoup
import pprint

def grab_links_and_subtext(num_of_pages, mega_links, mega_subtext):
    links_and_subtexts = []
    for page in range(1, num_of_pages + 1):
        res = requests.get("https://news.ycombinator.com/news?p=" + str(page))
        soup = BeautifulSoup(res.text, 'html.parser')
        links = soup.select(".titlelink")
        subtext = soup.select(".subtext")
        if len(mega_links) == 0 and len(mega_subtext) == 0:
            mega_links = links
            mega_subtext = subtext
        else:
            mega_links += links
            mega_subtext += subtext
        links_and_subtexts.append(mega_links)
        links_and_subtexts.append(mega_subtext)
    return links_and_subtexts
 
def sort_stories_by_votes(hnlist):
    return sorted(hnlist, key = lambda k : k['votes'], reverse = True)

def create_custom_hn(mega_links, mega_subtext):
    hn = []
    for idx, item in enumerate(mega_links):
        title = mega_links[idx].getText()
        href = mega_links[idx].get('href', None)
        vote = mega_subtext[idx].select('.score')
        if len(vote):
            points = int(vote[0].getText().replace(' points', ''))
            if points > 99:
                hn.append({'title' : title, 'link' : href, 'votes' : points})
    return sort_stories_by_votes(hn)

if __name__ == '__main__':
    num_of_pages = int(input('Enter number of pages you want to scrape : '))
    mega_links = list()
    mega_subtext = list()
    links_and_subtexts = grab_links_and_subtext(num_of_pages, mega_links, mega_subtext)
    pprint.pprint(create_custom_hn(links_and_subtexts[0], links_and_subtexts[1]))