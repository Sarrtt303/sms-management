import subprocess

class ProcessManager:
    @staticmethod
    def start_session(country, operator):
        session_name = f"sms_{country}_{operator}"
        cmd = f"screen -dmS {session_name} python script.py --country {country} --operator {operator}"
        subprocess.run(cmd, shell=True)
        return session_name

    @staticmethod
    def stop_session(session_name):
        cmd = f"screen -X -S {session_name} quit"
        subprocess.run(cmd, shell=True)