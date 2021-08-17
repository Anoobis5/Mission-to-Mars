# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager
import re


def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path':'C:/Users/icani/Desktop/Class/work/Mars_Scraping/chromedriver'}

    browser = Browser('chrome', **executable_path, headless=False)
    
    news_title, news_paragraph = mars_news(browser)
    hemisphere = scrape_hemisphere_data(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres": hemisphere,
        "last_modified": dt.datetime.now()
        
    }

    # Stop webdriver and return data
    #browser.quit()
    return data


def mars_news(browser):

    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_p


def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url

def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html()


def scrape_hemisphere_data(browser):

    # visit the URL 
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    
    # Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # Parse the data
    
    html = browser.html
    urls_soup = soup(html, 'html.parser')

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    divs = urls_soup.find("div", class_='collapsible results')
    anchors = divs.find_all('a')
    relative_urls = set([anchor['href'] for anchor in anchors])
    base_url = 'https://astrogeology.usgs.gov'
   
    for relative_url in relative_urls:
        print(f'Running {relative_url}')
        hemispheres = {}
        
        full_url = f'{base_url}{relative_url}'
        browser.visit(full_url)
        browser.links.find_by_text('Open').click()

        
        html = browser.html
        urls_soup = soup(html, 'html.parser')
        
        downloads_div = urls_soup.find('div', class_='downloads')
        img_anchor = downloads_div.find('a', text=re.compile('Sample'))
        img_url = img_anchor['href']
        #print(f'--> url: {img_url}')
        
        title_elem = urls_soup.select_one('div.content')
        title = title_elem.find("h2", class_='title').get_text()
        #print(f'--> title: {title}')
        hemispheres = {
            'img_url': img_url,
            'title': title,
        }
        hemisphere_image_urls.append(hemispheres)
       
    return hemisphere_image_urls

if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())