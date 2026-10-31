# Lecture 04: In-Lecture Quizzes

Live Mentimeter polls were run after the file-processing demos, after OCR, and at the end on Celery (Professor / TA Salma). The transcript gives the wording of each question only loosely; answers below follow the instructor’s readout.

---

## Quiz 1 - After file processing (PDF / CSV / Excel)

### Q1. Which popular Python library is commonly used to read and write Excel files?

| | |
|---|---|
| **Correct ✓** | **pandas** |

**Live note:** Most of the ~31 respondents got this right.

---

### Q2. Which pandas function reads an Excel file?

| | |
|---|---|
| **Correct ✓** | **`pd.read_excel()`** (instructor recapped `read_excel`; compare `read_csv` for CSV) |

---

### Q3. In which mode must a file be opened when writing text to a CSV?

| | |
|---|---|
| **Correct ✓** | Write mode **`"w"`** for text (instructor said both write options appeared acceptable; `"wb"` is binary and not what you use for text CSV) |

**Note:** The transcript is unclear on the exact option set. For text CSV with the `csv` module, use `"w"` (with `newline=""`).

---

## Quiz 2 - After OCR (classical tools)

### Q4. Which tool extracts text from a preprocessed image?

| | |
|---|---|
| **Correct concept ✓** | **pytesseract** (Tesseract wrapper); Pillow/OpenCV are for **reading and preprocessing** |

**Note:** The poll text was not read out in full; the instructor only confirmed the tool name.

---

## Quiz 3 - End of lecture (Celery)

### Q5. What is the primary role of Celery in a Python web application architecture?

| | |
|---|---|
| **Correct ✓** | **Take tasks from a task queue and have workers execute them in the background**, so the web app need not wait |

**Explanation:** Celery offloads heavy work from the request path; it is not a web framework, database, or HTTP client.

---

## Quick self-check

| Claim | True / False |
|-------|----------------|
| pdfplumber is the preferred tool for table extraction | **True** |
| Tesseract works well on raw, noisy scans with no preprocessing | **False** |
| FastAPI `async` runs CPU-bound tasks in parallel | **False** - it only interleaves waiting tasks |
| Calling `task(2, 3)` directly puts it on the Celery queue | **False** - use `.delay()` |
| A vision-LLM OCR call can return a refusal or `None` content | **True** |
| Celery workers must run on the same machine as the web app | **False** |
