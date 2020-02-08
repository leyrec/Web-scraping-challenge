# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import pandas as pd
import requests
import pymongo


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver. For Mac users:"/usr/local/bin/chromedriver"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                JKJKhnjknb jb  
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=True)


def scrape():
    browser = init_browser()

    # 1. Mars News
    url_1= 'https://mars.nasa.gov/news/'
    browser.visit(url_1)
    html_1 = browser.html
    soup_1 = bs(html_1, "html.parser")
   
    news_title= soup_1.find('div', class_= "content_title").text
    news_p= soup_1.find('div', class_= "rollover_description_inner").text
    print("----------------------------------------------------------------------------------------------------------")
    print(news_title)
    print(news_p)

    # 2. Featured Image
    url_2 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url_2) 
    html_2 = browser.html
    soup_2 = bs(html_2, "html.parser") 

    full_image_button=browser.find_by_id('full_image')
    full_image_button.click()
    more_info_button=browser.links.find_by_partial_text('more info')
    more_info_button.click()
    xpath = '//figure[@class="lede"]'
    results_2 = browser.find_by_xpath(xpath)
    img = results_2[0]
    img.click()
    print(img)

    html_2b = browser.html
    soup_2b = bs(html_2b, "html.parser")
    featured_image_url = soup_2b.find("img")['src']
    print(featured_image_url)
    
    # 3. Mars Weather
    url_3 = 'https://twitter.com/marswxreport?lang=en'
    tweet_response=requests.get(url_3)
    soup_3 = bs(tweet_response.text, "html.parser") 
    
    mars_weather= soup_3.find_all('div', class_= "js-tweet-text-container")
    mars_weather_latest= mars_weather[0].text.strip()
    mars_weather_latest

    # 4. Mars Facts
    url_4 ='https://space-facts.com/mars/'
    tables = pd.read_html(url_4)
    df=tables[0]
    df.columns = ['Mars Facts', ' ']
    df.set_index('Mars Facts', inplace=True)
    html_table = df.to_html (border=0)

    # 5. Mars Hemispheres
    url_5 = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url_5)
    html_5 = browser.html
    soup_5 = bs(html_5, "html.parser")
    # Create an empty list to place the results
    hemisphere_image_urls = []

    # Collect results in an iterable list
    results_5 = soup_5.find("div", class_ = "collapsible results" )
    #option 2: results = soup_5.find("div", class_ = "result-list" )
    hemispheres = results_5.find_all("div", class_="item")

    #Loop through results to get image title and image link
    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
        title = title.replace("Enhanced", "")
        end_link = hemisphere.find("a")["href"]
        # Url link to the full resolution hemisphere image
        image_link = "https://astrogeology.usgs.gov/" + end_link
        # Use Splinter to visit the webpage that contains the full resolution image 
        browser.visit(image_link)
        html_5b = browser.html
        soup_5b=bs(html_5b, "html.parser")
        # Select the class with the full resolution hemisphere image link
        downloads = soup_5b.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        #Append the dictionary with the image url string and the hemisphere title to a list
        hemisphere_image_urls.append({"title": title, "img_url": image_url})
        
        
    #Dictionary containing all Mars info scrapped

    mars_info = {
        "news_title": news_title,
        "news_p": news_p, 
        "featured__image_url": featured_image_url, 
        "mars_weather_latest": mars_weather_latest,
        "html_table":html_table, 
        "hemisphere_image_urls": hemisphere_image_urls
        } 
        
    return mars_info
