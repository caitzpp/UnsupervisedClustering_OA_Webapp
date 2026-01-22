# Osteoarthritis (OA) Severity Evaluation Webapp

**What?**  
A web application for evaluating unsupervised-generated clusters of osteoarthritis (OA) data.

**Who?**  
Designed for domain experts to provide feedback, or as a tool to explore OA data in embedding space.

**Why?**  
Developed as part of a master’s thesis. The goal is to support qualitative evaluation of clustering results and better understand relationships between data points and cluster assignments.

---

## Installation

The application can be run either:

- locally using Python, or  
- via Docker using a multi-container setup (recommended)

### Prerequisites

For Docker setup:
- Docker
- Docker Compose

For local Python setup:
- Python 3.10+ (recommended)
- pip or conda

### Step 1: Clone the repository

```bash
git clone <repository-url>
cd <repository-name>
```

### Step 2: Env. configuration
Copy the example environment file:
```bash
cp .env.example .env
```
Edit .env and provide the required variables.

* USE_LOCAL_ASSETS=true
Uses the local assets/ directory for loading data and images.
* If USE_LOCAL_ASSETS=false, Azure Blob Storage credentials must be provided to load assets remotely.

### Step 3: Run with Docker (recommended)

## Project Structure
```css
assets/
    raw/                    Raw OA datasets
    processed/              Processed datasets
    *.png / *.jpg           Image assets

dash_app/
    Visualization tool for exploring data in embedding space

streamlit_app/
    Main Streamlit application
    Embeds the Dash app
    Contains authentication, navigation, and application logic
```