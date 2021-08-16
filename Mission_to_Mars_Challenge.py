# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import re

executable_path = {'executable_path':'C:/Users/icani/Desktop/Class/work/Mars_Scraping/chromedriver'}

browser = Browser('chrome', **executable_path, headless=False)

# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)

html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')

slide_elem.find('div', class_='content_title')

# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### Featured Images

# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ## Mars Facts

df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df

df.to_html()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# 1. Use browser to visit the URL 
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
#'https://marshemispheres.com/'

browser.visit(url)

# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# Parse the data
html = browser.html
urls_soup = soup(html, 'html.parser')

# 3. Write code to retrieve the image urls and titles for each hemisphere.

divs = urls_soup.find("div", class_='collapsible results')
anchors = divs.find_all('a')
relative_urls = set([anchor['href'] for anchor in anchors])
print(f'Found {len(relative_urls)} URLs')

base_url = 'https://astrogeology.usgs.gov'

for relative_url in relative_urls:
    hemispheres = {}
    
    full_url = f'{base_url}{relative_url}'
    browser.visit(full_url)
    browser.links.find_by_text('Open').click()
    
    html = browser.html
    urls_soup = soup(html, 'html.parser')
    
    downloads_div = urls_soup.find('div', class_='downloads')
    img_anchor = downloads_div.find('a', text=re.compile('Sample'))
    img_url = img_anchor['href']
    print(f'--> url: {img_url}')
    
    title_elem = urls_soup.select_one('div.content')
    title = title_elem.find("h2", class_='title').get_text()
    print(f'--> title: {title}')
    hemispheres = {
        'img_url': img_url,
        'title': title,
    }
    hemisphere_image_urls.append(hemispheres)

# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls

# 5. Quit the browser
browser.quit()
