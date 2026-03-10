import reflex as rx

config = rx.Config(
    app_name="handyman",
    backend_host="0.0.0.0",
    backend_port=8000,
    plugins=[rx.plugins.SitemapPlugin()],
)
