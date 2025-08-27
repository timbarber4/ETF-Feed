import os
from datetime import datetime

def convert_tsv_to_html(tsv_file):
    try:
        basename = tsv_file.replace('.tsv', '')
        html_file = f"{basename}.html"
        
        with open(tsv_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        html_content = f'''<!DOCTYPE html>
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
    <table>
'''
        
        for i, line in enumerate(lines):
            cells = line.strip().split('\t')
            if i == 0:  # Header row
                html_content += '<tr>'
                for cell in cells:
                    html_content += f'<th>{cell}</th>'
                html_content += '</tr>'
            else:  # Data rows
                html_content += '<tr>'
                for cell in cells:
                    html_content += f'<td>{cell}</td>'
                html_content += '</tr>'
        
        html_content += '</table></body></html>'
        
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"Converted {tsv_file} to {html_file}")
        
    except Exception as e:
        print(f"Error converting {tsv_file}: {e}")

# Convert all TSV files
for file in os.listdir('.'):
    if file.endswith('.tsv'):
        convert_tsv_to_html(file)