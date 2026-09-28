"""Render entrypoint: run the Flask health/web app and Telegram bot together."""
import os
import signal
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT)

env = os.environ.copy()
env.setdefault("PORT", "10000")

web = None
bot = None


def stop_process(proc):
    if proc is not None and proc.poll() is None:
        try:
            proc.terminate()
            proc.wait(timeout=10)
        except Exception:
            try:
                proc.kill()
            except Exception:
                pass


def shutdown(signum, frame):
    print("Shutting down Render service...", flush=True)
    stop_process(bot)
    stop_process(web)
    raise SystemExit(0)


signal.signal(signal.SIGTERM, shutdown)
signal.signal(signal.SIGINT, shutdown)

print(f"Starting web server on port {env['PORT']}...", flush=True)
web = subprocess.Popen([sys.executable, "app.py"], env=env)

# Give Flask a moment to bind before starting the bot.
time.sleep(1)

print("Starting Telegram bot...", flush=True)
bot = subprocess.Popen([sys.executable, "main.py"], env=env)

while True:
    if web.poll() is not None:
        print(f"Web server stopped with code {web.returncode}", flush=True)
        stop_process(bot)
        raise SystemExit(web.returncode or 1)

    if bot.poll() is not None:
        print(f"Telegram bot stopped with code {bot.returncode}", flush=True)
        stop_process(web)
        raise SystemExit(bot.returncode or 1)

    time.sleep(2)
