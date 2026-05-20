import subprocess
result = subprocess.run(['/usr/bin/python3', '/Users/zhijian/workspace/ai-demand-research-v3/projects/宝爸宝妈-2026-05-19/04-signal-analysis/classify_layer1.py'], capture_output=True, text=True)
print(result.stdout)
print(result.stderr)
