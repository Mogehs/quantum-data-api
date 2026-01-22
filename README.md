# Massive API - Jinja2 Templates (FastAPI)

This project contains modular Jinja2 templates for the Massive API homepage, configured for use with **FastAPI**.

## Core Structure
- `templates/layout/base.html`: The main skeletal structure.
- `templates/partials/`: Reusable components (Navbar, Hero, Features, etc.).
- `templates/index.html`: The main page that extends the base layout.

## How to Run

These templates are rendered using FastAPI and the `jinja2` engine.

### 1. Install Dependencies
Ensure you have Python installed, then install FastAPI, Uvicorn, and Jinja2:
```bash
pip install fastapi uvicorn jinja2
```

### 2. Run the Application
Start the uvicorn server:
```bash
python app.py
```
*Alternatively, you can run:*
```bash
uvicorn app:app --reload
```

### 3. View the Site
Open your browser and navigate to:
[http://127.0.0.1:8000](http://127.0.0.1:8000)

## Design System
- **Styling**: Tailwind CSS (via CDN)
- **Icons**: Material Symbols Outlined
- **Fonts**: Inter & JetBrains Mono
