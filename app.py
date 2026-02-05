from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI(title="QuantDataApi", docs_url=None, redoc_url=None)

# Setup Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Sample Blog Data
blog_posts = [
    {
        "id": 1,
        "slug": "architecting-for-100us-latency",
        "title": "Architecting for 100μs Latency: Our New WebSocket Core",
        "date": "May 24, 2024",
        "author_name": "Erik Lindgren",
        "author_role": "Head of Infrastructure",
        "read_time": "12 min read",
        "category": "Engineering",
        "featured": True,
        "image": "https://images.unsplash.com/photo-1518770660439-4636190af475?q=80&w=2000&auto=format&fit=crop",
        "summary": "How we rebuilt our market data distribution engine from the ground up using Rust and kernel-bypass networking to deliver institutional-grade performance to retail developers.",
        "content_intro": "In the world of high-frequency trading and real-time market data, every microsecond counts. This post explores how we rebuilt our Market Data Core from the ground up using Rust and kernel-bypass networking to deliver sub-ms latency at massive scale.",
        "content": """
<h2>The Bottleneck: JSON Overhead</h2>
<p>
    When we first launched QuantDataApi, our feeds relied on standard JSON payloads. While human-readable and easy to debug, the serialization/deserialization cost became a significant bottleneck as we scaled to support more institutional clients.
</p>
<ul>
    <li><strong>Payload Size:</strong> JSON's verbosity leads to larger packet sizes, increasing network congestion.</li>
    <li><strong>CPU Cycles:</strong> Parsing large JSON objects 100,000 times per second puts unnecessary strain on client-side CPU.</li>
    <li><strong>Garbage Collection:</strong> Frequent object creation in languages like Java or Node.js leads to unpredictable GC pauses.</li>
</ul>
<blockquote>
    "Transitioning from JSON to a binary protocol reduced our total network egress by 64% and decreased client-side CPU usage by an average of 40%."
</blockquote>
<h2>Implementation: Switching to Protocol Buffers</h2>
<p>
    To address these issues, we implemented a custom binary protocol using Protocol Buffers (protobuf). This allows for strictly typed messages and minimal overhead. Here's how a typical tick update looks in our new implementation:
</p>
<div class="bg-surface rounded-xl overflow-hidden border border-border my-8 font-mono text-[13px]">
    <div class="flex items-center justify-between px-5 py-3 bg-background/50 border-b border-border">
        <span class="text-text-muted tracking-wider text-[11px] uppercase">market_feed.proto</span>
        <span class="material-symbols-outlined text-[16px] text-text-muted cursor-pointer hover:text-primary">content_copy</span>
    </div>
    <div class="p-6 text-text-muted leading-relaxed">
        <div><span class="text-secondary text-pink-400">syntax</span> = <span class="text-primary text-emerald-400">"proto3"</span>;</div>
        <div class="mt-4"><span class="text-secondary text-pink-400">message</span> <span class="text-text-main text-slate-100">MarketTick</span> {</div>
        <div class="pl-4"> <span class="text-secondary text-pink-400">string</span> symbol = <span class="text-primary text-emerald-400">1</span>;</div>
        <div class="pl-4"> <span class="text-secondary text-pink-400">double</span> price = <span class="text-primary text-emerald-400">2</span>;</div>
        <div class="pl-4"> <span class="text-secondary text-pink-400">uint64</span> timestamp = <span class="text-primary text-emerald-400">3</span>;</div>
        <div class="pl-4"> <span class="text-secondary text-pink-400">int32</span> volume = <span class="text-primary text-emerald-400">4</span>;</div>
        <div class="pl-4"> <span class="text-secondary text-pink-400">enum</span> Side { BUY = 0; SELL = 1; }</div>
        <div class="pl-4">  Side side = <span class="text-primary text-emerald-400">5</span>;</div>
        <div>}</div>
    </div>
</div>
<h3>Zero-Copy Buffer Management</h3>
<p>
    On the backend, we utilized zero-copy techniques in our Go implementation. By reusing buffers and avoiding memory allocations in the hot path, we eliminated latency spikes during high volatility periods (like market opens).
</p>
<div class="bg-surface rounded-xl overflow-hidden border border-border my-8 font-mono text-[13px]">
    <div class="flex items-center justify-between px-5 py-3 bg-background/50 border-b border-border">
        <span class="text-text-muted tracking-wider text-[11px] uppercase">latency_metrics.js</span>
        <span class="material-symbols-outlined text-[16px] text-text-muted cursor-pointer hover:text-primary">content_copy</span>
    </div>
    <div class="p-6 text-text-muted">
        <div class="text-text-muted/50">// Client-side measurement of E2E latency</div>
        <div class="text-secondary text-pink-400">const</div> <span class="text-text-main text-slate-100">socket</span> = <span class="text-secondary text-pink-400">new</span> <span class="text-primary text-emerald-400">QuantSocket</span>(API_KEY);<br/><br/>
        <span class="text-text-main text-slate-100">socket</span>.<span class="text-primary text-emerald-400">on</span>(<span class="text-secondary text-pink-400">'tick'</span>, (<span class="text-text-main text-slate-100">data</span>) => {<br/>
        &nbsp;&nbsp;<span class="text-secondary text-pink-400">const</span> <span class="text-text-main text-slate-100">latency</span> = <span class="text-text-main text-slate-100">Date</span>.<span class="text-primary text-emerald-400">now</span>() - <span class="text-text-main text-slate-100">data.serverTime</span>;<br/>
        &nbsp;&nbsp;<span class="text-text-main text-slate-100">console</span>.<span class="text-primary text-emerald-400">log</span>(<span class="text-secondary text-pink-400">`E2E Latency: ${latency}ms`</span>);<br/>
        });
    </div>
</div>
<h2>Conclusion</h2>
<p>
    Moving to binary protocols and implementing aggressive buffer management has transformed QuantDataApi from a developer-friendly tool to a professional-grade trading infrastructure. Our customers can now build production-ready trading bots that compete at the highest levels.
</p>
"""
    },
    {
        "id": 2,
        "slug": "mastering-high-frequency-backtesting",
        "title": "Mastering High-Frequency Backtesting with Parquet",
        "date": "May 18, 2024",
        "author_name": "Alex Miller",
        "author_role": "Data Scientist",
        "read_time": "8 min read",
        "category": "Engineering",
        "featured": False,
        "image": "https://images.unsplash.com/photo-1518770660439-4636190af475?q=80&w=1200&auto=format&fit=crop",
        "summary": "Learn how to efficiently process terabytes of historical tick data using the Apache Parquet format and DuckDB for ultra-fast local backtesting."
    },
    {
        "id": 3,
        "slug": "handling-corporate-actions-adjusted-price-guide",
        "title": "Handling Corporate Actions: The Adjusted Price Guide",
        "date": "May 12, 2024",
        "author_name": "Sarah Chen",
        "author_role": "Product Manager",
        "read_time": "5 min read",
        "category": "Market Data",
        "featured": False,
        "image": "https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?q=80&w=1200&auto=format&fit=crop",
        "summary": "Why adjusted prices matter and how our API handles stock splits, dividends, and spin-offs automatically to maintain your strategy's integrity."
    },
    {
        "id": 4,
        "slug": "extended-hours-options-chains",
        "title": "New: Extended Hours Options Chains Now Available",
        "date": "May 05, 2024",
        "author_name": "Pat Knight",
        "author_role": "Equity Analyst",
        "read_time": "4 min read",
        "category": "Product Updates",
        "featured": False,
        "image": "https://images.unsplash.com/photo-1620641788421-7a1c342ea42e?q=80&w=1200&auto=format&fit=crop",
        "summary": "We've expanded our options coverage to include pre-market and after-hours Greek calculations for the entire US equity universe."
    },
    {
        "id": 5,
        "slug": "real-time-risk-engine-go",
        "title": "Building a Real-Time Risk Engine with Go",
        "date": "Apr 28, 2024",
        "author_name": "James Doe",
        "author_role": "Backend Engineer",
        "read_time": "15 min read",
        "category": "Engineering",
        "featured": False,
        "image": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?q=80&w=1200&auto=format&fit=crop",
        "summary": "A deep dive into concurrency patterns for monitoring thousands of active streams while maintaining sub-millisecond safety checks."
    },
    {
        "id": 6,
        "slug": "zero-copy-serialization",
        "title": "Zero-Copy Serialization in Financial APIs",
        "date": "Apr 20, 2024",
        "author_name": "Erik Lindgren",
        "author_role": "Head of Infrastructure",
        "read_time": "10 min read",
        "category": "Engineering",
        "featured": False,
        "image": "https://images.unsplash.com/photo-1526628953301-3e589a6a8b74?q=80&w=1200&auto=format&fit=crop",
        "summary": "Explaining our transition from JSON to FlatBuffers for high-throughput market data distribution and why it matters for your app.",
        "content_intro": "As data throughput requirements grow, traditional serialization formats like JSON can become a significant bottleneck. This article explores how we implemented zero-copy serialization using FlatBuffers to achieve massive performance gains.",
        "content": """
<h2>The Serialization Challenge</h2>
<p>
    In high-frequency trading systems, the time spent converting data into a transmittable format can often exceed the actual transmission time. Standard JSON serialization involves heavy string manipulation and memory allocation that can't keep up with our 10ms update cycles.
</p>

<h3>JSON vs. FlatBuffers</h3>
<ul>
    <li><strong>JSON:</strong> Requires parsing the entire string into an object model before use. High CPU and memory overhead.</li>
    <li><strong>FlatBuffers:</strong> Allows accessing data without parsing or unpacking. You read values directly from the binary buffer.</li>
</ul>

<div class="bg-surface rounded-xl overflow-hidden border border-border my-8 font-mono text-[13px]">
    <div class="flex items-center justify-between px-5 py-3 bg-background/50 border-b border-border">
        <span class="text-text-muted tracking-wider text-[11px] uppercase">schema.fbs</span>
        <span class="material-symbols-outlined text-[16px] text-text-muted cursor-pointer hover:text-primary">content_copy</span>
    </div>
    <div class="p-6 text-text-muted">
        <span class="text-pink-400">table</span> <span class="text-slate-100">PriceUpdate</span> {<br/>
        &nbsp;&nbsp;symbol: <span class="text-emerald-400">string</span>;<br/>
        &nbsp;&nbsp;price: <span class="text-emerald-400">float64</span>;<br/>
        &nbsp;&nbsp;volume: <span class="text-emerald-400">int64</span>;<br/>
        }
    </div>
</div>

<h2>Wait-Free Performance</h2>
<p>
    By utilizing zero-copy techniques, our Go and Rust SDKs can process incoming price updates without ever allocating new memory on the heap. This leads to extremely stable latency profiles even during periods of extreme market volatility.
</p>

<blockquote>
    "Our zero-copy implementation reduced P99 latency by 85% during the high-volatility window of the market open."
</blockquote>

<h2>Conclusion</h2>
<p>
    Zero-copy serialization isn't just an optimization; it's a requirement for modern financial infrastructure. By adopting FlatBuffers, we ensure that QuantDataApi remains the fastest way for developers to receive market data.
</p>
"""
    },
    {
        "id": 7,
        "slug": "sip-vs-direct-feed-latency",
        "title": "Understanding SIP vs Direct Feed Latency",
        "date": "Apr 15, 2024",
        "author_name": "Alex Miller",
        "author_role": "Data Scientist",
        "read_time": "6 min read",
        "category": "Market Data",
        "featured": False,
        "image": "https://images.unsplash.com/photo-1639762681485-074b7f938ba0?q=80&w=1200&auto=format&fit=crop",
        "summary": "A technical comparison of the National Best Bid and Offer (NBBO) sources and how QuantDataApi aggregates them for consistency."
    },
    {
        "id": 8,
        "slug": "scaling-market-data-websockets",
        "title": "Scaling Market Data WebSockets to 1M Connections",
        "date": "Apr 05, 2024",
        "author_name": "Erik Lindgren",
        "author_role": "Head of Infrastructure",
        "read_time": "20 min read",
        "category": "Engineering",
        "featured": False,
        "image": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=1200&auto=format&fit=crop",
        "summary": "How we use edge computing and custom load balancing to handle massive scale for our WebSocket users."
    },
    {
        "id": 9,
        "slug": "python-sdk-v2-release",
        "title": "Announcing Python SDK v2.0: Now with Async Support",
        "date": "Mar 28, 2024",
        "author_name": "Sarah Chen",
        "author_role": "Product Manager",
        "read_time": "4 min read",
        "category": "Product Updates",
        "featured": False,
        "image": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?q=80&w=1200&auto=format&fit=crop",
        "summary": "Our popular Python SDK just got a major upgrade with full async support and improved type hinting for a better developer experience."
    },
    {
        "id": 10,
        "slug": "optimizing-postgres-for-timeseries",
        "title": "Optimizing PostgreSQL for Time-Series Market Data",
        "date": "Mar 15, 2024",
        "author_name": "Erik Lindgren",
        "author_role": "Head of Infrastructure",
        "read_time": "15 min read",
        "category": "Engineering",
        "featured": False,
        "image": "https://images.unsplash.com/photo-1544383835-bda2bc66a55d?q=80&w=1200&auto=format&fit=crop",
        "summary": "Deep dive into indexing strategies and partitioning techniques to keep your market data queries lightning fast as your database grows."
    },
    {
        "id": 11,
        "slug": "understanding-market-microstructure",
        "title": "A Beginner's Guide to Market Microstructure",
        "date": "Mar 05, 2024",
        "author_name": "Alex Miller",
        "author_role": "Data Scientist",
        "read_time": "10 min read",
        "category": "Market Data",
        "featured": False,
        "image": "https://images.unsplash.com/photo-1639762681485-074b7f938ba0?q=80&w=1200&auto=format&fit=crop",
        "summary": "Everything you need to know about order books, liquidity, and the role of market makers in modern electronic exchanges."
    },
    {
        "id": 12,
        "slug": "quantdata-api-status-page-v2",
        "title": "Introducing Our New Real-Time Status Dashboard",
        "date": "Feb 28, 2024",
        "author_name": "Sarah Chen",
        "author_role": "Product Manager",
        "read_time": "3 min read",
        "category": "Product Updates",
        "featured": False,
        "image": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?q=80&w=1200&auto=format&fit=crop",
        "summary": "We've rebuilt our status page from scratch to provide sub-second latency updates on all our major API endpoints and WebSocket feeds."
    },
    {
        "id": 13,
        "slug": "low-latency-networking-101",
        "title": "Low-Latency Networking 101 for Fintech Developers",
        "date": "Feb 15, 2024",
        "author_name": "Erik Lindgren",
        "author_role": "Head of Infrastructure",
        "read_time": "12 min read",
        "category": "Engineering",
        "featured": False,
        "image": "https://images.unsplash.com/photo-1544197150-b99a580bb7a8?q=80&w=1200&auto=format&fit=crop",
        "summary": "Understanding the networking stack from the perspective of a high-frequency trader: from NIC interrupts to kernel bypass."
    },
    {
        "id": 14,
        "slug": "distributed-consensus-financial-systems",
        "title": "Distributed Consensus in Financial Systems",
        "date": "Feb 05, 2024",
        "author_name": "James Doe",
        "author_role": "Backend Engineer",
        "read_time": "15 min read",
        "category": "Engineering",
        "featured": False,
        "image": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=1200&auto=format&fit=crop",
        "summary": "Comparing Paxos, Raft, and other consensus algorithms for maintaining high-availability order matching engines."
    },
    {
        "id": 15,
        "slug": "options-greeks-explained-developers",
        "title": "Options Greeks Explained for API Developers",
        "date": "Jan 28, 2024",
        "author_name": "Alex Miller",
        "author_role": "Data Scientist",
        "read_time": "8 min read",
        "category": "Market Data",
        "featured": False,
        "image": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?q=80&w=1200&auto=format&fit=crop",
        "summary": "A developer-first guide to Rho, Vega, Theta, Gamma, and Delta calculations in our real-time options feeds."
    },
    {
        "id": 16,
        "slug": "quantdata-api-mobile-app-preview",
        "title": "First Look: The QuantDataApi Mobile Monitoring App",
        "date": "Jan 15, 2024",
        "author_name": "Sarah Chen",
        "author_role": "Product Manager",
        "read_time": "5 min read",
        "category": "Product Updates",
        "featured": False,
        "image": "https://images.unsplash.com/photo-1512941937669-90a1b58e7e9c?q=80&w=1200&auto=format&fit=crop",
        "summary": "Monitor your WebSocket health and market data streams on the go with our upcoming iOS and Android companion apps."
    },
    {
        "id": 17,
        "slug": "modernizing-legacy-financial-data",
        "title": "Modernizing Legacy Financial Data Pipelines",
        "date": "Jan 05, 2014",
        "author_name": "Erik Lindgren",
        "author_role": "Head of Infrastructure",
        "read_time": "11 min read",
        "category": "Engineering",
        "featured": False,
        "image": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?q=80&w=1200&auto=format&fit=crop",
        "summary": "How we migrated from monolithic overnight batch jobs to a cloud-native real-time event-driven architecture."
    },
    {
        "id": 18,
        "slug": "understanding-market-impact-large-orders",
        "title": "Understanding Market Impact and Slippage",
        "date": "Dec 20, 2023",
        "author_name": "Alex Miller",
        "author_role": "Data Scientist",
        "read_time": "9 min read",
        "category": "Market Data",
        "featured": False,
        "image": "https://images.unsplash.com/photo-1543286386-713bdd548da4?q=80&w=1200&auto=format&fit=crop",
        "summary": "Measuring and modeling how large order execution affects market liquidity and price movement."
    },
    {
        "id": 19,
        "slug": "quantdata-api-v3-roadmap",
        "title": "QuantDataApi v3.0: The Future Roadmap",
        "date": "Dec 10, 2023",
        "author_name": "Sarah Chen",
        "author_role": "Product Manager",
        "read_time": "6 min read",
        "category": "Product Updates",
        "featured": False,
        "image": "https://images.unsplash.com/photo-1506784983877-45594efa4cbe?q=80&w=1200&auto=format&fit=crop",
        "summary": "A glimpse into 2024: Cross-asset correlation APIs, machine learning signals, and global equity expansion."
    }
]

@app.get("/blog")
async def blog_index(request: Request, page: int = 1, category: str = "All", q: str = ""):
    filtered_posts = blog_posts
    
    # 1. Search filter
    if q:
        q_lower = q.lower()
        filtered_posts = [p for p in filtered_posts if q_lower in p["title"].lower() or q_lower in p["summary"].lower()]
    
    # 2. Category filter
    if category != "All":
        filtered_posts = [p for p in filtered_posts if p["category"] == category]
    
    # 3. Featured post (always from full list for the section, or could be filtered)
    featured_post = next((p for p in blog_posts if p.get("featured")), None)
    
    # Remove featured from the grid if it's there
    posts_for_grid = [p for p in filtered_posts if not p.get("featured")]
    
    # 4. Pagination
    per_page = 6
    total_posts = len(posts_for_grid)
    total_pages = (total_posts + per_page - 1) // per_page
    
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    paginated_posts = posts_for_grid[start_idx:end_idx]
    
    return templates.TemplateResponse("blog/index.html", {
        "request": request,
        "page_name": "blog",
        "featured_post": featured_post,
        "posts": paginated_posts,
        "current_page": page,
        "total_pages": total_pages,
        "current_category": category,
        "search_query": q
    })

@app.get("/blog/{slug}")
async def blog_post(request: Request, slug: str):
    post = next((p for p in blog_posts if p["slug"] == slug), None)
    if not post:
        return templates.TemplateResponse("404.html", {"request": request}, status_code=404)
    
    # Simple related posts logic: other posts
    related_posts = [p for p in blog_posts if p["slug"] != slug][:6]
    
    return templates.TemplateResponse("blog/post.html", {
        "request": request,
        "page": "blog",
        "post": post,
        "related_posts": related_posts
    })

@app.get("/")
async def index(request: Request):
    # Pass first 3 non-featured posts for the homepage section
    recent_posts = [p for p in blog_posts if not p.get("featured")][:3]
    return templates.TemplateResponse("index.html", {
        "request": request,
        "recent_posts": recent_posts
    })

@app.get("/docs")
async def docs_overview(request: Request):
    return templates.TemplateResponse("docs/overview.html", {"request": request, "page": "overview", "title": "Overview"})

@app.get("/pricing")
async def pricing(request: Request):
    return templates.TemplateResponse("pricing.html", {"request": request, "page": "pricing"})

@app.get("/playground")
async def playground(request: Request):
    return templates.TemplateResponse("playground.html", {"request": request, "page": "playground"})

@app.get("/contact")
async def contact_page(request: Request):
    return templates.TemplateResponse("contact.html", {"request": request, "page": "contact"})

# @app.get("/terms")
# async def terms_of_service(request: Request):
#     return templates.TemplateResponse("terms.html", {"request": request, "page": "terms"})

# @app.get("/privacy")
# async def privacy_policy(request: Request):
#     return templates.TemplateResponse("privacy.html", {"request": request, "page": "privacy"})

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

@app.get("/docs-v2")
async def docs_v2(request: Request):
    return templates.TemplateResponse("docs/v2.html", {"request": request, "page": "docs-v2", "title": "Documentation V2"})

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
    import os
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("app:app", host="127.0.0.1", port=port, reload=True)
