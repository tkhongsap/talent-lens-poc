from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from .core.config import get_settings
from .db.mongodb import connect_to_mongo, close_mongo_connection
from .api.v1.routes import router as api_router

settings = get_settings()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="""
    TalentLens API provides powerful resume analysis and job matching capabilities.
    
    ## Features
    * 📄 Resume Processing & Analysis
    * 💼 Job Description Matching
    * 🔍 Professional Search
    * 📊 Analytics & Insights
    
    ## API Documentation
    * [Swagger UI](/docs) - Interactive API documentation
    * [ReDoc](/redoc) - Alternative API documentation
    """,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=None,  # Disable default docs url
    redoc_url=None  # Disable default redoc url
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database connection events
app.add_event_handler("startup", connect_to_mongo)
app.add_event_handler("shutdown", close_mongo_connection)

# Include routers
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/", response_class=HTMLResponse)
async def root():
    html_content = """
    <!DOCTYPE html>
    <html>
        <head>
            <title>TalentLens API</title>
            <style>
                body {
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 2rem;
                    line-height: 1.6;
                }
                .container {
                    background: white;
                    border-radius: 8px;
                    padding: 2rem;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }
                h1 {
                    color: #4F46E5;
                    margin-bottom: 1rem;
                }
                .version {
                    color: #6B7280;
                    font-size: 0.9rem;
                }
                .endpoints {
                    margin-top: 2rem;
                }
                .endpoint-group {
                    margin-bottom: 2rem;
                }
                .button {
                    display: inline-block;
                    padding: 0.5rem 1rem;
                    background-color: #4F46E5;
                    color: white;
                    text-decoration: none;
                    border-radius: 4px;
                    margin-right: 1rem;
                    transition: background-color 0.2s;
                }
                .button:hover {
                    background-color: #4338CA;
                }
                .features {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 1rem;
                    margin-top: 2rem;
                }
                .feature-card {
                    background: #F3F4F6;
                    padding: 1rem;
                    border-radius: 4px;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Welcome to TalentLens API</h1>
                <p class="version">Version: """ + settings.VERSION + """</p>
                
                <div class="endpoints">
                    <h2>API Documentation</h2>
                    <p>
                        <a href="/docs" class="button">Swagger UI</a>
                        <a href="/redoc" class="button">ReDoc</a>
                    </p>
                </div>

                <div class="endpoint-group">
                    <h2>Available Endpoints</h2>
                    <div class="feature-card">
                        <h3>Resume Analysis</h3>
                        <ul>
                            <li>POST /api/v1/uploads/resume - Upload resumes</li>
                            <li>POST /api/v1/uploads/job-description - Upload job description</li>
                        </ul>
                    </div>
                </div>

                <div class="features">
                    <div class="feature-card">
                        <h3>📄 Resume Processing</h3>
                        <p>Advanced resume parsing and analysis</p>
                    </div>
                    <div class="feature-card">
                        <h3>💼 Job Matching</h3>
                        <p>Intelligent job-candidate matching</p>
                    </div>
                    <div class="feature-card">
                        <h3>🔍 Search</h3>
                        <p>Advanced search capabilities</p>
                    </div>
                </div>
            </div>
        </body>
    </html>
    """
    return html_content

# Custom docs endpoints
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        title=f"{settings.PROJECT_NAME} - Swagger UI",
        swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css",
    )

@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        title=f"{settings.PROJECT_NAME} - ReDoc"
    )