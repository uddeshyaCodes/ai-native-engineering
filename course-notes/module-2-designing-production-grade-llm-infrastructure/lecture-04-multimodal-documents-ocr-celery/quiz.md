# Lecture 04: In-Lecture Quizzes

Live Mentimeter polls were run after the file-processing demos, after OCR, and at the end on Celery (Professor / TA Salma). Questions and options below are taken verbatim from the three Mentimeter decks ("CSV_Excel_process", "OCR", "Celery"; 6 questions in total). **The decks have no answer-key slides**, so correct answers are deduced from the lecture content; live-result notes come from the transcript where recorded.

---

## Quiz 1 - After file processing (PDF / CSV / Excel)

### Q1. Library for writing Excel files

**Stem:** Which popular Python library is commonly used to write data directly into Excel (.xlsx) files?

| Option | |
|---|---|
| **A ✓** | **panda** *(sic - the deck's spelling of pandas)* |
| B | pypdf |
| C | pytesseract |
| D | pika |

**Live note:** Most of the ~31 respondents got this right.

**Explanation:** pandas writes Excel via `DataFrame.to_excel()`. pypdf is for PDFs, pytesseract for OCR, pika for RabbitMQ.

---

### Q2. Reading an Excel file with pandas

**Stem:** When reading an Excel file using pandas, which function is used?

| Option | |
|---|---|
| A | pd.read_csv() |
| **B ✓** | **pd.read_excel()** |
| C | pd.open_xls() |
| D | pd.parse_excel() |

**Explanation:** Instructor recapped `read_excel`; compare `read_csv` for CSV. `open_xls` and `parse_excel` don't exist.

---

### Q3. File mode for writing a text CSV

**Stem:** What mode must a file be opened in when writing text data to a CSV file using Python's built-in csv module?

| Option | |
|---|---|
| A | "rb" |
| **B ✓** | **"w"** |
| C | "wb" |
| D | "x" |

**Explanation:** Text CSV with the `csv` module uses `"w"` (with `newline=""`). `"wb"` is binary and `"rb"` is read-only. Instructor said both write options looked acceptable live; `"x"` also only creates a new file and errors if it exists.

---

## Quiz 2 - After OCR (classical tools)

### Q4. Library for basic image handling

**Stem:** Which Python library is primarily used for basic image opening, manipulation, and saving?

| Option | |
|---|---|
| **A ✓** | **Pillow (PIL)** |
| B | pytesseract |
| C | pypdf |
| D | Celery |

**Explanation:** Pillow (and OpenCV) handle **reading and preprocessing** images; **pytesseract** is the Tesseract wrapper that extracts text from the preprocessed image.

---

## Quiz 3 - End of lecture (Celery)

### Q5. Primary role of Celery

**Stem:** What is the main primary role of Celery in a Python web application architecture?

| Option | |
|---|---|
| A | Database engine |
| **B ✓** | **Asynchronous task queue / background job processor** |
| C | Web server router |
| D | PDF renderer |

**Explanation:** Celery takes tasks from a task queue and has workers execute them in the background, so the web app need not wait. It is not a web framework, database, or HTTP client.

---

### Q6. Redis in a Celery workflow

**Stem:** In a Celery task workflow, what common role does Redis frequently play?

| Option | |
|---|---|
| **A ✓** | **Message Broker / Result Backend** |
| B | Frontend Framework |
| C | PDF Parser |
| D | Image Compression Engine |

**Explanation:** Redis (or RabbitMQ) holds the task queue the client enqueues into and the workers dequeue from; Redis can also store task results.

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

---

## Summary

| Quiz | When | Questions | Main topics |
|------|------|-----------|-------------|
| **1** | After file processing | **3** | pandas for Excel, `read_excel`, CSV write mode |
| **2** | After OCR | **1** | Pillow for image handling |
| **3** | End of lecture (Celery) | **2** | Celery's role, Redis as broker/backend |

**Total Menti questions:** **6** (3 + 1 + 2)
