"""Generate the code-only reference notebook from the four readable lab scripts."""
import json
import re
from pathlib import Path
root = Path(__file__).resolve().parents[1]
cells = []
for day in range(1, 5):
    text = (root / 'labs' / f'day{day}.py').read_text()
    chunks = re.split(r'(?m)(?=^# DAY \d - Cell \d+:)', text)
    for chunk in filter(str.strip, chunks):
        cells.append({'cell_type':'code','execution_count':None,'metadata':{},'outputs':[],
                      'source':chunk.splitlines(keepends=True)})
notebook = {'cells':cells,'metadata':{'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},
            'language_info':{'name':'python'},'colab':{'name':'murshid.ipynb','provenance':[]}},'nbformat':4,'nbformat_minor':5}
for i, cell in enumerate(cells): cell['id'] = f'murshid-{i+1:02}'
(root/'notebooks'/'murshid.ipynb').write_text(json.dumps(notebook,ensure_ascii=False,indent=2)+'\n')
