import subprocess
result = subprocess.run(
    ["python3", "/Users/zhijian/workspace/ai-demand-research-v3/projects/宝爸宝妈-2026-05-19/04-signal-analysis/layer2_structuring.py"],
    capture_output=True, text=True
)
print("STDOUT:", result.stdout)
print("STDERR:", result.stderr)
print("Return code:", result.returncode)
