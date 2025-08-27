import os
import html
from datetime import datetime

def convert_tsv_to_clean_html(tsv_file):
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
        all_rows = []
        for line in lines:
            # Split by tabs
            cells = [cell.strip() for cell in line.split('\t')]
            all_rows.append(cells)
        
        if not all_rows:
            print(f"No data to convert in {tsv_file}")
            return
        
        # Find the actual data rows - skip metadata rows
        data_start_index = 0
        header_row = None
        
        # Look for a row that starts with "Date Time" or similar
        for i, row in enumerate(all_rows):
            if len(row) > 0 and any(keyword in row[0].lower() for keyword in ['date', 'time', 'datetime']):
                data_start_index = i
                header_row = row
                break
        
        # If no proper header found, use the first row that has substantial data
        if header_row is None:
            for i, row in enumerate(all_rows):
                if len([cell for cell in row if cell.strip()]) > 3:  # At least 4 non-empty columns
                    data_start_index = i
                    header_row = row
                    break
        
        if header_row is None:
            print(f"Could not find proper header row in {tsv_file}")
            return
        
        # Clean up header - remove empty columns and their data
        clean_header = []
        keep_columns = []
        
        for i, header_cell in enumerate(header_row):
            # Keep column if header has meaningful content
            if header_cell.strip() and not header_cell.strip() in ['K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']:
                # Clean up the header text
                clean_header_text = header_cell.replace('[ID0.SG1]', '').replace('[ID0.SG2]', '').replace('[ID0.SG3]', '').replace('[ID0.SG4]', '').replace('[ID0.SG5]', '').replace('[ID0.SG6]', '').replace('[ID1.SG1]', '').replace('[ID1.SG2]', '').replace('[ID1.SG3]', '').replace('[ID1.SG4]', '').replace('[ID1.SG5]', '').replace('[ID1.SG6]', '').replace('[ID1.SG7]', '').replace('[ID1.SG8]', '').replace('[ID1.SG9]', '')
                clean_header_text = clean_header_text.strip()
                if clean_header_text:
                    clean_header.append(html.escape(clean_header_text))
                    keep_columns.append(i)
        
        # Get data rows (skip header)
        data_rows = all_rows[data_start_index + 1:]
        
        # Clean data rows - keep only the columns we're keeping
        clean_data_rows = []
        for row in data_rows:
            if len(row) > 0 and row[0].strip():  # Skip empty rows
                clean_row = []
                for col_index in keep_columns:
                    if col_index < len(row):
                        clean_row.append(html.escape(row[col_index].strip()))
                    else:
                        clean_row.append("")
                
                # Only add row if it has some actual data
                if any(cell.strip() for cell in clean_row):
                    clean_data_rows.append(clean_row)
        
        # Build HTML table
        if clean_header and clean_data_rows:
            table_html = '<table border="1" cellpadding="8" cellspacing="0" style="border-collapse: collapse; width: 100%; font-family: monospace; font-size: 12px;">\n'
            
            # Add header
            table_html += '  <thead>\n    <tr style="background-color: #2c3e50; color: white;">\n'
            for header in clean_header:
                table_html += f'      <th style="padding: 10px; text-align: left; border: 1px solid #34495e; font-weight: bold;">{header}</th>\n'
            table_html += '    </tr>\n  </thead>\n'
            
            # Add data rows
            table_html += '  <tbody>\n'
            for i, row in enumerate(clean_data_rows):
                bg_color = "#ecf0f1" if i % 2 == 0 else "#ffffff"
                table_html += f'    <tr style="background-color: {bg_color};">\n'
                for j, cell in enumerate(row):
                    # Right-align numeric data
                    align = "right" if cell.replace('.', '').replace('-', '').replace(',', '').isdigit() else "left"
                    table_html += f'      <td style="padding: 8px; border: 1px solid #bdc3c7; text-align: {align};">{cell}</td>\n'
                table_html += '    </tr>\n'
            table_html += '  </tbody>\n'
            
            table_html += '</table>'
        else:
            table_html = "<p>No valid data found to display</p>"
        
        # Create clean HTML
        html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{basename}</title>
    <style>
        body {{ 
            font-family: 'Segoe UI', Arial, sans-serif; 
            margin: 20px; 
            background: #f8f9fa; 
            color: #2c3e50;
        }}
        .container {{ 
            background: white; 
            padding: 30px; 
            border-radius: 10px; 
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            max-width: 100%;
            overflow-x: auto;
        }}
        h1 {{ 
            color: #2c3e50; 
            margin-bottom: 10px;
            font-size: 24px;
        }}
        .timestamp {{ 
            color: #7f8c8d; 
            margin-bottom: 25px; 
            font-size: 14px;
            font-style: italic;
        }}
        table {{ 
            min-width: 100%;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Trading Data: {basename.replace('_', ' ').replace('&', ' & ')}</h1>
        <div class="timestamp">📅 Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
        {table_html}
    </div>
</body>
</html>'''
        
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Converted {tsv_file} to {html_file}")
        print(f"   📋 Columns: {len(clean_header)}")
        print(f"   📊 Data rows: {len(clean_data_rows)}")
        
    except Exception as e:
        print(f"❌ Error converting {tsv_file}: {e}")

# Convert all TSV files in current directory
converted_count = 0
for file in os.listdir('.'):
    if file.endswith('.tsv'):
        convert_tsv_to_clean_html(file)
        converted_count += 1

print(f"\n🎉 Conversion complete! Processed {converted_count} files.")