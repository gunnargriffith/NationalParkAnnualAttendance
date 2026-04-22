# Tutorial: Installing and Running `nationalparksdata`

This guide explains how to install and use the `nationalparksdata` Python package from the GitHub repository.

---

# What This Package Does

`nationalparksdata` gathers National Park Service park data and annual visitation data, then combines it into a clean dataset for analysis.

The package can:

* Scrape fresh National Park data from the NPS API
* Build a final combined dataset
* Save output files as `.csv`
* Return a pandas DataFrame for analysis

---

# Prerequisites

Before installing, make sure you have:

* Python 3.10 or newer installed
* pip installed
* Internet connection
* A National Park Service API key


# Step 1: Install the Package

From inside the folder you want to save the data, run:

```bash
pip install nationalparksdata
```

This installs the package locally.

---

# Step 2: Get an API Key

This project uses the National Park Service API.

Get a free API key from:

https://www.nps.gov/subjects/developer/get-started.htm

---

# Step 3: Create a `.env` File

Inside the project folder, create a file named:

```text
.env
```

Add this line:

```text
API_KEY=your_api_key_here
```

Example:

```text
API_KEY=abc123xyz456
```

---

# Step 4: Run the Package

## Option A: Full Refresh (Recommended)

Runs scraper + builds final dataset.

Create a Python file:

```python
from nationalparksdata import refresh_dataset

df = refresh_dataset()

print(df.head())
```

Run:

```bash
python your_file.py
```

---

## Option B: Build Dataset From Existing Files Only

If raw files already exist:

```python
from nationalparksdata import build_dataset

df = build_dataset()

print(df.head())
```

---

## Option C: Run Scraper Only

```python
from nationalparksdata import run_scraper

run_scraper()
```

---

# Option D: Find Parks With Certain Activities
By passing a comma separated list of activities, the function will find the parks with all listed activities.
```python
from nationalparksdata import parks_with_activity
parks_with_activity('horseback riding', 'hiking')
```


# Output Files

The package saves data into the `data/` folder.

Typical outputs:

```text
data/base_data.csv
data/csv_dictionary.json
data/final.csv
```

---

# Using in Jupyter Notebook

You may also use the package in Jupyter:

```python
from nationalparksdata import refresh_dataset

df = refresh_dataset()
df.head()
```

---

# Troubleshooting

## Error: 403 Forbidden

Cause: API key missing or invalid.

Fix:

* Check `.env` file exists
* Verify `API_KEY=` line is correct

---

## Error: Module Not Found

Reinstall package:

```bash
pip install .
```

---

## Selenium Errors

If browser automation fails, update Chrome and ChromeDriver.

---

# Uninstalling

```bash
pip uninstall nationalparksdata
```

---

# Authors

* Gunnar Griffith
* Elijah Barnes

---

# Notes

This package was created for academic and data analysis purposes.
