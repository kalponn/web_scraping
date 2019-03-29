# Import BeautifulSoup
from bs4 import BeautifulSoup
import time
import requests
import pandas as pd
from splinter import Browser

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)

# In[2]:
def scrape():
    #create a python dictionary to hold the results
    mars_dict = {}
    # initialize the browser
    browser = init_browser()
    
    ### NASA Mars New
    # Visit the following URL 
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    time.sleep(1)

    #scrape the mars site into soup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    latest = soup.find('ul', class_='item_list')

    latest_hl = latest.find('li')

    news_title = latest_hl.find('div',class_='content_title').text

    news_p =  latest_hl.find('div',class_='article_teaser_body').text

    mars_dict["news_title"] = news_title
    mars_dict["news_para"] = news_p

    ### JPL Mars Space Images - Featured Image
    # Visit the following URL
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

    #use splinter to navigate thru the pages
    time.sleep(5)
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(5)
    browser.click_link_by_partial_text('more info')

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    #find full resulution image
    #results = soup.find_all('div', class_='download_tiff')
    #for result in results:
    #    image_data = result.find('p')
    #    if image_data.text.find('Full-Res JPG'):
    #        fullres_data = image_data.find('a')
    #        fullres_image_url = "https:" +  fullres_data['href']
    #        print(fullres_image_url)

    #find full image url
    results = soup.find('article')
    url_path = results.find('figure', 'lede').a['href']
    url_link = "https://www.jpl.nasa.gov"
    featured_image_url = url_link + url_path
    #print(featured_image_url)
    mars_dict["featured_image_url"] = featured_image_url


    ### Mars Weather
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)  
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    latest_tweet = soup.find('div', class_='js-tweet-text-container')
    mars_weather = latest_tweet.find('p').text
    mars_dict["mars_weather"] = mars_weather
	

    ### Mars Facts
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    df = tables[0]
    df.columns = ["Description", "Value"]
    df.set_index('Description', inplace=True)
    
    html_table = df.to_html()
    remove_nl = html_table.replace('\n' , '')
    mars_dict["mars_facts"] = remove_nl


    ### Mars Hemispheres
    mars_image_urls = []
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

    #cerberus hemisphere
    browser.click_link_by_partial_text('Cerberus Hemisphere')
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    download_link = soup.find('div', class_='downloads').a['href']
    cerberus = {
        "title": "Cerberus Hemisphere",
        "img_url": download_link
    }

    mars_image_urls.append(cerberus)

    ## go back to the main page
    browser.click_link_by_partial_text('Back')
    browser.click_link_by_partial_text('Schiaparelli Hemisphere')
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    download_link = soup.find('div', class_='downloads').a['href']
    Schiaparelli = {
        "title": "Schiaparelli Hemisphere",
        "img_url": download_link
    }

    mars_image_urls.append(Schiaparelli)


    browser.click_link_by_partial_text('Back')
    browser.click_link_by_partial_text('Syrtis Major Hemisphere')
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    download_link = soup.find('div', class_='downloads').a['href']
    Syrtis = {
        "title": "Syrtis Major Hemisphere",
        "img_url": download_link
    }
    mars_image_urls.append(Syrtis)

    browser.click_link_by_partial_text('Back')
    browser.click_link_by_partial_text('Valles Marineris Hemisphere')
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    download_link = soup.find('div', class_='downloads').a['href']
    Valles = {
        "title": "Valles Marineris Hemisphere",
        "img_url": download_link
    }
    mars_image_urls.append(Valles)
    
    mars_dict["hemisphere_img_urls"] = mars_image_urls
    
    # Close the browser after scraping
    browser.quit()
    
    #return results
    return mars_dict

