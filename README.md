# ProHandyman Service Site

Full-stack Python service website template for a local handyman business.
Built with [Reflex](https://reflex.dev) (frontend + backend) and FastAPI (REST API).

## Features

- Hero section with CTA buttons
- Services grid (6 cards)
- "Why Us" trust section
- Contact form — saves to SQLite, emails the owner
- REST API at `/api/contact` and `/api/services`
- Seattle "Emerald City" theme

## Requirements

- Python 3.11+
- Node.js 18+

## Quick Start

```bash
./run.sh
```

That's it. The script handles venv creation, dependency installs, and Reflex init automatically.

The app runs at **http://localhost:3000** and the API at **http://localhost:8000/api**.

---

## Email Notification Setup

When a visitor submits the contact form, the site saves the submission to a local SQLite database (`submissions.db`) and optionally sends you an email notification.

The database works out of the box with no configuration. Email requires a one-time Gmail setup.

### Step 1 — Create your `.env` file

```bash
cp .env.example .env
```

### Step 2 — Generate a Gmail App Password

Gmail does not allow your regular password for SMTP. You need to generate an **App Password**:

1. Go to your [Google Account](https://myaccount.google.com)
2. Navigate to **Security**
3. Under *"How you sign in to Google"*, open **2-Step Verification** (must be enabled)
4. Scroll to the bottom and click **App Passwords**
5. Choose a name (e.g. `ProHandyman`) and click **Create**
6. Copy the 16-character password that appears

### Step 3 — Fill in `.env`

```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=you@gmail.com
SMTP_PASSWORD=xxxx-xxxx-xxxx-xxxx

# Where notification emails are sent (defaults to SMTP_USER)
NOTIFY_EMAIL=you@gmail.com
```

### Step 4 — Restart the app

```bash
./run.sh
```

Every form submission will now save to `submissions.db` **and** send an HTML email to `NOTIFY_EMAIL`. The email includes the visitor's name, email, phone, and message, with a reply-to set so you can respond directly.

> **Note:** If `SMTP_USER` or `SMTP_PASSWORD` are missing, email is silently skipped and submissions are still saved to the database.

---

## Viewing Submissions

You can query the database directly at any time:

```bash
sqlite3 submissions.db "SELECT * FROM submissions;"
```

---

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/services` | Returns the services catalogue as JSON |
| `POST` | `/api/contact` | Accepts `{name, email, phone?, message}` |
| `GET` | `/api/docs` | Swagger UI |

---

## Deploying to Fly.io

Pushing to `main` automatically deploys via GitHub Actions. Do the one-time setup below first.

### Step 1 — Install flyctl and log in

```bash
brew install flyctl   # or: curl -L https://fly.io/install.sh | sh
fly auth login
```

### Step 2 — Create the app

```bash
fly apps create your-app-name
```

Then update `fly.toml` with your chosen app name:

```toml
app = "your-app-name"
```

### Step 3 — Create the persistent volume

SQLite data is stored on a Fly volume so it survives deploys and restarts.

```bash
fly volumes create handyman_data --size 1 --region sea
```

### Step 4 — Set email secrets

SMTP credentials are stored as Fly secrets, not in the repo.

```bash
fly secrets set \
  SMTP_USER=you@gmail.com \
  SMTP_PASSWORD=xxxx-xxxx-xxxx-xxxx \
  NOTIFY_EMAIL=you@gmail.com
```

See [Email Notification Setup](#email-notification-setup) above for how to generate a Gmail App Password.

### Step 5 — Add the deploy token to GitHub

1. Generate a token: `fly tokens create deploy -x 999999h`
2. In your GitHub repo go to **Settings → Secrets and variables → Actions**
3. Add a secret named `FLY_API_TOKEN` with the token value

### Step 6 — Deploy

```bash
git push origin main
```

The GitHub Action (`.github/workflows/deploy.yml`) will build and deploy automatically on every push to `main`. You can watch it in the **Actions** tab of your repo.

### Viewing production submissions

```bash
fly ssh console -C "sqlite3 /data/submissions.db 'SELECT * FROM submissions;'"
```

---

## Customisation

All site content (business name, phone, address, services list) is defined at the top of `handyman/handyman.py` in the `BRAND` and `SERVICES` constants.
