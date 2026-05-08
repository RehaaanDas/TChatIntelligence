# TChatIntelligence
Uses selenium to interact with discords UI (a separate discord botting framework for anyone to bot accounts is on its way) and read responses sent by discorders as the "LLMs" responses, and beams it to the client page through websockets.

## Usage
run `python3 TCI.py "your username"` to run the server and visit the `TCI.html` client page that connects to it

## Diff Servers?
change `driver.get()` argument in source code to url to channel you want to run the bot on
