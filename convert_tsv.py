import os
import pandas as pd
from datetime import datetime

def convert_tsv_to_html(tsv_file):
    try:
        df = pd.read_csv(tsv_file, sep='\t')
        basename = os.path.splitext(tsv_file)[0]
        html_file = f"{basename}.html"
        
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>{basename}</title>
    <meta http-equiv="refresh" content="60">
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
    </style>
</head>
<body>
    <h1>Trading Data: {basename}</h1>
    <p>Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    {df.to_html(index=False, escape=False)}
</body>
</html>"""
        
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"Converted {tsv_file} to {html_file}")
        
    except Exception as e:
        print(f"Error converting {tsv_file}: {e}")

# Convert all TSV files
for file in os.listdir('.'):
    if file.endswith('.tsv'):
        convert_tsv_to_html(file)