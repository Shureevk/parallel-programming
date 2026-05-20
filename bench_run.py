import subprocess
import csv
import os
import re
import time

SIZES = [10, 50, 100, 200, 400, 600, 800, 1000]
STATS_FILE = 'stats.csv'
EXE_PATH = 'src/matrix'

def run_command(cmd, description):
    print(f"{description}...", end=" ", flush=True)
    start = time.time()
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    elapsed = time.time() - start
    
    if result.returncode != 0:
        print(f"ERROR")
        return False, result.stdout + result.stderr, elapsed
    
    print(f"OK ({elapsed:.2f}s)")
    return True, result.stdout + result.stderr, elapsed

def main():
    if not os.path.exists(EXE_PATH):
        print(f"Error: {EXE_PATH} not found!")
        print("Run: g++ src/main.cpp -o src/matrix -O2")
        return
    
    results = []
    
    for n in SIZES:
        print(f"\n--- Size: {n}x{n} ---")
        
        success, _, _ = run_command(f"python3 generate.py {n}", "Generate matrices")
        if not success:
            continue
        
        success, output, _ = run_command(EXE_PATH, "Multiply matrices")
        if not success:
            continue
        
        time_match = re.search(r"Computation time:\s*([\d.e\-+]+)\s*seconds", output)
        if time_match:
            exec_time = float(time_match.group(1))
        else:
            exec_time = 0.0
        
        operations = n ** 3
        
        verify_result = subprocess.run("python3 verify.py", shell=True, capture_output=True, text=True)
        verify_output = verify_result.stdout + verify_result.stderr
        
        if verify_result.returncode == 0 and "PASSED" in verify_output:
            status = "PASSED"
            print("VERIFY: PASSED")
        else:
            status = "FAILED"
            print("VERIFY: FAILED")
        
        results.append({
            'Size': n,
            'Time_sec': exec_time,
            'Operations': operations,
            'Status': status
        })
        
        print(f"Time: {exec_time:.6f} sec | Ops: {operations:,}")
    
    if results:
        with open(STATS_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['Size', 'Time_sec', 'Operations', 'Status'])
            writer.writeheader()
            writer.writerows(results)
        
        print(f"\nResults saved to {STATS_FILE}")
        
        print("\nResults table:")
        print(f"{'Size':<8} {'Time(sec)':<12} {'Operations':<15} {'Status'}")
        for r in results:
            print(f"{r['Size']:<8} {r['Time_sec']:<12.6f} {r['Operations']:<15,} {r['Status']}")

if __name__ == "__main__":
    main()
