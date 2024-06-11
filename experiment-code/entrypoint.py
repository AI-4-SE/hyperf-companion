import argparse
import subprocess
import os
import time
port1 = 8083
port2 = 8084

cwd_wluncert = '/app/wluncert'

def main():
    parser = argparse.ArgumentParser(description="Entrypoint for Docker container tasks")

    parser.add_argument('command', choices=['experiment', 'dashboards'], help="The command to run")
    parser.add_argument('--jobs', type=int, default=1, help="Defines how many models are trained in parallel")
    parser.add_argument('--store', action='store_true', help="Store insights into posterior distributions")
    parser.add_argument('--reps', type=int, default=1, help="Defines the number of repetitions")
    parser.add_argument('--training-set-size', type=float,
                        help="Disables the sweep over different training set sizes and uses the given size")

    args = parser.parse_args()

    os.chdir(cwd_wluncert)
    if args.command == 'experiment':
        run_experiment(args)
    elif args.command == 'dashboards':
        start_dashboards()
    else:
        print(f"Unknown command: {args.command}")

def start_dashboards():
    run_metrics_dashboard()
    time.sleep(0.25)
    run_insights_dashboard()


def run_metrics_dashboard():
    dashboard1_cmd = ["streamlit", "run", "playground/metricsdashboard.py", "--server.port", str(port1)]
    subprocess.Popen(dashboard1_cmd, cwd=cwd_wluncert)

def run_insights_dashboard():
    dashboard1_cmd = ["streamlit", "run", "playground/insights-dashboard.py", "--server.port", str(port2)]
    subprocess.Popen(dashboard1_cmd, cwd=cwd_wluncert)

def run_experiment(args):
    # Construct the command for the experiment task
    cmd = ["python3.9", "main.py", "--experiment", "multitask", "--jobs", str(args.jobs), "--reps", str(args.reps)]
    if args.store:
        cmd.append("--store")
    if args.training_set_size is not None:
        cmd.extend(["--training-set-size", str(args.training_set_size)])
    print("Running experiment task with the following command:")
    print(" ".join(cmd))
    # Run the constructed command
    subprocess.run(cmd, cwd=cwd_wluncert)

    insights_cmd = ["python3.9", "modelinsights.py"]
    subprocess.run(insights_cmd, cwd=cwd_wluncert)




if __name__ == "__main__":
    main()
