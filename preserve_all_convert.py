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
        
        # Parse ALL TSV data - don't remove anything
        all_rows = []
        for line in lines:
            # Split by tabs and escape HTML but keep everything
            cells = [html.escape(cell) for cell in line.split('\t')]
            all_rows.append(cells)
        
        if not all_rows:
            print(f"No data to convert in {tsv_file}")
            return
        
        # Find where the actual tabular data starts (rows with "Date Time")
        data_start_index = None
        for i, row in enumerate(all_rows):
            if len(row) > 0 and any(keyword in row[0].lower() for keyword in ['date', 'time', 'datetime']):
                data_start_index = i
                break
        
        # Build HTML table with ALL data preserved
        table_html = '<table border="1" cellpadding="6" cellspacing="0" style="border-collapse: collapse; width: 100%; font-family: monospace; font-size: 11px;">\n'
        
        for row_index, row in enumerate(all_rows):
            # Determine row styling based on content
            if data_start_index is not None and row_index < data_start_index:
                # Header/metadata rows - special styling
                row_style = 'background-color: #34495e; color: white; font-weight: bold;'
                cell_style = 'padding: 12px; border: 1px solid #2c3e50; text-align: center;'
            elif data_start_index is not None and row_index == data_start_index:
                # Column headers - distinctive styling
                row_style = 'background-color: #3498db; color: white; font-weight: bold;'
                cell_style = 'padding: 10px; border: 1px solid #2980b9; text-align: left; font-size: 12px;'
            else:
                # Data rows - alternating colors
                if (row_index - (data_start_index or 0)) % 2 == 0:
                    row_style = 'background-color: #ecf0f1;'
                else:
                    row_style = 'background-color: #ffffff;'
                cell_style = 'padding: 8px; border: 1px solid #bdc3c7;'
            
            table_html += f'  <tr style="{row_style}">\n'
            
            # Add all cells in the row
            max_cols = max(len(r) for r in all_rows)  # Ensure consistent column count
            
            for col_index in range(max_cols):
                if col_index < len(row):
                    cell_content = row[col_index] if row[col_index] else ''
                else:
                    cell_content = ''
                
                # Determine alignment for data rows
                if data_start_index is not None and row_index > data_start_index:
                    # For data rows, right-align numbers
                    is_number = cell_content.replace('.', '').replace('-', '').replace(',', '').replace(':', '').isdigit()
                    align = 'right' if is_number and col_index > 0 else 'left'  # Keep first column (dates) left-aligned
                    final_cell_style = f'{cell_style} text-align: {align};'
                else:
                    final_cell_style = cell_style
                
                # Use th for header rows, td for data
                tag = 'th' if (data_start_index is None or row_index <= data_start_index) else 'td'
                table_html += f'    <{tag} style="{final_cell_style}">{cell_content}</{tag}>\n'
            
            table_html += '  </tr>\n'
        
        table_html += '</table>'
        
        # Create HTML with enhanced styling but all data preserved
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
            margin-top: 10px;
        }}
        tr:hover td {{
            background-color: #d5dbdb !important;
        }}
        .data-note {{
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            border-radius: 5px;
            padding: 10px;
            margin: 15px 0;
            font-size: 12px;
            color: #856404;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Sierra Chart Data: {basename.replace('_', ' ').replace('&', ' & ')}</h1>
        <div class="timestamp">📅 Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
        
        <div class="data-note">
            <strong>📋 Complete Data Export:</strong> All original Sierra Chart data preserved with enhanced formatting for readability.
        </div>
        
        {table_html}
    </div>
</body>
</html>'''
        
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Converted {tsv_file} to {html_file}")
        print(f"   📊 Total rows: {len(all_rows)}")
        print(f"   📋 Max columns: {max(len(r) for r in all_rows)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error converting {tsv_file}: {e}")
        return False

# Convert all TSV files in current directory
def main():
    print("🔄 Converting TSV files with ALL data preserved...")
    
    tsv_files = [f for f in os.listdir('.') if f.endswith('.tsv')]
    
    if not tsv_files:
        print("❌ No TSV files found!")
        return
    
    converted_count = 0
    for tsv_file in tsv_files:
        print(f"\n📊 Processing: {tsv_file}")
        if convert_tsv_to_clean_html(tsv_file):
            converted_count += 1
    
    print(f"\n🎉 Conversion complete! Processed {converted_count} files with ALL data preserved!")

if __name__ == "__main__":
    main()