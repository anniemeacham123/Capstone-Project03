from fastapi import FastAPI, HTTPException
from typing import Optional
import subprocess
import time

app = FastAPI()

INVENTORY = "api/ansible/inventory.yml"

def run_playbook(playbook_path: str, extra_vars: Optional[dict] = None):
    cmd = ["ansible-playbook", playbook_path, "-i", INVENTORY]
    if extra_vars:
        ev = " ".join([f"{k}='{v}'" for k, v in extra_vars.items()])
        cmd += ["--extra-vars", ev]

    start = time.time()
    p = subprocess.run(cmd, capture_output=True, text=True)
    duration = time.time() - start

    return {
        "return_code": p.returncode,
        "duration_seconds": round(duration, 2),
        "stdout": p.stdout,
        "stdout_lines": p.stdout.splitlines(),
        "stderr": p.stderr,
        "stderr_lines": p.stderr.splitlines(),
        "command": " ".join(cmd),
    }

@app.post("/ops/ping-mainframe")
def ping_mainframe():
    res = run_playbook("api/ansible/playbooks/ping.yml")
    if res["return_code"] != 0:
        raise HTTPException(status_code=500, detail=res)
    return res

@app.post("/ops/submit-jcl")
def submit_jcl(job_name: str = "DEMOJOB"):
    # Pre-flight
    ping = run_playbook("api/ansible/playbooks/ping.yml")
    if ping["return_code"] != 0:
        raise HTTPException(status_code=500, detail={"stage": "ping", **ping})

    # Run JCL
    res = run_playbook("api/ansible/playbooks/submit_jcl.yml", {"job_name": job_name})
    if res["return_code"] != 0:
        raise HTTPException(status_code=500, detail={"stage": "submit_jcl", **res})
    return res
    
