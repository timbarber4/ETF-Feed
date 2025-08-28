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
        
        # Extract important title information from first few rows
        title_info = []
        chart_info = ""
        formula_info = ""
        
        # Look for chart and indicator information in first few rows
        for i, row in enumerate(all_rows[:5]):  # Check first 5 rows for metadata
            if len(row) > 0:
                first_cell = row[0].strip()
                # Look for chart identification
                if any(indicator in first_cell for indicator in ['[ID0]', '[ID1]', 'SPY', 'Chart']):
                    if 'SPY' in first_cell or 'Chart' in first_cell:
                        chart_info = first_cell
                
                # Look for additional info in other cells
                for cell in row:
                    cell_content = cell.strip()
                    if cell_content and len(cell_content) > 5:  # Meaningful content
                        if any(keyword in cell_content for keyword in ['Formula', 'Sheet', 'Average', 'VWAP', 'Volume', 'Point of Control']):
                            if cell_content not in title_info and 'modify formulas' not in cell_content.lower():
                                title_info.append(cell_content)
        
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
        
        # Clean up header - preserve meaningful names but remove ID tags
        clean_header = []
        keep_columns = []
        
        for i, header_cell in enumerate(header_row):
            # Keep column if header has meaningful content
            if header_cell.strip() and not header_cell.strip() in ['K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']:
                # Clean up the header text but preserve important information
                clean_header_text = header_cell
                
                # Remove ID tags but preserve descriptive text
                id_replacements = ['[ID0.SG1]', '[ID0.SG2]', '[ID0.SG3]', '[ID0.SG4]', '[ID0.SG5]', '[ID0.SG6]', 
                                  '[ID1.SG1]', '[ID1.SG2]', '[ID1.SG3]', '[ID1.SG4]', '[ID1.SG5]', '[ID1.SG6]', 
                                  '[ID1.SG7]', '[ID1.SG8]', '[ID1.SG9]', '[ID2.SG1]', '[ID3.SG1]', '[ID4.SG1]', 
                                  '[ID5.SG1]', '[ID6.SG1]', '[ID7.SG1]', '[ID8.SG1]', '[ID9.SG1]']
                
                for replacement in id_replacements:
                    clean_header_text = clean_header_text.replace(replacement, '')
                
                # Clean up extra spaces but preserve meaningful text
                clean_header_text = ' '.join(clean_header_text.split())
                
                # If we removed everything, try to give it a meaningful name based on position
                if not clean_header_text:
                    if i < len(['Date Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Trades']):
                        standard_names = ['Date Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Trades']
                        clean_header_text = standard_names[i] if i < len(standard_names) else f"Column {i+1}"
                    else:
                        clean_header_text = f"Indicator {i-6}"  # Assuming first 7 are OHLCV data
                
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
        
        # Build title section with extracted info
        title_section = ""
        if chart_info or title_info:
            title_section = '<div class="chart-info">'
            if chart_info:
                title_section += f'<div class="chart-title">{html.escape(chart_info)}</div>'
            
            if title_info:
                for info in title_info[:3]:  # Limit to first 3 pieces of info
                    title_section += f'<div class="indicator-info">📈 {html.escape(info)}</div>'
            
            title_section += '</div>'
        
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
        
        # Create clean HTML with preserved titles
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
            margin-bottom: 15px; 
            font-size: 14px;
            font-style: italic;
        }}
        .chart-info {{
            background: #e8f4fd;
            border-left: 4px solid #3498db;
            padding: 15px;
            margin: 15px 0 25px 0;
            border-radius: 5px;
        }}
        .chart-title {{
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 8px;
            font-size: 16px;
        }}
        .indicator-info {{
            color: #34495e;
            margin: 5px 0;
            font-size: 14px;
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
        {title_section}
        {table_html}
    </div>
</body>
</html>'''
        
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Converted {tsv_file} to {html_file}")
        print(f"   📋 Columns: {len(clean_header)}")
        print(f"   📊 Data rows: {len(clean_data_rows)}")
        if chart_info:
            print(f"   📈 Chart: {chart_info}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error converting {tsv_file}: {e}")
        return False

def main():
    print("🔄 Converting TSV files with preserved titles...")
    
    # Find all TSV files
    tsv_files = [f for f in os.listdir('.') if f.endswith('.tsv')]
    
    if not tsv_files:
        print("❌ No TSV files found in current directory!")
        print(f"📁 Current directory: {os.getcwd()}")
        return
    
    print(f"📄 Found {len(tsv_files)} TSV files to convert")
    
    converted_count = 0
    for tsv_file in tsv_files:
        print(f"\n📊 Processing: {tsv_file}")
        
        if convert_tsv_to_clean_html(tsv_file):
            converted_count += 1
    
    print(f"\n🎉 Conversion complete! Successfully converted {converted_count}/{len(tsv_files)} files")

if __name__ == "__main__":
    main()