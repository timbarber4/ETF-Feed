import os
from datetime import datetime

def convert_tsv_to_html(tsv_file):
    try:
        basename = tsv_file.replace('.tsv', '')
        html_file = f"{basename}.html"
        
        # Read the TSV file
        with open(tsv_file, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        
        # Split into lines and handle empty lines
        lines = [line for line in content.split('\n') if line.strip()]
        
        if not lines:
            print(f"No data found in {tsv_file}")
            return
            
        html_content = f'''<!DOCTYPE html>
<html>
<head>
    <title>{basename}</title>
    <meta http-equiv="refresh" content="30">
    <style>
        body {{ font-family: monospace; margin: 20px; background: #f5f5f5; }}
        .container {{ background: white; padding: 20px; border-radius: 8px; }}
        h1 {{ color: #333; }}
        .timestamp {{ color: #666; margin-bottom: 15px; }}
        pre {{ background: #f8f8f8; padding: 15px; overflow-x: auto; border: 1px solid #ddd; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Trading Data: {basename.replace('_', ' ')}</h1>
        <div class="timestamp">Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
        <pre>{content}</pre>
    </div>
</body>
</html>'''
        
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"Converted {tsv_file} to {html_file}")
        
    except Exception as e:
        print(f"Error converting {tsv_file}: {e}")

# Convert all TSV files in current directory
for file in os.listdir('.'):
    if file.endswith('.tsv'):
        convert_tsv_to_html(file)

print("Conversion complete!")