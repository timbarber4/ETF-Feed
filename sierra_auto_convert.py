import os
import html
import time
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
            return False
        
        # Parse TSV data
        all_rows = []
        for line in lines:
            cells = [cell.strip() for cell in line.split('\t')]
            all_rows.append(cells)
        
        if not all_rows:
            print(f"No data to convert in {tsv_file}")
            return False
        
        # Find the maximum number of columns
        max_cols = max(len(row) for row in all_rows)
        
        # Identify which columns to keep (remove empty middle columns)
        columns_to_keep = []
        
        for col_index in range(max_cols):
            # Check if this column has any meaningful data
            has_data = False
            
            for row in all_rows:
                if col_index < len(row):
                    cell_content = row[col_index].strip()
                    # Keep column if it has meaningful content (not just single letters or empty)
                    if cell_content and not (len(cell_content) == 1 and cell_content.isalpha() and cell_content.isupper()):
                        has_data = True
                        break
            
            if has_data:
                columns_to_keep.append(col_index)
        
        # Filter all rows to keep only the meaningful columns
        filtered_rows = []
        for row in all_rows:
            filtered_row = []
            for col_index in columns_to_keep:
                if col_index < len(row):
                    filtered_row.append(html.escape(row[col_index]))
                else:
                    filtered_row.append('')
            filtered_rows.append(filtered_row)
        
        # Find where the actual tabular data starts
        data_start_index = None
        for i, row in enumerate(filtered_rows):
            if len(row) > 0 and any(keyword in row[0].lower() for keyword in ['date', 'time', 'datetime']):
                data_start_index = i
                break
        
        # Build HTML table with all preserved data
        table_html = '<table border="1" cellpadding="6" cellspacing="0" style="border-collapse: collapse; width: 100%; font-family: monospace; font-size: 11px;">\n'
        
        for row_index, row in enumerate(filtered_rows):
            # Determine row styling
            if data_start_index is not None and row_index < data_start_index:
                # Header/metadata rows - special styling
                row_style = 'background-color: #34495e; color: white; font-weight: bold;'
                cell_style = 'padding: 12px; border: 2px solid #2c3e50; text-align: center;'
                cell_tag = 'th'
            elif data_start_index is not None and row_index == data_start_index:
                # Column headers - distinctive styling
                row_style = 'background-color: #3498db; color: white; font-weight: bold;'
                cell_style = 'padding: 10px; border: 2px solid #2980b9; text-align: left; font-size: 12px;'
                cell_tag = 'th'
            else:
                # Data rows - alternating colors with stronger lines
                if (row_index - (data_start_index or 0)) % 2 == 0:
                    row_style = 'background-color: #f8f9fa;'
                else:
                    row_style = 'background-color: #ffffff;'
                cell_style = 'padding: 8px; border: 1px solid #6c757d;'
                cell_tag = 'td'
            
            table_html += f'  <tr style="{row_style}">\n'
            
            # Add all cells in the filtered row
            for col_index, cell_content in enumerate(row):
                # For data rows, right-align numbers
                if cell_tag == 'td' and col_index > 0:  # Skip first column (dates)
                    is_number = cell_content.replace('.', '').replace('-', '').replace(',', '').isdigit()
                    align = 'right' if is_number else 'left'
                    final_cell_style = f'{cell_style} text-align: {align};'
                else:
                    final_cell_style = cell_style
                
                table_html += f'    <{cell_tag} style="{final_cell_style}">{cell_content}</{cell_tag}>\n'
            
            table_html += '  </tr>\n'
        
        table_html += '</table>'
        
        # Create HTML with auto-refresh every 30 seconds
        html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="refresh" content="30">
    <title>{basename}</title>
    <style>
        body {{ 
            font-family: 'Segoe UI', Arial, sans-serif; 
            margin: 15px; 
            background: #f8f9fa; 
            color: #2c3e50;
        }}
        .container {{ 
            background: white; 
            padding: 25px; 
            border-radius: 10px; 
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            max-width: 100%;
            overflow-x: auto;
        }}
        h1 {{ 
            color: #2c3e50; 
            margin-bottom: 8px;
            font-size: 22px;
            text-align: center;
        }}
        .timestamp {{ 
            color: #7f8c8d; 
            margin-bottom: 20px; 
            font-size: 14px;
            font-style: italic;
            text-align: center;
        }}
        .auto-refresh {{
            background: #d4edda;
            border: 1px solid #c3e6cb;
            border-radius: 5px;
            padding: 8px;
            margin: 15px 0;
            text-align: center;
            font-size: 12px;
            color: #155724;
        }}
        table {{ 
            width: 100%;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-top: 15px;
        }}
        tr:hover td {{
            background-color: #e3f2fd !important;
            transition: background-color 0.2s;
        }}
        th {{
            font-weight: bold !important;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 {basename.replace('_', ' ').replace('&', ' & ')}</h1>
        <div class="timestamp">📅 Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
        
        <div class="auto-refresh">
            🔄 Auto-refreshes every 30 seconds | 📊 Empty columns removed for clarity
        </div>
        
        {table_html}
    </div>
</body>
</html>'''
        
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return True
        
    except Exception as e:
        print(f"❌ Error converting {tsv_file}: {e}")
        return False

def monitor_and_convert():
    """Continuously monitor and convert TSV files every 30 seconds"""
    print("🚀 Starting Sierra Chart Auto-Converter")
    print("🔄 Updates every 30 seconds")
    print("📊 Removes empty middle columns")
    print("Press Ctrl+C to stop")
    print("=" * 60)
    
    while True:
        try:
            current_time = datetime.now().strftime('%H:%M:%S')
            
            # Find all TSV files
            tsv_files = [f for f in os.listdir('.') if f.endswith('.tsv')]
            
            if not tsv_files:
                print(f"[{current_time}] ⚠️  No TSV files found")
            else:
                converted_count = 0
                
                for tsv_file in tsv_files:
                    if convert_tsv_to_clean_html(tsv_file):
                        converted_count += 1
                
                if converted_count > 0:
                    print(f"[{current_time}] ✅ Updated {converted_count} HTML files")
                else:
                    print(f"[{current_time}] 💤 No conversions needed")
            
            # Wait 30 seconds
            time.sleep(30)
            
        except KeyboardInterrupt:
            print("\n👋 Stopping auto-converter...")
            break
        except Exception as e:
            print(f"[{current_time}] ❌ Error: {e}")
            time.sleep(30)

def convert_once():
    """Convert all TSV files once"""
    tsv_files = [f for f in os.listdir('.') if f.endswith('.tsv')]
    
    if not tsv_files:
        print("❌ No TSV files found!")
        return
    
    print(f"📄 Converting {len(tsv_files)} TSV files...")
    
    for tsv_file in tsv_files:
        print(f"📊 Processing: {tsv_file}")
        convert_tsv_to_clean_html(tsv_file)
    
    print("🎉 One-time conversion complete!")

if __name__ == "__main__":
    print("Choose conversion mode:")
    print("1. Convert once (immediate)")
    print("2. Auto-update every 30 seconds (continuous)")
    
    choice = input("Enter 1 or 2: ").strip()
    
    if choice == "2":
        monitor_and_convert()
    else:
        convert_once()