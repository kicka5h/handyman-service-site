"""Handyman Service Website — Full Stack Python with Reflex + FastAPI."""
import asyncio
import fastapi
import reflex as rx
from pydantic import BaseModel

from handyman.contact_backend import handle_submission, init_db

init_db()

# ── Brand & Content Data ──────────────────────────────────────────────────────

BRAND = {
    "name": "ProHandyman",
    "tagline": "Your Trusted Local Home Expert",
    "phone": "(555) 867-5309",
    "email": "hello@prohandyman.com",
    "address": "Greater Seattle Area, WA",
}

SERVICES = [
    {
        "icon": "hammer",
        "title": "General Repairs",
        "description": "From fixing leaky faucets to patching drywall, we handle all your repair needs quickly and professionally.",
        "color": "#3B82F6",
    },
    {
        "icon": "wrench",
        "title": "Plumbing",
        "description": "Faucet replacement, toilet repairs, pipe fixes, and more to keep your water flowing right.",
        "color": "#06B6D4",
    },
    {
        "icon": "zap",
        "title": "Electrical",
        "description": "Outlet installation, ceiling fans, light fixtures, and basic wiring done safely and to code.",
        "color": "#F59E0B",
    },
    {
        "icon": "paint-roller",
        "title": "Painting",
        "description": "Interior and exterior painting with clean, professional results that transform your space.",
        "color": "#8B5CF6",
    },
    {
        "icon": "ruler",
        "title": "Carpentry",
        "description": "Custom shelving, furniture assembly, door repairs, and more crafted with skill and precision.",
        "color": "#10B981",
    },
    {
        "icon": "home",
        "title": "Home Maintenance",
        "description": "Seasonal maintenance, gutter cleaning, pressure washing, and upkeep to protect your investment.",
        "color": "#EF4444",
    },
]

WHY_US = [
    {
        "icon": "shield-check",
        "title": "Licensed & Insured",
        "desc": "Fully licensed and insured for your complete peace of mind.",
    },
    {
        "icon": "clock",
        "title": "Always On Time",
        "desc": "We respect your schedule and show up exactly when promised.",
    },
    {
        "icon": "star",
        "title": "5-Star Rated",
        "desc": "Hundreds of happy customers across the community.",
    },
    {
        "icon": "badge-dollar-sign",
        "title": "Fair Pricing",
        "desc": "Transparent quotes with no hidden fees or surprises.",
    },
]


# ── State ─────────────────────────────────────────────────────────────────────

class State(rx.State):
    submitted: bool = False

    async def handle_contact_submit(self, form_data: dict):
        """Save to SQLite and email the owner. Runs off the event loop thread."""
        await asyncio.to_thread(
            handle_submission,
            form_data.get("name", ""),
            form_data.get("email", ""),
            form_data.get("phone", ""),
            form_data.get("message", ""),
        )
        self.submitted = True

    def reset_form(self):
        self.submitted = False


# ── Navbar ────────────────────────────────────────────────────────────────────

def navbar() -> rx.Component:
    return rx.box(
        rx.flex(
            # Logo
            rx.hstack(
                rx.icon("wrench", color="#D97706", size=22),
                rx.text(
                    BRAND["name"],
                    color="white",
                    font_size="1.25rem",
                    font_weight="700",
                    letter_spacing="-0.02em",
                ),
                spacing="2",
                align="center",
            ),
            # Desktop nav links
            rx.hstack(
                rx.link(
                    "Services",
                    href="#services",
                    color="rgba(255,255,255,0.75)",
                    font_weight="500",
                    text_decoration="none",
                    _hover={"color": "white"},
                ),
                rx.link(
                    "Why Us",
                    href="#why-us",
                    color="rgba(255,255,255,0.75)",
                    font_weight="500",
                    text_decoration="none",
                    _hover={"color": "white"},
                ),
                rx.link(
                    "Contact",
                    href="#contact",
                    color="rgba(255,255,255,0.75)",
                    font_weight="500",
                    text_decoration="none",
                    _hover={"color": "white"},
                ),
                rx.link(
                    rx.button(
                        "Free Quote",
                        size="2",
                        background="#D97706",
                        color="white",
                        border_radius="8px",
                        font_weight="600",
                        cursor="pointer",
                        _hover={"background": "#B45309"},
                    ),
                    href="#contact",
                    text_decoration="none",
                ),
                spacing="6",
                align="center",
                display=["none", "none", "flex"],
            ),
            justify="between",
            align="center",
            width="100%",
            max_width="1200px",
            margin="0 auto",
        ),
        background="#0B3D2E",
        padding_x="2rem",
        padding_y="1rem",
        position="sticky",
        top="0",
        z_index="100",
        box_shadow="0 2px 12px rgba(0,0,0,0.3)",
        width="100%",
    )


# ── Hero ──────────────────────────────────────────────────────────────────────

def hero() -> rx.Component:
    return rx.box(
        rx.center(
            rx.vstack(
                rx.badge(
                    "⭐  Serving the Greater Seattle Area for 15+ Years",
                    variant="soft",
                    color_scheme="amber",
                    size="2",
                    padding="8px 16px",
                    border_radius="999px",
                ),
                rx.heading(
                    "Your Trusted Local ",
                    rx.text.span("Handyman", color="#D97706"),
                    as_="h1",
                    size="9",
                    font_weight="800",
                    color="white",
                    text_align="center",
                    line_height="1.1",
                    letter_spacing="-0.03em",
                ),
                rx.text(
                    "Quality work, fair prices, on time every time. "
                    "From small repairs to big projects — we've got you covered.",
                    color="rgba(255,255,255,0.8)",
                    font_size=["1rem", "1.15rem", "1.2rem"],
                    text_align="center",
                    max_width="600px",
                    line_height="1.7",
                ),
                rx.hstack(
                    rx.link(
                        rx.button(
                            rx.icon("message-square", size=16),
                            "Get Free Quote",
                            size="4",
                            background="#D97706",
                            color="white",
                            cursor="pointer",
                            border_radius="10px",
                            font_weight="600",
                            _hover={"background": "#B45309"},
                            gap="2",
                        ),
                        href="#contact",
                        text_decoration="none",
                    ),
                    rx.link(
                        rx.button(
                            rx.icon("phone", size=16),
                            BRAND["phone"],
                            size="4",
                            variant="outline",
                            color="white",
                            border_color="rgba(255,255,255,0.4)",
                            cursor="pointer",
                            border_radius="10px",
                            font_weight="600",
                            _hover={
                                "background": "rgba(255,255,255,0.08)",
                                "border_color": "white",
                            },
                            gap="2",
                        ),
                        href=f"tel:{BRAND['phone'].replace(' ', '').replace('(', '').replace(')', '').replace('-', '')}",
                        text_decoration="none",
                    ),
                    spacing="4",
                    flex_wrap="wrap",
                    justify="center",
                ),
                spacing="7",
                align="center",
                max_width="750px",
                padding_x="1.5rem",
            ),
        ),
        background="linear-gradient(135deg, #061C10 0%, #0B3D2E 50%, #174D3A 100%)",
        min_height="88vh",
        width="100%",
        display="flex",
        align_items="center",
        justify_content="center",
    )


# ── Services Section ──────────────────────────────────────────────────────────

def service_card(service: dict) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.box(
                rx.icon(service["icon"], size=26, color=service["color"]),
                background=f"{service['color']}18",
                border_radius="12px",
                padding="0.9rem",
                display="inline-flex",
                align_items="center",
                justify_content="center",
            ),
            rx.heading(service["title"], size="4", color="#1E293B"),
            rx.text(
                service["description"],
                color="#64748B",
                font_size="0.92rem",
                line_height="1.65",
                text_align="center",
            ),
            spacing="3",
            align="center",
        ),
        background="white",
        border_radius="16px",
        padding="2rem 1.5rem",
        box_shadow="0 2px 12px rgba(0,0,0,0.06)",
        border="1px solid #F1F5F9",
        transition="all 0.25s ease",
        _hover={
            "box_shadow": "0 10px 32px rgba(0,0,0,0.12)",
            "transform": "translateY(-5px)",
            "border_color": "#E2E8F0",
        },
    )


def services_section() -> rx.Component:
    return rx.box(
        rx.box(id="services"),
        rx.vstack(
            rx.vstack(
                rx.text(
                    "WHAT WE DO",
                    color="#D97706",
                    font_weight="700",
                    font_size="0.82rem",
                    letter_spacing="0.12em",
                ),
                rx.heading("Our Services", size="8", color="#1E293B"),
                rx.text(
                    "From quick fixes to complete renovations — professional quality on every job.",
                    color="#64748B",
                    font_size="1.1rem",
                    text_align="center",
                    max_width="500px",
                ),
                spacing="3",
                align="center",
            ),
            rx.grid(
                *[service_card(s) for s in SERVICES],
                columns=rx.breakpoints(initial="1", sm="2", lg="3"),
                gap="6",
                width="100%",
            ),
            spacing="9",
            align="center",
            width="100%",
            max_width="1200px",
            margin="0 auto",
        ),
        background="#F2FDF7",
        padding_x="2rem",
        padding_y="5rem",
        width="100%",
    )


# ── Why Us Section ────────────────────────────────────────────────────────────

def why_us_card(item: dict) -> rx.Component:
    return rx.vstack(
        rx.box(
            rx.icon(item["icon"], size=26, color="white"),
            background="rgba(217,119,6,0.85)",
            border_radius="50%",
            width="64px",
            height="64px",
            display="flex",
            align_items="center",
            justify_content="center",
            flex_shrink="0",
        ),
        rx.heading(item["title"], size="4", color="white"),
        rx.text(
            item["desc"],
            color="rgba(255,255,255,0.7)",
            text_align="center",
            font_size="0.93rem",
            line_height="1.6",
        ),
        spacing="3",
        align="center",
    )


def why_us_section() -> rx.Component:
    return rx.box(
        rx.box(id="why-us"),
        rx.vstack(
            rx.vstack(
                rx.text(
                    "WHY CHOOSE US",
                    color="#D97706",
                    font_weight="700",
                    font_size="0.82rem",
                    letter_spacing="0.12em",
                ),
                rx.heading("The ProHandyman Difference", size="8", color="white"),
                spacing="3",
                align="center",
            ),
            rx.grid(
                *[why_us_card(i) for i in WHY_US],
                columns=rx.breakpoints(initial="1", sm="2", lg="4"),
                gap="8",
                width="100%",
            ),
            spacing="9",
            align="center",
            width="100%",
            max_width="1100px",
            margin="0 auto",
        ),
        background="linear-gradient(135deg, #0B3D2E 0%, #061C10 100%)",
        padding_x="2rem",
        padding_y="5rem",
        width="100%",
    )


# ── Contact Section ───────────────────────────────────────────────────────────

def contact_info() -> rx.Component:
    return rx.vstack(
        rx.vstack(
            rx.text(
                "GET IN TOUCH",
                color="#D97706",
                font_weight="700",
                font_size="0.82rem",
                letter_spacing="0.12em",
            ),
            rx.heading("Request a Free Quote", size="7", color="#1E293B"),
            rx.text(
                "Describe your project and we'll get back to you within 24 hours "
                "with a free, no-obligation estimate.",
                color="#64748B",
                line_height="1.7",
                font_size="1rem",
            ),
            spacing="4",
            align="start",
        ),
        rx.separator(width="100%"),
        rx.vstack(
            rx.hstack(
                rx.icon("phone", size=18, color="#D97706"),
                rx.text(BRAND["phone"], color="#374151", font_weight="500"),
                spacing="3",
                align="center",
            ),
            rx.hstack(
                rx.icon("mail", size=18, color="#D97706"),
                rx.text(BRAND["email"], color="#374151", font_weight="500"),
                spacing="3",
                align="center",
            ),
            rx.hstack(
                rx.icon("map-pin", size=18, color="#D97706"),
                rx.text(BRAND["address"], color="#374151", font_weight="500"),
                spacing="3",
                align="center",
            ),
            spacing="4",
            align="start",
        ),
        spacing="6",
        align="start",
        flex="1",
        min_width="260px",
    )


def contact_form_widget() -> rx.Component:
    return rx.box(
        rx.cond(
            State.submitted,
            # ── Success state ──
            rx.vstack(
                rx.box(
                    rx.icon("check", size=36, color="white"),
                    background="#10B981",
                    border_radius="50%",
                    width="80px",
                    height="80px",
                    display="flex",
                    align_items="center",
                    justify_content="center",
                ),
                rx.heading("Message Sent!", size="6", color="#1E293B"),
                rx.text(
                    "Thank you! We'll be in touch within 24 hours.",
                    color="#64748B",
                    text_align="center",
                ),
                rx.button(
                    "Send Another Message",
                    on_click=State.reset_form,
                    variant="outline",
                    cursor="pointer",
                    color_scheme="amber",
                ),
                spacing="5",
                align="center",
                padding_y="3rem",
            ),
            # ── Form ──
            rx.form(
                rx.vstack(
                    rx.grid(
                        rx.vstack(
                            rx.text(
                                "Full Name",
                                font_weight="600",
                                color="#374151",
                                font_size="0.88rem",
                            ),
                            rx.input(
                                name="name",
                                placeholder="John Smith",
                                required=True,
                                width="100%",
                            ),
                            spacing="1",
                            width="100%",
                        ),
                        rx.vstack(
                            rx.text(
                                "Email",
                                font_weight="600",
                                color="#374151",
                                font_size="0.88rem",
                            ),
                            rx.input(
                                name="email",
                                type="email",
                                placeholder="john@example.com",
                                required=True,
                                width="100%",
                            ),
                            spacing="1",
                            width="100%",
                        ),
                        columns=rx.breakpoints(initial="1", sm="2"),
                        gap="4",
                        width="100%",
                    ),
                    rx.vstack(
                        rx.text(
                            "Phone",
                            font_weight="600",
                            color="#374151",
                            font_size="0.88rem",
                        ),
                        rx.input(
                            name="phone",
                            placeholder="(555) 123-4567",
                            width="100%",
                        ),
                        spacing="1",
                        width="100%",
                    ),
                    rx.vstack(
                        rx.text(
                            "Describe your project",
                            font_weight="600",
                            color="#374151",
                            font_size="0.88rem",
                        ),
                        rx.text_area(
                            name="message",
                            placeholder="Tell us what you need help with — the more detail, the better!",
                            required=True,
                            rows="5",
                            width="100%",
                            resize="vertical",
                        ),
                        spacing="1",
                        width="100%",
                    ),
                    rx.button(
                        rx.icon("send", size=16),
                        "Send Message",
                        type="submit",
                        size="4",
                        background="#D97706",
                        color="white",
                        cursor="pointer",
                        font_weight="600",
                        border_radius="10px",
                        width="100%",
                        gap="2",
                        _hover={"background": "#B45309"},
                    ),
                    spacing="5",
                    width="100%",
                ),
                on_submit=State.handle_contact_submit,
                width="100%",
            ),
        ),
        background="white",
        border_radius="18px",
        padding="2.5rem",
        box_shadow="0 6px 30px rgba(0,0,0,0.09)",
        border="1px solid #F1F5F9",
        flex="1.2",
        min_width="300px",
        max_width="560px",
    )


def contact_section() -> rx.Component:
    return rx.box(
        rx.box(id="contact"),
        rx.flex(
            contact_info(),
            contact_form_widget(),
            gap="4rem",
            flex_wrap="wrap",
            align="start",
            justify="center",
            max_width="1100px",
            margin="0 auto",
        ),
        background="#F0FDF4",
        padding_x="2rem",
        padding_y="5rem",
        width="100%",
    )


# ── Footer ────────────────────────────────────────────────────────────────────

def footer() -> rx.Component:
    return rx.box(
        rx.flex(
            # Brand
            rx.vstack(
                rx.hstack(
                    rx.icon("wrench", color="#D97706", size=20),
                    rx.text(
                        BRAND["name"],
                        color="white",
                        font_size="1.15rem",
                        font_weight="700",
                    ),
                    spacing="2",
                    align="center",
                ),
                rx.text(
                    BRAND["tagline"],
                    color="rgba(255,255,255,0.45)",
                    font_size="0.88rem",
                ),
                spacing="2",
                align="start",
                min_width="200px",
            ),
            # Quick links
            rx.vstack(
                rx.text("Quick Links", color="white", font_weight="600"),
                rx.link(
                    "Services",
                    href="#services",
                    color="rgba(255,255,255,0.55)",
                    text_decoration="none",
                    _hover={"color": "white"},
                ),
                rx.link(
                    "Why Us",
                    href="#why-us",
                    color="rgba(255,255,255,0.55)",
                    text_decoration="none",
                    _hover={"color": "white"},
                ),
                rx.link(
                    "Contact",
                    href="#contact",
                    color="rgba(255,255,255,0.55)",
                    text_decoration="none",
                    _hover={"color": "white"},
                ),
                spacing="2",
                align="start",
                min_width="140px",
            ),
            # Contact info
            rx.vstack(
                rx.text("Contact Us", color="white", font_weight="600"),
                rx.text(BRAND["phone"], color="rgba(255,255,255,0.55)", font_size="0.9rem"),
                rx.text(BRAND["email"], color="rgba(255,255,255,0.55)", font_size="0.9rem"),
                rx.text(BRAND["address"], color="rgba(255,255,255,0.55)", font_size="0.9rem"),
                spacing="2",
                align="start",
                min_width="200px",
            ),
            gap="4rem",
            flex_wrap="wrap",
            justify="between",
            align="start",
            max_width="1100px",
            margin="0 auto",
            width="100%",
        ),
        rx.separator(margin_y="2rem", color_scheme="gray"),
        rx.text(
            f"© 2025 {BRAND['name']}. All rights reserved. | Licensed & Insured.",
            color="rgba(255,255,255,0.35)",
            font_size="0.83rem",
            text_align="center",
        ),
        background="#061C10",
        padding_x="2rem",
        padding_y="3rem",
        width="100%",
    )


# ── Page ──────────────────────────────────────────────────────────────────────

def index() -> rx.Component:
    return rx.box(
        navbar(),
        hero(),
        services_section(),
        why_us_section(),
        contact_section(),
        footer(),
        font_family="'Inter', system-ui, -apple-system, BlinkMacSystemFont, sans-serif",
        min_height="100vh",
    )


# ── FastAPI Routes (via Reflex's internal FastAPI server) ─────────────────────

class ContactRequest(BaseModel):
    name: str
    email: str
    phone: str = ""
    message: str


# ── App ───────────────────────────────────────────────────────────────────────

app = rx.App(
    theme=rx.theme(
        accent_color="amber",
        gray_color="slate",
        radius="medium",
        scaling="100%",
    ),
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap",
    ],
)

app.add_page(
    index,
    route="/",
    title=f"{BRAND['name']} — {BRAND['tagline']}",
    description="Professional handyman services in the Greater Seattle Area — repairs, plumbing, electrical, painting, and more.",
)


# ── FastAPI sub-app mounted at /api ───────────────────────────────────────────
# Reflex's internal server is Starlette; we mount a FastAPI app for typed REST routes.

api = fastapi.FastAPI(title="ProHandyman API", docs_url="/api/docs")


@api.post("/contact")
async def api_contact(data: ContactRequest):
    """Save to SQLite and email the owner."""
    await asyncio.to_thread(
        handle_submission, data.name, data.email, data.phone, data.message
    )
    return {"status": "success", "message": f"Thanks {data.name}, we'll be in touch!"}


@api.get("/services")
async def api_services():
    """Return the full services catalogue as JSON."""
    return {"services": SERVICES}


app._api.mount("/api", api)
