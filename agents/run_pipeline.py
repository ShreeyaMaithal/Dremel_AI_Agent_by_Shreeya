from pathlib import Path
import subprocess
import sys

BASE_DIR = Path(__file__).resolve().parent.parent

def run_script(script_name):
    script_path = BASE_DIR / "agents" / script_name

    print(f"Running {script_name}...")

    result = subprocess.run(
        [sys.executable, str(script_path)],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(result.stderr)
        raise Exception(
            f"{script_name} failed.\n\nSTDOUT:\n{result.stdout}\n\nSTDERR:\n{result.stderr}"
        )

    print(f"{script_name} completed.")

def run_all_agents():

    run_script("trend_scout.py")
    run_script("insight_agent.py")
    run_script("strategy_agent.py")
    run_script("report_agent.py")

    print("All agents completed successfully.")

if __name__ == "__main__":
    run_all_agents()