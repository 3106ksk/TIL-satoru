import csv
import sys
import os
import argparse
from datetime import datetime

def process_session_export(input_path, start_date_str, end_date_str, output_dir):
    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        
        # Determine output filename
        output_filename = f"Sessions_DB_{start_date_str}_to_{end_date_str}.md"
        output_path = os.path.join(output_dir, output_filename)
        
        # Read and Filter
        rows = []
        header = None
        
        print(f"Reading from: {input_path}")
        
        with open(input_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            try:
                header = next(reader)
            except StopIteration:
                print("Error: Empty CSV file")
                sys.exit(1)
            
            # Find Date column
            date_col_idx = -1
            for i, col in enumerate(header):
                if col.strip() == 'Date':
                    date_col_idx = i
                    break
            
            if date_col_idx == -1:
                print("Error: 'Date' column not found in CSV")
                sys.exit(1)

            # Filter rows
            for row in reader:
                if len(row) <= date_col_idx:
                    continue
                date_str = row[date_col_idx]
                try:
                    row_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                    if start_date <= row_date <= end_date:
                        rows.append(row)
                except ValueError:
                    continue
        
        print(f"Filtered {len(rows)} rows between {start_date_str} and {end_date_str}")
        
        # Convert to Markdown
        md_lines = []
        
        # Header
        cleaned_header = [col.replace('|', '\\|').replace('\n', '<br>') for col in header]
        md_lines.append('| ' + ' | '.join(cleaned_header) + ' |')
        md_lines.append('| ' + ' | '.join(['---'] * len(header)) + ' |')
        
        # Rows
        for row in rows:
            cleaned_row = []
            for cell in row:
                cell_content = cell.replace('|', '\\|').replace('\n', '<br>')
                cleaned_row.append(cell_content)
            md_lines.append('| ' + ' | '.join(cleaned_row) + ' |')
            
        # Write to file
        os.makedirs(output_dir, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(md_lines))
            
        print(f"Successfully created: {output_path}")
        return output_path

    except Exception as e:
        print(f"Error processing file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process Notion Sessions DB Export')
    parser.add_argument('input_csv', help='Path to the input CSV file')
    parser.add_argument('start_date', help='Start date (YYYY-MM-DD)')
    parser.add_argument('end_date', help='End date (YYYY-MM-DD)')
    parser.add_argument('output_dir', help='Directory to save the output Markdown file')
    
    args = parser.parse_args()
    
    process_session_export(args.input_csv, args.start_date, args.end_date, args.output_dir)
