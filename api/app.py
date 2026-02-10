from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import uuid

app = FastAPI(title="Capstone Ops API")

class RunRequest(BaseModel):
    playbook: str = "submit_jcl.yml"
    extra_vars: dict = {}

@app.post("/run")
def run_playbook(req: RunRequest):
    try:
        import ansible_runner
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ansible_runner import failed: {e}")

    run_id = str(uuid.uuid4())

    base_dir = os.path.dirname(__file__)
    private_data_dir = os.path.join(base_dir, "ansible")

    result = ansible_runner.run(
        private_data_dir=private_data_dir,
        playbook=req.playbook,
        inventory=os.path.join(private_data_dir, "inventory.ini"),
        extravars=req.extra_vars,
        ident=run_id,
        quiet=True,
    )

    if result.rc != 0:
        raise HTTPException(
            status_code=500,
            detail={
                "run_id": run_id,
                "status": result.status,
                "rc": result.rc,
            },
        )

    return {
        "run_id": run_id,
        "status": result.status,
        "rc": result.rc,
    }

@app.get("/health")
def health():
    return {"ok": True}
