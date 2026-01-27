# QuantDataApi - Financial Data APIs

This project contains modular Jinja2 templates for the **QuantDataApi** platform, focused on high-performance financial data for developers.

## Core Structure
- `templates/layout/base.html`: The main skeletal structure.
- `templates/partials/`: Reusable components (Navbar, Hero, Features, etc.).
- `templates/index.html`: The main landing page.
- `templates/docs.html`: Technical API documentation.

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

### 3. View the Site
Open your browser and navigate to:
[http://127.0.0.1:8000](http://127.0.0.1:8000)
Documentation is at [/docs](http://127.0.0.1:8000/docs)

## Design System
- **Styling**: Tailwind CSS (via CDN)
- **Icons**: Material Symbols Outlined
- **Fonts**: Inter & JetBrains Mono
