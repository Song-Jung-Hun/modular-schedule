import fitz  # pymupdf
import os, json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

OUT = r"C:\Users\great\Desktop\refs"
os.makedirs(OUT, exist_ok=True)

PDF1 = r"C:\Users\great\Desktop\모듈러 공기\OTKCRK191021.pdf"
PDF2 = r"C:\Users\great\Desktop\모듈러 공기\1. 주택건설공사 공사기간 산정지침.pdf"

# ── 추출할 페이지 정의 ─────────────────────────────────────────────────────
# (출력파일명, PDF경로, 문서페이지번호, 라벨)
# 문서 페이지 번호 = PDF에 인쇄된 번호
# PyMuPDF page index = 0-based → 보통 표지/목차 몇 장 있어서 offset 필요
# → 실제 index는 스캔해서 맞춤

pages_to_extract = [
    # OTKCRK
    ("otkcrk_p8",    PDF1,  7,  "OTKCRK p.8 — 공기산정기준(안)"),
    ("otkcrk_p135",  PDF1, 134, "OTKCRK p.135 — 표4-39 현장조립 세부"),
    ("otkcrk_p148",  PDF1, 147, "OTKCRK p.148 — 공사 준비기간"),
    ("otkcrk_p149",  PDF1, 148, "OTKCRK p.149 — 공사 준비기간(계속)"),
    ("otkcrk_p153",  PDF1, 152, "OTKCRK p.153 — 코어골조 8일/층"),
    ("otkcrk_p156",  PDF1, 155, "OTKCRK p.156 — 부대공사 기준"),
    # LH 지침
    ("lh_p10",  PDF2,  9,  "LH 지침 p.10 — 기초공사 직타공법"),
    ("lh_p12",  PDF2, 11,  "LH 지침 p.12 — 조경공사 기간"),
    ("lh_p16",  PDF2, 15,  "LH 지침 p.16 — 별표1 비작업일(1)"),
    ("lh_p17",  PDF2, 16,  "LH 지침 p.17 — 별표1 비작업일(2)"),
    ("lh_p18",  PDF2, 17,  "LH 지침 p.18 — 별표2 비작업일(1)"),
    ("lh_p19",  PDF2, 18,  "LH 지침 p.19 — 별표2 비작업일(2)"),
]

results = {}
for fname, pdf_path, page_idx, label in pages_to_extract:
    try:
        doc = fitz.open(pdf_path)
        page = doc[page_idx]
        mat = fitz.Matrix(2.0, 2.0)  # 2x = 144dpi → 충분히 선명
        pix = page.get_pixmap(matrix=mat, alpha=False)
        out_path = os.path.join(OUT, fname + ".png")
        pix.save(out_path)
        doc.close()
        results[fname] = {"label": label, "file": "refs/" + fname + ".png", "ok": True}
        print(f"OK  {fname}.png  ({label})")
    except Exception as e:
        results[fname] = {"label": label, "file": None, "ok": False, "err": str(e)}
        print(f"ERR {fname}: {e}")

# 메타데이터 저장
with open(os.path.join(OUT, "index.json"), "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"\n완료: {OUT}")
