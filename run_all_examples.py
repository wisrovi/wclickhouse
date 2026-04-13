import os
import subprocess
import sys
from pathlib import Path

def run_example(example_path: Path):
    print(f"Running {example_path}...", end=" ", flush=True)
    env = os.environ.copy()
    env["PYTHONPATH"] = "src"
    
    result = subprocess.run(
        [sys.executable, str(example_path)],
        capture_output=True,
        text=True,
        env=env,
        timeout=30
    )
    
    if result.returncode == 0:
        print("PASSED")
        return True
    else:
        print("FAILED")
        print(f"Error: {result.stderr}")
        return False

def main():
    examples_root = Path("examples")
    all_examples = sorted(list(examples_root.glob("**/*.py")))
    
    passed = 0
    failed = []
    
    for example in all_examples:
        # Skip basic_usage as we just ran it
        if example.name == "basic_usage.py":
            continue
            
        if run_example(example):
            passed += 1
        else:
            failed.append(str(example))
            
    print(f"\nSummary: {passed} passed, {len(failed)} failed.")
    if failed:
        print("Failed examples:")
        for f in failed:
            print(f" - {f}")
        sys.exit(1)

if __name__ == "__main__":
    main()
