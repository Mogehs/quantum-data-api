from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI(title="QuantDataApi", docs_url=None, redoc_url=None)

# Setup Jinja2 templates
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/docs")
async def docs_overview(request: Request):
    return templates.TemplateResponse("docs/overview.html", {"request": request, "page": "overview", "title": "Overview"})

@app.get("/pricing")
async def pricing(request: Request):
    return templates.TemplateResponse("pricing.html", {"request": request, "page": "pricing"})

@app.get("/playground")
async def playground(request: Request):
    return templates.TemplateResponse("playground.html", {"request": request, "page": "playground"})

@app.get("/docs/auth")
async def docs_auth(request: Request):
    return templates.TemplateResponse("docs/auth.html", {"request": request, "page": "auth", "title": "Authentication"})

@app.get("/docs/concepts")
async def docs_concepts(request: Request):
    return templates.TemplateResponse("docs/concepts.html", {"request": request, "page": "concepts", "title": "Core Concepts"})

@app.get("/docs/architecture")
async def docs_architecture(request: Request):
    return templates.TemplateResponse("docs/architecture.html", {"request": request, "page": "architecture", "title": "Architecture"})

@app.get("/docs/api-reference")
async def docs_api_reference(request: Request):
    return templates.TemplateResponse("docs/api_reference.html", {"request": request, "page": "api-reference", "title": "Daily Time Series"})

@app.get("/docs/quickstart")
async def docs_quickstart(request: Request):
    return templates.TemplateResponse("docs/quickstart.html", {"request": request, "page": "quickstart", "title": "Quickstart Guide"})

@app.get("/docs/sdks")
async def docs_sdks(request: Request):
    return templates.TemplateResponse("docs/sdks.html", {"request": request, "page": "sdks", "title": "SDKs & Libraries"})

@app.get("/docs/intraday")
async def docs_intraday(request: Request):
    return templates.TemplateResponse("docs/intraday.html", {"request": request, "page": "intraday", "title": "Intraday APIs"})

@app.get("/docs/monthly")
async def docs_monthly(request: Request):
    return templates.TemplateResponse("docs/monthly.html", {"request": request, "page": "monthly", "title": "Monthly APIs"})

@app.get("/docs/limits")
async def docs_limits(request: Request):
    return templates.TemplateResponse("docs/limits.html", {"request": request, "page": "limits", "title": "Rate Limits"})

@app.get("/docs/errors")
async def docs_errors(request: Request):
    return templates.TemplateResponse("docs/errors.html", {"request": request, "page": "errors", "title": "Errors & Responses"})

@app.get("/docs/versioning")
async def docs_versioning(request: Request):
    return templates.TemplateResponse("docs/versioning.html", {"request": request, "page": "versioning", "title": "Versioning"})

@app.get("/docs/{slug}")
async def docs_placeholder(request: Request, slug: str):
    # Mapping slug to readable title
    titles = {
        "concepts": "Core Concepts",
        "architecture": "Architecture",
        "quickstart": "Quickstart Guide",
        "auth": "Authentication", 
        "sdks": "SDKs & Libraries",
        "intraday": "Intraday APIs",
        "monthly": "Monthly APIs",
        "limits": "Rate Limits",
        "errors": "Errors & Responses",
        "versioning": "Versioning"
    }
    title = titles.get(slug, slug.replace("-", " ").title())
    return templates.TemplateResponse("docs/under_development.html", {
        "request": request, 
        "page": slug,
        "title": title
    })

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
