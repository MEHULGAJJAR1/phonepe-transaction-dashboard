# PhonePe Transaction Dashboard — Comprehensive Documentation

**Version:** 1.0.0  
**Date:** March 2026  
**Document Type:** Technical & User Documentation  
**Classification:** Public

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Introduction](#2-introduction)
3. [System Architecture](#3-system-architecture)
4. [Features & Functionality](#4-features--functionality)
5. [User Interface Design](#5-user-interface-design)
6. [Installation & Setup Guide](#6-installation--setup-guide)
7. [API Documentation](#7-api-documentation)
8. [User Guide](#8-user-guide)
9. [Advanced Features](#9-advanced-features)
10. [Security & Compliance](#10-security--compliance)
11. [Performance Optimization](#11-performance-optimization)
12. [Troubleshooting & FAQs](#12-troubleshooting--faqs)
13. [Best Practices](#13-best-practices)
14. [Future Enhancements](#14-future-enhancements)

---

# 1. Executive Summary

## 1.1 Overview of the PhonePe Transaction Dashboard

The **PhonePe Transaction Dashboard** is a full-stack web application that provides real-time visibility into digital payment transactions processed through India's PhonePe payment platform. Built with a Python/Flask backend and an HTML/CSS/JavaScript frontend, the dashboard aggregates, visualises, and filters millions of transaction records stored in a MySQL relational database, enabling stakeholders to make data-driven decisions at a glance.

The platform ingests raw transaction, user, and insurance data exported from the PhonePe Pulse public data repository and loads it into normalised MySQL tables. Once loaded, the application exposes an intuitive browser-based interface that surfaces key performance indicators (KPIs), interactive charts, a state-level choropleth map, and paginated tabular data — all updated in near real time as new data is loaded.

The dashboard targets three distinct audiences:

| Audience | Primary Need |
|---|---|
| Business Analysts | Trend analysis, KPI monitoring, export-ready reports |
| System Administrators | Data pipeline management, performance tuning, access control |
| Developers | API integration, extending functionality, deployment |

In its current form, the platform handles data spanning multiple years and quarters across all 36 Indian states and union territories, covering transaction amounts totalling several trillion rupees and hundreds of millions of user registrations.

## 1.2 Key Features and Benefits

**Core Capabilities:**

- **Real-Time KPI Cards** — Instant display of total transaction value, total registered users, and total insurance value across the entire dataset.
- **Flexible Filtering** — Three-axis filtering by year, state, and transaction type with instant query execution.
- **Paginated Data Table** — Clean, paginated view of aggregated transaction records (20 rows per page) for detailed inspection.
- **Interactive Charts** — Year-over-year transaction trends (bar chart), transaction type distribution (pie/doughnut chart), and top-10 state rankings (horizontal bar chart) powered by Chart.js.
- **Geospatial Map View** — State-level heat map rendered via Plotly's choropleth engine, highlighting regional transaction concentration.
- **Top Performers Page** — Ranked table of top-10 states by transaction value.
- **REST API Layer** — JSON endpoints for yearly totals, transaction type breakdowns, and top-state data, enabling external integration.

**Business Benefits:**

- Reduces time-to-insight from hours (manual SQL queries) to seconds (browser interaction).
- Supports strategic decisions around market expansion, product prioritisation, and fraud detection.
- Provides a foundation for building more sophisticated analytics pipelines on top of the existing data model.
- Lightweight deployment footprint — runs on a single server with minimal dependencies.

## 1.3 Target Audience

This document is intended for:

- **Developers** who need to understand the codebase, extend the API, or integrate the dashboard with other systems.
- **System Administrators** responsible for deployment, configuration, and day-to-day maintenance.
- **End Users** (business analysts and managers) who interact with the dashboard through the browser.
- **Data Engineers** who manage the ETL pipeline that populates the underlying database.

---

# 2. Introduction

## 2.1 Background on Digital Payment Systems

The digital payments landscape in India has undergone a seismic transformation over the past decade. Driven by the government's Jan Dhan-Aadhaar-Mobile (JAM) trinity, the introduction of the Unified Payments Interface (UPI) in 2016, and the demonetisation event of the same year, India has become one of the world's largest and fastest-growing digital payments markets.

**Key Market Statistics (2023–2024):**

| Metric | Value |
|---|---|
| UPI monthly transactions | ~13–14 billion |
| UPI monthly value | ~₹20 lakh crore (~USD 240 billion) |
| Registered UPI users | ~350 million |
| PhonePe market share (UPI) | ~47–48% |

PhonePe, launched in 2015 and headquartered in Bengaluru, is India's leading digital payments platform by volume. It operates on the UPI rail and offers peer-to-peer transfers, merchant payments, bill payments, insurance, mutual funds, and gold investment — all from a single application. As of 2024, PhonePe processes approximately 6–7 billion transactions per month.

The sheer volume of transaction data generated by such platforms creates a pressing need for robust data infrastructure and accessible analytics tooling. The PhonePe Pulse initiative — a publicly available dataset of aggregated transaction metadata across states, districts, and pincodes — provides a rich foundation for this kind of analysis.

## 2.2 PhonePe Platform Overview

PhonePe's product ecosystem can be broadly categorised into four pillars:

1. **Payments** — P2P transfers, QR-code-based merchant payments, UPI autopay (recurring payments).
2. **Financial Services** — Mutual funds, digital gold, fixed deposits, loans, insurance (two-wheeler, life, health).
3. **Commerce** — Recharges, utility bill payments, travel bookings, e-commerce checkout integrations.
4. **Platform (PhonePe for Business)** — Payment gateway APIs for merchants and enterprises.

Transaction types captured in the PhonePe Pulse dataset that this dashboard visualises include:

- **Peer-to-Peer (P2P)** — Direct fund transfers between individuals.
- **Peer-to-Merchant (P2M)** — Payments to registered merchants.
- **Recharge & Bill Payments** — Mobile recharges, electricity, water, gas bills.
- **Financial Services** — Insurance premiums, mutual fund SIPs, gold purchases.
- **Others** — Miscellaneous transactions that do not fall into the above categories.

## 2.3 Dashboard Purpose and Objectives

The PhonePe Transaction Dashboard was built to bridge the gap between raw, file-based transaction data (JSON/CSV exports from the PhonePe Pulse repository) and actionable visual analytics. Its design objectives are:

**Objective 1 — Centralised Data Repository**  
Consolidate transaction, user, and insurance data from multiple data sources (state-level JSON files) into a single, queryable MySQL database.

**Objective 2 — Accessible Analytics**  
Provide a browser-based interface that requires no SQL knowledge, enabling non-technical stakeholders to explore the data independently.

**Objective 3 — Extensibility**  
Expose a clean REST API so that the dashboard's data layer can feed downstream systems such as BI tools (Tableau, Power BI) or custom reporting workflows.

**Objective 4 — Performance**  
Deliver page loads and chart renders in under two seconds even for datasets with millions of rows, through appropriate use of SQL aggregation, indexing, and pagination.

**Objective 5 — Simplicity of Deployment**  
Keep the dependency footprint minimal so that the application can run on a modest server or a local development machine without complex infrastructure.

---

# 3. System Architecture

## 3.1 Technical Stack

The application is implemented using a compact, well-understood stack:

| Layer | Technology | Version | Proportion of Codebase |
|---|---|---|---|
| Backend | Python 3.x / Flask | Flask 2.x | ~45.4% |
| Frontend (Structure) | HTML5 (Jinja2 templates) | — | ~32.7% |
| Frontend (Styling) | CSS3 | — | ~21.9% |
| Database | MySQL 8.x | — | — |
| Charts | Chart.js | 4.x | — |
| Maps | Plotly.js | 5.x | — |
| WSGI Server (production) | Gunicorn | 20.x | — |

**Python Dependencies (requirements.txt):**

```
Flask
mysql-connector-python
pandas
matplotlib
seaborn
plotly
numpy
requests
gunicorn
```

## 3.2 Backend Architecture

The backend follows a straightforward **monolithic Flask application** pattern. All routes, database queries, and business logic reside in a single `app.py` file, with database connectivity abstracted into `db_connection.py`.

```
backend/
├── app.py                          # Main Flask application (routes + logic)
├── db_connection.py                # MySQL connection factory
├── charts.py                       # Chart generation helpers (Matplotlib/Seaborn)
├── generate_charts.py              # Standalone chart generation script
├── load_all_data.py                # Orchestrates all ETL loaders
├── load_aggregated_transaction.py  # ETL: aggregated_transaction table
├── load_aggregated_transaction_state.py
├── load_aggregated_user.py         # ETL: aggregated_user table
├── load_aggregated_insurance.py    # ETL: aggregated_insurance table
├── load_map_transaction.py         # ETL: map_transaction table
├── load_map_transaction_state.py
├── load_map_user.py                # ETL: map_user table
├── load_map_insurance.py           # ETL: map_insurance table
├── load_top_transaction.py         # ETL: top_transaction table
├── load_top_user.py                # ETL: top_user table
├── load_top_insurance.py           # ETL: top_insurance table
├── requirements.txt
├── static/                         # CSS, JS, images
└── templates/                      # Jinja2 HTML templates
```

**Request Lifecycle:**

```
Browser
  │
  ▼
HTTP Request (GET /)
  │
  ▼
Flask Router (app.py)
  │
  ├─► db_connection.get_connection() → MySQL Connection
  │       │
  │       └─► SQL Query Execution → Result Set
  │
  ├─► Business Logic (filtering, pagination)
  │
  └─► render_template(template, **context)
            │
            ▼
        Jinja2 Template Engine
            │
            ▼
        HTML Response → Browser
```

**Connection Management:**  
Each HTTP request opens a new database connection and closes it before returning the response. This pattern is simple and correct for low-to-medium traffic loads. For production deployments handling concurrent users, a connection pool (e.g., SQLAlchemy with pool_size configuration) is recommended.

## 3.3 Frontend Components

The frontend is rendered server-side by Flask's Jinja2 template engine. JavaScript is used exclusively for client-side chart rendering via CDN-hosted Chart.js and Plotly libraries — there is no client-side routing or SPA framework.

**Template Inventory:**

| Template | Route | Purpose |
|---|---|---|
| `index.html` | `/` | Main dashboard: KPI cards, filters, data table, pagination |
| `charts.html` | `/charts` | Interactive charts page (yearly trend, type distribution) |
| `map.html` | `/map` | Choropleth map of state-level transaction amounts |
| `top.html` | `/top` | Top-10 states by transaction value |
| `about.html` | `/about` | About/information page |

**Static Assets:**

```
backend/static/
├── css/
│   └── style.css          # Global stylesheet
├── js/
│   └── charts.js          # Chart.js initialisation and data fetch logic
└── images/
    └── phonepe-logo.png   # Brand asset
```

## 3.4 Database Design

The application uses a MySQL database named `phonepe_db`. The schema mirrors the structure of the PhonePe Pulse public dataset, organised into three tiers — **Aggregated**, **Map**, and **Top** — each covering three domains: **Transaction**, **User**, and **Insurance**.

**Entity-Relationship Overview:**

```
aggregated_transaction        map_transaction           top_transaction
──────────────────────        ───────────────           ───────────────
state (VARCHAR)               state (VARCHAR)           state (VARCHAR)
year (INT)                    year (INT)                year (INT)
quarter (INT)                 quarter (INT)             quarter (INT)
transaction_type (VARCHAR)    district (VARCHAR)        district (VARCHAR)
transaction_amount (DECIMAL)  transaction_amount (DEC)  pincode (VARCHAR)
transaction_count (BIGINT)    transaction_count (BIGINT) transaction_amount (DEC)
                                                        transaction_count (BIGINT)

aggregated_user               map_user                  top_user
───────────────               ────────                  ────────
state (VARCHAR)               state (VARCHAR)           state (VARCHAR)
year (INT)                    year (INT)                year (INT)
quarter (INT)                 quarter (INT)             quarter (INT)
user_count (BIGINT)           district (VARCHAR)        district (VARCHAR)
                              registered_users (BIGINT) pincode (VARCHAR)
                                                        registered_users (BIGINT)

aggregated_insurance          map_insurance             top_insurance
────────────────────          ─────────────             ─────────────
state (VARCHAR)               state (VARCHAR)           state (VARCHAR)
year (INT)                    year (INT)                year (INT)
quarter (INT)                 quarter (INT)             quarter (INT)
insurance_amount (DECIMAL)    district (VARCHAR)        district (VARCHAR)
insurance_count (BIGINT)      insurance_amount (DEC)    pincode (VARCHAR)
                              insurance_count (BIGINT)  insurance_amount (DEC)
                                                        insurance_count (BIGINT)
```

**Recommended Indexes:**

```sql
-- Aggregated transaction: most frequently queried table
CREATE INDEX idx_agg_txn_year   ON aggregated_transaction(year);
CREATE INDEX idx_agg_txn_state  ON aggregated_transaction(state);
CREATE INDEX idx_agg_txn_type   ON aggregated_transaction(transaction_type);

-- Map transaction: used for choropleth and top-states queries
CREATE INDEX idx_map_txn_state  ON map_transaction(state);
```

---

# 4. Features & Functionality

## 4.1 Transaction Viewing and Filtering

The main dashboard page (`/`) is the application's primary interface. It presents three interactive dropdown filters that can be combined in any permutation:

| Filter | Source Column | Default Behaviour |
|---|---|---|
| Year | `aggregated_transaction.year` | All years (no filter) |
| State | `map_transaction.state` | All states |
| Transaction Type | `aggregated_transaction.transaction_type` | All types |

When the user selects values and submits the form, Flask constructs a parameterised SQL query dynamically:

```python
query = """
SELECT state, year, quarter, transaction_type,
SUM(transaction_amount), SUM(transaction_count)
FROM aggregated_transaction
WHERE 1=1
"""
params = []

if year and year != "":
    query += " AND year=%s"
    params.append(year)

if state and state != "":
    query += " AND state=%s"
    params.append(state)

if ttype and ttype != "":
    query += " AND transaction_type=%s"
    params.append(ttype)

query += """
GROUP BY state, year, quarter, transaction_type
LIMIT %s OFFSET %s
"""
params.extend([per_page, offset])
```

The use of parameterised queries (`%s` placeholders with a separate `params` list) prevents SQL injection attacks.

## 4.2 Real-Time Analytics and Reporting

Three summary KPI cards appear at the top of the main dashboard, computed from `SELECT SUM(...)` queries:

| Card | Source Query | Display |
|---|---|---|
| Total Transaction Value | `SUM(transaction_amount)` from `aggregated_transaction` | Formatted rupee value |
| Total Registered Users | `SUM(user_count)` from `aggregated_user` | Formatted integer |
| Total Insurance Value | `SUM(insurance_amount)` from `aggregated_insurance` | Formatted rupee value |

These values reflect the entire dataset and are not affected by the filter controls — they provide a persistent, unfiltered baseline for context.

## 4.3 Payment Methods Overview

The **Transaction Types** chart on the `/charts` page breaks down total transaction value by payment category. The data is fetched from the `/api/types` endpoint:

```json
{
  "types": ["Peer-to-peer payments", "Merchant payments", "Recharge & bill payments", "Financial Services", "Others"],
  "amounts": [1234567890.00, 987654321.00, ...]
}
```

This allows analysts to instantly identify which payment modalities dominate the PhonePe network and how they trend over time.

## 4.4 Transaction History Management

All historical transaction data is stored persistently in MySQL. The ETL pipeline (`load_all_data.py`) is designed to be re-run safely — each loader script typically truncates or upserts its target table before inserting new records, preventing duplication.

**ETL Pipeline Flow:**

```
PhonePe Pulse JSON Files
        │
        ▼
load_aggregated_transaction.py  ──► aggregated_transaction
load_aggregated_user.py         ──► aggregated_user
load_aggregated_insurance.py    ──► aggregated_insurance
load_map_transaction.py         ──► map_transaction
load_map_user.py                ──► map_user
load_map_insurance.py           ──► map_insurance
load_top_transaction.py         ──► top_transaction
load_top_user.py                ──► top_user
load_top_insurance.py           ──► top_insurance
        │
        ▼
   load_all_data.py (orchestrator)
```

## 4.5 Search and Sorting Capabilities

The current filtering system operates through HTML `<select>` dropdowns submitted via HTTP GET. Filter state is preserved in the URL query string (e.g., `/?year=2022&state=Maharashtra&type=P2P`), making filtered views bookmarkable and shareable.

**Pagination** is implemented server-side:

```python
page     = request.args.get("page", 1, type=int)
per_page = 20
offset   = (page - 1) * per_page
```

The current page number is appended to the URL as `?page=N`, enabling browser back/forward navigation to work correctly.

## 4.6 Status Tracking

The dashboard tracks three high-level status metrics in real time via the KPI cards:

1. **Transaction Volume** — Total monetary value transacted across all time, states, and types.
2. **User Adoption** — Total number of registered PhonePe users.
3. **Insurance Penetration** — Total insurance premium value, indicating how deeply insurance products have been adopted alongside the core payments product.

These macro indicators serve as quick health checks for the PhonePe ecosystem.

---

# 5. User Interface Design

## 5.1 Dashboard Layout and Components

The main dashboard (`index.html`) follows a **top-down linear layout** with four distinct zones:

```
┌─────────────────────────────────────────────┐
│  Navigation Bar  (Logo | Nav Links)          │
├─────────────────────────────────────────────┤
│  KPI Cards Row   (3 cards, equal width)      │
├─────────────────────────────────────────────┤
│  Filter Controls (Year | State | Type | Go)  │
├─────────────────────────────────────────────┤
│  Data Table      (paginated, 20 rows)        │
│  Pagination Bar                              │
└─────────────────────────────────────────────┘
```

**Navigation Bar** contains the PhonePe logo, links to Dashboard (`/`), Charts (`/charts`), Map (`/map`), Top Performers (`/top`), and About (`/about`).

**KPI Cards** use a three-column flexbox row. Each card has an icon, a label, and a large numerical value formatted for readability.

**Filter Controls** use a horizontal flexbox row of `<select>` elements and a submit button, all wrapped in a `<form method="GET">` tag. The current filter values are pre-selected on page load by comparing them to the query string parameters passed from Flask.

**Data Table** renders a standard HTML `<table>` with `<thead>` and `<tbody>` sections. Column headers are: State, Year, Quarter, Type, Total Amount, and Total Count.

## 5.2 Navigation Structure

```
/ (Dashboard)
├── /charts   (Interactive Charts)
├── /map      (Geospatial Map)
├── /top      (Top Performers)
└── /about    (About Page)

REST API Endpoints (no UI):
├── /api/yearly
├── /api/types
└── /api/topstates
```

The navigation is persistent across all pages, rendered in the `<nav>` section of each template. Active page highlighting is applied using Jinja2 conditional logic:

```html
<a href="/" class="{{ 'active' if request.path == '/' else '' }}">Dashboard</a>
```

## 5.3 HTML/CSS Design Patterns

The application uses **vanilla CSS3** without any CSS framework (Bootstrap, Tailwind, etc.). The stylesheet (`static/css/style.css`) defines:

**Colour Palette:**

| Token | Value | Usage |
|---|---|---|
| Primary Purple | `#6A0DAD` | Navigation, headings, buttons |
| Accent Light Purple | `#9B59B6` | Hover states, secondary elements |
| Background | `#F4F0F8` | Page background |
| Card Background | `#FFFFFF` | KPI cards, table container |
| Text Primary | `#2C2C2C` | Body text |
| Text Secondary | `#666666` | Labels, captions |
| Success Green | `#27AE60` | Positive indicators |
| Danger Red | `#E74C3C` | Error states |

**Layout Patterns:**

```css
/* KPI Cards Row */
.cards-row {
    display: flex;
    gap: 1.5rem;
    justify-content: space-between;
    margin-bottom: 2rem;
}

/* Individual Card */
.card {
    flex: 1;
    background: #fff;
    border-radius: 12px;
    padding: 1.5rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}

/* Filter Row */
.filter-row {
    display: flex;
    gap: 1rem;
    align-items: center;
    margin-bottom: 1.5rem;
}
```

**Typography:**

The application uses the system font stack for maximum compatibility:

```css
body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI',
                 Roboto, Oxygen, Ubuntu, sans-serif;
    font-size: 16px;
    line-height: 1.6;
}
```

## 5.4 Responsive Design Principles

The layout adapts to different viewport sizes using CSS media queries:

```css
@media (max-width: 768px) {
    .cards-row {
        flex-direction: column;
    }
    .filter-row {
        flex-wrap: wrap;
    }
    table {
        display: block;
        overflow-x: auto;
    }
}
```

On mobile devices:
- KPI cards stack vertically.
- Filter controls wrap to multiple lines.
- Tables become horizontally scrollable.
- The navigation collapses to a hamburger menu (if implemented).

## 5.5 User Experience Best Practices

**Progressive Disclosure** — Complex chart and map views are segregated onto dedicated pages (`/charts`, `/map`) rather than loading everything on the main dashboard, keeping initial page load fast.

**State Preservation** — All filter selections are reflected in the URL query string, so users can bookmark or share a specific filtered view.

**Empty State Handling** — When no data matches the applied filters, the table renders an empty `<tbody>` with a "No records found" message, preventing a blank or confusing layout.

**Loading Feedback** — Chart pages call the REST API asynchronously on page load. A spinner or skeleton state should be shown while the fetch is in progress (recommended enhancement for future iterations).

**Accessibility** — Form elements use `<label>` tags with `for` attributes to link labels to their corresponding `<select>` controls. Table headers use `<th scope="col">` for screen-reader compatibility.

---

# 6. Installation & Setup Guide

## 6.1 System Requirements

| Component | Minimum | Recommended |
|---|---|---|
| OS | Ubuntu 20.04 / Windows 10 | Ubuntu 22.04 LTS |
| Python | 3.8 | 3.11 |
| MySQL | 8.0 | 8.0.x (latest patch) |
| RAM | 2 GB | 4 GB |
| Disk | 5 GB free | 20 GB free (for full dataset) |
| CPU | 2 cores | 4 cores |
| Network | Internet access (for pip install) | — |

## 6.2 Installation Steps

### Step 1 — Clone the Repository

```bash
git clone https://github.com/MEHULGAJJAR1/phonepe-transaction-dashboard.git
cd phonepe-transaction-dashboard
```

### Step 2 — Create and Activate a Virtual Environment

```bash
# Create the virtual environment
python -m venv venv

# Activate (Linux/macOS)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate
```

### Step 3 — Install Python Dependencies

```bash
pip install -r backend/requirements.txt
```

### Step 4 — Install and Configure MySQL

```bash
# Ubuntu
sudo apt update
sudo apt install mysql-server -y
sudo systemctl start mysql
sudo systemctl enable mysql

# Set root password (first-time setup)
sudo mysql_secure_installation
```

### Step 5 — Create the Database

```sql
-- Log in to MySQL
mysql -u root -p

-- Create database
CREATE DATABASE phonepe_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Verify
SHOW DATABASES;
EXIT;
```

### Step 6 — Configure Database Credentials

Open `backend/db_connection.py` and update the connection parameters to match your environment:

```python
import mysql.connector

def get_connection():
    connection = mysql.connector.connect(
        host="localhost",      # MySQL server host
        user="root",           # MySQL username
        password="YOUR_PWD",   # MySQL password
        database="phonepe_db"  # Database name
    )
    return connection
```

> **Security Note:** In production, store credentials in environment variables rather than hardcoding them. See Section 10 for details.

### Step 7 — Load the Data

```bash
cd backend
python load_all_data.py
```

This will execute all ETL loaders in sequence. The initial load may take several minutes depending on dataset size and hardware.

### Step 8 — Start the Development Server

```bash
cd backend
python app.py
```

The application will start on `http://127.0.0.1:5000/` by default.

## 6.3 Configuration Guide

Flask supports configuration through environment variables or a configuration file. For a quick development setup, you can set the following environment variables before starting the server:

```bash
export FLASK_APP=backend/app.py
export FLASK_ENV=development    # Enables debug mode and auto-reload
export FLASK_DEBUG=1
```

For MySQL connection parameters, the recommended approach is:

```python
import os, mysql.connector

def get_connection():
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        user=os.environ.get("DB_USER", "root"),
        password=os.environ.get("DB_PASSWORD", ""),
        database=os.environ.get("DB_NAME", "phonepe_db")
    )
```

Then set variables in your shell or in a `.env` file (loaded with `python-dotenv`):

```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_secure_password
DB_NAME=phonepe_db
```

## 6.4 Environment Setup

**Development Environment:**

```bash
export FLASK_ENV=development
export FLASK_DEBUG=1
cd backend && python app.py
```

**Production Environment (using Gunicorn):**

```bash
cd backend
gunicorn --workers 4 --bind 0.0.0.0:8000 app:app
```

**Reverse Proxy (Nginx) configuration:**

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass         http://127.0.0.1:8000;
        proxy_set_header   Host $host;
        proxy_set_header   X-Real-IP $remote_addr;
        proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /static/ {
        alias /path/to/backend/static/;
        expires 30d;
    }
}
```

## 6.5 Database Initialization

To initialise the database schema from scratch, run the following SQL script:

```sql
USE phonepe_db;

CREATE TABLE IF NOT EXISTS aggregated_transaction (
    id                 BIGINT AUTO_INCREMENT PRIMARY KEY,
    state              VARCHAR(100) NOT NULL,
    year               SMALLINT     NOT NULL,
    quarter            TINYINT      NOT NULL,
    transaction_type   VARCHAR(100) NOT NULL,
    transaction_amount DECIMAL(20,2),
    transaction_count  BIGINT,
    INDEX (year),
    INDEX (state),
    INDEX (transaction_type)
);

CREATE TABLE IF NOT EXISTS aggregated_user (
    id          BIGINT AUTO_INCREMENT PRIMARY KEY,
    state       VARCHAR(100) NOT NULL,
    year        SMALLINT     NOT NULL,
    quarter     TINYINT      NOT NULL,
    user_count  BIGINT,
    INDEX (year),
    INDEX (state)
);

CREATE TABLE IF NOT EXISTS aggregated_insurance (
    id                BIGINT AUTO_INCREMENT PRIMARY KEY,
    state             VARCHAR(100) NOT NULL,
    year              SMALLINT     NOT NULL,
    quarter           TINYINT      NOT NULL,
    insurance_amount  DECIMAL(20,2),
    insurance_count   BIGINT,
    INDEX (year),
    INDEX (state)
);

CREATE TABLE IF NOT EXISTS map_transaction (
    id                 BIGINT AUTO_INCREMENT PRIMARY KEY,
    state              VARCHAR(100) NOT NULL,
    year               SMALLINT     NOT NULL,
    quarter            TINYINT      NOT NULL,
    district           VARCHAR(150),
    transaction_amount DECIMAL(20,2),
    transaction_count  BIGINT,
    INDEX (state),
    INDEX (year)
);

CREATE TABLE IF NOT EXISTS map_user (
    id               BIGINT AUTO_INCREMENT PRIMARY KEY,
    state            VARCHAR(100) NOT NULL,
    year             SMALLINT     NOT NULL,
    quarter          TINYINT      NOT NULL,
    district         VARCHAR(150),
    registered_users BIGINT,
    INDEX (state)
);

CREATE TABLE IF NOT EXISTS map_insurance (
    id               BIGINT AUTO_INCREMENT PRIMARY KEY,
    state            VARCHAR(100) NOT NULL,
    year             SMALLINT     NOT NULL,
    quarter          TINYINT      NOT NULL,
    district         VARCHAR(150),
    insurance_amount DECIMAL(20,2),
    insurance_count  BIGINT,
    INDEX (state)
);

CREATE TABLE IF NOT EXISTS top_transaction (
    id                 BIGINT AUTO_INCREMENT PRIMARY KEY,
    state              VARCHAR(100) NOT NULL,
    year               SMALLINT     NOT NULL,
    quarter            TINYINT      NOT NULL,
    district           VARCHAR(150),
    pincode            VARCHAR(20),
    transaction_amount DECIMAL(20,2),
    transaction_count  BIGINT
);

CREATE TABLE IF NOT EXISTS top_user (
    id               BIGINT AUTO_INCREMENT PRIMARY KEY,
    state            VARCHAR(100) NOT NULL,
    year             SMALLINT     NOT NULL,
    quarter          TINYINT      NOT NULL,
    district         VARCHAR(150),
    pincode          VARCHAR(20),
    registered_users BIGINT
);

CREATE TABLE IF NOT EXISTS top_insurance (
    id               BIGINT AUTO_INCREMENT PRIMARY KEY,
    state            VARCHAR(100) NOT NULL,
    year             SMALLINT     NOT NULL,
    quarter          TINYINT      NOT NULL,
    district         VARCHAR(150),
    pincode          VARCHAR(20),
    insurance_amount DECIMAL(20,2),
    insurance_count  BIGINT
);
```

---

# 7. API Documentation

## 7.1 REST API Endpoints

The dashboard exposes three JSON REST API endpoints under the `/api/` prefix. All endpoints use HTTP GET and return `application/json` responses.

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/yearly` | Total transaction amounts grouped by year |
| GET | `/api/types` | Total transaction amounts grouped by transaction type |
| GET | `/api/topstates` | Top 10 states ranked by total transaction amount |

Additionally, the main HTML routes can be considered semi-API endpoints in that they accept query string parameters:

| Method | Endpoint | Query Parameters |
|---|---|---|
| GET | `/` | `year`, `state`, `type`, `page` |
| GET | `/charts` | — |
| GET | `/map` | — |
| GET | `/top` | — |

## 7.2 Request/Response Formats

### GET /api/yearly

**Description:** Returns total transaction amounts grouped by calendar year.

**Request:**
```
GET /api/yearly HTTP/1.1
Host: localhost:5000
```

**Response (200 OK):**
```json
{
  "years": [2018, 2019, 2020, 2021, 2022, 2023],
  "amounts": [
    125000000000.00,
    480000000000.00,
    1200000000000.00,
    2800000000000.00,
    5600000000000.00,
    9800000000000.00
  ]
}
```

**Field Descriptions:**

| Field | Type | Description |
|---|---|---|
| `years` | `Array<int>` | Calendar years present in the dataset |
| `amounts` | `Array<float>` | Total transaction amount (INR) for each year |

---

### GET /api/types

**Description:** Returns total transaction amounts grouped by transaction type.

**Request:**
```
GET /api/types HTTP/1.1
Host: localhost:5000
```

**Response (200 OK):**
```json
{
  "types": [
    "Financial Services",
    "Merchant payments",
    "Others",
    "Peer-to-peer payments",
    "Recharge & bill payments"
  ],
  "amounts": [
    450000000000.00,
    8200000000000.00,
    320000000000.00,
    12500000000000.00,
    1800000000000.00
  ]
}
```

**Field Descriptions:**

| Field | Type | Description |
|---|---|---|
| `types` | `Array<string>` | Distinct transaction type labels |
| `amounts` | `Array<float>` | Total transaction amount (INR) for each type |

---

### GET /api/topstates

**Description:** Returns the top 10 states ranked by total transaction amount from the `map_transaction` table.

**Request:**
```
GET /api/topstates HTTP/1.1
Host: localhost:5000
```

**Response (200 OK):**
```json
{
  "states": [
    "Telangana",
    "Maharashtra",
    "Karnataka",
    "Andhra Pradesh",
    "Rajasthan",
    "Uttar Pradesh",
    "Tamil Nadu",
    "Gujarat",
    "West Bengal",
    "Madhya Pradesh"
  ],
  "amounts": [
    18000000000000.00,
    14500000000000.00,
    12200000000000.00,
    10800000000000.00,
    9500000000000.00,
    8900000000000.00,
    8200000000000.00,
    7600000000000.00,
    6800000000000.00,
    6100000000000.00
  ]
}
```

## 7.3 Authentication Methods

**Current State:** The API endpoints are unauthenticated. They are intended for internal frontend consumption only (Chart.js makes fetch calls to these endpoints from the same origin).

**Recommended Authentication for External Access:**

For production deployments where the API needs to be accessed by external clients, implement token-based authentication using Flask-JWT-Extended:

```python
from flask_jwt_extended import JWTManager, jwt_required, create_access_token

app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")
jwt = JWTManager(app)

@app.route("/api/yearly")
@jwt_required()
def yearly_chart():
    # ... existing implementation
```

**Obtaining a Token:**

```bash
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "secret"}'
```

**Using the Token:**

```bash
curl http://localhost:5000/api/yearly \
  -H "Authorization: Bearer <your_token_here>"
```

## 7.4 Error Handling

The application currently returns Flask's default error pages for HTTP errors. For a production-grade API, structured JSON error responses are recommended:

```python
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found", "status": 404}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error", "status": 500}), 500

@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": "Bad request", "status": 400}), 400
```

**Common HTTP Status Codes:**

| Code | Meaning | When Returned |
|---|---|---|
| 200 | OK | Successful GET request |
| 400 | Bad Request | Invalid query parameters |
| 404 | Not Found | Route does not exist |
| 500 | Internal Server Error | Unhandled exception (DB unavailable, etc.) |

## 7.5 Rate Limiting

**Current State:** No rate limiting is implemented.

**Recommended Implementation using Flask-Limiter:**

```bash
pip install Flask-Limiter
```

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route("/api/yearly")
@limiter.limit("30 per minute")
def yearly_chart():
    # ... existing implementation
```

**Rate Limit Headers (added automatically by Flask-Limiter):**

```
X-RateLimit-Limit: 30
X-RateLimit-Remaining: 29
X-RateLimit-Reset: 1700000000
```

When the rate limit is exceeded:

```json
HTTP/1.1 429 Too Many Requests
{
  "error": "Rate limit exceeded",
  "retry_after": 42
}
```

---

# 8. User Guide

## 8.1 Getting Started

### Prerequisites

Before using the PhonePe Transaction Dashboard, ensure:

1. The application is running (either locally or on a server).
2. The database has been populated with PhonePe Pulse data.
3. You have a modern web browser (Chrome 90+, Firefox 88+, Safari 14+, Edge 90+).

### Accessing the Dashboard

Open your web browser and navigate to:

- **Development:** `http://localhost:5000`
- **Production:** `https://your-domain.com`

You will be taken directly to the main dashboard page.

## 8.2 Navigating the Dashboard

The navigation bar at the top of every page provides links to all major sections:

| Link | URL | Description |
|---|---|---|
| Dashboard | `/` | Main page with KPIs, filters, and data table |
| Charts | `/charts` | Interactive bar and pie charts |
| Map | `/map` | State-level choropleth map |
| Top | `/top` | Top 10 states by transaction value |
| About | `/about` | Application information |

Click any link to navigate to that section. Your browser's back and forward buttons work normally, and filter states are preserved in the URL.

## 8.3 Filtering and Searching Transactions

On the main Dashboard page:

**Step 1:** Locate the filter row below the KPI cards.

**Step 2:** Select values from one or more dropdowns:
- **Year** — Select a specific calendar year (e.g., 2022).
- **State** — Select a specific Indian state or union territory.
- **Transaction Type** — Select a payment category (e.g., Peer-to-peer payments).

**Step 3:** Click the **Apply Filters** (or **Go**) button.

**Step 4:** The data table below refreshes with results matching your selected criteria. The total count of matching records and the current page are shown.

**Clearing Filters:**  
To remove all filters and view the complete dataset, select the default "All" option in each dropdown and click Apply Filters, or navigate directly to `http://localhost:5000/`.

**Bookmarking a Filtered View:**  
The current filter state is encoded in the URL query string. For example:
```
http://localhost:5000/?year=2022&state=Maharashtra&type=Peer-to-peer+payments
```
Bookmark this URL in your browser to return to the same filtered view later.

## 8.4 Generating Reports

**Using the Charts Page:**

1. Navigate to `/charts`.
2. Two charts load automatically:
   - **Yearly Transaction Trend** (bar chart) — Compares total transaction values across years.
   - **Transaction Type Distribution** (doughnut chart) — Shows the proportional breakdown by payment category.
3. Hover over chart elements to see precise values in tooltips.
4. Click legend items to toggle individual series on/off.

**Using the Map Page:**

1. Navigate to `/map`.
2. An interactive choropleth map of India loads, colour-coded by total transaction amount.
3. Hover over a state to see its name and total transaction value.
4. Zoom and pan the map using mouse scroll and drag (Plotly controls).

## 8.5 Exporting Data

**Current Export Capabilities:**

The application does not currently provide a built-in export button. However, data can be exported via the following methods:

**Method 1 — Browser Table Copy:**  
Select all rows in the data table (`Ctrl+A` on the table), copy, and paste into Excel or Google Sheets.

**Method 2 — API Export via curl:**
```bash
# Export yearly data as JSON
curl http://localhost:5000/api/yearly > yearly_data.json

# Export type data as JSON
curl http://localhost:5000/api/types > type_data.json
```

**Method 3 — Direct MySQL Export:**
```bash
mysql -u root -p phonepe_db \
  -e "SELECT * FROM aggregated_transaction" \
  | sed 's/\t/,/g' > export.csv
```

**Method 4 — Python pandas Export (recommended for analysts):**
```python
import pandas as pd
import mysql.connector

conn = mysql.connector.connect(
    host="localhost", user="root",
    password="YOUR_PWD", database="phonepe_db"
)

df = pd.read_sql("SELECT * FROM aggregated_transaction", conn)
df.to_csv("aggregated_transaction_export.csv", index=False)
df.to_excel("aggregated_transaction_export.xlsx", index=False)

conn.close()
```

## 8.6 Account Management

The current version of the dashboard does not implement user accounts or authentication — it is designed as an internal tool with network-level access control (i.e., accessible only from within a trusted network or via VPN).

For multi-user deployments requiring individual access control, see Section 10 (Security & Compliance) and the Authentication recommendations in Section 7.3.

---

# 9. Advanced Features

## 9.1 Custom Analytics

The existing SQL schema supports a wide range of ad-hoc analytics beyond what the UI exposes. Some useful custom queries:

**Quarter-over-Quarter Growth Rate:**
```sql
SELECT
    year,
    quarter,
    SUM(transaction_amount) AS total_amount,
    LAG(SUM(transaction_amount)) OVER (ORDER BY year, quarter) AS prev_quarter,
    ROUND(
        (SUM(transaction_amount) - LAG(SUM(transaction_amount))
          OVER (ORDER BY year, quarter))
        / LAG(SUM(transaction_amount)) OVER (ORDER BY year, quarter) * 100,
        2
    ) AS qoq_growth_pct
FROM aggregated_transaction
GROUP BY year, quarter
ORDER BY year, quarter;
```

**State Market Share:**
```sql
SELECT
    state,
    SUM(transaction_amount) AS state_total,
    ROUND(SUM(transaction_amount) /
        (SELECT SUM(transaction_amount) FROM map_transaction) * 100, 2
    ) AS market_share_pct
FROM map_transaction
GROUP BY state
ORDER BY state_total DESC;
```

**Year-over-Year Comparison by State:**
```sql
SELECT
    state,
    SUM(CASE WHEN year = 2022 THEN transaction_amount ELSE 0 END) AS y2022,
    SUM(CASE WHEN year = 2023 THEN transaction_amount ELSE 0 END) AS y2023,
    ROUND(
        (SUM(CASE WHEN year = 2023 THEN transaction_amount ELSE 0 END) -
         SUM(CASE WHEN year = 2022 THEN transaction_amount ELSE 0 END))
        / NULLIF(SUM(CASE WHEN year = 2022 THEN transaction_amount ELSE 0 END), 0) * 100,
        2
    ) AS yoy_growth_pct
FROM map_transaction
GROUP BY state
ORDER BY yoy_growth_pct DESC;
```

## 9.2 Data Visualization

The dashboard currently uses:

- **Chart.js** for the bar and doughnut charts on the `/charts` page.
- **Plotly** for the choropleth map on the `/map` page.
- **Matplotlib / Seaborn** (available in `charts.py` and `generate_charts.py`) for generating static PNG images server-side.

**Extending Chart.js Visualisations:**

To add a new chart to the `/charts` page, follow this pattern:

1. Add a new API endpoint in `app.py`:
```python
@app.route("/api/quarterly")
def quarterly_chart():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT year, quarter, SUM(transaction_amount)
        FROM aggregated_transaction
        GROUP BY year, quarter
        ORDER BY year, quarter
    """)
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify({
        "labels": [f"Q{r[1]} {r[0]}" for r in data],
        "amounts": [float(r[2]) for r in data]
    })
```

2. Add a `<canvas>` element to `charts.html`:
```html
<canvas id="quarterlyChart"></canvas>
```

3. Fetch and render in the JavaScript section:
```javascript
fetch('/api/quarterly')
  .then(r => r.json())
  .then(data => {
    new Chart(document.getElementById('quarterlyChart'), {
      type: 'line',
      data: {
        labels: data.labels,
        datasets: [{
          label: 'Transaction Amount (₹)',
          data: data.amounts,
          borderColor: '#6A0DAD',
          fill: false
        }]
      }
    });
  });
```

## 9.3 Alert Systems

Currently, no automated alert system exists. A recommended implementation using Python's `smtplib` and a scheduled job (cron or APScheduler):

```python
# alert_monitor.py
import smtplib, mysql.connector
from email.mime.text import MIMEText
from apscheduler.schedulers.blocking import BlockingScheduler

THRESHOLD_AMOUNT = 1_000_000_000  # Alert if daily total exceeds ₹1 billion

def check_daily_threshold():
    conn = mysql.connector.connect(...)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT SUM(transaction_amount)
        FROM aggregated_transaction
        WHERE year = YEAR(CURDATE()) AND quarter = QUARTER(CURDATE())
    """)
    total = cursor.fetchone()[0] or 0
    conn.close()

    if total > THRESHOLD_AMOUNT:
        send_alert_email(total)

def send_alert_email(total):
    msg = MIMEText(f"Daily transaction threshold exceeded: ₹{total:,.2f}")
    msg["Subject"] = "PhonePe Dashboard Alert"
    msg["From"] = "alerts@yourdomain.com"
    msg["To"] = "admin@yourdomain.com"
    with smtplib.SMTP("smtp.yourdomain.com", 587) as server:
        server.starttls()
        server.login("user", "password")
        server.send_message(msg)

scheduler = BlockingScheduler()
scheduler.add_job(check_daily_threshold, 'cron', hour=8)
scheduler.start()
```

## 9.4 Integration Capabilities

**Connecting to BI Tools:**

The REST API endpoints (`/api/yearly`, `/api/types`, `/api/topstates`) can be used as data sources in BI platforms:

- **Power BI** — Use the "Web" data connector to pull JSON from the API endpoints.
- **Tableau** — Use the "Web Data Connector" or "JSON" connector.
- **Grafana** — Use the "JSON API" plugin to pull dashboard data.
- **Apache Superset** — Configure the MySQL database as a database connection.

**Webhook Integration:**

To push transaction summaries to external systems (Slack, Teams, PagerDuty), add a Flask endpoint that other systems can call:

```python
@app.route("/api/webhook/summary", methods=["POST"])
def webhook_summary():
    # Validate the incoming request
    # Compute summary
    # Return JSON summary
    pass
```

## 9.5 Bulk Operations

**Bulk Data Reload:**

To reload all data from scratch:
```bash
# Drop and recreate the database
mysql -u root -p -e "DROP DATABASE phonepe_db; CREATE DATABASE phonepe_db;"

# Re-run all ETL loaders
cd backend && python load_all_data.py
```

**Selective Table Reload:**

To reload a specific table without affecting others:
```bash
cd backend && python load_aggregated_transaction.py
```

**Bulk Export with pandas:**

```python
import pandas as pd, mysql.connector

tables = [
    "aggregated_transaction", "aggregated_user", "aggregated_insurance",
    "map_transaction", "map_user", "map_insurance",
    "top_transaction", "top_user", "top_insurance"
]

conn = mysql.connector.connect(
    host="localhost", user="root",
    password="YOUR_PWD", database="phonepe_db"
)

with pd.ExcelWriter("phonepe_full_export.xlsx") as writer:
    for table in tables:
        df = pd.read_sql(f"SELECT * FROM {table}", conn)
        df.to_excel(writer, sheet_name=table[:31], index=False)

conn.close()
print("Export complete: phonepe_full_export.xlsx")
```

---

# 10. Security & Compliance

## 10.1 Data Encryption

**Data in Transit:**

In development, the Flask server uses plain HTTP. For production deployments, all traffic must be encrypted using TLS (HTTPS). The recommended approach is to terminate TLS at the Nginx reverse proxy using a Let's Encrypt certificate:

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Obtain and install certificate
sudo certbot --nginx -d your-domain.com
```

**Data at Rest:**

MySQL 8.0 supports Transparent Data Encryption (TDE) for tablespace-level encryption:

```sql
-- Enable InnoDB tablespace encryption
ALTER TABLE aggregated_transaction ENCRYPTION='Y';
```

For full-disk encryption, use the host operating system's capabilities (e.g., LUKS on Linux).

**Database Connection:**

MySQL connections can be encrypted using SSL:

```python
import mysql.connector, ssl

def get_connection():
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        database=os.environ.get("DB_NAME"),
        ssl_ca="/path/to/ca-cert.pem",
        ssl_verify_cert=True
    )
```

## 10.2 User Authentication

For deployments requiring user authentication:

**Flask-Login (session-based):**

```python
from flask_login import LoginManager, login_required

login_manager = LoginManager(app)
login_manager.login_view = "login"

@app.route("/")
@login_required
def home():
    # ... existing implementation
```

**Password Hashing (bcrypt):**

```python
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

# Hashing a password
password_hash = bcrypt.generate_password_hash("user_password").decode("utf-8")

# Verifying a password
is_valid = bcrypt.check_password_hash(password_hash, "user_password")
```

## 10.3 Authorization Levels

A recommended three-tier RBAC model:

| Role | Permissions |
|---|---|
| `viewer` | Read-only access to dashboard, charts, map, and API endpoints |
| `analyst` | All viewer permissions + data export capabilities |
| `admin` | All analyst permissions + ETL triggers, user management, system configuration |

**Implementation using Flask-Principal:**

```python
from flask_principal import Principal, Permission, RoleNeed

principals = Principal(app)

viewer_permission  = Permission(RoleNeed("viewer"))
analyst_permission = Permission(RoleNeed("analyst"))
admin_permission   = Permission(RoleNeed("admin"))

@app.route("/admin/reload")
@admin_permission.require(http_exception=403)
def reload_data():
    # Trigger ETL pipeline
    pass
```

## 10.4 GDPR Compliance

The PhonePe Transaction Dashboard processes **aggregated, anonymised** data from the PhonePe Pulse public dataset. The dataset does not contain personally identifiable information (PII) such as individual user names, phone numbers, or transaction IDs. As a result, the GDPR compliance burden for this application is minimal.

**Data Minimisation:** The database stores only the fields necessary for the analytics use cases supported by the dashboard. No raw transaction logs or user identifiers are stored.

**Data Retention:** Establish a data retention policy aligned with business requirements. Automated cleanup jobs can remove records older than the retention window:

```sql
-- Example: Remove records older than 5 years
DELETE FROM aggregated_transaction WHERE year < YEAR(CURDATE()) - 5;
```

**Right to Erasure:** Since no PII is stored, GDPR right-to-erasure requests do not apply to this data. However, if the application is extended to store user accounts or access logs, a deletion workflow must be implemented.

**Data Processing Agreement:** If this application is deployed as a service for third parties, a Data Processing Agreement (DPA) should be established between the operator and any data processors (cloud providers, etc.).

## 10.5 Security Best Practices

**1. Secrets Management:**

Never hardcode credentials in source code. Use environment variables or a secrets management service:

```python
# Bad (hardcoded)
password = "12345678"

# Good (environment variable)
password = os.environ.get("DB_PASSWORD")

# Better (secrets manager, e.g., AWS Secrets Manager)
import boto3, json
secret = json.loads(
    boto3.client("secretsmanager").get_secret_value(SecretId="phonepe/db")["SecretString"]
)
password = secret["password"]
```

**2. SQL Injection Prevention:**

Always use parameterised queries (already implemented in `app.py`):

```python
# Correct (parameterised)
cursor.execute("SELECT * FROM aggregated_transaction WHERE year=%s", (year,))

# Never do this (vulnerable to SQL injection)
cursor.execute(f"SELECT * FROM aggregated_transaction WHERE year={year}")
```

**3. CSRF Protection:**

For forms that modify state (POST/PUT/DELETE), add CSRF token validation using Flask-WTF:

```python
from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect(app)
```

**4. Security Headers:**

Add security-related HTTP response headers:

```python
@app.after_request
def add_security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self' https://cdn.jsdelivr.net; "
        "style-src 'self' 'unsafe-inline';"
    )
    return response
```

**5. Dependency Scanning:**

Regularly audit Python dependencies for known vulnerabilities:

```bash
pip install pip-audit
pip-audit -r requirements.txt
```

---

# 11. Performance Optimization

## 11.1 Caching Strategies

**Flask-Caching (in-memory, Redis, or Memcached):**

The KPI card values (`SUM` of full tables) and API responses are strong candidates for caching, since they change only when new data is loaded via ETL.

```bash
pip install Flask-Caching
```

```python
from flask_caching import Cache

cache = Cache(app, config={"CACHE_TYPE": "SimpleCache", "CACHE_DEFAULT_TIMEOUT": 3600})

@app.route("/api/yearly")
@cache.cached(timeout=3600, key_prefix="yearly_chart")
def yearly_chart():
    # ... existing implementation (result cached for 1 hour)
```

**Cache Invalidation on ETL Run:**

```python
def clear_all_caches():
    cache.delete("yearly_chart")
    cache.delete("type_chart")
    cache.delete("topstates_chart")

# Call this at the end of load_all_data.py
```

**Redis-backed Caching (recommended for production):**

```python
cache = Cache(app, config={
    "CACHE_TYPE": "RedisCache",
    "CACHE_REDIS_URL": os.environ.get("REDIS_URL", "redis://localhost:6379/0"),
    "CACHE_DEFAULT_TIMEOUT": 3600
})
```

## 11.2 Database Optimization

**Query Analysis:**

Use MySQL's `EXPLAIN` to analyse slow queries:

```sql
EXPLAIN
SELECT state, year, quarter, transaction_type,
SUM(transaction_amount), SUM(transaction_count)
FROM aggregated_transaction
WHERE year = 2022 AND state = 'Maharashtra'
GROUP BY state, year, quarter, transaction_type;
```

**Composite Indexes:**

For the filtered query on `aggregated_transaction`, a composite index on the filter columns significantly reduces query time:

```sql
CREATE INDEX idx_agg_txn_filter
ON aggregated_transaction (year, state, transaction_type);
```

**Connection Pooling:**

Replace the naive per-request connection with a connection pool:

```python
from mysql.connector.pooling import MySQLConnectionPool

pool = MySQLConnectionPool(
    pool_name="phonepe_pool",
    pool_size=10,
    host=os.environ.get("DB_HOST", "localhost"),
    user=os.environ.get("DB_USER"),
    password=os.environ.get("DB_PASSWORD"),
    database=os.environ.get("DB_NAME", "phonepe_db")
)

def get_connection():
    return pool.get_connection()
```

**Table Partitioning:**

For very large datasets, partition `aggregated_transaction` by year:

```sql
ALTER TABLE aggregated_transaction
PARTITION BY RANGE (year) (
    PARTITION p2018 VALUES LESS THAN (2019),
    PARTITION p2019 VALUES LESS THAN (2020),
    PARTITION p2020 VALUES LESS THAN (2021),
    PARTITION p2021 VALUES LESS THAN (2022),
    PARTITION p2022 VALUES LESS THAN (2023),
    PARTITION p2023 VALUES LESS THAN (2024),
    PARTITION p_future VALUES LESS THAN MAXVALUE
);
```

## 11.3 Frontend Optimization

**Static Asset Caching:**

Configure Nginx to serve static files with long cache headers:

```nginx
location /static/ {
    alias /path/to/backend/static/;
    expires 30d;
    add_header Cache-Control "public, immutable";
}
```

**Minification:**

Minify CSS and JavaScript files before deployment to reduce payload sizes:

```bash
# CSS minification (using cleancss)
npx cleancss -o static/css/style.min.css static/css/style.css

# JS minification (using terser)
npx terser static/js/charts.js -o static/js/charts.min.js
```

**Chart.js Lazy Loading:**

Load chart data only when the user navigates to the `/charts` page. This is already the case in the current implementation — chart JavaScript is included only in `charts.html`.

## 11.4 Load Handling

**Gunicorn Workers:**

Calculate the optimal number of Gunicorn workers based on CPU cores:

```bash
# Formula: (2 * num_cores) + 1
# For a 4-core machine: 9 workers
gunicorn --workers 9 --bind 0.0.0.0:8000 --timeout 120 app:app
```

**Asynchronous Workers (gevent):**

For I/O-bound workloads (waiting for MySQL queries), use async workers:

```bash
pip install gevent
gunicorn --worker-class gevent --workers 4 --bind 0.0.0.0:8000 app:app
```

**Load Balancer (Nginx upstream):**

For multiple application instances:

```nginx
upstream phonepe_app {
    server 127.0.0.1:8000;
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;
}

server {
    location / {
        proxy_pass http://phonepe_app;
    }
}
```

---

# 12. Troubleshooting & FAQs

## 12.1 Common Issues and Solutions

### Issue 1 — Application Fails to Start

**Symptom:**
```
Error: Could not import "app".
ModuleNotFoundError: No module named 'flask'
```

**Solution:**
```bash
# Ensure you are in the correct directory and virtual environment is active
cd backend
source ../venv/bin/activate
pip install -r requirements.txt
python app.py
```

---

### Issue 2 — Database Connection Error

**Symptom:**
```
mysql.connector.errors.InterfaceError: 2003 (HY000):
Can't connect to MySQL server on 'localhost' (111)
```

**Solutions:**
```bash
# 1. Check if MySQL is running
sudo systemctl status mysql

# 2. Start MySQL if it is not running
sudo systemctl start mysql

# 3. Verify credentials
mysql -u root -p

# 4. Check db_connection.py for correct credentials
cat backend/db_connection.py
```

---

### Issue 3 — Empty Dashboard (No Data)

**Symptom:** KPI cards show `None` or `0`, data table is empty.

**Solution:**
```bash
# Verify the database has been populated
mysql -u root -p phonepe_db -e "SELECT COUNT(*) FROM aggregated_transaction;"

# If count is 0, run the ETL loaders
cd backend && python load_all_data.py
```

---

### Issue 4 — Charts Not Loading

**Symptom:** Charts page shows blank canvases or JavaScript console errors.

**Diagnosis:**
1. Open browser developer tools (`F12`).
2. Check the **Console** tab for JavaScript errors.
3. Check the **Network** tab for failed API calls to `/api/yearly` or `/api/types`.

**Common Causes:**
- Database is empty → run ETL.
- API returns non-numeric values → check for `NULL` in `transaction_amount` column.
- CDN scripts not loading → check internet connectivity or switch to locally hosted Chart.js.

---

### Issue 5 — Map Page Not Rendering

**Symptom:** `/map` shows a blank page or a Python traceback.

**Diagnosis:**
```python
# In app.py map_insights(), add debug logging
import logging
logging.basicConfig(level=logging.DEBUG)
```

**Common Cause:** `map_transaction` table is empty. Run `load_map_transaction.py`.

---

### Issue 6 — Slow Page Loads

**Symptom:** Dashboard takes more than 5 seconds to load.

**Solutions:**
1. Add database indexes (see Section 11.2).
2. Enable query result caching (see Section 11.1).
3. Reduce `per_page` from 20 to 10 to reduce the amount of data fetched per page.
4. Run `ANALYZE TABLE aggregated_transaction;` in MySQL to update statistics.

---

### Issue 7 — Port Already in Use

**Symptom:**
```
OSError: [Errno 98] Address already in use
```

**Solution:**
```bash
# Find the process using port 5000
lsof -i :5000

# Kill the process (replace PID with actual process ID)
kill -9 <PID>

# Or use a different port
python app.py --port 5001
```

---

### Issue 8 — ETL Loader Fails

**Symptom:** `load_aggregated_transaction.py` raises a `FileNotFoundError` or `KeyError`.

**Common Causes:**
- PhonePe Pulse data files are not in the expected directory path.
- Data file format has changed in a new version of the Pulse dataset.

**Solution:**
```bash
# Verify the data directory structure
ls -la data/

# Check the loader script for the expected file path
head -30 backend/load_aggregated_transaction.py
```

## 12.2 Frequently Asked Questions

**Q: How do I add a new year's data after the annual release?**  
A: Download the latest PhonePe Pulse data for the new year, place it in the `data/` directory following the existing folder structure, and re-run `python load_all_data.py`. The existing data is not affected.

**Q: Can I use a different database (PostgreSQL, SQLite)?**  
A: Yes. Replace `mysql-connector-python` with the appropriate driver (`psycopg2` for PostgreSQL, `sqlite3` built-in for SQLite), and update `db_connection.py` accordingly. Minor SQL syntax adjustments may be needed (e.g., `%s` placeholders are valid for both MySQL and PostgreSQL).

**Q: How do I run the application on a cloud server (AWS EC2, GCP, Azure)?**  
A: Follow the Installation Guide (Section 6), replacing "localhost" references with the server's internal IP or hostname. Use Gunicorn + Nginx in production, and ensure the server's security group/firewall allows inbound traffic on port 80/443.

**Q: How many concurrent users can the application support?**  
A: With a 4-core server, 4 Gunicorn workers, and a MySQL connection pool of size 10, the application can comfortably serve 50–100 concurrent users. For higher loads, implement caching (Section 11.1) and read replicas.

**Q: Is the PhonePe Pulse data real?**  
A: The PhonePe Pulse dataset contains real, anonymised, aggregated transaction data published by PhonePe under an open data licence. It does not contain individual user or transaction details.

**Q: Can I display district-level data?**  
A: Yes. The `map_transaction` table includes a `district` column. You can extend the filters and map view to show district-level data with additional frontend and backend work.

**Q: How do I reset the database?**  
A: Connect to MySQL and run `DROP DATABASE phonepe_db; CREATE DATABASE phonepe_db;`, then re-run the ETL loaders.

## 12.3 Error Codes and Meanings

| Error Code / Message | Meaning | Action |
|---|---|---|
| `2003 (HY000)` | Cannot connect to MySQL server | Start MySQL; check host/port |
| `1045 (28000)` | Access denied for user | Check username and password |
| `1049 (42000)` | Unknown database | Create `phonepe_db` database |
| `1146 (42S02)` | Table doesn't exist | Run ETL loaders |
| `500 Internal Server Error` | Unhandled Python exception | Check Flask console logs |
| `404 Not Found` | Route does not exist | Verify the URL path |
| `ImportError: No module named X` | Missing Python package | Run `pip install -r requirements.txt` |

## 12.4 Support Resources

- **GitHub Repository:** https://github.com/MEHULGAJJAR1/phonepe-transaction-dashboard
- **Flask Documentation:** https://flask.palletsprojects.com/
- **MySQL Documentation:** https://dev.mysql.com/doc/
- **Chart.js Documentation:** https://www.chartjs.org/docs/
- **Plotly Python Documentation:** https://plotly.com/python/
- **PhonePe Pulse Data Repository:** https://github.com/PhonePe/pulse

---

# 13. Best Practices

## 13.1 Code Standards

**Python Style:**

Follow [PEP 8](https://pep8.org/) style guidelines:

```python
# Good: snake_case function and variable names
def get_yearly_totals():
    transaction_amount = 0
    ...

# Good: 4-space indentation
def home():
    if year:
        query += " AND year=%s"

# Good: docstrings for public functions
def get_connection():
    """
    Create and return a MySQL database connection.
    Credentials are read from environment variables.
    """
    return mysql.connector.connect(...)
```

**Project Structure:**

```
phonepe-transaction-dashboard/
├── backend/
│   ├── app.py              # Flask routes (keep thin — delegate logic to helpers)
│   ├── db_connection.py    # Database utility
│   ├── etl/                # ETL loaders (group related files)
│   │   ├── load_all_data.py
│   │   └── load_aggregated_transaction.py
│   ├── static/
│   │   ├── css/style.css
│   │   └── js/charts.js
│   └── templates/
├── data/                   # Source data files (PhonePe Pulse)
├── database/               # SQL schema files
├── tests/                  # Unit and integration tests
├── requirements.txt
└── README.md
```

**Git Commit Messages:**

Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
feat: add quarterly chart to /charts page
fix: resolve null transaction_amount causing chart error
docs: update API documentation for /api/types endpoint
refactor: extract db connection pool into separate module
perf: add composite index on aggregated_transaction filter columns
```

## 13.2 Security Practices

1. **Never commit secrets.** Use `.gitignore` to exclude `.env` files and secret files:
   ```
   # .gitignore
   .env
   *.pem
   *.key
   venv/
   __pycache__/
   ```

2. **Always use parameterised queries.** Never use f-strings or string concatenation for SQL.

3. **Keep dependencies updated.** Run `pip-audit` monthly to detect vulnerabilities.

4. **Use HTTPS in production.** Never transmit credentials or session cookies over plain HTTP.

5. **Apply the principle of least privilege.** Create a dedicated MySQL user for the application with only SELECT privileges on `phonepe_db`:
   ```sql
   CREATE USER 'phonepe_app'@'localhost' IDENTIFIED BY 'strong_password';
   GRANT SELECT ON phonepe_db.* TO 'phonepe_app'@'localhost';
   FLUSH PRIVILEGES;
   ```

## 13.3 Testing Procedures

**Unit Testing (pytest):**

```bash
pip install pytest pytest-flask
```

```python
# tests/test_app.py
import pytest
from backend.app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"PhonePe" in response.data

def test_yearly_api(client):
    response = client.get("/api/yearly")
    assert response.status_code == 200
    data = response.get_json()
    assert "years" in data
    assert "amounts" in data
    assert len(data["years"]) == len(data["amounts"])

def test_types_api(client):
    response = client.get("/api/types")
    assert response.status_code == 200
    data = response.get_json()
    assert "types" in data
    assert "amounts" in data
```

**Running Tests:**

```bash
cd phonepe-transaction-dashboard
pytest tests/ -v
```

**Integration Testing:**

Test the full request cycle including database queries:

```bash
# Set up a test database with a small fixture dataset
mysql -u root -p < tests/fixtures/test_data.sql
pytest tests/test_integration.py -v
```

## 13.4 Deployment Guidelines

**Pre-deployment Checklist:**

- [ ] `FLASK_ENV` is set to `production` (not `development`).
- [ ] `FLASK_DEBUG` is `0` or unset.
- [ ] Database credentials are stored in environment variables, not in source code.
- [ ] TLS/HTTPS is configured on the reverse proxy.
- [ ] Security headers are enabled (see Section 10.5).
- [ ] Gunicorn is used instead of Flask's development server.
- [ ] Logs are configured to write to a persistent log file.
- [ ] A process manager (systemd, Supervisor) is configured to restart the application on crash.

**systemd Service File:**

```ini
# /etc/systemd/system/phonepe-dashboard.service
[Unit]
Description=PhonePe Transaction Dashboard
After=network.target mysql.service

[Service]
User=www-data
WorkingDirectory=/opt/phonepe-transaction-dashboard/backend
Environment="DB_HOST=localhost"
Environment="DB_USER=phonepe_app"
Environment="DB_PASSWORD=strong_password"
Environment="DB_NAME=phonepe_db"
ExecStart=/opt/phonepe-transaction-dashboard/venv/bin/gunicorn \
    --workers 4 --bind 0.0.0.0:8000 \
    --access-logfile /var/log/phonepe/access.log \
    --error-logfile /var/log/phonepe/error.log \
    app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable phonepe-dashboard
sudo systemctl start phonepe-dashboard
```

---

# 14. Future Enhancements

## 14.1 Planned Features

The following features are identified as high-value enhancements for future development iterations:

| Priority | Feature | Description |
|---|---|---|
| High | **User Authentication** | Login system with RBAC to control access to sensitive data and admin functions |
| High | **Data Export (CSV/Excel)** | One-click export of filtered table data directly from the UI |
| High | **District-Level Drill-Down** | Extend the map view to support district and pincode level granularity |
| Medium | **Date Range Filter** | Replace year/quarter dropdowns with a flexible date range picker |
| Medium | **Dashboard Customisation** | Allow users to configure which charts and KPIs appear on their home screen |
| Medium | **Automated ETL Scheduling** | Cron-based or Celery-based automatic data refresh when new Pulse data is released |
| Medium | **Email Report Subscriptions** | Scheduled PDF/Excel reports emailed to stakeholders on a weekly or monthly basis |
| Low | **Multi-Language Support (i18n)** | Support for Hindi and other Indian regional languages |
| Low | **Dark Mode** | CSS dark mode toggle for improved usability in low-light environments |
| Low | **Mobile App (React Native)** | Native mobile companion application for on-the-go analytics |

## 14.2 Technology Roadmap

**Near-Term (0–6 months):**
- Migrate from raw `mysql-connector-python` queries to SQLAlchemy ORM for cleaner, safer database interaction.
- Add pytest-based test coverage (target: 80% coverage).
- Implement Flask-Caching backed by Redis.
- Add CSV/Excel export endpoints.
- Add user authentication using Flask-Login.

**Mid-Term (6–18 months):**
- Introduce a task queue (Celery + Redis) for long-running ETL jobs, freeing the web server thread.
- Migrate frontend to a React.js SPA for richer interactivity and real-time updates via WebSockets.
- Integrate Apache Kafka or a message queue to support streaming transaction data ingestion.
- Add a full-text search capability on transaction metadata using Elasticsearch.

**Long-Term (18+ months):**
- Introduce a machine learning layer for anomaly detection and transaction forecasting using scikit-learn or Prophet.
- Build a GraphQL API layer for flexible data querying by BI tools.
- Add multi-tenancy support for serving multiple client organisations from a single deployment.
- Explore cloud-native deployment on AWS/GCP using managed services (RDS, ElastiCache, EKS).

## 14.3 Scalability Considerations

**Database Scalability:**

As the dataset grows beyond tens of millions of rows, the following strategies should be considered:

- **Read Replicas:** Offload dashboard read queries to a MySQL read replica, keeping the primary for ETL writes.
- **Data Warehousing:** Migrate to a columnar analytical database (ClickHouse, Redshift, BigQuery) optimised for aggregation-heavy analytical queries.
- **Pre-Aggregated Summary Tables:** Create materialised summary tables (e.g., `daily_transaction_summary`) that store pre-computed aggregates, drastically reducing query time for KPI cards and charts.

**Application Scalability:**

- **Horizontal Scaling:** The Flask application is stateless (no server-side session state) and can be scaled horizontally behind a load balancer.
- **Container Orchestration:** Dockerise the application and deploy on Kubernetes (k8s) for auto-scaling, self-healing, and zero-downtime deployments.

**Dockerfile (example):**

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .

ENV FLASK_ENV=production
EXPOSE 8000

CMD ["gunicorn", "--workers", "4", "--bind", "0.0.0.0:8000", "app:app"]
```

**docker-compose.yml (example):**

```yaml
version: "3.9"
services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DB_HOST=db
      - DB_USER=phonepe_app
      - DB_PASSWORD=${DB_PASSWORD}
      - DB_NAME=phonepe_db
    depends_on:
      - db

  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD}
      MYSQL_DATABASE: phonepe_db
      MYSQL_USER: phonepe_app
      MYSQL_PASSWORD: ${DB_PASSWORD}
    volumes:
      - mysql_data:/var/lib/mysql

volumes:
  mysql_data:
```

---

*End of Document*

---

**Document Information**

| Field | Value |
|---|---|
| Document Title | PhonePe Transaction Dashboard — Comprehensive Documentation |
| Version | 1.0.0 |
| Date | March 2026 |
| Author | MEHULGAJJAR1 |
| Repository | https://github.com/MEHULGAJJAR1/phonepe-transaction-dashboard |
| License | MIT |

---

*This document is intended for educational and reference purposes. The PhonePe brand and associated trademarks are the property of PhonePe Private Limited.*
