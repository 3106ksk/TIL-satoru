import json
import os
import glob
import re
import sys
import argparse
from datetime import datetime, timedelta

# --- Configuration ---
BASE_DIR = '/Users/310tea/Documents/Learning_log'
SESSIONS_DIR = os.path.join(BASE_DIR, 'Sessions')
DAILY_DIR = os.path.join(BASE_DIR, 'daily')
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
    
    for cat, keywords in CATEGORY_MAP.items():
        for k in keywords:
            if k in raw_type:
                return cat
    return "Other"

def parse_notion_date(date_str):
    if not date_str:
        return None
    
    clean_str = re.sub(r'\s*\(.*\)', '', date_str).strip()
    
    try:
        dt = datetime.strptime(clean_str, '%B %d, %Y %I:%M %p')
        return dt.strftime('%Y-%m-%dT%H:%M:%S+09:00')
    except ValueError:
        try:
             dt = datetime.strptime(clean_str, '%Y-%m-%d')
             return dt.strftime('%Y-%m-%dT00:00:00+09:00')
        except ValueError:
             pass
        return None

def parse_daily_markdown(date_str):
    file_path = os.path.join(DAILY_DIR, f"daily_{date_str}.md")
    result = {
        "stats": {
            "budget_min": 0,
            "total_min": 0,
            "pure_study_min": 0,
            "rest_min": 0,
            "exercise_min": 0,
            "avg_deep_score": 0.0
        },
        "plan": {
            "top1": "",
            "done_condition": "",
            "if_interrupted": ""
        },
        "feedback": {
            "top1_done_condition": {"quantitative": [], "qualitative": []},
            "time_allocation": {"quantitative": [], "qualitative": []}
        },
        "reflection": {
            "worked": [],
            "slipped": [],
            "insight": [],
            "strategy_for_next_day": []
        },
        "learning_record": {
            "what_i_did": [],
            "what_i_struggled_with": [],
            "why_it_happened": [],
            "what_i_learned": []
        },
        "day_mode": "Unknown"
    }

    if not os.path.exists(file_path):
        return result

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        current_section = None
        current_subsection = None

        def extract_digits(s):
            match = re.search(r'([\d.]+)', s)
            return float(match.group(1)) if match else 0

        for line in lines:
            stripped = line.strip()

            if not stripped:
                continue

            if stripped.startswith("## ■"):
                current_subsection = None
                if "Stats" in stripped:
                    current_section = "stats"
                elif "Top1" in stripped and "フィードバック" in stripped:
                    current_section = "feedback_top1"
                elif "時間配分" in stripped:
                    current_section = "feedback_time"
                elif "Worked" in stripped:
                    current_section = "worked"
                elif "Slipped" in stripped:
                    current_section = "slipped"
                elif "Insight" in stripped:
                    current_section = "insight"
                elif "今日の学習記録" in stripped:
                    current_section = "learning_record"
                elif "Study Strategy" in stripped:
                    current_section = "strategy_for_next_day"
                elif "Technical Learnings" in stripped:
                    current_section = "technical_learnings"
                else:
                    current_section = None
                continue

            if current_section in ["feedback_top1", "feedback_time"] and stripped.startswith("**["):
                if "定量" in stripped:
                    current_subsection = "quantitative"
                elif "定性" in stripped:
                    current_subsection = "qualitative"
                continue

            if current_section == "learning_record" and not stripped.startswith("-"):
                if "今日やったこと" in stripped:
                    current_subsection = "what_i_did"
                    continue
                elif "詰まったこと" in stripped:
                    current_subsection = "what_i_struggled_with"
                    continue
                elif "なぜそうなったか" in stripped:
                    current_subsection = "why_it_happened"
                    continue
                elif "何を学んだか" in stripped:
                    current_subsection = "what_i_learned"
                    continue

            if "- **Day Mode**:" in stripped:
                if "Off" in stripped or "OFF" in stripped:
                    result["day_mode"] = "Off"
                elif "Shift" in stripped or "ON" in stripped:
                    result["day_mode"] = "Shift"
                continue

            if "- **Budget**:" in stripped:
                result["stats"]["budget_min"] = int(extract_digits(stripped))
                continue
            if "- **Total Min**:" in stripped:
                result["stats"]["total_min"] = int(extract_digits(stripped))
                continue
            if "- **純粋な学習時間**:" in stripped:
                result["stats"]["pure_study_min"] = int(extract_digits(stripped))
                continue
            if "- **休憩時間**:" in stripped:
                result["stats"]["rest_min"] = int(extract_digits(stripped))
                continue
            if "- **運動時間**:" in stripped:
                result["stats"]["exercise_min"] = int(extract_digits(stripped))
                continue
            if "- **Avg Deep Score**:" in stripped:
                result["stats"]["avg_deep_score"] = extract_digits(stripped)
                continue
            
            if "- **Top1**:" in stripped:
                val = stripped.split(":", 1)[1].replace("**", "").strip() if ":" in stripped else stripped
                result["plan"]["top1"] = val.lstrip(" :").strip()
                continue
            if "- **Done条件**:" in stripped:
                val = stripped.split(":", 1)[1].replace("**", "").strip() if ":" in stripped else stripped
                result["plan"]["done_condition"] = val.lstrip(" :").strip()
                continue
            if "- **切れたら→**:" in stripped:
                val = stripped.split(":", 1)[1].replace("**", "").strip() if ":" in stripped else stripped
                result["plan"]["if_interrupted"] = val.lstrip(" :").strip()
                continue

            content = stripped.lstrip("-・ ").strip()
            content = re.sub(r'^\*{0,2}(事実|Fact|Why)\*{0,2}[:：]\s*', '', content)

            if re.match(r'^\*{0,2}\d+\.\s+.*\*{0,2}$', stripped):
                continue

            if not content:
                continue

            if current_section == "strategy_for_next_day":
                result["reflection"]["strategy_for_next_day"].append(content)
            elif current_section in ["worked", "slipped", "insight"]:
                if stripped.startswith("-") or stripped.startswith("・"):
                    result["reflection"][current_section].append(content)
            elif current_section == "feedback_top1" and current_subsection:
                if stripped.startswith("-") or stripped.startswith("・"):
                    result["feedback"]["top1_done_condition"][current_subsection].append(content)
            elif current_section == "feedback_time" and current_subsection:
                if stripped.startswith("-") or stripped.startswith("・"):
                    result["feedback"]["time_allocation"][current_subsection].append(content)
            elif current_section == "learning_record" and current_subsection:
                if not "■" in content and not "---" in content and "今日やったこと" not in content and "詰まったこと" not in content and "なぜそうなったか" not in content and "何を学んだか" not in content:
                    result["learning_record"][current_subsection].append(content)

    except Exception as e:
        print(f"Error parsing daily {date_str}: {e}")

    return result

def find_latest_sessions_md():
    pattern = os.path.join(SESSIONS_DIR, "Sessions_DB_*.md")
    files = glob.glob(pattern)
    if not files:
        return None
    
    # Sort files based on the end date in the filename YYYY-MM-DD_to_YYYY-MM-DD.md
    def extract_end_date(filepath):
        basename = os.path.basename(filepath)
        match = re.search(r'to_(\d{4}-\d{2}-\d{2})\.md', basename)
        if match:
            return match.group(1)
        return ""
        
    files.sort(key=extract_end_date, reverse=True)
    return files[0]

def parse_markdown_table(file_path):
    print(f"Reading logic: Parsing Markdown table from {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]
        
    if len(lines) < 3:
        print("Error: Markdown file does not contain a valid table (less than 3 lines).")
        sys.exit(1)
        
    # Parse header
    header_line = lines[0]
    headers = [col.strip() for col in header_line.split('|')[1:-1]]
    
    # Clean BOM if present in first header
    if headers and headers[0].startswith('\ufeff'):
         headers[0] = headers[0].replace('\ufeff', '')
         
    # Check required columns
    required_cols = ['Date', 'Type', 'Deep Score', 'start time', 'end time', 'Notes']
    missing = [c for c in required_cols if c not in headers and (c != 'duration (m)f' and 'Duration' not in headers)]
    if missing:
        print(f"Error: Missing required columns in Markdown table: {missing}")
        sys.exit(1)
        
    # Track metrics
    total_parsed = 0
    skipped_count = 0
    
    sessions_by_date = {}
    all_dates = set()
    
    for idx, row_line in enumerate(lines[2:], start=3):
        cols = [col.strip() for col in row_line.split('|')[1:-1]]
        
        # If column counts don't match, we try to safely skip
        if len(cols) != len(headers):
            skipped_count += 1
            print(f"Warning: Line {idx} column count ({len(cols)}) does not match header count ({len(headers)}). Skipped.")
            continue
            
        row = dict(zip(headers, cols))
        
        # Extract Date
        date_val = row.get('Date', '')
        if not date_val:
            st = parse_notion_date(row.get('start time', ''))
            if st:
                date_val = st.split('T')[0]
                
        if not date_val:
            skipped_count += 1
            continue
            
        all_dates.add(date_val)
        if date_val not in sessions_by_date:
            sessions_by_date[date_val] = []
            
        # Extract and clean data
        deep_score_str = row.get('Deep Score', '3')
        try:
            deep_score = float(deep_score_str) if deep_score_str else 3.0
        except ValueError:
            deep_score = 3.0
            
        duration_str = row.get('duration (m)f', '0')
        if not duration_str:
            duration_str = row.get('Duration', '0')
        try:
            duration = int(float(duration_str))
        except ValueError:
            duration = 0
            
        session_data = {
            "start_time": parse_notion_date(row.get('start time')),
            "end_time": parse_notion_date(row.get('end time')),
            "duration_min": duration,
            "category": normalize_category(row.get('Type')),
            "original_type": row.get('Type', ''),
            "deep_score": deep_score,
            "notes": row.get('Notes', '').replace('<br>', '\n')
        }
        
        sessions_by_date[date_val].append(session_data)
        total_parsed += 1
        
    print(f"Extracted {total_parsed} valid sessions. Skipped {skipped_count} lines.")
    
    if not all_dates:
        print("No valid data found in Markdown table.")
        sys.exit(1)
        
    return sessions_by_date, sorted(list(all_dates))

def main():
    parser = argparse.ArgumentParser(description="Normalize Learning Logs from Markdown")
    parser.add_argument("--input", help="Explicit path to the Sessions_DB_*.md file to use.")
    args = parser.parse_args()

    print("--- Starting Learning Log Normalization (Markdown Edition) ---")
    
    # 1. Provide MD Input
    md_path = args.input
    if md_path:
        if not os.path.exists(md_path):
            print(f"Specified input file not found: {md_path}")
            sys.exit(1)
    else:
        md_path = find_latest_sessions_md()
        if not md_path:
            print(f"No 'Sessions_DB_*.md' found in {SESSIONS_DIR}. Please run process_sessions_db_export skill first.")
            sys.exit(1)
            
    print(f"Reading: {md_path}")
    
    # 2. Parse Markdown
    sessions_by_date, sorted_dates = parse_markdown_table(md_path)
    
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
            "total_hours": 0,
            "average_deep_score": 0
        },
        "days": []
    }
    
    total_min = 0
    total_score = 0
    score_count = 0
    
    for d in sorted_dates:
        reflection = parse_daily_markdown(d)
        
        sessions = sessions_by_date.get(d, [])
        sessions.sort(key=lambda x: x['start_time'] if x['start_time'] else "")
        
        for s in sessions:
            total_min += s['duration_min']
            if s['deep_score'] > 0:
                total_score += s['deep_score']
                score_count += 1
                
        if reflection['day_mode'] == "Unknown":
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
            "stats": reflection['stats'],
            "plan": reflection['plan'],
            "feedback": reflection['feedback'],
            "reflection": reflection['reflection'],
            "learning_record": reflection['learning_record'],
            "sessions": sessions
        }
        output_data['days'].append(day_obj)
        
    output_data['weekly_summary']['total_hours'] = round(total_min / 60, 2)
    output_data['weekly_summary']['average_deep_score'] = round(total_score / score_count, 2) if score_count > 0 else 0
    
    # 4. Output JSON
    output_filename = f"normalized_data_{start_date}_to_{end_date}.json"
    output_json_path = os.path.join(OUTPUT_DIR, output_filename)
    
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
        
    print(f"Success! Normalized data saved to: {output_json_path}")

if __name__ == "__main__":
    main()
