from flask import Flask
import subprocess

app = Flask(__name__)

@app.route("/run-pipeline")
def run_pipeline():
    subprocess.run(["python", "process_bills.py"])
    return {
    "status": "success",
    "message": "Receipt pipeline executed",
    "timestamp": datetime.now().isoformat()
}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)