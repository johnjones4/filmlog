import os
from pathlib import Path
import pystache
import subprocess
from pathlib import Path

# Utility function to chunk a list
def chunk(lst, n):
    return [lst[i:i + n] for i in range(0, len(lst), n)]

sizes = [8, 16, 24, 36]

out_dir = Path(__file__).parent / 'out'
out_dir.mkdir(exist_ok=True)

meta_fields = [
    'Roll Number',
    'Date Exposed',
    'Date Processed',
    'Date Expired',
    'Film Stock',
    'Box Speed',
    'Exposed Speed',
    'Camera/Lens',
    'Developer',
    'Developer Age',
    'Development Time/Temp',
]

def render_pdf_with_chrome(html_path, pdf_path):
    chrome_path = os.environ.get("CHROME_BIN", '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
    subprocess.run([
        chrome_path,
        '--headless',
        '--disable-gpu',
        '--print-to-pdf=' + str(pdf_path),
        str(html_path)
    ], check=True)

with open('template.html', encoding='utf-8') as f:
    template = f.read()

for size in sizes:
    view = {
        'metaFields': meta_fields,
        'frameColumns': chunk(list(range(1, size + 1)), size // 2)
    }

    # Render HTML with Mustache
    output_html = pystache.render(template, view)
    html_path = out_dir / f'{size}.html'

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(output_html)

    # Convert HTML to PDF using Pandoc
    pdf_path = out_dir / f'{size}.pdf'
    render_pdf_with_chrome(html_path, pdf_path)
    print(f"Generated {pdf_path}")
