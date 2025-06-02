import os
import httpx
import re
from typing import List, Dict, Any, Optional
from mcp.server.fastmcp import FastMCP, Context
from mcp.server.fastmcp.prompts import base
from dotenv import load_dotenv
from email.utils import parsedate_to_datetime
from datetime import datetime

# Load environment variables
load_dotenv()
API_TOKEN = os.getenv("WEB3_CAREER_API_TOKEN")
if not API_TOKEN:
    raise ValueError("WEB3_CAREER_API_TOKEN environment variable is not set")

# Initialize MCP server
mcp = FastMCP("Web3 Jobs Server", dependencies=["httpx", "python-dotenv"])

# Base URL for the API
BASE_URL = "https://web3.career/api/v1"

async def fetch_jobs(params: Dict[str, Any] = None) -> List[Dict]:
    """Fetch jobs from web3.career API with given parameters."""
    async with httpx.AsyncClient() as client:
        try:
            params = params or {}
            params["token"] = API_TOKEN
            response = await client.get(BASE_URL, params=params)
            response.raise_for_status()
            # API returns a list with metadata and job listings
            data = response.json()
            if len(data) > 2:
                return data[2]  # Job listings are in the third element
            return []
        except httpx.HTTPStatusError as e:
            raise ValueError(f"API request failed: {e}")
        except Exception as e:
            raise ValueError(f"Error fetching jobs: {e}")

def strip_html(text: str) -> str:
    """Remove HTML tags from text and clean up whitespace."""
    if not text:
        return ""
    # Remove HTML tags
    clean = re.sub(r'<[^>]+>', '', text)
    # Replace multiple whitespace with single space, strip newlines
    clean = re.sub(r'\s+', ' ', clean).strip()
    return clean

def jobs_to_markdown(jobs: List[Dict], show_description: bool) -> str:
    """Convert job list to a Markdown list."""
    lines = ["# Web3 Job Listings\n"]
    for job in jobs:
        description = strip_html(job.get("description", "")) if show_description else ""
        # Truncate description to 100 characters for readability
        if description:
            description = description[:100] + ("..." if len(description) > 100 else "")
        apply_url = f"[Apply]({job['apply_url']})"
        # Get publication date from 'date_epoch'
        dt = datetime.fromtimestamp(int(job["date_epoch"]))
        published_at = dt.strftime("%Y-%m-%d")
        lines.append(f"- **Job ID**: {job['id']}")
        lines.append(f"  - **Title**: {job['title']}")
        lines.append(f"  - **Company**: {job['company']}")
        lines.append(f"  - **Location**: {job['location']}")
        lines.append(f"  - **Remote**: {'Yes' if job['is_remote'] else 'No'}")
        lines.append(f"  - **Published At**: {published_at}")
        lines.append(f"  - **Apply URL**: {apply_url}")
        if show_description:
            lines.append(f"  - **Description**: {description}")
        lines.append("")  # Blank line between jobs
    
    lines.append("*Source: web3.career*")
    return "\n".join(lines)

# Tool: Query jobs with filters
@mcp.tool()
async def query_jobs(
    remote: Optional[bool] = None,
    country: Optional[str] = None,
    tag: Optional[str] = None,
    limit: Optional[int] = 50,
    ctx: Context = None
) -> str:
    """
    Query Web3 job listings from the web3.career API with optional filters.
    
    Returns a Markdown-formatted list of jobs, including Job ID, Title, Company, Location,
    Remote status, Published At date, Apply URL, and Description (always included).
    
    Parameters:
        remote (Optional[bool]): Filter for remote jobs. Set to True for remote-only,
            False for non-remote, or None for no filter. Defaults to None.
        country (Optional[str]): Filter by country (e.g., "United States", "Canada").
            Case-insensitive, spaces are converted to hyphens (e.g., "united-states").
            Defaults to None (no country filter).
        tag (Optional[str]): Filter by job tag (e.g., "react", "blockchain").
            Case-insensitive. Defaults to None (no tag filter).
        limit (Optional[int]): Maximum number of jobs to return. Must be between 1 and 100.
            Defaults to 50. Raises ValueError if limit exceeds 100.
        ctx (Context): MCP context for logging and internal use. Automatically provided
            by the MCP framework. Defaults to None.
    
    Returns:
        str: A Markdown string containing a list of job listings with the specified fields.
    
    Notes:
        - Descriptions are always included (show_description is hardcoded to True),
          truncated to 100 characters, and have HTML tags removed.
        - Published At is derived from the 'date_epoch' field, formatted as YYYY-MM-DD.
        - Apply URL is included as a clickable Markdown link for each job.
        - Source is credited to web3.career per API terms.
    """
    if limit > 100:
        raise ValueError("Limit cannot exceed 100")
    params = {"limit": limit}
    if remote is not None:
        params["remote"] = str(remote).lower()
    if country:
        params["country"] = country.lower().replace(" ", "-")
    if tag:
        params["tag"] = tag.lower()

    ctx.info(f"Querying jobs with parameters: {params}")
    jobs = await fetch_jobs(params)
    ctx.info(f"Retrieved {len(jobs)} jobs")
    return jobs_to_markdown(jobs, show_description=True)

# Prompt: Generate a job search query
@mcp.prompt()
def search_jobs_prompt(role: str, location: Optional[str] = None) -> List[base.Message]:
    """Generate a prompt for searching Web3 jobs based on role and optional location."""
    query = f"Find Web3 jobs for a {role} role"
    if location:
        query += f" in {location}"
    query += ". Provide job titles, companies, locations, and application links from web3.career."
    return [
        base.UserMessage(query),
        base.AssistantMessage("I'll search for relevant Web3 jobs. Here are the results:")
    ]

if __name__ == "__main__":
    mcp.run()
