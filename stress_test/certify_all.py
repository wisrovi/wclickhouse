import os
import subprocess
import sys
import re
from pathlib import Path

TARGET_IP = "10.37.63.23"

def run_and_validate(example_path: Path):
    with open(example_path, 'r') as f:
        content = f.read()
    
    # Temporarily change host to TARGET_IP
    temp_content = re.sub(r'"host": ".*?"', f'"host": "{TARGET_IP}"', content)
    
    with open(example_path, 'w') as f:
        f.write(temp_content)
    
    print(f"Testing {example_path} on {TARGET_IP}...", end=" ", flush=True)
    
    env = os.environ.copy()
    env["PYTHONPATH"] = "src"
    
    try:
        result = subprocess.run(
            [sys.executable, str(example_path)],
            capture_output=True,
            text=True,
            env=env,
            timeout=30
        )
        if result.returncode == 0:
            print("OK")
            success = True
        else:
            print("FAIL")
            print(f"Error: {result.stderr}")
            success = False
    except Exception as e:
        print(f"ERROR: {e}")
        success = False
    finally:
        # Restore original content
        with open(example_path, 'w') as f:
            f.write(content)
            
    return success

def main():
    examples_root = Path("examples")
    all_examples = sorted(list(examples_root.glob("**/*.py")))
    
    results = []
    for example in all_examples:
        results.append(run_and_validate(example))
        
    print(f"\nFinal Certification: {sum(results)}/{len(results)} PASSED")
    if all(results):
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
