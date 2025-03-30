from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
import pyautogui


chrome_options = Options()
chrome_options.add_argument("--user-data-dir=D:\\generate_image\\whatsapp_session")  
chrome_options.add_argument("--profile-directory=Default")

service = Service(r"D:\\generate_image\\chromedriver.exe") 
driver = webdriver.Chrome(service=service, options=chrome_options) 


driver.get("https://web.whatsapp.com")

try:
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '//div[@role="textbox"]')))
    print("WhatsApp Web loaded successfully.")
except:
    print("Failed to load WhatsApp Web. Scan QR code manually.")
    driver.quit()
    exit()

def open_meta_ai_chat():
    print("Searching for Meta AI chat...")
    search_box = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, '//div[@role="textbox"]'))
    )
    search_box.click()
    search_box.send_keys("Meta AI")
    time.sleep(3)
    search_box.send_keys(Keys.ENTER)
    time.sleep(5)
    print("Meta AI chat opened!")

def send_prompt_to_meta_ai(prompt):
    print(f"Sending prompt: {prompt}")
    chat_box = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]'))
    )
    chat_box.click()
    time.sleep(1)
    chat_box.send_keys(prompt)
    time.sleep(1)
    chat_box.send_keys(Keys.ENTER)
    print("Prompt sent!")

def wait_for_new_image(timeout=90):
    print("Waiting for new image generation...")
    start_time = time.time()
    previous_images = driver.find_elements(By.XPATH, '//img[contains(@src, "blob:")]')

    while time.time() - start_time < timeout:
        try:
            current_images = driver.find_elements(By.XPATH, '//img[contains(@src, "blob:")]')

            if len(current_images) > len(previous_images):  # Detect new image
                print("New image detected!")
                return current_images[-1]  # Return the latest image
        except Exception as e:
            print(f"Error: {str(e)}")
        
        time.sleep(3)
    
    print("Timeout waiting for new image")
    return None

def right_click_and_save(image_element):
    print("Right-clicking on image and saving...")

    
    driver.execute_script("arguments[0].scrollIntoView();", image_element)
    time.sleep(2)

    
    actions = ActionChains(driver)
    actions.context_click(image_element).perform()
    time.sleep(2)

    
    pyautogui.press('down')  
    time.sleep(1)
    pyautogui.press('down')
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(2)

    
    save_path = os.path.join(os.path.expanduser("~"), "Downloads", f"meta_ai_image_{int(time.time())}.png")
    pyautogui.write(save_path)
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(2) 

    print(f"Image saved successfully at {save_path}!")

def main():
    open_meta_ai_chat()

    while True:
        user_prompt = input("\nEnter your prompt (or 'exit'): ").strip()
        if user_prompt.lower() == 'exit':
            break

        send_prompt_to_meta_ai(user_prompt)

        new_image = wait_for_new_image()
        if new_image:
            right_click_and_save(new_image)
        else:
            print("No new image received. Try adjusting your prompt.")

    print("\nClosing WhatsApp Web...")
    driver.quit()

if __name__ == "__main__":
    main()
