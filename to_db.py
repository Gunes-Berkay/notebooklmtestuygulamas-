import sqlite3
import re
import os

def sanitize_table_name(name: str) -> str:
    # sadece harf, rakam ve alt çizgi bırak
    return re.sub(r"[^0-9A-Za-z_]", "_", name)

def create_table_if_not_exists(conn: sqlite3.Connection, table_name: str):
    conn.execute(f"""
        CREATE TABLE IF NOT EXISTS "{table_name}" (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT,
            question TEXT UNIQUE,
            A TEXT,
            B TEXT,
            C TEXT,
            D TEXT,
            correct TEXT
        )
    """)
    conn.commit()

def insert_questions_from_txt(txt_path: str, db_path: str, table_name: str) -> int:
    """
    txt_path -> path to the txt file (e.g. tests/6_Testing.txt)
    db_path  -> path to database file used by quiz app (e.g. database.db)
    table_name -> desired table name (without quotes), will be sanitized
    Returns number of inserted rows (approx).
    """
    if not os.path.exists(txt_path):
        raise FileNotFoundError(f"{txt_path} bulunamadı.")

    table_name = sanitize_table_name(table_name)

    # read file
    with open(txt_path, "r", encoding="utf-8") as f:
        text = f.read()

    # pattern expects groups: source, question, A, B, C, D, (the text before final paren?), correct_letter
    # adjusted for your provided format: (source)(question)(A) (..)(B) (..)(C) (..)(D) (..)(CorrectLetter)
    pattern = re.compile(
        r"\((.*?)\)\((.*?)\)\(A\)\s*\((.*?)\)\(B\)\s*\((.*?)\)\(C\)\s*\((.*?)\)\(D\)\s*\((.*?)\)\s*\(\s*([A-Da-d])\s*\)",
        re.DOTALL
    )

    matches = pattern.findall(text)

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    create_table_if_not_exists(conn, table_name)

    inserted = 0
    for m in matches:
        # m groups: (source, question, Atext, Btext, Ctext, Dtext, maybe_extra, correct_letter)
        # Some inputs may produce an extra capture before last paren; we captured 7 groups before correct letter
        source = m[0].strip()
        question = m[1].strip()
        A_text = m[2].strip()
        B_text = m[3].strip()
        C_text = m[4].strip()
        D_text = m[5].strip()
        # m[6] would be the text captured before the final parenthesis if pattern matched differently; ignore
        correct_letter = m[6].strip().upper() if len(m) >= 7 else None

        # defensive: ensure correct_letter is A-D
        if correct_letter not in ("A", "B", "C", "D"):
            # try to infer from the trailing text if possible (fallback)
            # skip this record if cannot determine
            continue

        try:
            cur.execute(
                f'INSERT OR IGNORE INTO "{table_name}" (source, question, A, B, C, D, correct) VALUES (?, ?, ?, ?, ?, ?, ?)',
                (source, question, A_text, B_text, C_text, D_text, correct_letter)
            )
            if cur.rowcount:  # sqlite's rowcount may be -1 on some drivers, but usually >0 if inserted
                inserted += 1
        except Exception as e:
            print(f"[{table_name}] Eklerken hata: {e}\nSoru: {question[:60]}...")

    conn.commit()
    conn.close()

    print(f"{txt_path} -> {table_name}: {len(matches)} eşleşme bulundu, yaklaşık {inserted} yeni kayıt eklendi.")
    return inserted


# Eğer dosya doğrudan çalıştırılırsa tests klasöründeki tüm txtleri db'ye aktar
# if __name__ == "__main__":
#     DB = "database.db"  # quiz.py'de kullandığın DB dosyasıyla aynı olmalı
#     TESTS_DIR = "tests"
#     os.makedirs(TESTS_DIR, exist_ok=True)
#     txts = [f for f in os.listdir(TESTS_DIR) if f.lower().endswith(".txt")]
#     for t in txts:
#         path = os.path.join(TESTS_DIR, t)
#         table = os.path.splitext(t)[0]
#         print(f"İşleniyor: {t} -> tablo: {table}")
#         insert_questions_from_txt(path, DB, table)
#     print("Tamamlandı.")
    
if __name__ == "__main__":
    DB = "database.db"  # quiz.py'de kullandığın DB dosyasıyla aynı olmalı
    TESTS_DIR = "tests"
    insert_questions_from_txt(os.path.join(TESTS_DIR, "cloud.txt"), DB, "cloud1")
    print("Tamamlandı.")

