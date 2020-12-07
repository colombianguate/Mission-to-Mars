# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


get_ipython().system('which chromedriver')


# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path':'C:\webdrivers\chromedriver.EXE'}
browser = Browser('chrome', **executable_path, headless=False)



# Visit the mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)




html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('ul.item_list li.slide')



slide_elem.find("div", class_='content_title')


# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find("div", class_='content_title').get_text()
news_title


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
news_p


# ### Featured Images


# Visit URL
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)


# Find and click the full image button
full_image_elem = browser.find_by_id('full_image')
full_image_elem.click()


# Find the more info button and click that
browser.is_element_present_by_text('more info', wait_time=1)
more_info_elem = browser.links.find_by_partial_text('more info')
more_info_elem.click()


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# Find the relative image url
img_url_rel = img_soup.select_one('figure.lede a img').get("src")
img_url_rel


# Use the base URL to create an absolute URL
img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
img_url


df = pd.read_html('http://space-facts.com/mars/')[0]
df.columns=['description', 'value']
df.set_index('description', inplace=True)
df


df.to_html()


browser.quit()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres


# 1. Use browser to visit the URL 
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)



# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

base_url = 'https://astrogeology.usgs.gov/'

# 3. Write code to retrieve the image urls and titles for each hemisphere.

#parse the HTMl
html = browser.html
html_soup=soup(html, 'html.parser')

divs_list = html_soup.find_all('div', class_ ='item')

#iterating through the obejcts to get the titles
titles = [i.find('h3').get_text() for i in divs_list]

for i in titles:
    #empty dictionary
    hemisphere={
        'img_url': f"{base_url}{img_url}",
        'title' : title
    }
    
    browser.find_by_text(i).click()
    html_soup_2 = soup(browser.html, "html.parser")
    img_url= html_soup_2.find('img', class_ = 'wide-image')["src"]
    title = i
    
    #add to list
    hemisphere_image_urls.append(hemisphere)
    browser.visit(url)   



# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# 5. Quit the browser
browser.quit()



