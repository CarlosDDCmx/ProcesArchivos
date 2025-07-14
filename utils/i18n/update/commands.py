"""
Contiene una función utilitaria para ejecutar comandos externos.
"""
import subprocess

def run(cmd: list[str], cwd=None):
    result = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)
    if result.returncode != 0:
        print(f"❌ Error al ejecutar: {' '.join(cmd)}")
        print(result.stderr)
    return result
