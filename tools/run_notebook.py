"""Execute code cells in a fresh namespace and retain actual stdout; standard library."""
import contextlib
import io
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def run(path, skip_setup=False):
    path = path.resolve()
    notebook = json.loads(path.read_text(encoding='utf-8'))
    namespace = {'__name__': '__main__'}
    old = Path.cwd()
    os.chdir(ROOT)
    try:
        for index, cell in enumerate(notebook['cells'], 1):
            if cell['cell_type'] != 'code':
                continue
            source = ''.join(cell['source'])
            if skip_setup and ('pip' in source and 'subprocess' in source):
                source = "import importlib.metadata\nprint('Dependencies installed in isolated local environment:')\nfor package in ('torch', 'transformers', 'sentencepiece'):\n    print(package, importlib.metadata.version(package))\n"
                # Keep the Colab install source; annotate how it was executed locally.
                cell['metadata']['local_execution_note'] = 'Install cell replaced during local execution by installed-version verification; original Colab setup retained.'
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                exec(compile(source, f'{path.name}:cell-{index}', 'exec'), namespace)
            cell['execution_count'] = index
            cell['outputs'] = [{'output_type': 'stream', 'name': 'stdout', 'text': output.getvalue().splitlines(keepends=True)}] if output.getvalue() else []
            print(f'{path.name}: cell {index} completed', flush=True)
    finally:
        os.chdir(old)
    path.write_text(json.dumps(notebook, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    return namespace

if __name__ == '__main__':
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT/'notebooks/murshid.ipynb'
    run(target, '--installed' in sys.argv)
