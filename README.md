# Mission-to-Mars

![unnamed](https://user-images.githubusercontent.com/84881187/129815653-b62e7d2d-b225-4a2b-a671-8323b57bf537.jpg)


## Project Overview

Our client has tasked us with using BeautifulSoup and Splinter to scrape full-sized images of Mars' hemisphere with titles. We stored the scraped images in a Mongo database, and used HTML code to display the data we collected on a web page. We altered the design of the page to accomodate the new images.


## Code Process


Our first task was to scrape full-resolution images of Mars' Hemisphere and their titles to our Mongo Database. We scraped the images from this web page: https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars


We refactored our code to allow us to:

  - have a list that will hold the image URL and the titles
  - write code to retrieve the hemisphere images with a .jpg extension
  - loop through the full-reolution image URLs and save all the pertinent data information in a dictionary of items.


Next we updated our HTML file to display our data. We modified our index.html file to access our database and retrieve the necessary data as it looped through the disctionary. By running our app.py, and opening the index.html file, we can click "Scrape New Data" to display all of our scraped data onto our webpage.

We made added a few Bootstrap 3 Components to make our visualization web page mobile responsive and thematic. 

Please see below for a screenshot of the modified webpage:

![WebPage_1](https://user-images.githubusercontent.com/84881187/129816693-2976a188-887a-4b30-ac87-1fba8893140a.PNG)
