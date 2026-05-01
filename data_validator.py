"""
Project: Mega Data Cleaner & Validator
Process 1 MILLION records in seconds using:
- Threading for file reading (concurrent I/O)
- Multiprocessing for data validation (parallel CPU)
- Separate reports for VALID and INVALID records
"""

import os
import time
import threading
import multiprocessing
import queue
import random
import string
from datetime import datetime
from collections import defaultdict

# ===================== CONFIGURATION =====================
DATA_FILE = "million_data.txt"
VALID_OUTPUT = "valid_records.txt"
INVALID_OUTPUT = "invalid_records.txt"
ERROR_REPORT = "error_report.txt"
NUM_THREADS = 4
NUM_PROCESSES = multiprocessing.cpu_count()
RECORDS_TO_GENERATE = 1000000  # 1 JUTA

# ===================== GENERATE 1 MILLION DATA RECORDS =====================
def generate_million_records(num_records=RECORDS_TO_GENERATE):
    """Generate 1 million data records quickly"""
    
    if os.path.exists(DATA_FILE):
        file_size = os.path.getsize(DATA_FILE) / (1024 * 1024)
        print(f"[*] Data file already exists: {DATA_FILE} ({file_size:.2f} MB)")
        return
    
    print(f"\n[+] Generating {num_records:,} data records...")
    print(f"    This may take 1-2 minutes...")
    
    with open(DATA_FILE, 'w') as f:
        for i in range(num_records):
            # Generate random user data
            user_id = f"USER{i:08d}"
            name = ''.join(random.choices(string.ascii_letters, k=10))
            email = f"{name.lower()}@example.com"
            age = str(random.randint(18, 80))
            city = random.choice(["KL", "JB", "PG", "IPOH", "KK"])
            amount = str(round(random.uniform(10, 10000), 2))
            
            # Add some bad data (5% errors)
            error_type = None
            if random.random() < 0.05:
                error_choice = random.random()
                if error_choice < 0.25:
                    age = ""  # Missing age
                    error_type = "MISSING_AGE"
                elif error_choice < 0.5:
                    email = "invalid_email"  # Invalid email
                    error_type = "INVALID_EMAIL"
                elif error_choice < 0.75:
                    amount = "invalid_amount"  # Invalid amount
                    error_type = "INVALID_AMOUNT"
                else:
                    # Duplicate ID (will be created later)
                    error_type = "POTENTIAL_DUPLICATE"
            
            # Add error type as comment at end
            if error_type:
                f.write(f"{user_id}|{name}|{email}|{age}|{city}|{amount}|{error_type}\n")
            else:
                f.write(f"{user_id}|{name}|{email}|{age}|{city}|{amount}|VALID\n")
            
            if (i + 1) % 50000 == 0:
                print(f"  Generated {i+1:,}/{num_records:,} records")
    
    file_size = os.path.getsize(DATA_FILE) / (1024 * 1024)
    print(f"[+] Data file created: {DATA_FILE} ({file_size:.2f} MB)")

# ===================== THREADING FOR FAST FILE READING =====================
class FastFileReader:
    """Read large file using multiple threads"""
    
    def __init__(self, filename, num_threads=NUM_THREADS):
        self.filename = filename
        self.num_threads = num_threads
        self.lines = []
        self.lock = threading.Lock()
    
    def read_chunk(self, chunk_info):
        """Read a chunk of the file"""
        start_byte, end_byte = chunk_info
        lines = []
        
        with open(self.filename, 'r') as f:
            f.seek(start_byte)
            if start_byte != 0:
                f.readline()  # Skip partial line
            
            while f.tell() < end_byte:
                line = f.readline()
                if not line:
                    break
                lines.append(line.strip())
        
        with self.lock:
            self.lines.extend(lines)
        
        return len(lines)
    
    def read_all(self):
        """Read file using multiple threads"""
        print(f"\n[📖 CONCURRENT] Reading file with {self.num_threads} threads...")
        start_time = time.time()
        
        file_size = os.path.getsize(self.filename)
        chunk_size = file_size // self.num_threads
        
        chunks = []
        for i in range(self.num_threads):
            start = i * chunk_size
            end = (i + 1) * chunk_size if i < self.num_threads - 1 else file_size
            chunks.append((start, end))
        
        threads = []
        for chunk in chunks:
            t = threading.Thread(target=self.read_chunk, args=(chunk,))
            t.start()
            threads.append(t)
        
        for t in threads:
            t.join()
        
        elapsed = time.time() - start_time
        print(f"[✓] Read {len(self.lines):,} lines in {elapsed:.3f}s")
        
        return self.lines, elapsed

# ===================== DATA VALIDATOR (MULTIPROCESSING) =====================
def validate_batch(batch_lines):
    """Validate a batch of data records"""
    results = {
        'total': 0,
        'valid': 0,
        'invalid': 0,
        'valid_records': [],
        'invalid_records': [],
        'error_types': defaultdict(int),
        'missing_age': 0,
        'invalid_email': 0,
        'invalid_amount': 0,
        'duplicates': []
    }
    
    seen_ids = set()
    
    for line in batch_lines:
        if not line:
            continue
        
        results['total'] += 1
        parts = line.split('|')
        
        if len(parts) < 6:
            results['invalid'] += 1
            results['invalid_records'].append(line + "|INVALID_FORMAT")
            results['error_types']['INVALID_FORMAT'] += 1
            continue
        
        user_id = parts[0]
        name = parts[1]
        email = parts[2]
        age = parts[3]
        city = parts[4]
        amount = parts[5]
        
        # Check for duplicate ID
        if user_id in seen_ids:
            results['duplicates'].append(user_id)
            results['invalid_records'].append(line + "|DUPLICATE_ID")
            results['error_types']['DUPLICATE_ID'] += 1
            results['invalid'] += 1
            continue
        else:
            seen_ids.add(user_id)
        
        # Validate fields
        errors = []
        
        if not age or not age.isdigit():
            errors.append("MISSING_AGE")
            results['missing_age'] += 1
        
        if '@' not in email or '.' not in email:
            errors.append("INVALID_EMAIL")
            results['invalid_email'] += 1
        
        try:
            amount_float = float(amount)
            if amount_float < 0:
                errors.append("NEGATIVE_AMOUNT")
        except:
            errors.append("INVALID_AMOUNT")
            results['invalid_amount'] += 1
        
        # Check city
        valid_cities = ["KL", "JB", "PG", "IPOH", "KK"]
        if city not in valid_cities:
            errors.append("INVALID_CITY")
        
        if errors:
            results['invalid'] += 1
            error_str = "|".join(errors)
            results['invalid_records'].append(line + f"|{error_str}")
            for err in errors:
                results['error_types'][err] += 1
        else:
            results['valid'] += 1
            results['valid_records'].append(line)
    
    return results

def parallel_validate(data_lines, num_processes=None):
    """Validate data using multiprocessing"""
    
    if num_processes is None:
        num_processes = NUM_PROCESSES
    
    print(f"\n[⚡ PARALLEL] Validating {len(data_lines):,} records using {num_processes} CPU cores...")
    start_time = time.time()
    
    # Split into batches
    batch_size = max(1, len(data_lines) // num_processes)
    batches = [data_lines[i:i+batch_size] for i in range(0, len(data_lines), batch_size)]
    
    # Process in parallel
    with multiprocessing.Pool(processes=num_processes) as pool:
        batch_results = pool.map(validate_batch, batches)
    
    # Combine results
    final_results = {
        'total': 0,
        'valid': 0,
        'invalid': 0,
        'valid_records': [],
        'invalid_records': [],
        'error_types': defaultdict(int),
        'missing_age': 0,
        'invalid_email': 0,
        'invalid_amount': 0,
        'duplicates': []
    }
    
    for result in batch_results:
        final_results['total'] += result['total']
        final_results['valid'] += result['valid']
        final_results['invalid'] += result['invalid']
        final_results['valid_records'].extend(result['valid_records'])
        final_results['invalid_records'].extend(result['invalid_records'])
        final_results['missing_age'] += result['missing_age']
        final_results['invalid_email'] += result['invalid_email']
        final_results['invalid_amount'] += result['invalid_amount']
        final_results['duplicates'].extend(result['duplicates'])
        
        for err, count in result['error_types'].items():
            final_results['error_types'][err] += count
    
    elapsed = time.time() - start_time
    rate = final_results['total'] / elapsed if elapsed > 0 else 0
    print(f"[✓] Validation completed in {elapsed:.3f}s ({rate:.0f} records/sec)")
    
    return final_results, elapsed

# ===================== SAVE SEPARATE REPORTS =====================
def save_separate_reports(results, total_records):
    """Save valid and invalid records to separate files"""
    
    print(f"\n📁 SAVING SEPARATE REPORTS...")
    print("-" * 50)
    
    # Save VALID records
    with open(VALID_OUTPUT, 'w', encoding='utf-8') as f:
        f.write(f"# VALID RECORDS REPORT\n")
        f.write(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"# Total Valid Records: {len(results['valid_records']):,}\n")
        f.write(f"# Format: user_id|name|email|age|city|amount\n")
        f.write("#" + "=" * 60 + "\n\n")
        
        for record in results['valid_records']:
            f.write(record + "\n")
    
    valid_size = os.path.getsize(VALID_OUTPUT) / (1024 * 1024)
    print(f"  ✓ VALID records saved: {VALID_OUTPUT}")
    print(f"    • {len(results['valid_records']):,} records")
    print(f"    • {valid_size:.2f} MB")
    
    # Save INVALID records with error details
    with open(INVALID_OUTPUT, 'w', encoding='utf-8') as f:
        f.write(f"# INVALID RECORDS REPORT\n")
        f.write(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"# Total Invalid Records: {len(results['invalid_records']):,}\n")
        f.write(f"# Format: user_id|name|email|age|city|amount|ERROR_TYPE\n")
        f.write("#" + "=" * 60 + "\n\n")
        
        for record in results['invalid_records']:
            f.write(record + "\n")
    
    invalid_size = os.path.getsize(INVALID_OUTPUT) / (1024 * 1024)
    print(f"\n  ✓ INVALID records saved: {INVALID_OUTPUT}")
    print(f"    • {len(results['invalid_records']):,} records")
    print(f"    • {invalid_size:.2f} MB")
    
    # Save ERROR SUMMARY report
    with open(ERROR_REPORT, 'w', encoding='utf-8') as f:
        f.write("=" * 60 + "\n")
        f.write("ERROR SUMMARY REPORT\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("ERROR TYPE BREAKDOWN:\n")
        f.write("-" * 40 + "\n")
        for error, count in sorted(results['error_types'].items(), key=lambda x: x[1], reverse=True):
            percentage = (count / results['invalid']) * 100 if results['invalid'] > 0 else 0
            f.write(f"  {error:<20} : {count:>8,} ({percentage:>5.1f}%)\n")
        
        f.write("\n" + "-" * 40 + "\n")
        f.write(f"  {'TOTAL INVALID':<20} : {results['invalid']:>8,}\n")
    
    error_size = os.path.getsize(ERROR_REPORT) / 1024
    print(f"\n  ✓ Error summary saved: {ERROR_REPORT}")
    print(f"    • {error_size:.2f} KB")
    
    return VALID_OUTPUT, INVALID_OUTPUT, ERROR_REPORT

# ===================== SEQUENTIAL BENCHMARK =====================
def sequential_validate(data_lines, sample_size=10000):
    """Sequential validation for baseline"""
    print(f"\n[🐢 SEQUENTIAL] Running benchmark on {sample_size:,} records...")
    start_time = time.time()
    
    sample = data_lines[:sample_size]
    results = validate_batch(sample)
    
    elapsed = time.time() - start_time
    print(f"[✓] Benchmark completed in {elapsed:.3f}s")
    
    return elapsed

# ===================== MAIN REPORT =====================
def generate_main_report(results, sequential_time, parallel_time, total_records, read_time):
    """Generate main validation report"""
    
    duplicate_count = len(set(results['duplicates']))
    
    print("\n" + "=" * 70)
    print("📊 DATA VALIDATION REPORT")
    print("=" * 70)
    
    print("\n📈 SUMMARY:")
    print("-" * 50)
    print(f"  Total Records       : {total_records:,}")
    print(f"  Valid Records       : {results['valid']:,} ({results['valid']/total_records*100:.1f}%)")
    print(f"  Invalid Records     : {results['invalid']:,} ({results['invalid']/total_records*100:.1f}%)")
    
    print("\n⚠️  ISSUES DETECTED:")
    print("-" * 50)
    print(f"  Missing Age         : {results['missing_age']:,}")
    print(f"  Invalid Email       : {results['invalid_email']:,}")
    print(f"  Invalid Amount      : {results['invalid_amount']:,}")
    print(f"  Duplicate IDs       : {duplicate_count:,}")
    
    # Show error breakdown
    if results['error_types']:
        print("\n📋 ERROR TYPE BREAKDOWN:")
        print("-" * 50)
        for error, count in sorted(results['error_types'].items(), key=lambda x: x[1], reverse=True)[:5]:
            percentage = (count / results['invalid']) * 100 if results['invalid'] > 0 else 0
            bar_len = int(percentage / 2)
            bar = "█" * bar_len + "░" * (50 - bar_len)
            print(f"  {error:<20} {count:>8,} ({percentage:>5.1f}%) {bar}")
    
    print("\n⚡ PERFORMANCE:")
    print("-" * 50)
    print(f"  File Reading (Threading) : {read_time:.3f}s")
    print(f"  Sequential (est)         : {sequential_time * (total_records/10000):.3f}s")
    print(f"  Parallel (Multiprocessing): {parallel_time:.3f}s")
    print(f"  SPEEDUP                   : {(sequential_time * (total_records/10000)) / parallel_time:.1f}x FASTER 🚀")
    
    print("\n💻 SYSTEM:")
    print("-" * 50)
    print(f"  CPU Cores           : {NUM_PROCESSES}")
    print(f"  Threads             : {NUM_THREADS}")
    print(f"  Processing Rate     : {total_records/parallel_time:.0f} records/sec")
    
    print("\n📁 OUTPUT FILES:")
    print("-" * 50)
    print(f"  Valid records   : {VALID_OUTPUT}")
    print(f"  Invalid records : {INVALID_OUTPUT}")
    print(f"  Error summary   : {ERROR_REPORT}")
    
    print("\n" + "=" * 70)
    print("✅ VALIDATION COMPLETE!")
    print("=" * 70)

# ===================== MAIN =====================
def main():
    print("=" * 70)
    print("📊 MEGA DATA CLEANER & VALIDATOR")
    print("   Process 1 MILLION Records in Seconds")
    print("   With SEPARATE Valid/Invalid Reports")
    print("=" * 70)
    print(f"\n⚙️  Configuration:")
    print(f"   • Target Records    : {RECORDS_TO_GENERATE:,}")
    print(f"   • CPU Cores         : {NUM_PROCESSES}")
    print(f"   • Threads for I/O   : {NUM_THREADS}")
    print("=" * 70)
    
    # Generate data
    generate_million_records(RECORDS_TO_GENERATE)
    
    # Step 1: Read file using THREADING
    reader = FastFileReader(DATA_FILE, NUM_THREADS)
    data_lines, read_time = reader.read_all()
    
    if not data_lines:
        print("[!] No data found!")
        return
    
    total_records = len(data_lines)
    
    # Step 2: Sequential benchmark
    sequential_time = sequential_validate(data_lines, sample_size=10000)
    
    # Step 3: Parallel validation using MULTIPROCESSING
    results, parallel_time = parallel_validate(data_lines, NUM_PROCESSES)
    
    # Step 4: Save separate reports for valid and invalid records
    save_separate_reports(results, total_records)
    
    # Step 5: Generate main report
    generate_main_report(results, sequential_time, parallel_time, total_records, read_time)

if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()