import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
import threading
import asyncio
from websockets.asyncio.server import serve

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(options=options)

#bot channel
driver.get("https://discord.com/channels/251072485095636994/251116850132287490")
input("Login then Enter to continue...")
print(driver.title)

curr = ""

def send(text):
    textbox = driver.find_element(by=By.CSS_SELECTOR, value="div[role='textbox']")
    textbox.send_keys(f"{text}\n")
    global curr
    curr = text

async def feed(action):
    seen = []
    while True:
        msgs = driver.find_elements(by=By.CLASS_NAME, value="hasReply_c19a55")
        for msg in msgs:
            try:
                if(msg not in seen):
                    content = msg.find_elements(by=By.CLASS_NAME, value="messageContent_c19a55");
                    prompt = msg.find_element(by=By.CLASS_NAME, value="repliedMessage_c19a55").get_attribute("aria-label").split(" replying to ");
                    if(prompt[1] == sys.argv[1]):
                        if(content[0].text == curr): await action(content[1].text)
                    seen.append(msg)
            except: 
                pass

async def incoming(websocket):
    t = threading.Thread(target=lambda: asyncio.run(feed(websocket.send)))
    t.start()
    async for message in websocket:
        print(message)
        send(message)

async def main():
    async with serve(incoming, "localhost", 8003) as server:
        await server.serve_forever()

asyncio.run(main())
