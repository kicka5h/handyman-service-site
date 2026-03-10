import reflex as rx

config = rx.Config(
    app_name="handyman",
    # Production URL — the frontend JS uses this to open the WebSocket.
    api_url="https://handyman-service-site.fly.dev",
    plugins=[rx.plugins.SitemapPlugin()],
)
