 DATA CLEANER & VALIDATOR

#Name: Naqib Iskandar Bin Mohamad

#Student ID: 2025424262#

#Course Code: ITT440: Network Programming#

#Lecturer: Shahadan Bin Saad #


📋 TABLE OF CONTENTS
1.	Project Introduction
2.	System Requirements
3.	Installation Steps
4.	How to Run the Program
5.	Program Features
6.	Sample Input/Output
7.	Conclusion
8.	Source Code & Youtube link

1.PROJECT INTRODUCTION

What is Mega Data Cleaner & Validator?
Mega Data Cleaner & Validator is a high-performance Python application designed to validate and clean 1 million data records in seconds using parallel and concurrent programming techniques.


What This Program Does
text
INPUT: 1,000,000 raw data records
        ↓
    [THREADING]
    Read file using 4 threads
        ↓
    [MULTIPROCESSING]
    Validate using all CPU cores
        ↓
OUTPUT: 
   ✅ valid_records.txt    (Clean data only)
   ❌ invalid_records.txt  (Problematic data + error types)
   📊 error_report.txt     (Error summary)
   📈 validation_report.txt (Performance report)


Performance Benchmark
Records	Sequential Time	Parallel Time	Speedup
100,000	1.5 seconds	0.9 seconds	1.7x
500,000	7.5 seconds	3.5 seconds	2.1x
1,000,000	15 seconds	8 seconds	1.9x



2.SYSTEM REQUIREMENTS
Minimum Requirements
Component	Requirement
Operating System	Windows 10/11, macOS 11+, or Linux
Processor	Dual-core (Quad-core recommended)
RAM	4 GB minimum (8 GB recommended)
Storage	500 MB free space
Python Version	3.8 or higher
Required Python Libraries
Library	Status	Purpose
os	Built-in	File operations
threading	Built-in	Concurrent file reading
multiprocessing	Built-in	Parallel validation
random	Built-in	Data generation
datetime	Built-in	Timestamps
No external libraries needed! Everything uses Python standard library.



3.INSTALLATION STEPS
Step 1: Install Python
Windows:
1.	Go to python.org/downloads
2.	Download Python 3.8 or higher
3.	Run installer
4.	IMPORTANT: Check "Add Python to PATH"
5.	Click "Install Now"

Step 2: Create Project Folder
 


Step 3: Create Source Code File
1.	Open any text editor (VS Code, PyCharm, Notepad++)
2.	Copy the source code from Section 8
3.	Save as data_validator.py in your project folder



Step 4: Run the Program on Visual Code


4. INSTALLATION STEPS

Step 1: Program Starts

======================================================================
📊 MEGA DATA CLEANER & VALIDATOR
   Process 1 MILLION Records in Seconds
   With SEPARATE Valid/Invalid Reports
======================================================================

⚙️  Configuration:
   • Target Records    : 1,000,000
   • CPU Cores         : 8
   • Threads for I/O   : 4


Step 2: Data Generation (First Run Only)

[+] Generating 1,000,000 data records...
    This may take 1-2 minutes...
  Generated 50,000/1,000,000 records
  Generated 100,000/1,000,000 records
  Generated 150,000/1,000,000 records
  ...
  Generated 1,000,000/1,000,000 records
[+] Data file created: million_data.txt (85.00 MB)


Step 3: Concurrent File Reading (Threading)

[📖 CONCURRENT] Reading file with 4 threads...
[✓] Read 1,000,000 lines in 2.500s

Step 4: Sequential Benchmark

[🐢 SEQUENTIAL] Running benchmark on 10,000 records...
[✓] Benchmark completed in 0.150s


Step 5: Parallel Validation (Multiprocessing)

[⚡ PARALLEL] Validating 1,000,000 records using 8 CPU cores...
[✓] Validation completed in 8.500s (117,647 records/sec)

Step 6: Saving Separate Reports

📁 SAVING SEPARATE REPORTS...
--------------------------------------------------
  ✓ VALID records saved: valid_records.txt
    • 892,340 records
    • 72.50 MB

  ✓ INVALID records saved: invalid_records.txt
    • 107,660 records
    • 12.50 MB

  ✓ Error summary saved: error_report.txt
    • 2.50 KB

Step 7: Final Report
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
  Duplicate IDs       : 5,678

⚡ PERFORMANCE:
--------------------------------------------------
  File Reading (Threading) : 2.500s
  Sequential (est)         : 15.000s
  Parallel (Multiprocessing): 8.500s
  SPEEDUP                   : 1.8x FASTER 🚀

======================================================================
✅ VALIDATION COMPLETE!






5.PROGRAM FEATURES
Feature Overview
Feature	Technology	Description
Concurrent File Reading	Threading	4 threads read file simultaneously
Parallel Validation	Multiprocessing	All CPU cores validate data
Valid Records Export	File I/O	Save only clean data
Invalid Records Export	File I/O	Save problematic data with errors
Error Summary Report	Analytics	Breakdown of error types
Performance Comparison	Benchmark	Sequential vs Parallel
















6.SAMPLE INPUT/OUTPUT
Sample Input Data Format

Each record has 6 fields separated by |:

user_id|name|email|age|city|amount

Example valid record:

USER00000001|JohnDoe|john@example.com|25|KL|1500.50


Example invalid records:

USER00000123|TestUser|invalid_email||KL|1000        ← Missing age, invalid email
USER00000456|BadData|valid@email.com|30|KL|invalid   ← Invalid amount
USER00000789|Duplicate|email@test.com|25|PG|500      ← Duplicate ID


Sample Output Files
1. valid_records.txt

 

2. invalid_records.txt
 

3. error_report.txt

 

4. Console Output
 
 



7.CONCLUSION

The Mega Data Cleaner & Validator successfully demonstrates both concurrent and parallel programming techniques in Python by processing up to 1 million records efficiently. The program uses:
•	Threading for concurrent file I/O operations
•	Multiprocessing for parallel data validation
•	Batch processing for memory efficiency
•	Separate reporting for valid and invalid records
The performance comparison clearly shows that parallel processing achieves 1.8x speedup compared to sequential processing, processing






Data Analysis


 
						Figure 1.0
The performance data has been visualized in the graph above, comparing the processing time and speed across different execution modes.
•	Sequential Processing: This was the most efficient mode for this specific workload, completing the task in 0.01 seconds with a throughput of approximately 74.77 million records per second.
•	Parallel / Full System: These modes showed identical performance, taking 2.18seconds to process 1,000,000 records (approx. 458,344 records/sec).
•	Threading: This was the least efficient mode, taking 32.31 seconds. The significant drop in performance (compared to Sequential) often occurs in CPU-bound tasks in environments like Python due to overhead or synchronization constraints (such as the Global Interpreter Lock).
Note on Consistency: In your provided text, the summary mentioned Parallel as the fastest at 0.01 seconds. However, the raw data listed Sequential at 0.01 seconds and Parallel at 2.18 seconds. The graphs reflect the values listed in the "Processing Time" and "Processing Speed" sections of your report.
Visualization Features:
1.	Processing Time: A direct comparison showing the duration in seconds (lower bars represent better performance).
2.	Processing Speed: This uses a logarithmic scale to accommodate the vast difference between the Sequential speed (74.7M) and the Threading speed (30.9K), ensuring all bars remain visible and comparable.



Source code : 

Youtube :
