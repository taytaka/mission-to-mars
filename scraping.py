# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

# Create scraping function
def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres": hemispheres(browser)
    }
    # Stop webdriver and return data
    browser.quit()
    return data

# Create news function
def mars_news(browser):

    # Scrape Mars News
    # Visit the Mars NASA news site
    url = 'https://redplanetscience.com'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Set up HTML parser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    #Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None
    
    return news_title, news_p

# ## JPL Space Images Featured Image

# Create image function
def featured_image(browser):

    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting HTML with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url

# ## Mars Facts

# Create facts function
def mars_facts():



    # Create try/except:
    try:
        # use 'read_html' to scrape the facts table into a DataFrame
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None

    # Assign columns and set index of DataFrame
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)
    
    # Convert DataFrame to HTML, add bootstrap
    return df.to_html()

# ## Mars Hemispheres Images

# Create hemispheres function
def hemispheres(browser):

    url = 'https://marshemispheres.com/'
    browser.visit(url)
    
    # Create try/except:
    try:
        # 2. Create a list to hold the images and titles.
        hemisphere_image_urls = []
        # 3. Write code to retrieve the image urls and titles for each hemisphere.
        links = browser.find_by_css('a.product-item img')

        for i in range(len(links)):
            hemisphere = {}
            
            browser.find_by_css('a.product-item img')[i].click()
            
            sample_elem = browser.links.find_by_text('Sample').first
            hemisphere['img_url'] = sample_elem['href']
            
            hemisphere['title'] = browser.find_by_css('h2.title').text
            
            hemisphere_image_urls.append(hemisphere)
            
            browser.back()

    except BaseException:
        return None

    return hemisphere_image_urls

if __name__ == "__main__":
    # If running as a script, print scraped data
    print(scrape_all())