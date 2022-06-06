# hidden-chat
A set of utilities that gives access to the hidden chat.


Hidden-chat consists of 2 utilities:
1. `reader.py` is for showing and saving all the messages 
2. `sender.py` is for issuing a new token, saving it locally and sending messages


## Quick start


```bash
python src/reader.py # to be able to see the messages from the chat
```
In a separate terminal:
```bash
# to register a new user and send a message to the chat
python src/sender.py -m "The test message to the chat" --user myUser
```

## Setting environment
```bash
python -m venv venv && source venv/bin/activate
```
