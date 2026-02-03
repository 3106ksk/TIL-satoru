import csv
import os
import sys
import glob
from datetime import datetime

# Configuration
EXPORT_DIR = '/Users/310tea/Documents/学習アウトプット/notion_exports'
WEEKLY_DIR = '/Users/310tea/Documents/学習アウトプット/weekly'

def find_latest_csv():
    # Find files matching "Weekly Review*.csv"
    pattern = os.path.join(EXPORT_DIR, "Weekly Review*.csv")
    files = glob.glob(pattern)
    if not files:
        return None
    # Sort by modification time, newest first
    files.sort(key=os.path.getmtime, reverse=True)
    return files[0]

def parse_csv_and_convert(csv_path):
    print(f"Processing file: {csv_path}")
    
    target_row = None
    today = datetime.now()
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            
        print(f"Found {len(rows)} rows in CSV.")
        
        # 1. Identify the target week (Row containing Today)
        for row in rows:
            start_str = row.get('Start')
            end_str = row.get('End')
            
            if not start_str or not end_str:
                continue
                
            try:
                # Handle connection strings or partial formats if necessary
                # Format seen: "January 26, 2026"
                start_date = datetime.strptime(start_str, '%B %d, %Y')
                end_date = datetime.strptime(end_str, '%B %d, %Y').replace(hour=23, minute=59, second=59)
                
                print(f"Checking row: {row.get('Week')} ({start_str} - {end_str})")
                
                if start_date <= today <= end_date:
                    target_row = row
                    print(f"Match found! This is the current week.")
                    break
            except ValueError as e:
                print(f"Date parse error: {e}")
                continue
        
        # Fallback: If no "current week" found (e.g. running on Monday for last week),
        # use the most recent week in the CSV (Row 0 usually).
        # OR ask the user? For "One word" automation, let's pick the latest if reasonable.
        if not target_row and rows:
            print("Current week not found in CSV dates. Selecting the latest entry.")
            target_row = rows[0]

        if not target_row:
            print("No valid data found.")
            return

        # 2. Extract Data
        week_label = target_row.get('Week', 'Unknown')
        start_date_str = target_row.get('Start')
        end_date_str = target_row.get('End')
        
        # Parse dates for filename (YYYY-MM-DD)
        # We need strict formatting for the filename
        try:
            s_dt = datetime.strptime(start_date_str, '%B %d, %Y')
            e_dt = datetime.strptime(end_date_str, '%B %d, %Y')
            filename_date_part = f"{s_dt.strftime('%Y-%m-%d')}_to_{e_dt.strftime('%Y-%m-%d')}"
        except:
            # Fallback if date parsing fails again (unlikely if we got here)
            filename_date_part = week_label.replace('-', '_')

        output_filename = f"weekly_{filename_date_part}.md"
        output_path = os.path.join(WEEKLY_DIR, output_filename)
        
        # 3. Generate Markdown
        md = f"# Weekly Review: {week_label}\n\n"
        md += f"**Period**: {start_date_str} - {end_date_str}\n\n"
        
        # Metrics
        md += "## Metrics\n"
        metrics = [
            'Total Min', 'Deep Work Min', 'Avg Deep Score', 
            'Budget Sum', 'Budget Adherence', 
            'Interview Total Min', 'Interview Prep Min', 'Interview Min', 'WrapUp Min'
        ]
        
        md += "| Metric | Value |\n| --- | --- |\n"
        for m in metrics:
            val = target_row.get(m, '')
            if val:
                md += f"| {m} | {val} |\n"
        md += "\n"

        # Text Sections
        text_fields = [
            'WIns', 'Friction Pattern', 'Principle', 'Keep', 'Stop', 'Next', 
            'Seed運用', 'Daily Reviews', 'Technical Interviews'
        ]
        
        for field in text_fields:
            val = target_row.get(field, '').strip()
            if val:
                md += f"## {field}\n{val}\n\n"

        # 4. Write File
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(md)
        print(f"Created: {output_path}")
        
        # 5. Cleanup
        os.remove(csv_path)
        print(f"Deleted original CSV: {csv_path}")
        
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    csv_file = find_latest_csv()
    if csv_file:
        parse_csv_and_convert(csv_file)
    else:
        print("No 'Weekly Review' CSV file found in export directory.")
