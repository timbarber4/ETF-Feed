import os
import html
import time
from datetime import datetime

def convert_tsv_to_clean_html(tsv_file):
    try:
        basename = tsv_file.replace('.tsv', '')
        html_file = f"{basename}.html"
        
        print(f"  📖 Reading {tsv_file}...")
        
        # Read the TSV file with multiple encoding attempts
        content = None
        encodings = ['utf-8', 'utf-8-sig', 'cp1252', 'iso-8859-1']
        
        for encoding in encodings:
            try:
                with open(tsv_file, 'r', encoding=encoding) as f:
                    content = f.read().strip()
                print(f"  ✅ Successfully read with {encoding} encoding")
                break
            except UnicodeDecodeError:
                continue
        
        if not content:
            print(f"  ❌ Could not read {tsv_file} with any encoding")
            return False
        
        # Split into lines and handle empty lines
        lines = [line for line in content.split('\n') if line.strip()]
        print(f"  📊 Found {len(lines)} lines of data")
        
        if not lines:
            print(f"  ⚠️  No data found in {tsv_file}")
            return False
        
        # Parse TSV data
        all_rows = []
        for line in lines:
            cells = [cell.strip() for cell in line.split('\t')]
            all_rows.append(cells)
        
        if not all_rows:
            print(f"  ⚠️  No data to convert in {tsv_file}")
            return False
        
        # Find the maximum number of columns
        max_cols = max(len(row) for row in all_rows)
        print(f"  📋 Maximum columns: {max_cols}")
        
        # Identify which columns to keep (remove empty middle columns)
        columns_to_keep = []
        
        for col_index in range(max_cols):
            # Check if this column has any meaningful data across all rows
            has_meaningful_data = False
            
            for row in all_rows:
                if col_index < len(row):
                    cell_content = row[col_index].strip()
                    # Keep column if it has meaningful content
                    if cell_content and not (len(cell_content) == 1 and cell_content.isalpha() and cell_content.isupper()):
                        # Also skip completely empty cells
                        if cell_content:
                            has_meaningful_data = True
                            break
            
            if has_meaningful_data:
                columns_to_keep.append(col_index)
        
        print(f"  🎯 Keeping columns: {columns_to_keep} (removed {max_cols - len(columns_to_keep)} empty columns)")
        
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
        
        print(f"  📅 Data starts at row: {data_start_index}")
        
        # Build HTML table
        table_html = '<table border="1" cellpadding="6" cellspacing="0" style="border-collapse: collapse; width: 100%; font-family: monospace; font-size: 11px;">\n'
        
        for row_index, row in enumerate(filtered_rows):
            # Determine row styling
            if data_start_index is not None and row_index < data_start_index:
                # Header/metadata rows
                row_style = 'background-color: #2c3e50; color: white; font-weight: bold;'
                cell_style = 'padding: 12px; border: 2px solid #34495e; text-align: center; font-size: 13px;'
                cell_tag = 'th'
            elif data_start_index is not None and row_index == data_start_index:
                # Column headers
                row_style = 'background-color: #3498db; color: white; font-weight: bold;'
                cell_style = 'padding: 10px; border: 2px solid #2980b9; text-align: left; font-size: 12px;'
                cell_tag = 'th'
            else:
                # Data rows
                if (row_index - (data_start_index or 0)) % 2 == 0:
                    row_style = 'background-color: #f8f9fa;'
                else:
                    row_style = 'background-color: #ffffff;'
                cell_style = 'padding: 8px; border: 1px solid #6c757d;'
                cell_tag = 'td'
            
            table_html += f'  <tr style="{row_style}">\n'
            
            # Add all cells in the row
            for col_index, cell_content in enumerate(row):
                # For data rows, right-align numbers
                if cell_tag == 'td' and col_index > 0:
                    is_number = cell_content.replace('.', '').replace('-', '').replace(',', '').replace(':', '').isdigit()
                    align = 'right' if is_number else 'left'
                    final_cell_style = f'{cell_style} text-align: {align};'
                else:
                    final_cell_style = cell_style
                
                table_html += f'    <{cell_tag} style="{final_cell_style}">{cell_content}</{cell_tag}>\n'
            
            table_html += '  </tr>\n'
        
        table_html += '</table>'
        
        # Create HTML with 30-second auto-refresh
        html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="refresh" content="30">
    <title>{basename} - Auto-Refresh</title>
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
            margin-bottom: 15px; 
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
            box-shadow: 0 3px 6px rgba(0,0,0,0.1);
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
            🔄 Page auto-refreshes every 30 seconds | 📊 {len(filtered_rows)} rows | 📋 {len(columns_to_keep)} columns
        </div>
        
        {table_html}
    </div>
</body>
</html>'''
        
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"  ✅ Created {html_file}")
        return True
        
    except Exception as e:
        print(f"  ❌ Error converting {tsv_file}: {e}")
        import traceback
        traceback.print_exc()
        return False

def monitor_files_with_timestamps():
    """Monitor files and track when they were last modified"""
    print("🚀 Starting Enhanced Sierra Chart Monitor")
    print("=" * 60)
    
    file_timestamps = {}
    conversion_count = 0
    
    while True:
        try:
            current_time = datetime.now()
            time_str = current_time.strftime('%H:%M:%S')
            
            # Find all TSV files
            tsv_files = [f for f in os.listdir('.') if f.endswith('.tsv')]
            
            if not tsv_files:
                print(f"[{time_str}] ⚠️  No TSV files found in directory")
                time.sleep(30)
                continue
            
            files_processed = 0
            files_updated = 0
            
            for tsv_file in tsv_files:
                try:
                    # Get file modification time
                    mod_time = os.path.getmtime(tsv_file)
                    mod_datetime = datetime.fromtimestamp(mod_time)
                    
                    # Check if file was modified since last check
                    if tsv_file not in file_timestamps or file_timestamps[tsv_file] < mod_time:
                        print(f"[{time_str}] 🔄 {tsv_file} updated at {mod_datetime.strftime('%H:%M:%S')}")
                        
                        if convert_tsv_to_clean_html(tsv_file):
                            file_timestamps[tsv_file] = mod_time
                            files_updated += 1
                            conversion_count += 1
                    
                    files_processed += 1
                    
                except Exception as e:
                    print(f"[{time_str}] ❌ Error processing {tsv_file}: {e}")
            
            if files_updated > 0:
                print(f"[{time_str}] ✅ Updated {files_updated}/{files_processed} files (Total conversions: {conversion_count})")
            else:
                print(f"[{time_str}] 💤 {files_processed} files checked, no updates needed")
            
            # Wait 30 seconds
            print(f"[{time_str}] ⏰ Waiting 30 seconds for next check...")
            time.sleep(30)
            
        except KeyboardInterrupt:
            print(f"\n👋 Stopping monitor after {conversion_count} total conversions...")
            break
        except Exception as e:
            print(f"[{time_str}] ❌ Monitor error: {e}")
            time.sleep(30)

if __name__ == "__main__":
    print("🎯 Sierra Chart TSV Auto-Converter")
    print("Choose mode:")
    print("1. Convert all files once")
    print("2. Monitor and auto-convert every 30 seconds")
    print("3. Show file status (debug)")
    
    choice = input("Enter 1, 2, or 3: ").strip()
    
    if choice == "2":
        monitor_files_with_timestamps()
    elif choice == "3":
        # Debug mode - show file info
        tsv_files = [f for f in os.listdir('.') if f.endswith('.tsv')]
        print(f"\n📋 Found {len(tsv_files)} TSV files:")
        for f in tsv_files:
            stat = os.stat(f)
            mod_time = datetime.fromtimestamp(stat.st_mtime)
            print(f"  • {f} - Modified: {mod_time} - Size: {stat.st_size:,} bytes")
    else:
        # Convert once
        tsv_files = [f for f in os.listdir('.') if f.endswith('.tsv')]
        
        if not tsv_files:
            print("❌ No TSV files found!")
        else:
            print(f"📄 Converting {len(tsv_files)} TSV files...")
            
            for tsv_file in tsv_files:
                print(f"\n📊 Processing: {tsv_file}")
                convert_tsv_to_clean_html(tsv_file)
            
            print("🎉 Conversion complete!")