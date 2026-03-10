import reflex as rx

config = rx.Config(
    app_name="handyman",
    # Python backend runs on 8001 behind nginx; nginx is the public-facing port.
    backend_host="127.0.0.1",
    backend_port=8001,
    # Production URL — the frontend JS uses this to open the WebSocket.
    api_url="https://handyman-service-site.fly.dev",
    plugins=[rx.plugins.SitemapPlugin()],
)
