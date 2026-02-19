"""
O-Level History 2059 Past Paper Scraper
=========================================
Downloads question papers & mark schemes from GCE Guide,
extracts text with pdfplumber, parses Q&A pairs, and
populates the 'past_papers' section of history_data.json.

Run from the History/ root directory:
    python scripts/scrape_past_papers.py
"""

import sys
import io
# Fix Windows console encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import os
import re
import json
import time
import requests
import pdfplumber

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────

DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "history_data.json")
DOWNLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "downloaded_papers")

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# GCE Guide base URL for O-Level History 2059
GCE_BASE = "https://papers.gceguide.cc/Cambridge%20O%20Level/History%20(2059)"

# Papers to download: (year, season_code, paper_code)
# season_code: s = May/June, w = Oct/Nov
# paper_code: 1 = Paper 1
PAPERS = [
    # ── 2024 ──
    ("2024", "s24", "2059_s24_qp_1"),
    ("2024", "s24", "2059_s24_ms_1"),
    ("2024", "w24", "2059_w24_qp_1"),
    ("2024", "w24", "2059_w24_ms_1"),
    # ── 2023 ──
    ("2023", "s23", "2059_s23_qp_1"),
    ("2023", "s23", "2059_s23_ms_1"),
    ("2023", "w23", "2059_w23_qp_1"),
    ("2023", "w23", "2059_w23_ms_1"),
    # ── 2022 ──
    ("2022", "s22", "2059_s22_qp_1"),
    ("2022", "s22", "2059_s22_ms_1"),
    ("2022", "w22", "2059_w22_qp_1"),
    ("2022", "w22", "2059_w22_ms_1"),
    # ── 2021 ──
    ("2021", "s21", "2059_s21_qp_1"),
    ("2021", "s21", "2059_s21_ms_1"),
    ("2021", "w21", "2059_w21_qp_1"),
    ("2021", "w21", "2059_w21_ms_1"),
    # ── 2020 ──
    ("2020", "s20", "2059_s20_qp_1"),
    ("2020", "s20", "2059_s20_ms_1"),
    ("2020", "w20", "2059_w20_qp_1"),
    ("2020", "w20", "2059_w20_ms_1"),
    # ── 2019 ──
    ("2019", "s19", "2059_s19_qp_1"),
    ("2019", "s19", "2059_s19_ms_1"),
    ("2019", "w19", "2059_w19_qp_1"),
    ("2019", "w19", "2059_w19_ms_1"),
    # ── 2018 ──
    ("2018", "s18", "2059_s18_qp_1"),
    ("2018", "s18", "2059_s18_ms_1"),
    ("2018", "w18", "2059_w18_qp_1"),
    ("2018", "w18", "2059_w18_ms_1"),
]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}


# ─────────────────────────────────────────────────────────────────────────────
# STEP 1: DOWNLOAD PDF
# ─────────────────────────────────────────────────────────────────────────────

def build_url(year: str, season: str, filename: str) -> str:
    """Build the direct GCE Guide PDF URL."""
    return f"{GCE_BASE}/{year}/{filename}.pdf"


def download_pdf(url: str, dest_path: str) -> bool:
    """Download a PDF from url to dest_path. Returns True on success."""
    if os.path.exists(dest_path):
        print(f"  ✅ Already downloaded: {os.path.basename(dest_path)}")
        return True
    try:
        response = requests.get(url, headers=HEADERS, timeout=30)
        if response.status_code == 200 and b"%PDF" in response.content[:10]:
            with open(dest_path, "wb") as f:
                f.write(response.content)
            print(f"  ✅ Downloaded: {os.path.basename(dest_path)}")
            return True
        else:
            print(f"  ❌ Failed (HTTP {response.status_code}): {url}")
            return False
    except Exception as e:
        print(f"  ❌ Error downloading {url}: {e}")
        return False


# ─────────────────────────────────────────────────────────────────────────────
# STEP 2: EXTRACT TEXT FROM PDF
# ─────────────────────────────────────────────────────────────────────────────

def extract_pdf_text(pdf_path: str) -> str:
    """Extract full text from a PDF using pdfplumber."""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            pages_text = []
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    pages_text.append(text)
            return "\n".join(pages_text)
    except Exception as e:
        print(f"  ⚠️  pdfplumber error on {pdf_path}: {e}")
        return ""


# ─────────────────────────────────────────────────────────────────────────────
# STEP 3: PARSE QUESTION PAPER
# ─────────────────────────────────────────────────────────────────────────────

def parse_question_paper(text: str, year: str, season_label: str) -> list:
    """
    Parse a question paper PDF text to extract questions.
    Returns a list of dicts: {question_num, marks, question_text}
    """
    questions = []
    
    # Pattern: "1  (a)  Describe..." or "Question 1" or numbered lines
    # O-Level Hist 2059 Paper 1 format:
    # Section A: 4-mark questions (describe / how / why)  
    # Section B: 7-mark questions
    # Section C: 14-mark questions
    
    patterns = [
        # Match "1 Describe..." or "1. Describe..."
        r'(?m)^(\d+)\s*[\.\)]\s*(.+?)(?=^\d+\s*[\.\)]|\Z)',
        # Match "Question 1" style
        r'(?m)^(?:Question\s+)?(\d+)\s*\n(.+?)(?=^(?:Question\s+)?\d+\s*\n|\Z)',
    ]
    
    # Try to split by mark indicators [4], [7], [14]
    mark_pattern = re.compile(
        r'((?:(?:Describe|Explain|How|Why|Assess|Was|To what extent|\"[^\"]+\")[^\[]+))\[(\d+)\]',
        re.IGNORECASE | re.DOTALL
    )
    
    matches = mark_pattern.findall(text)
    for i, (q_text, marks) in enumerate(matches, 1):
        q_text = q_text.strip()
        # Clean up whitespace
        q_text = re.sub(r'\s+', ' ', q_text)
        if len(q_text) > 15:  # skip tiny fragments
            questions.append({
                "question_num": i,
                "question": q_text,
                "marks": int(marks),
                "year": year,
                "season": season_label
            })
    
    # Fallback: line-by-line keyword search
    if not questions:
        lines = text.split('\n')
        q_num = 0
        for line in lines:
            line = line.strip()
            keywords = ['describe', 'explain', 'how', 'why', 'assess', 'was ', 
                       'what extent', 'compare', 'important']
            if any(kw in line.lower() for kw in keywords) and len(line) > 20:
                q_num += 1
                # Try to find marks at end of line
                mark_match = re.search(r'\[(\d+)\]\s*$', line)
                marks = int(mark_match.group(1)) if mark_match else 4
                questions.append({
                    "question_num": q_num,
                    "question": re.sub(r'\[\d+\]\s*$', '', line).strip(),
                    "marks": marks,
                    "year": year,
                    "season": season_label
                })
    
    return questions


# ─────────────────────────────────────────────────────────────────────────────
# STEP 4: PARSE MARK SCHEME
# ─────────────────────────────────────────────────────────────────────────────

def parse_mark_scheme(text: str, year: str, season_label: str) -> list:
    """
    Parse a mark scheme PDF text to extract marking points.
    Returns list of dicts: {question, points, total_marks}
    """
    mark_entries = []
    
    # ── Pattern 1: Cambridge-style mark scheme blocks ──
    # "1  (a)  Any TWO of the following: • Point 1 • Point 2..."
    # or "Award marks for..."
    
    # Split into question blocks using question numbers
    # Cambridge MSs often have: "1 (a)" or just "1" as section headers
    
    block_pattern = re.compile(
        r'(?m)^(\d+)\s*(?:\([ab]\))?\s*\n(.*?)(?=^\d+\s*(?:\([ab]\))?\s*\n|\Z)',
        re.DOTALL
    )
    
    blocks = block_pattern.findall(text)
    
    if not blocks:
        # Alternative: split by "Question X" or mark award lines
        block_pattern2 = re.compile(
            r'(?:^|\n)(\d+)\b(.*?)(?=\n\d+\b|\Z)',
            re.DOTALL
        )
        blocks = block_pattern2.findall(text)
    
    for q_num, block_text in blocks:
        # Extract bullet points (• or –, or numbered)
        points = []
        
        # Find bullet/dash points
        bullet_re = re.compile(r'[•\-–]\s*([^\n•\-–]+)')
        for match in bullet_re.finditer(block_text):
            pt = match.group(1).strip()
            pt = re.sub(r'\s+', ' ', pt)
            if len(pt) > 10:
                points.append(pt)
        
        # Also grab "Award X marks for..." lines
        award_re = re.compile(r'Award\s+\d+\s+marks?\s+for\s+([^\n]+)', re.IGNORECASE)
        for match in award_re.finditer(block_text):
            points.append("Award: " + match.group(1).strip())
        
        # Look for indicative content lines (numbered 1. 2. 3.)
        if not points:
            numbered_re = re.compile(r'(?m)^\s*\d+[\.\)]\s*(.+)$')
            for match in numbered_re.finditer(block_text):
                pt = match.group(1).strip()
                if len(pt) > 10:
                    points.append(pt)
        
        # Detect total marks from block
        mark_total_re = re.compile(r'\[(\d+)\]|\((\d+)\s*marks?\)', re.IGNORECASE)
        mark_match = mark_total_re.search(block_text)
        total_marks = int(mark_match.group(1) or mark_match.group(2)) if mark_match else 4
        
        # Try to extract question text from block header
        q_header_lines = block_text.strip().split('\n')[:3]
        question_hint = ' '.join(q_header_lines).strip()[:200]
        
        if points:
            mark_entries.append({
                "question_num": int(q_num),
                "question": question_hint,
                "points": points[:15],  # max 15 marking points
                "total_marks": total_marks,
                "year": year,
                "season": season_label
            })
    
    return mark_entries


# ─────────────────────────────────────────────────────────────────────────────
# STEP 5: MATCH Q-PAPER + MARK SCHEME 
# ─────────────────────────────────────────────────────────────────────────────

def merge_qa_with_marks(questions: list, mark_entries: list, 
                         year: str, season_label: str) -> list:
    """
    Merge question paper questions with mark scheme entries.
    Returns combined list ready for past_papers JSON.
    """
    merged = []
    
    mark_lookup = {m["question_num"]: m for m in mark_entries}
    
    for q in questions:
        q_num = q["question_num"]
        ms = mark_lookup.get(q_num, {})
        
        merged.append({
            "question": q["question"],
            "marks": q.get("marks", ms.get("total_marks", 4)),
            "year": year,
            "season": season_label,
            "mark_scheme_points": ms.get("points", []),
            "examiner_tips": extract_examiner_tips(ms.get("points", []))
        })
    
    # If no questions were parsed from QP, use mark scheme entries alone
    if not merged and mark_entries:
        for ms in mark_entries:
            merged.append({
                "question": ms["question"],
                "marks": ms["total_marks"],
                "year": year,
                "season": season_label,
                "mark_scheme_points": ms["points"],
                "examiner_tips": extract_examiner_tips(ms["points"])
            })
    
    return merged


def extract_examiner_tips(points: list) -> list:
    """Extract examiner-style tips from mark scheme points."""
    tips = []
    tip_keywords = ['award', 'credit', 'accept', 'note', 'do not', 'must', 'maximum']
    for point in points:
        if any(kw in point.lower() for kw in tip_keywords):
            tips.append(point)
    return tips[:5]


# ─────────────────────────────────────────────────────────────────────────────
# STEP 6: BUILD SEASON LABEL
# ─────────────────────────────────────────────────────────────────────────────

def get_season_label(season_code: str) -> str:
    """Convert season code like 's23' → 'May_June_2023'"""
    code = season_code.lower()
    year_suffix = re.search(r'\d+', code).group()
    year_full = f"20{year_suffix}" if len(year_suffix) == 2 else year_suffix
    if code.startswith('s'):
        return f"May_June_{year_full}"
    elif code.startswith('w'):
        return f"Oct_Nov_{year_full}"
    return f"Unknown_{year_full}"


# ─────────────────────────────────────────────────────────────────────────────
# STEP 7: UPDATE history_data.json
# ─────────────────────────────────────────────────────────────────────────────

def update_history_data(all_results: dict):
    """Load history_data.json and populate/update the 'past_papers' section."""
    print(f"\n📂 Loading: {DATA_FILE}")
    
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        history_data = json.load(f)
    
    # Merge scraped data into past_papers
    existing_pp = history_data.get("past_papers", {})
    
    for year, seasons in all_results.items():
        if year not in existing_pp:
            existing_pp[year] = {}
        for season_label, entries in seasons.items():
            if season_label not in existing_pp[year]:
                existing_pp[year][season_label] = {}
            # Store under paper_1
            existing_pp[year][season_label]["paper_1"] = {
                "mark_scheme": entries
            }
    
    history_data["past_papers"] = existing_pp
    
    # Write back
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(history_data, f, indent=2, ensure_ascii=False)
    
    total_entries = sum(
        len(seasons[s].get("paper_1", {}).get("mark_scheme", []))
        for year, seasons in all_results.items()
        for s in seasons
    )
    print(f"\n✅ Updated history_data.json with {total_entries} mark scheme entries")
    print(f"   Covering {len(all_results)} years, across multiple seasons.")


# ─────────────────────────────────────────────────────────────────────────────
# MAIN PIPELINE
# ─────────────────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("  O-Level History 2059 - Past Paper Scraper")
    print("=" * 60)

    # Group papers by year/season
    grouped: dict = {}
    for year, season_code, filename in PAPERS:
        season_label = get_season_label(season_code)
        key = (year, season_label, season_code)
        if key not in grouped:
            grouped[key] = {"qp": None, "ms": None}
        if "_qp_" in filename:
            grouped[key]["qp"] = filename
        elif "_ms_" in filename:
            grouped[key]["ms"] = filename

    all_results: dict = {}

    for (year, season_label, season_code), files in grouped.items():
        print(f"\n{'='*50}")
        print(f"  [{year}] {season_label.replace('_', ' ')}")
        print(f"{'='*50}")

        questions = []
        mark_entries = []

        # ── Download & parse Question Paper ──
        if files["qp"]:
            url = build_url(year, season_code, files["qp"])
            dest = os.path.join(DOWNLOAD_DIR, f"{files['qp']}.pdf")
            print(f"\n  [QP] {url}")
            if download_pdf(url, dest):
                text = extract_pdf_text(dest)
                if text:
                    questions = parse_question_paper(text, year, season_label)
                    print(f"  -> Parsed {len(questions)} questions from QP")
                else:
                    print("  ⚠️  Empty text extracted from QP")
            time.sleep(1.5)  # polite delay

        # ── Download & parse Mark Scheme ──
        if files["ms"]:
            url = build_url(year, season_code, files["ms"])
            dest = os.path.join(DOWNLOAD_DIR, f"{files['ms']}.pdf")
            print(f"\n  [MS] {url}")
            if download_pdf(url, dest):
                text = extract_pdf_text(dest)
                if text:
                    mark_entries = parse_mark_scheme(text, year, season_label)
                    print(f"  -> Parsed {len(mark_entries)} mark scheme entries")
                else:
                    print("  ⚠️  Empty text extracted from MS")
            time.sleep(1.5)

        # ── Merge QP + MS ──
        merged = merge_qa_with_marks(questions, mark_entries, year, season_label)
        print(f"\n  [MERGE] {len(merged)} final Q&A pairs for {year} {season_label}")

        if year not in all_results:
            all_results[year] = {}
        all_results[year][season_label] = merged

    # ── Write to JSON ──
    update_history_data(all_results)

    print("\n" + "=" * 60)
    print("  SCRAPING COMPLETE!")
    print("=" * 60)
    print("\nSummary of scraped data:")
    for year, seasons in sorted(all_results.items()):
        for season, entries in seasons.items():
            print(f"  {year} {season.replace('_',' ')}: {len(entries)} entries")


if __name__ == "__main__":
    main()
