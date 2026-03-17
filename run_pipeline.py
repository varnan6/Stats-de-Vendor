import subprocess
import time

def run(module):

    print(f"\n=== Running {module} ===")
    start = time.time()
    result = subprocess.run(["python", "-m", {module}])

    if result.returncode != 0:
        print(f"Failed at {module}")
        exit(1)

    print(f"\n=== {module} finshed execution in {time.time() - start}s ===")

def main():

    pipeline = [
        "scripts.init_db",
        "scripts.seed_vendor",
        "scripts.generate_data",
        "scripts.build_vendor_features",
        "scripts.vendor_anomaly_detection",
        "scripts.vendor_risk_scoring",
        "scripts.build_vendor_embeddings"
    ]

    print("=== Running Pipeline ===")

    for module in pipeline:
        subprocess.run(["python", "-m", module])

    print("=== Pipeline completed successfully")

if __name__ == "__main__":
    main()