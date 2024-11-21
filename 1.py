from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import pyautogui
from config import username, password
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os


max_unique_posts = 3








def like_the_post():
    try:
        like_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.button.button-like.button-blue.no-border.transparent.p-0'))
        )
        like_button.click()
        print("Like button clicked successfully.")
    except Exception as e:
        print(f"Failed to click like button: {e}")

def read_existing_post_ids(file_path):
    if not os.path.exists(file_path):
        return set()
    with open(file_path, 'r') as file:
        return set(file.read().splitlines())

def write_post_id(file_path, post_id):
    with open(file_path, 'a') as file:
        file.write(post_id + '\n')


def redirect_to_main():
    try:
        # Wait for the redirection page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//a[contains(@href, "https://www.mmk-portal.mmk.ru/")]'))
        )
        
        # Extract the URL from the redirection page
        redirect_link = driver.find_element(By.XPATH, '//a[contains(@href, "https://www.mmk-portal.mmk.ru/")]')
        post_url = redirect_link.get_attribute('href')
        
        # Navigate to the extracted URL
        driver.get(post_url)
        
        # Wait for the post page to load (you might need to adjust the sleep time)
        time.sleep(2)
        
        # Use WebDriverWait to wait for the like button to be present and clickable

    except Exception as e:
        print(f"Redirection page not found or link extraction failed: {e}")

def redirect_to_last_page():
    try:
        pagination_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="pagination__list"]'))
        )
        
        # Wait for the last page number to be present
        last_page_link = WebDriverWait(pagination_element, 10).until(
            EC.presence_of_element_located((By.XPATH, './/div[@class="pagination__list-item"][last()]/a'))
        )
        
        # Click the last page number
        last_page_link.click()
        print("Navigated to the last page successfully.")
    except Exception as e:
        print(f"Failed to navigate to the last page: {e}")

def comment_post1():
    
    existing_post_ids = read_existing_post_ids('commented_posts.txt')



    try:
        post_elements = driver.find_elements(By.XPATH, '//div[contains(@class, "news-list_item") or contains(@class, "news-list__item")]')
        print(f"Post elements found: {post_elements}")  # Debugging: Print the number of post elements

        for post_element in post_elements:
            # Print the element's HTML for debugging
            # print(post_element.get_attribute('outerHTML'))

            # Find the <a> tag within the post element
            a_tag = post_element.find_element(By.TAG_NAME, 'a')
            if a_tag is None:
                print("No <a> tag found in this element, skipping this element.")
                continue
            
            # Get the href attribute from the <a> tag
            post_url = a_tag.get_attribute('href')
            if post_url is None:
                print("Post URL is None, skipping this element.")
                continue
            
            post_id = post_url.split('/')[-2] if post_url.endswith('/') else post_url.split('/')[-1]
            
            print(post_id)
            if post_id not in existing_post_ids:
                # Navigate to the post page
                driver.get(f'https://www.mmk-portal.mmk.ru/{post_url}')
                
                # Wait for the post page to load (you might need to adjust the sleep time)
                time.sleep(2)
                
                # Comment on the post (this part will be implemented later)
                # For now, let's just print that we are commenting
                print(f"Commenting on post with ID: {post_id}")
                
                # Write the post ID to the file
                write_post_id('commented_posts.txt', post_id)


    except Exception as e:
        print(f"Failed to extract post IDs: {e}")
        
def comment_post():
    existing_post_ids = read_existing_post_ids('commented_posts.txt')

    try:
        # Updated XPath to match both 'news-list item' and 'news-list__item'
        post_elements = driver.find_elements(By.XPATH, '//div[contains(@class, "news-list_item") or contains(@class, "news-list__item")]')
        print(f"Post elements found: {len(post_elements)}")  # Debugging: Print the number of post elements

        for post_element in post_elements:
            try:
                # Find the <a> tag within the post element
                a_tag = post_element.find_element(By.XPATH, './/div[@class="item-top"]/a')
                if a_tag is None:
                    print("No <a> tag found in this element, skipping this element.")
                    continue
                
                # Get the href attribute from the <a> tag
                post_url = a_tag.get_attribute('href')
                if post_url is None:
                    print("Post URL is None, skipping this element.")
                    continue
                
                post_id = post_url.split('/')[-2] if post_url.endswith('/') else post_url.split('/')[-1]
                
                print(post_id)
                if post_id not in existing_post_ids:
                    # Navigate to the post page
                    driver.get(post_url)
                    
                    # Wait for the post page to load (you might need to adjust the sleep time)
                    time.sleep(2)
                    
                    # Comment on the post (this part will be implemented later)
                    # For now, let's just print that we are commenting
                    print(f"Commenting on post with ID: {post_id}")
                    
                    # Write the post ID to the file
                    write_post_id('commented_posts.txt', post_id)
            except Exception as e:
                print(f"Failed to process post element: {e}")

    except Exception as e:
        print(f"Failed to extract post IDs: {e}")




# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--start-maximized")


driver = webdriver.Chrome(options=chrome_options)
driver.get('https://www.mmk-portal.mmk.ru/')  # Update this URL to the actual news page

# Wait for the page to load
time.sleep(1)  # You might want to use WebDriverWait for more robust waiting

pyautogui.typewrite(username)

pyautogui.press("tab")

pyautogui.typewrite(password)

pyautogui.press("enter")





redirect_to_main()





# for unique_posts_commented in range(max_unique_posts):
redirect_to_last_page()
comment_post()

# driver.get('https://www.mmk-portal.mmk.ru/news/')
time.sleep(2)


time.sleep(20)
driver.quit()



# Failed to process post element: Message: no such element: Unable to locate element: {"method":"xpath","selector":".//div[@class="item-top"]/a"}
#   (Session info: chrome=130.0.6723.117); For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#no-such-element-exception
# Stacktrace:
#         GetHandleVerifier [0x00007FF7DA9138A5+3004357]
#         (No symbol) [0x00007FF7DA5A9970]
#         (No symbol) [0x00007FF7DA45582A]
#         (No symbol) [0x00007FF7DA4A5B8E]
#         (No symbol) [0x00007FF7DA4A5E7C]
#         (No symbol) [0x00007FF7DA4993DC]
#         (No symbol) [0x00007FF7DA4CBC1F]
#         (No symbol) [0x00007FF7DA4992A6]
#         (No symbol) [0x00007FF7DA4CBDF0]
#         (No symbol) [0x00007FF7DA4EBA4C]
#         (No symbol) [0x00007FF7DA4CB983]
#         (No symbol) [0x00007FF7DA497628]
#         (No symbol) [0x00007FF7DA498791]
#         GetHandleVerifier [0x00007FF7DA93A00D+3161901]
#         GetHandleVerifier [0x00007FF7DA98E060+3506048]
#         GetHandleVerifier [0x00007FF7DA98400D+3465005]
#         GetHandleVerifier [0x00007FF7DA700EEB+830987]
#         (No symbol) [0x00007FF7DA5B467F]
#         (No symbol) [0x00007FF7DA5B09D4]
#         (No symbol) [0x00007FF7DA5B0B6D]
#         (No symbol) [0x00007FF7DA5A0149]
#         BaseThreadInitThunk [0x00007FFE91517AC4+20]
#         RtlUserThreadStart [0x00007FFE93A8A8C1+33]
