# Sports Analytics ETL Pipeline

A production-ready **Extract, Transform, Load (ETL)** pipeline for sports data analytics, automated with GitHub Actions to run every Saturday and Sunday.

## 🎯 Project Overview

This project automatically:
1. **Extracts** sports data from websites (web scraping)
2. **Transforms** the data into structured formats
3. **Loads** data to two cloud storage locations:
   - **Azure Blob Storage** (Parquet files)
   - **Azure PostgreSQL Database**

The entire pipeline is **scheduled and automated** using GitHub Actions, running every weekend during sports season.

---

## 📁 Project Structure

```
Sports_Analytics/
├── .github/
│   └── workflows/
│       └── weekend_schedule.yml          # GitHub Actions workflow
├── data_sources/
│   └── website/
│       └── scrape.py                     # Web scraping logic
├── data_storage/
│   └── Azure/
│       ├── blob/
│       │   └── push_to_blob.py          # Upload to Blob Storage
│       └── synapse/
│           └── push_to_database.py       # Push to PostgreSQL
├── azure_main.py                         # Main ETL orchestrator
├── requirements.txt                      # Python dependencies
├── .env                                  # Environment variables (not committed)
└── README.md                             # This file
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Azure Blob Storage account
- Azure PostgreSQL Database
- GitHub repository with Actions enabled

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/Sports_Analytics.git
   cd Sports_Analytics
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Create a `.env` file in the project root:
   ```env
   AZURE_STORAGE_CONNECTION_STRING=your_blob_storage_connection_string
   AZURE_DATABASE_CONNECTION_STRING=postgresql://user:password@host:5432/database
   ```

5. **Run the pipeline locally:**
   ```bash
   python azure_main.py
   ```

---

## 🔧 Features

### Data Extraction (`scrape.py`)
- Scrapes sports data from websites
- Functions: `league_table()`, `top_scorers()`
- Returns Pandas DataFrames

### Data Storage Options

#### 1. Azure Blob Storage (`push_to_blob.py`)
- Converts DataFrames to **Parquet format**
- Uploads to Azure Blob Storage container (Eg: `utstg`)
- Files: `league_table.parquet`, `top_scorers.parquet`
![alt text](image.png)

#### 2. Azure PostgreSQL Database (`push_to_database.py`)
- Stores data in PostgreSQL tables
- Tables: `league_table`, `top_scorers`
- Uses connection string from environment variables
![alt text](image-1.png)

---

## ⏰ GitHub Actions Automation

### How It Works
The workflow (`.github/workflows/weekend_schedule.yml`) automatically runs:
- **Every Saturday at 00:00 UTC**
- **Every Sunday at 00:00 UTC**
- During the entire sports season

### Workflow Steps
1. Checkout repository code
2. Setup Python 3.11 environment
3. Install dependencies
4. Execute the ETL pipeline
5. Upload logs if execution fails

### Manual Trigger
You can also manually run the workflow anytime:
1. Go to **Actions** tab
2. On the left sidebar, select **"Sports Analytics ETL Pipeline"** from the workflows list
3. Click **"Run workflow"** button → **"Run workflow"**

---

## 🔐 GitHub Secrets Setup

Store sensitive credentials as GitHub secrets:

1. Go to your repository **Settings** → **Secrets and variables** → **Actions**
2. Click **"New repository secret"** for each:

| Secret Name | Value |
|---|---|
| `AZURE_STORAGE_CONNECTION_STRING` | Your Blob Storage connection string |
| `AZURE_DATABASE_CONNECTION_STRING` | Your PostgreSQL connection string |

These are automatically injected into the workflow as environment variables.

---

## 📦 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `pandas` | >=3.0.1 | Data manipulation and SQL operations |
| `numpy` | >=2.0.0 | Numerical computing |
| `pyarrow` | >=14.0.0 | Parquet file format support |
| `azure-storage-blob` | 12.17.0 | Azure Blob Storage client |
| `sqlalchemy` | >=2.0.36 | Database ORM and connection management |
| `psycopg2` | 2.9.11 | PostgreSQL adapter |
| `beautifulsoup4` | 4.12.2 | Web scraping |
| `requests` | 2.31.0 | HTTP requests for web scraping |
| `python-dotenv` | 1.0.0 | Load environment variables from .env |

**NumPy 2.x Compatibility:** All dependencies are compatible with NumPy 2.x, ensuring stable execution.

---

## 🔄 Data Flow Diagram

```
Website Data
    ↓
scrape.py (Extract)
    ├─→ league_table() → DataFrame
    └─→ top_scorers() → DataFrame
    ↓
azure_main.py (Orchestrate)
    ├─→ push_to_blob.py (Transform & Load)
    │   └─→ Convert to Parquet
    │   └─→ Upload to Blob Storage ✅
    │
    └─→ push_to_database.py (Transform & Load)
        └─→ Push to PostgreSQL ✅
```

---

## 🐛 Troubleshooting

### Issue: GitHub Actions Fails

**Check logs in Actions tab:**
1. Go to **Actions** tab in your repository
2. Click on the failed workflow run
3. Expand the step that failed
4. Review error messages

**Common Issues:**

| Error | Solution |
|-------|----------|
| `ImportError: No module named 'scrape'` | Check file paths in `azure_main.py` |
| `AttributeError: 'Engine' object has no attribute 'cursor'` | Use connection string, not connection object |
| `psycopg2.errors.SyntaxError` | Ensure PostgreSQL connection string format is correct |
| `numpy` compatibility errors | Update PyArrow: `pip install pyarrow>=14.0.0` |

### Issue: Local Execution Fails

1. **Verify `.env` file exists** with correct credentials
2. **Test web scraping:** `python data_sources/website/scrape.py`
3. **Test Blob upload:** `python data_storage/Azure/blob/push_to_blob.py`
4. **Test DB push:** `python data_storage/Azure/synapse/push_to_database.py`

---

## 📊 Monitoring

### View Workflow Runs
1. Go to **Actions** tab
2. Click **"Sports Analytics ETL Pipeline"**
3. See all historical runs with status and execution time

### Enable Notifications
GitHub can notify you of:
- Workflow failures via email
- Workflow completion (in-app)
- Custom webhook notifications

---

## 🔄 Updating the Schedule

To change when the workflow runs, edit `.github/workflows/weekend_schedule.yml`:

```yaml
on:
  schedule:
    - cron: '0 0 * * 0,6'  # Current: Every Sat/Sun at midnight UTC
```

**Cron Format:** `minute hour * * day_of_week`
- `0 0` = 00:00 (midnight)
- `0,6` = Saturday (6) and Sunday (0)

**Examples:**
- `0 12 * * 0` = Every Sunday at noon UTC
- `0 8 * * 1-5` = Every weekday at 8 AM UTC

---

## 📈 Performance & Costs

- **Execution Time:** ~20-30 seconds per run
- **Frequency:** 2 runs per week (weekends)
- **Azure Blob Storage:** Minimal cost (parquet files are ~6-8 KB)
- **Azure PostgreSQL:** Check your database tier for compute costs

---

## 🤝 Contributing

1. Create a new branch for features
2. Test locally before pushing
3. Submit pull requests with detailed descriptions

---

## 📝 License

This project is for personal or educational use.

---

## 👤 Author

**Utkarsh Trivedi**  
- GitHub: [@utkarshtrvd27](https://github.com/utkarshtrvd27)
- Project: Sports Analytics ETL Pipeline

