
# 📄 Public Job Scraper

A beginner-friendly Python script that scrapes Python-related job listings from a public job board (Real Python's demo site). It extracts job **titles**, **company names**, and **links**, then saves the results in a **timestamped JSON file**.

---

## 🧠 What It Does

- 🔍 Scrapes job data from: [https://realpython.github.io/fake-jobs/](https://realpython.github.io/fake-jobs/)
- ✅ Filters only **Python**-related jobs
- 🏷 Extracts:
  - Job title
  - Company name
  - Job application link
- 💾 Saves the output as a JSON file in the `output/` directory (e.g., `jobs_2025-06-25_14-40-02.json`)

---

## 📂 Folder Structure

```bash
public-job-scraper/
├── main.py               # Main scraping script
├── requirements.txt      # Required Python packages
├── output/               # Stores JSON job data files
└── README.md             # You are here 📘
```

## 🚀 How to Run


## 1. ✅ Clone the repository and navigate to the folder
```bash
git clone https://github.com/your-username/scraping-scripts-main.git
cd scraping-scripts-main/public-job-scraper
```

## 2. 🧱 (Optional but Recommended) Create a virtual environment
```
python -m venv venv
source venv/bin/activate      # On macOS/Linux
venv\Scripts\activate         # On Windows
```


## 3. 📦 Install dependencies
```
pip install -r requirements.txt
```
## 4. ▶️ Run the script
```
python main.py
```

## Output:
```
# A timestamped .json file will be saved to the output/ folder
```

---

## 📦 Example Output

```json
[
    {
        "title": "Senior Python Developer",
        "company": "ExampleCorp",
        "link": "https://realpython.github.io/fake-jobs/jobs/senior-python-developer-0.html"
    },
    {
        "title": "Python QA Engineer",
        "company": "CodeCheckers",
        "link": "https://realpython.github.io/fake-jobs/jobs/python-qa-engineer-12.html"
    }
]
```
