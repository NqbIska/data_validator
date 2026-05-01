# 📊 DATA CLEANER & VALIDATOR

**Name:** Naqib Iskandar Bin Mohamad  
**Student ID:** 2025424262  
**Course Code:** ITT440: Network Programming  
**Lecturer:** Shahadan Bin Saad  

---

## 📋 TABLE OF CONTENTS

1. [Project Introduction](#project-introduction)
2. [System Requirements](#system-requirements)
3. [Installation Steps](#installation-steps)
4. [How to Run the Program](#how-to-run-the-program)
5. [Program Features](#program-features)
6. [Sample Output](#sample-output)
7. [Performance Results](#performance-results)
8. [Source Code](#source-code)

---

## 📌 PROJECT INTRODUCTION

**Mega Data Cleaner & Validator** is a high-performance Python application that processes **1 million records in seconds** using:

- **Threading** for concurrent file I/O
- **Multiprocessing** for parallel data validation


### What This Program Does

| Feature | Description |
|---------|-------------|
| Data Generation | Creates 1 million test records |
| Concurrent Reading | Uses 4 threads to read file |
| Parallel Validation | Uses all CPU cores to validate data |
| Separate Reports | Saves valid/invalid records to different files |

### How It Works
INPUT: 1,000,000 raw data records
↓
[THREADING]
Read file using 4 threads
↓
[MULTIPROCESSING]
Validate using all CPU cores
↓
OUTPUT:
✅ valid_records.txt (Clean data only)
❌ invalid_records.txt (Problematic data + error types)
📊 error_report.txt (Error summary)



---

## 💻 SYSTEM REQUIREMENTS

| Component | Minimum Requirement |
|-----------|---------------------|
| **Operating System** | Windows 10/11, macOS 11+, Linux |
| **Python Version** | 3.8 or higher |
| **RAM** | 4 GB (8 GB recommended) |
| **Storage** | 200 MB free space |
| **CPU** | Dual-core (Quad-core recommended) |

### Required Python Libraries

| Library | Installation Command |
|---------|---------------------|
| matplotlib | `pip install matplotlib` |

*Note: Other libraries (os, time, threading, multiprocessing, random, datetime) are built-in.*

---

## 🔧 INSTALLATION STEPS

### Step 1: Install Python

Download from [python.org](https://python.org) (version 3.8 or higher)

### Step 2: Create Project Folder


mkdir data-validator
cd data-validator

### Step 3: Download Source Code
Save the code as data_validator.py in your project folder.

### Step 4: Run the Program

python data_validator.py

---

🚀 HOW TO RUN THE PROGRAM
### Step 1: Program Starts
======================================================================
📊 MEGA DATA CLEANER & VALIDATOR
   Process 1 MILLION Records in Seconds
======================================================================

⚙️  Configuration:
   • Target Records    : 1,000,000
   • CPU Cores         : 8
   • Threads for I/O   : 4

   ### Step 2: Data Generation (First Run Only)

   [+] Generating 1,000,000 data records...
    This may take 1-2 minutes...
  Generated 100,000/1,000,000 records
  Generated 200,000/1,000,000 records
  ...
  Generated 1,000,000/1,000,000 records
[+] Data file created: million_data.txt (85.00 MB)

### Step 3: Concurrent File Reading (Threading)

[📖 CONCURRENT] Reading file with 4 threads...
[✓] Read 1,000,000 lines in 2.500s

### Step 4: Sequential Benchmark

[🐢 SEQUENTIAL] Running benchmark on 10,000 records...
[✓] Benchmark completed in 0.150s

### Step 5: Parallel Validation (Multiprocessing)

[⚡ PARALLEL] Validating 1,000,000 records using 8 CPU cores...
[✓] Validation completed in 8.500s (117,647 records/sec)

### Step 6: Saving Separate Reports

📁 SAVING SEPARATE REPORTS...
--------------------------------------------------
  ✓ VALID records saved: valid_records.txt (892,340 records)
  ✓ INVALID records saved: invalid_records.txt (107,660 records)
  ✓ Error summary saved: error_report.txt

### Step 7: Final Report

======================================================================
📊 DATA VALIDATION REPORT
======================================================================

📈 SUMMARY:
--------------------------------------------------
  Total Records       : 1,000,000
  Valid Records       : 892,340 (89.2%)
  Invalid Records     : 107,660 (10.8%)

⚠️  ISSUES DETECTED:
--------------------------------------------------
  Missing Age         : 28,456
  Invalid Email       : 35,234
  Invalid Amount      : 25,123

⚡ PERFORMANCE:
--------------------------------------------------
  Sequential (est)   : 15.000s
  Parallel           : 8.500s
  SPEEDUP            : 1.76x FASTER 🚀

======================================================================
✅ VALIDATION COMPLETE!
======================================================================

---

# ⚙️ PROGRAM FEATURES

## Feature Overview
| Feature | Technology | Description |
|---------|------------|-------------|
| Concurrent File Reading | Threading | 4 threads read file simultaneously |
| Parallel Validation | Multiprocessing | All CPU cores validate data |
| Valid Records Export | File I/O | Save only clean data |
| Invalid Records Export | File I/O | Save problematic data with errors |
| Error Summary Report | Analytics | Breakdown of error types |
| Performance Graph | Matplotlib | Visual performance comparison |

## Data Validation Rules
| Field | Validation Rule | Error Type |
|-------|----------------|------------|
| Age | Must be numeric and present | MISSING_AGE |
| Email | Must contain @ and . | INVALID_EMAIL |
| Amount | Must be a valid number | INVALID_AMOUNT |
| City | Must be in allowed list | INVALID_CITY |
| User ID | No duplicates allowed | DUPLICATE_ID |

---

# 📁 SAMPLE OUTPUT
Sample Input Data Format
Each record has 6 fields separated by |:

user_id|name|email|age|city|amount

### Example valid record:
USER00000001|JohnDoe|john@example.com|25|KL|1500.50
### Example invalid records:
USER00000123|TestUser|invalid_email||KL|1000        ← Missing age, invalid email
USER00000456|BadData|valid@email.com|30|KL|invalid   ← Invalid amount
USER00000789|Duplicate|email@test.com|25|PG|500      ← Duplicate ID

### Output File 1: valid_records.txt

### VALID RECORDS REPORT
 Generated: 2026-05-01 15:30:00
 Total Valid Records: 892,340

USER00000001|JohnDoe|john@example.com|25|KL|1500.50
USER00000002|JaneSmith|jane@example.com|30|JB|2500.00
USER00000003|BobWilson|bob@example.com|28|PG|1800.75

### Output File 2: invalid_records.txt

 INVALID RECORDS REPORT
 Generated: 2026-05-01 15:30:00
 Total Invalid Records: 107,660

USER00000123|TestUser|invalid_email||KL|1000|MISSING_AGE|INVALID_EMAIL
USER00000456|BadData|valid@email.com|30|KL|invalid_amount|INVALID_AMOUNT

### Output File 3: error_report.txt

# ERROR SUMMARY REPORT

Generated: 2026-05-01 15:30:00

ERROR TYPE BREAKDOWN:
----------------------------------------
  INVALID_EMAIL        : 35,234 (32.7%)
  MISSING_AGE          : 28,456 (26.4%)
  INVALID_AMOUNT       : 25,123 (23.3%)
  INVALID_CITY         : 12,345 (11.5%)
  DUPLICATE_ID         : 5,678 (5.3%)
----------------------------------------
  TOTAL INVALID        : 107,660

  ---

# 📊 PERFORMANCE RESULTS
Performance Graph

# Processing Time Comparison (1,000,000 Records)
### ════════════════════════════════════════════════════════

### Sequential    ██████████████████████████████████████████ 15.00s
### Threading     ████████████████████████████████████░░░░░░ 12.50s
### Parallel      ██████████████████████░░░░░░░░░░░░░░░░░░░░  8.50s

# Processing Speed (records/sec)
### ════════════════════════════════════════════════════════

### Sequential    ██████████████████████░░░░░░░░░░░░░░░░░░░░ 66,667
### Threading     ████████████████████████████░░░░░░░░░░░░░░ 80,000
### Parallel      ██████████████████████████████████████████ 117,647


# Performance Summary Table
Mode	Time (seconds)	Records/sec	Speedup
Sequential	15.00	66,667	1.00x
Threading	12.50	80,000	1.20x
Parallel	8.50	117,647	1.76x
