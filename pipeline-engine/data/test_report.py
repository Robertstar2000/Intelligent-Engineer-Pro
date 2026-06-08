import subprocess, sys, json, os
script = "/home/bob/.hermes/.openclaw/workspace/pipeline-engine/data/content-generator.py"
cwd = "/home/bob/.hermes/.openclaw/workspace/pipeline-engine/data"

print(f"cwd exists: {os.path.isdir(cwd)}")
print(f"script exists: {os.path.isfile(script)}")

r = subprocess.run([sys.executable, script, "--report"], capture_output=True, text=True, cwd=cwd)
print(f"RC: {r.returncode}")
print(f"STDOUT: {r.stdout[:2000]}")
print(f"STDERR: {r.stderr[:2000] if r.stderr else '(none)'}")
