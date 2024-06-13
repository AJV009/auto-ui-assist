module.exports = {
    apps: [{
        name: "AutoUIAssist API",
        script: "source autoui/bin/activate; uvicorn app:app --host 0.0.0.0 --port 8000",
        watch: true,
        max_memory_restart: "1000M",
        autorestart: true,
        max_restarts: 10,
    }]
}
