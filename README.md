# Auto UI Assist
[WIP Idea Canvas] https://www.figma.com/file/4qYTMikqQXniv77Yh0HZCh/UI-Assist?type=whiteboard&node-id=0-1&t=UIlPgcAWoWSZxHfM-0 

An independent multi-platform assistant to help you with your daily tasks on your computer.

## Setup

### Server Setup
1. Install Python 3.10
2. Use the following pip command to install the required packages
```bash
pip install anthropic python-dotenv fastapi pydantic
```
3. Create a .env file copied from sample.env and fill in the required values.

### Client Setup
1. Install Python 3.10
2. Use the following pip command to install the required packages
```bash
pip install anthropic python-dotenv fastapi pydantic
```
3. Create a .env file copied from sample.env and fill in the required values.

### Start Server
```bash
cd api
uvicorn app:app --reload
```

### Start Client
Put in your query in the .env file and run the following command
```bash
cd app/windows
python main.py
```
