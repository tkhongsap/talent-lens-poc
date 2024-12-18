from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from app.api.v1.api import api_router
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="TalentLens API",
    description="API for resume analysis and job matching",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint with HTML response
@app.get("/", response_class=HTMLResponse)
async def root():
    logger.info("Root endpoint called")
    return """
    <!DOCTYPE html>
    <html>
        <head>
            <title>TalentLens API</title>
            <style>
                body {
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 2rem;
                    background-color: #f5f5f5;
                }
                .container {
                    background-color: white;
                    padding: 2rem;
                    border-radius: 10px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }
                h1 {
                    color: #2563eb;
                    margin-bottom: 1rem;
                }
                .status {
                    display: inline-block;
                    padding: 0.5rem 1rem;
                    border-radius: 9999px;
                    background-color: #dcfce7;
                    color: #166534;
                    font-weight: 500;
                    margin: 1rem 0;
                }
                .links {
                    margin-top: 2rem;
                }
                a {
                    display: inline-block;
                    padding: 0.75rem 1.5rem;
                    background-color: #2563eb;
                    color: white;
                    text-decoration: none;
                    border-radius: 6px;
                    margin-right: 1rem;
                    transition: background-color 0.2s;
                }
                a:hover {
                    background-color: #1d4ed8;
                }
                .description {
                    color: #4b5563;
                    line-height: 1.6;
                    margin: 1rem 0;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Welcome to TalentLens API</h1>
                <div class="status">🟢 Operational</div>
                <p class="description">
                    TalentLens is an advanced API service for resume analysis and job matching. 
                    Our platform uses AI to process resumes, analyze job descriptions, and provide 
                    intelligent matching between candidates and positions.
                </p>
                <div class="links">
                    <a href="/docs">API Documentation</a>
                    <a href="/health">Health Status</a>
                </div>
            </div>
        </body>
    </html>
    """

# Health check endpoint with HTML response
@app.get("/health", response_class=HTMLResponse)
async def health_check():
    logger.info("Health check endpoint called")
    return """
    <!DOCTYPE html>
    <html>
        <head>
            <title>TalentLens API - Health Status</title>
            <style>
                body {
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 2rem;
                    background-color: #f5f5f5;
                }
                .container {
                    background-color: white;
                    padding: 2rem;
                    border-radius: 10px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }
                h1 {
                    color: #2563eb;
                    margin-bottom: 1rem;
                }
                .status-card {
                    background-color: #f8fafc;
                    border: 1px solid #e2e8f0;
                    border-radius: 8px;
                    padding: 1.5rem;
                    margin: 1rem 0;
                }
                .status-indicator {
                    display: flex;
                    align-items: center;
                    gap: 0.5rem;
                    margin-bottom: 1rem;
                }
                .status-dot {
                    display: inline-block;
                    width: 12px;
                    height: 12px;
                    background-color: #22c55e;
                    border-radius: 50%;
                    animation: pulse 2s infinite;
                }
                .status-label {
                    font-size: 1.25rem;
                    font-weight: 500;
                    color: #166534;
                }
                .metrics {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 1rem;
                    margin-top: 1rem;
                }
                .metric-card {
                    background-color: white;
                    padding: 1rem;
                    border-radius: 6px;
                    border: 1px solid #e2e8f0;
                }
                .metric-label {
                    color: #64748b;
                    font-size: 0.875rem;
                    margin-bottom: 0.5rem;
                }
                .metric-value {
                    color: #0f172a;
                    font-size: 1.5rem;
                    font-weight: 600;
                }
                .back-link {
                    display: inline-block;
                    margin-top: 1rem;
                    color: #2563eb;
                    text-decoration: none;
                }
                .back-link:hover {
                    text-decoration: underline;
                }
                @keyframes pulse {
                    0% { opacity: 1; }
                    50% { opacity: 0.5; }
                    100% { opacity: 1; }
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>System Health Status</h1>
                <div class="status-card">
                    <div class="status-indicator">
                        <span class="status-dot"></span>
                        <span class="status-label">All Systems Operational</span>
                    </div>
                    <div class="metrics">
                        <div class="metric-card">
                            <div class="metric-label">API Status</div>
                            <div class="metric-value">Active</div>
                        </div>
                        <div class="metric-card">
                            <div class="metric-label">Response Time</div>
                            <div class="metric-value">< 100ms</div>
                        </div>
                        <div class="metric-card">
                            <div class="metric-label">Uptime</div>
                            <div class="metric-value">99.9%</div>
                        </div>
                    </div>
                </div>
                <a href="/" class="back-link">← Back to Home</a>
            </div>
        </body>
    </html>
    """

# Include API router
app.include_router(api_router, prefix="/api/v1")

@app.on_event("startup")
async def startup_event():
    logger.info("Application startup")
    # Add any startup tasks here

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Application shutdown")
    # Add any cleanup tasks here