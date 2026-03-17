import subprocess
import time

def run(script):

    print(f"\n=== Running {script} ===")
    start = time.time()
    result = subprocess.run(["python", script])

    if result.returncode != 0:
        print(f"Failed at {script}")
        exit(1)

    print(f"\n=== {script} finshed execution in {time.time() - start}s ===")

def main():

    pipeline = [
        "scripts/init_db.py",
        "scripts/seed_vendor.py",
        "scripts/generate_data.py",
        "scripts/build_vendor_features.py",
        "scripts/build_anomaly_detection.py",
        "scripts/vendor_risk_scoring.py",
        "scripts/build_vendor_embeddings.py"
    ]

    print("=== Running Pipeline ===")

    for script in pipeline:
        run(script)

    print("=== Pipeline completed successfully")

if __name__ == "__main__":
    main()