import subprocess, sys, json, os
script = "/home/bob/.hermes/.openclaw/workspace/pipeline-engine/data/content-generator.py"
cwd = "/home/bob/.hermes/.openclaw/workspace/pipeline-engine"

print("="*60)
print("TEST 1: --report mode")
print("="*60)
r = subprocess.run([sys.executable, script, "--report"], capture_output=True, text=True, cwd=cwd)
print(r.stdout[:2000])
if r.stderr: print("STDERR:", r.stderr[:500])

print("="*60)
print("TEST 2: --social only")
print("="*60)
r = subprocess.run([sys.executable, script, "--social", "only"], capture_output=True, text=True, cwd=cwd)
print(r.stdout[:1000])

print("="*60)
print("TEST 3: --blog only")
print("="*60)
r = subprocess.run([sys.executable, script, "--blog", "only"], capture_output=True, text=True, cwd=cwd)
print(r.stdout[:1000])

print("="*60)
print("TEST 4: Full generation")
print("="*60)
r = subprocess.run([sys.executable, script], capture_output=True, text=True, cwd=cwd)
print(r.stdout[:1000])

print("="*60)
print("TEST 5: Pipeline filter")
print("="*60)
r = subprocess.run([sys.executable, script, "--pipeline", "books", "--social", "only"], capture_output=True, text=True, cwd=cwd)
print(r.stdout[:800])

for f in ["data/generated-social-content.json", "data/generated-blog-posts.json"]:
    path = os.path.join(cwd, f)
    if os.path.exists(path):
        with open(path) as fh:
            data = json.load(fh)
        print(f"✅ {f}: {len(data)} items")
    else:
        print(f"❌ {f}: NOT FOUND")
