import subprocess
import typer

scripts = [
        "check_quick.py",
        "check_resources.py",
        "check_security.py",
        "check_logs.py",
        "check_network.py",
        "check_services.py",
]





app = typer.Typer()


@app.command()
def quick():
    check_quick = subprocess.run(
        ['python3', f'../agent/checks/check_quick.py', '--json'], capture_output=True, text=True)
    print(check_quick.stdout)

@app.command()
def resources():
    check_resources = subprocess.run(
        ['python3', f'../agent/checks/check_resources.py', '--json'], capture_output=True, text=True)
    print(check_resources.stdout)


@app.command()
def security():
    check_security = subprocess.run(
        ['python3', f'../agent/checks/check_security.py', '--json'], capture_output=True, text=True)
    print(check_security.stdout)


@app.command()
def logs():
    check_logs = subprocess.run(
        ['python3', f'../agent/checks/check_logs.py', '--json'], capture_output=True, text=True)
    print(check_logs.stdout)


@app.command()
def network():
    check_network = subprocess.run(
        ['python3', f'../agent/checks/check_network.py', '--json'], capture_output=True, text=True)
    print(check_network.stdout)


@app.command()
def services():
    check_services = subprocess.run(
        ['python3', f'../agent/checks/check_services.py', '--json'], capture_output=True, text=True)
    print(check_services.stdout)


@app.command()
def full():
    for script in scripts:
        check_full = subprocess.run(
            ['python3', f'../agent/checks/{script}', '--json'], capture_output=True, text=True)
        print(check_full.stdout)


if __name__ == "__main__": app()