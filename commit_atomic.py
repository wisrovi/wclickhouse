import subprocess

def run_git(cmd):
    subprocess.run(["git"] + cmd, cwd="wclickhouse")

# 1. Reset everything first to commit file by file
run_git(["reset"])

# 2. Get the list of all changed files (new, modified, deleted)
status = subprocess.check_output(["git", "status", "--porcelain"], cwd="wclickhouse").decode()
files = [line[3:].strip() for line in status.splitlines()]

for file in files:
    print(f"Committing {file}...")
    run_git(["add", file])
    msg = f"feat: add/update {file}"
    if file.startswith("src/"):
        msg = f"feat(core): update {file}"
    elif file.startswith("examples/"):
        msg = f"docs(examples): add {file}"
    elif file.startswith("test/"):
        msg = f"test: add {file}"
    
    run_git(["commit", "-m", msg])

print("All commits completed.")
