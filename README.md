# Auto UI Assist
[WIP Idea Canvas] https://www.figma.com/file/4qYTMikqQXniv77Yh0HZCh/UI-Assist?type=whiteboard&node-id=0-1&t=UIlPgcAWoWSZxHfM-0 

An independent multi-platform assistant to help you with your daily tasks on your computer.

## API Server Setup

### Prerequisites

- Python 3.x
- `git` (optional, for cloning the repository)

### Installation

1. **Clone the repository (if using version control):**
    ```sh
    git clone https://github.com/AJV009/auto-ui-assist
    cd auto-ui-assist/api
    ```

2. **Create a virtual environment:**
    ```sh
    python3 -m venv autoui
    ```

3. **Activate the virtual environment:**
    ```sh
    source autoui/bin/activate
    ```

4. **Install the required packages:**
    ```sh
    pip install -r requirements.txt
    ```

### Running the Application

1. **Activate the virtual environment (if not already activated):**
    ```sh
    source autoui/bin/activate
    ```

2. **Run the FastAPI application using `uvicorn`:**
    ```sh
    uvicorn app:app --reload
    ```

   This will start the server on `http://127.0.0.1:8000`.

### Running the Application using pm2

1. **Install pm2:**
    ```sh
    npm install pm2 -g
    ```
    Note: You can setup pm2 as a service using `pm2 startup`.

2. **Run the FastAPI application using `pm2`:**
    ```sh
    pm2 start
    ```

3. **Save the process list:**
    ```sh
    pm2 save
    ```

    This will start the server on `http://127.0.0.1:8000`.

## Application Setup

### Readme to be updated here...
