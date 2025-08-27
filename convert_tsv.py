import os
import html
from datetime import datetime

def convert_tsv_to_github_html(tsv_file):
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
        
        # Parse TSV data
        rows = []
        for line in lines:
            # Split by tabs and escape HTML characters
            cells = [html.escape(cell.strip()) for cell in line.split('\t')]
            rows.append(cells)
        
        # Build HTML table
        if rows:
            # First row as header
            header_row = rows[0]
            data_rows = rows[1:] if len(rows) > 1 else []
            
            table_html = '<table border="1" cellpadding="5" cellspacing="0" style="border-collapse: collapse; width: 100%; font-family: monospace;">\n'
            
            # Add header
            table_html += '  <thead style="background-color: #f0f0f0;">\n    <tr>\n'
            for cell in header_row:
                table_html += f'      <th style="padding: 8px; text-align: left; border: 1px solid #ddd;">{cell}</th>\n'
            table_html += '    </tr>\n  </thead>\n'
            
            # Add data rows
            if data_rows:
                table_html += '  <tbody>\n'
                for i, row in enumerate(data_rows):
                    bg_color = "#f9f9f9" if i % 2 == 0 else "#ffffff"
                    table_html += f'    <tr style="background-color: {bg_color};">\n'
                    for cell in row:
                        table_html += f'      <td style="padding: 8px; border: 1px solid #ddd;">{cell}</td>\n'
                    table_html += '    </tr>\n'
                table_html += '  </tbody>\n'
            
            table_html += '</table>'
        else:
            table_html = "<p>No data to display</p>"
            
        # Simple HTML structure that GitHub can handle
        html_content = f'''<!DOCTYPE html>
<html>
<head>
    <title>{basename}</title>
</head>
<body>
    <h1>Trading Data: {basename.replace('_', ' ')}</h1>
    <p><em>Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</em></p>
    {table_html}
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
        convert_tsv_to_github_html(file)

print("Conversion complete!")