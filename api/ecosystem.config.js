// PM2 Configuration for Auto UI Assist API

module.exports = {
    apps: [{
        // Name of the application
        name: "auto-ui-assist-api",
        
        // Command to run the application
        // This activates the virtual environment and starts the FastAPI server
        script: "source autoui/bin/activate; uvicorn app:app --host 0.0.0.0 --port 8000",
        
        // Disable file watching to prevent unnecessary restarts
        watch: false,
        
        // Restart the app if it exceeds 1GB of memory usage
        max_memory_restart: "1000M",
        
        // Automatically restart the application if it crashes
        autorestart: true,
        
        // Maximum number of times to restart the app within a short period
        max_restarts: 10,
    }]
}

// This configuration file is used by PM2 (Process Manager 2) to manage the Auto UI Assist API process.
// It ensures that the API is always running, automatically restarts it if it crashes or uses too much memory,
// and limits the number of rapid restarts to prevent issues.
