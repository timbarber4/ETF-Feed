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
        
        # Find header row
        data_start_index = 0
        header_row = None
        
        for i, row in enumerate(all_rows):
            if len(row) > 0 and any(keyword in row[0].lower() for keyword in ['date', 'time', 'datetime']):
                data_start_index = i
                header_row = row
                break
        
        if header_row is None:
            for i, row in enumerate(all_rows):
                if len([cell for cell in row if cell.strip()]) > 3:
                    data_start_index = i
                    header_row = row
                    break
        
        if header_row is None:
            print(f"Could not find proper header row in {tsv_file}")
            return False
        
        # Clean up headers
        clean_header = []
        keep_columns = []
        
        for i, header_cell in enumerate(header_row):
            if header_cell.strip() and not header_cell.strip() in ['K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']:
                clean_header_text = header_cell
                replacements = ['[ID0.SG1]', '[ID0.SG2]', '[ID0.SG3]', '[ID0.SG4]', '[ID0.SG5]', '[ID0.SG6]', 
                               '[ID1.SG1]', '[ID1.SG2]', '[ID1.SG3]', '[ID1.SG4]', '[ID1.SG5]', '[ID1.SG6]', 
                               '[ID1.SG7]', '[ID1.SG8]', '[ID1.SG9]', '[ID2.SG1]', '[ID3.SG1]', '[ID4.SG1]', 
                               '[ID5.SG1]', '[ID6.SG1]']
                
                for replacement in replacements:
                    clean_header_text = clean_header_text.replace(replacement, '')
                
                clean_header_text = clean_header_text.strip()
                if clean_header_text:
                    clean_header.append(html.escape(clean_header_text))
                    keep_columns.append(i)
        
        # Process data rows
        data_rows = all_rows[data_start_index + 1:]
        clean_data_rows = []
        
        for row in data_rows:
            if len(row) > 0 and row[0].strip():
                clean_row = []
                for col_index in keep_columns:
                    if col_index < len(row):
                        clean_row.append(html.escape(row[col_index].strip()))
                    else:
                        clean_row.append("")
                
                if any(cell.strip() for cell in clean_row):
                    clean_data_rows.append(clean_row)
        
        # Build HTML
        if clean_header and clean_data_rows:
            table_html = '<table border="1" cellpadding="8" cellspacing="0" style="border-collapse: collapse; width: 100%; font-family: monospace; font-size: 12px;">\n'
            
            table_html += '  <thead>\n    <tr style="background-color: #2c3e50; color: white;">\n'
            for header in clean_header:
                table_html += f'      <th style="padding: 10px; text-align: left; border: 1px solid #34495e; font-weight: bold;">{header}</th>\n'
            table_html += '    </tr>\n  </thead>\n'
            
            table_html += '  <tbody>\n'
            for i, row in enumerate(clean_data_rows):
                bg_color = "#ecf0f1" if i % 2 == 0 else "#ffffff"
                table_html += f'    <tr style="background-color: {bg_color};">\n'
                for cell in row:
                    align = "right" if cell.replace('.', '').replace('-', '').replace(',', '').isdigit() else "left"
                    table_html += f'      <td style="padding: 8px; border: 1px solid #bdc3c7; text-align: {align};">{cell}</td>\n'
                table_html += '    </tr>\n'
            table_html += '  </tbody>\n'
            table_html += '</table>'
        else:
            table_html = "<p>No valid data found to display</p>"
        
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
        
        return True
        
    except Exception as e:
        print(f"❌ Error converting {tsv_file}: {e}")
        return False

def monitor_and_convert():
    """Continuously monitor TSV files and convert when they change"""
    print("🚀 Starting TSV Monitor & Auto-Converter")
    print("Press Ctrl+C to stop")
    print("=" * 60)
    
    file_timestamps = {}
    
    try:
        while True:
            current_time = datetime.now().strftime('%H:%M:%S')
            
            # Find TSV files
            tsv_files = [f for f in os.listdir('.') if f.endswith('.tsv')]
            
            if not tsv_files:
                print(f"[{current_time}] ⚠️  No TSV files found")
                time.sleep(30)
                continue
            
            files_converted = 0
            
            for tsv_file in tsv_files:
                try:
                    # Get current modification time
                    current_mod_time = os.path.getmtime(tsv_file)
                    
                    # Check if file has been updated
                    if tsv_file not in file_timestamps or file_timestamps[tsv_file] < current_mod_time:
                        print(f"[{current_time}] 🔄 {tsv_file} updated, converting...")
                        
                        if convert_tsv_to_clean_html(tsv_file):
                            file_timestamps[tsv_file] = current_mod_time
                            files_converted += 1
                        
                except Exception as e:
                    print(f"[{current_time}] ❌ Error with {tsv_file}: {e}")
            
            if files_converted > 0:
                print(f"[{current_time}] ✅ Converted {files_converted} files")
            else:
                print(f"[{current_time}] 💤 No updates needed")
            
            # Wait 1 minute before checking again
            time.sleep(60)
            
    except KeyboardInterrupt:
        print("\n👋 Stopping auto-converter...")

if __name__ == "__main__":
    # Option 1: Run once
    print("Choose mode:")
    print("1. Convert all TSV files once")
    print("2. Monitor and auto-convert continuously")
    
    choice = input("Enter 1 or 2: ").strip()
    
    if choice == "2":
        monitor_and_convert()
    else:
        # Convert all files once
        tsv_files = [f for f in os.listdir('.') if f.endswith('.tsv')]
        
        if not tsv_files:
            print("❌ No TSV files found!")
        else:
            print(f"📄 Converting {len(tsv_files)} TSV files...")
            
            for tsv_file in tsv_files:
                convert_tsv_to_clean_html(tsv_file)
            
            print("🎉 Conversion complete!")