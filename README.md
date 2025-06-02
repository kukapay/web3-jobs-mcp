# Web3 Jobs MCP Server

An MCP server that provides AI agents with real-time access to curated Web3 jobs from [web3.career](https://web3.career/), enabling intelligent job discovery and career insights.

![GitHub License](https://img.shields.io/github/license/kukapay/web3-jobs-mcp)
![Python Version](https://img.shields.io/badge/python-3.10+-blue)
![Status](https://img.shields.io/badge/status-active-brightgreen.svg)


## Features

- **Job Query Tool**: Filter Web3 jobs by:
  - Remote status (`remote=True` for remote-only jobs)
  - Country (e.g., `"United States"`, case-insensitive)
  - Job tag (e.g., `"react"`, `"blockchain"`, case-insensitive)
  - Limit (1–100 jobs, default 50)
- **Markdown Output**: Returns job listings as a formatted Markdown list with:
  - Job ID, Title, Company, Location, Remote status
  - Published At (from `date_epoch`, formatted as `YYYY-MM-DD`)
  - Apply URL (clickable link to web3.career)
  - Description (plain text, truncated to 100 characters)
- **Search Prompt**: Generates user-friendly job search queries based on role and optional location.

## Prerequisites

- Python 3.10+
- A web3.career API token (request at [web3.career/web3-jobs-api](https://web3.career/web3-jobs-api))
- [uv](https://github.com/astral-sh/uv) for dependency management (recommended)

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/kukapay/web3-jobs-mcp.git
   cd web3-jobs-mcp
   ```

2. **Install Dependencies**:
   Using `uv`:
   ```bash
   uv sync
   ```
   Alternatively, with `pip`:
   ```bash
   pip install mcp[cli] python-dotenv
   ```
   
3. **Installing to Claude Desktop**:

    Install the server as a Claude Desktop application:
    ```bash
    uv run mcp install cli.py --name "Web3 Jobs"
    ```

    Configuration file as a reference:

    ```json
    {
       "mcpServers": {
           "Web3 Jobs": {
               "command": "uv",
               "args": [ "--directory", "/path/to/web3-jobs-mcp", "run", "main.py" ],
               "env": { "WEB3_CAREER_API_TOKEN", "your-api-token" },  
           }
       }
    }
    ```
    Replace `/path/to/web3-jobs-mcp` with your actual installation path, and `your-api-token` with your web3.career API token.
    
## Usage

### Running the Server

Start the server in development mode with the MCP Inspector:
```bash
uv run mcp dev main.py
```
This opens a web interface for testing tools and prompts.

Alternatively, run directly:
```bash
uv run main.py
```

### Using the `query_jobs` Tool

In the MCP Inspector or a compatible client (e.g., Claude Desktop), call the `query_jobs` tool:

- **Example 1**: Get 5 remote blockchain jobs:
  ```bash
  query_jobs(remote=True, tag="blockchain", limit=5)
  ```

- **Example 2**: Get 10 jobs in the United States:
  ```bash
  query_jobs(country="United States", limit=10)
  ```

**Sample Output**:
```markdown
# Web3 Job Listings

- **Job ID**: 103945
  - **Title**: Applied Crypto-Economics & Mechanism Design
  - **Company**: Subzero Labs
  - **Location**: Remote Remote Remote
  - **Remote**: Yes
  - **Published At**: 2025-06-01
  - **Apply URL**: [Apply](https://web3.career/r/1QTOzATM__UVWHaa)
  - **Description**: About Rialo We are a pioneering force in the decentralized finance (DeFi) space...

- **Job ID**: 103944
  - **Title**: Blockchain Engineer
  - **Company**: CryptoTech
  - **Location**: Remote
  - **Remote**: Yes
  - **Published At**: 2025-05-31
  - **Description**: Join our team to build cutting-edge blockchain solutions for global clients...
  - **Apply URL**: [Apply](https://web3.career/r/2XYZabc123)

*Source: web3.career*
```

### Using the `search_jobs_prompt`

Generate a search prompt for a specific role and location:
```bash
/search_jobs_prompt role="blockchain developer" location="remote"
```
This returns a prompt like:
```
Find Web3 jobs for a blockchain developer role in remote. Provide job titles, companies, locations, and application links from web3.career.
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

