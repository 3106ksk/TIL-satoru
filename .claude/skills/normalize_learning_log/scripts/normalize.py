import csv
import json
import os
import glob
import re
import sys
from datetime import datetime, timedelta
from datetime import datetime, timedelta
import re # Ensure re is imported if not already, though likely imported above

# --- Configuration ---
BASE_DIR = '/Users/310tea/Documents/学習アウトプット'
EXPORT_DIR = os.path.join(BASE_DIR, 'notion_exports')
DAILY_DIR = os.path.join(BASE_DIR, 'daily')
WEEKLY_DIR = os.path.join(BASE_DIR, 'weekly')
OUTPUT_DIR = os.path.join(BASE_DIR, 'normalized_data')

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# --- Mappings ---
CATEGORY_MAP = {
    'Coding': ['👨‍💻 カリキュラム', 'Coding', 'Dev', 'Project', 'Implement', 'Create', 'Debug'],
    'Reading': ['📚 読書', 'Reading', 'Book', 'Input', 'Research'],
    'Interview': ['🗣 Interview', 'Interview', '面接練習', '対策', 'Output Practice', 'Mokumoku'],
    'Planning': ['📝 Planning', 'Planning', 'Log', 'Review', 'WrapUp', '🧠 計画・振り返り'],
    'Other': [] # Fallback
}

def normalize_category(raw_type):
    if not raw_type:
        return "Other"
    
    # Remove emoji? For matching, we keep it, but output clean.
    # Simple substring matching
    for cat, keywords in CATEGORY_MAP.items():
        for k in keywords:
            if k in raw_type:
                return cat
    return "Other" # Default

def parse_notion_date(date_str):
    """
    Parses Notion date string like 'January 26, 2026 6:41 PM (GMT+9)'
    Returns ISO 8601 string with timezone.
    """
    if not date_str:
        return None
    
    # Remove (GMT+9) or similar if present
    # Example: January 26, 2026 6:41 PM (GMT+9) -> January 26, 2026 6:41 PM
    clean_str = re.sub(r'\s*\(.*\)', '', date_str).strip()
    
    try:
        # Standard Notion export format: "Month DD, YYYY H:MM AM/PM"
        # e.g. "December 23, 2025 9:13 AM"
        dt = datetime.strptime(clean_str, '%B %d, %Y %I:%M %p')
        
        # Manually set to +09:00 representation (assuming JST from context)
        # Create a timezone-aware datetime or just format with timezone string
        # To match previous logic: T... +09:00
        dt_str = dt.strftime('%Y-%m-%dT%H:%M:%S+09:00')
        return dt_str

    except ValueError:
        # Try without AM/PM or other formats if needed, or just fail gracefully
        # Sometimes it might just be a date "YYYY-MM-DD"
        try:
             dt = datetime.strptime(clean_str, '%Y-%m-%d')
             dt_str = dt.strftime('%Y-%m-%dT00:00:00+09:00')
             return dt_str
        except ValueError:
             pass

        print(f"Date parse error for '{date_str}'")
        return None

def parse_daily_markdown(date_str):
    """
    Reads daily_YYYY-MM-DD.md and extracts Worked, Slipped, Insight, Strategy.
    Supports both old format (### Worked) and new format (## ■ Worked).
    Returns a dict with lists.
    """
    file_path = os.path.join(DAILY_DIR, f"daily_{date_str}.md")
    result = {
        "worked": [],
        "slipped": [],
        "insight": [],
        "strategy_for_next_day": [],
        "day_mode": "Unknown"
    }

    if not os.path.exists(file_path):
        return result

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        current_section = None
        for line in lines:
            stripped = line.strip()

            # Day Mode detection
            if "**Day Mode**" in stripped:
                if "Off" in stripped or "OFF" in stripped:
                    result["day_mode"] = "Off"
                elif "Shift" in stripped or "ON" in stripped:
                    result["day_mode"] = "Shift"

            # Section detection (new format: ## ■ X / old format: ### X)
            stripped_lower = stripped.lower()
            if "worked" in stripped_lower and ("## ■" in line or "### " in line or "**Worked**" in stripped):
                current_section = "worked"
                continue
            elif "slipped" in stripped_lower and ("## ■" in line or "### " in line or "**Slipped**" in stripped):
                current_section = "slipped"
                continue
            elif "strategy" in stripped_lower and ("## ■" in line or "### " in line):
                current_section = "strategy_for_next_day"
                continue
            elif "insight" in stripped_lower and ("## ■" in line or "### " in line or "**Insight**" in stripped):
                current_section = "insight"
                continue
            elif line.startswith("## ") or line.startswith("### "):
                current_section = None
                continue

            # Content extraction (bullet points)
            if current_section and (stripped.startswith("-") or stripped.startswith("・")):
                content = stripped.lstrip("-・ ").strip()
                content = re.sub(r'^\*{0,2}(事実|Fact|Why)\*{0,2}[:：]\s*', '', content)
                result[current_section].append(content)

    except Exception as e:
        print(f"Error parsing daily {date_str}: {e}")

    return result

def find_latest_sessions_csv():
    # Look for "Sessions DB*.csv" or similar
    # User might name it differently, but "Sessions DB" or just "*.csv" with "Type" column?
    # Let's stick to "Sessions DB*.csv" based on user history
    pattern = os.path.join(EXPORT_DIR, "Sessions DB*.csv")
    files = glob.glob(pattern)
    if not files:
        # Fallback: Just any CSV in export dir?
        # Maybe check for 'Type' and 'Deep Score' in headers
        return None
    
    files.sort(key=os.path.getmtime, reverse=True)
    return files[0]

def main():
    print("--- Starting Learning Log Normalization ---")
    
    # 1. Find CSV
    csv_path = find_latest_sessions_csv()
    if not csv_path:
        print(f"No 'Sessions DB*.csv' found in {EXPORT_DIR}")
        sys.exit(1)
        
    print(f"Reading: {csv_path}")
    
    sessions_by_date = {}
    all_dates = set()

    # Determine "This Week" (Monday to Sunday)
    today = datetime.now().date()
    # Python weekday: Mon=0, Sun=6
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    
    target_start_str = start_of_week.strftime('%Y-%m-%d')
    target_end_str = end_of_week.strftime('%Y-%m-%d')
    
    print(f"Targeting logic: Current Week ({target_start_str} to {target_end_str})")
    
    # 2. Parse CSV
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Extract Date (YYYY-MM-DD)
            date_val = row.get('Date', '')
            if not date_val:
                # Fallback to start time parsing
                st = parse_notion_date(row.get('start time', ''))
                if st:
                    date_val = st.split('T')[0]
            
            if not date_val:
                continue
            
            # FILTER: Only include dates within the target week
            if not (target_start_str <= date_val <= target_end_str):
                continue
                
            all_dates.add(date_val)
            
            if date_val not in sessions_by_date:
                sessions_by_date[date_val] = []
                
            # Normalize Session
            deep_score_str = row.get('Deep Score', '3')
            try:
                deep_score = float(deep_score_str) if deep_score_str.strip() else 3.0
            except:
                deep_score = 3.0
                
            duration_str = row.get('duration (m)f', '0') # Or 'Duration'
            if not duration_str:
                 duration_str = row.get('Duration', '0')
            try:
                duration = int(float(duration_str))
            except:
                duration = 0
                
            session_data = {
                "start_time": parse_notion_date(row.get('start time')),
                "end_time": parse_notion_date(row.get('end time')),
                "duration_min": duration,
                "category": normalize_category(row.get('Type')),
                "original_type": row.get('Type', ''),
                "deep_score": deep_score,
                "notes": row.get('Notes', '')
            }
            sessions_by_date[date_val].append(session_data)

    if not all_dates:
        print("No valid data found in CSV.")
        sys.exit(1)
        
    sorted_dates = sorted(list(all_dates))
    start_date = sorted_dates[0]
    end_date = sorted_dates[-1]
    
    print(f"Period: {start_date} to {end_date}")
    
    # 3. Aggregate Data
    output_data = {
        "period": {
            "start_date": start_date,
            "end_date": end_date
        },
        "weekly_summary": {
            # Simple aggregation
            "total_hours": 0,
            "average_deep_score": 0
        },
        "days": []
    }
    
    total_min = 0
    total_score = 0
    score_count = 0
    
    for d in sorted_dates:
        # Parse Daily Review
        reflection = parse_daily_markdown(d)
        
        # Day Data
        sessions = sessions_by_date.get(d, [])
        sessions.sort(key=lambda x: x['start_time'] if x['start_time'] else "")
        
        # Stats for summary
        for s in sessions:
            total_min += s['duration_min']
            if s['deep_score'] > 0:
                total_score += s['deep_score']
                score_count += 1
        
        # Determine day_mode fallback
        if reflection['day_mode'] == "Unknown":
            # Simple heuristic: Sat/Sun = Off
            try:
                dt = datetime.strptime(d, '%Y-%m-%d')
                if dt.weekday() >= 5: # 5=Sat, 6=Sun
                    reflection['day_mode'] = 'Off'
                else:
                    reflection['day_mode'] = 'Shift'
            except:
                pass

        day_obj = {
            "date": d,
            "day_mode": reflection['day_mode'],
            "reflection": {
                "worked": reflection['worked'],
                "slipped": reflection['slipped'],
                "insight": reflection['insight'],
                "strategy_for_next_day": reflection['strategy_for_next_day']
            },
            "sessions": sessions
        }
        output_data['days'].append(day_obj)
        
    # Finalize Summary
    output_data['weekly_summary']['total_hours'] = round(total_min / 60, 2)
    output_data['weekly_summary']['average_deep_score'] = round(total_score / score_count, 2) if score_count > 0 else 0
    
    # 4. Output JSON
    output_filename = f"normalized_data_{start_date}_to_{end_date}.json"
    output_json_path = os.path.join(OUTPUT_DIR, output_filename)
    
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
        
    print(f"Success! Normalized data saved to: {output_json_path}")

    # 5. Output Markdown (Session Query Log)
    # Replicate process_sessions_db_export functionality
    print("Generating Markdown export for Sessions...")
    sessions_md_dir = os.path.join(BASE_DIR, 'Sessions')
    os.makedirs(sessions_md_dir, exist_ok=True)
    
    md_filename = f"Sessions_DB_{start_date}_to_{end_date}.md"
    md_output_path = os.path.join(sessions_md_dir, md_filename)
    
    # We need to read the CSV raw again or use the data we have. 
    # To be "faithful" to the original CSV content (headers etc), let's re-read the CSV and filter.
    # This ensures exact table replication as per the original skill.
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            
            # Find Date column
            date_col_idx = -1
            for i, col in enumerate(header):
                if col.strip() == 'Date':
                    date_col_idx = i
                    break
            
            if date_col_idx != -1:
                md_rows = []
                # Header conversion
                cleaned_header = [col.replace('|', '\\|').replace('\n', '<br>') for col in header]
                md_rows.append('| ' + ' | '.join(cleaned_header) + ' |')
                md_rows.append('| ' + ' | '.join(['---'] * len(header)) + ' |')
                
                start_dt = datetime.strptime(start_date, '%Y-%m-%d').date()
                end_dt = datetime.strptime(end_date, '%Y-%m-%d').date()
                
                for row in reader:
                    if len(row) <= date_col_idx: continue
                    try:
                        row_date = datetime.strptime(row[date_col_idx], '%Y-%m-%d').date()
                        if start_dt <= row_date <= end_dt:
                             cleaned_row = [c.replace('|', '\\|').replace('\n', '<br>') for c in row]
                             md_rows.append('| ' + ' | '.join(cleaned_row) + ' |')
                    except ValueError:
                        continue
                        
                with open(md_output_path, 'w', encoding='utf-8') as f_md:
                    f_md.write('\n'.join(md_rows))
                print(f"Success! Markdown export saved to: {md_output_path}")

    except Exception as e:
        print(f"Error generating Markdown: {e}")

    # Optional: Delete CSV?
    # import_weekly_skill functionality implies automated cleanup.
    # Since we have processed it into BOTH JSON and MD, we can arguably delete it if the user wants full automation.
    # For now, let's just print a reminder.
    print(f"Note: Original CSV at '{csv_path}' was NOT deleted.")

if __name__ == "__main__":
    main()
