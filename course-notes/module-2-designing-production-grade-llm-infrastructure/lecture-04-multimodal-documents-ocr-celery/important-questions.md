# Lecture 04: Important Exam Q&A

Practice questions aligned with lecture emphasis and in-class quizzes. Answers are concise for revision.

---

## PDF processing

### Q1. Which PDF library is best for table extraction, and what does it return?

**A.** **pdfplumber** - `page.extract_tables()` returns a **nested list** (tables, then rows). An empty list means no table on that page.

### Q2. Compare pypdf, pdfplumber and PyMuPDF in one line each.

**A.** **pypdf:** basic text, images, metadata. **pdfplumber:** layout analysis and tables. **PyMuPDF (`fitz`):** most extensive - text, images, page rendering, links, metadata, annotation.

### Q3. How do you extract an embedded image with PyMuPDF?

**A.** `page.get_images()` for metadata incl. **`xref`**, then `doc.extract_image(xref)` giving image **bytes** and **extension**; write bytes to a file in `wb` mode.

### Q4. How do you highlight a word in a PDF with PyMuPDF?

**A.** `page.search_for(term)` returns bounding boxes; call `page.add_highlight_annot(rect)` for each; `doc.save(...)`.

### Q5. How do you turn a PDF page into an image?

**A.** `page.get_pixmap()` then `.save("page0.png")` (PyMuPDF only of the three).

---

## CSV and Excel (pandas)

### Q6. What is a DataFrame and where does it live?

**A.** A 2-D tabular structure held **in memory (RAM)**; reading a file loads it, writing saves it back.

### Q7. Match the parameter to its effect: `skiprows`, `header=None`, `names`, `nrows`, `na_values`, `usecols`.

**A.** Skip leading rows; treat first row as data; set custom column names; read only first *n* rows; map placeholder strings (`N/A`, `-999`) to **NaN**; load only chosen columns.

### Q8. Why pass `index=False` to `to_csv` / `to_excel`?

**A.** pandas adds an unnamed row index; `index=False` stops it being written as an extra column.

### Q9. How do you force a column (e.g. zip code) to stay a string when reading Excel?

**A.** `pd.read_excel(path, dtype={"zip": str})` - avoids losing leading zeros.

### Q10. What does `converters` do in `read_excel`?

**A.** Applies a function to **each cell** of a column during load (e.g. replace NA in one column with a fixed name and in another with `None`).

### Q11. What do `df.info()`, `df.describe()`, `df.shape`, `df.dtypes` return?

**A.** Structure, non-null counts and memory; summary statistics (mean, std, min, max); `(rows, columns)` tuple; per-column data types.

---

## Classical OCR

### Q12. What are the two stages of the classical OCR pipeline and the tools for each?

**A.** **Preprocess** with Pillow / OpenCV, then **recognise** with **pytesseract**.

### Q13. Why must images be preprocessed before Tesseract?

**A.** Raw, noisy, skewed or thick/thin text gives very poor recognition; preprocessing makes characters clean and high contrast.

### Q14. What does `cv2.threshold(src, thresh, maxval, type)` do?

**A.** Binarises a greyscale image - with `THRESH_BINARY`, pixels above `thresh` become `maxval`, others 0. Only two pixel values remain.

### Q15. Erosion vs dilation?

**A.** **Erosion** thins strokes; **dilation** thickens them. Both use a **kernel** (small matrix) and an **iteration** count. Typical pattern: invert, apply, invert back.

### Q16. How does the lecture’s noise-removal function work?

**A.** Dilate (thicker stroke swallows specks), erode (back to normal width), then **`medianBlur`** (each pixel set to the median of its neighbourhood).

### Q17. Pillow vs OpenCV - when would you choose each?

**A.** Pillow for simple tasks (open, rotate, resize, crop, `convert("L")`). OpenCV for richer processing (invert, threshold, morphology, blur).

---

## Vision-model OCR

### Q18. Why base64-encode the image for an OpenAI vision call?

**A.** The image must travel inside a JSON message; base64 turns binary into an ASCII string sent as an `image_url` (data URL) content part.

### Q19. What does a multimodal user message look like?

**A.** `content` is a **list**: one `{"type": "text", ...}` part (the prompt) and one `{"type": "image_url", ...}` part.

### Q20. How do you get JSON back and keep cost bounded?

**A.** `response_format={"type": "json_object"}` and a cap such as `max_completion_tokens`.

### Q21. What failure cases must response-handling code cover?

**A.** **`refusal`** set, **`content` is `None`**, and invalid JSON; only then parse and save.

### Q22. Where should an API key live?

**A.** In an **environment variable** (e.g. `OPENAI_API_KEY`) - never hard-coded in source.

### Q23. Give two advantages and two drawbacks of vision-LLM OCR over Tesseract.

**A.** Advantages: handles handwriting and layout, returns structured JSON, little preprocessing. Drawbacks: per-token cost, data sent to a third party, possible refusals or hallucinated fields.

---

## FastAPI limits and Celery

### Q24. Why is FastAPI `async` not enough for heavy tasks?

**A.** It interleaves tasks **waiting on I/O** but runs on one process and one machine; CPU-bound or long tasks still **block** others. No true parallelism.

### Q25. Name the three components of a Celery system.

**A.** **Client/producer** (enqueues), **broker / task queue** (Redis or RabbitMQ), **worker(s)** (execute tasks). Plus a **result store**.

### Q26. What does `.delay()` do?

**A.** Enqueues the task on the broker instead of running it inline; the caller returns immediately.

### Q27. Describe the Celery request flow.

**A.** `.delay()` enqueues, client gets an immediate reply, a worker takes **one task at a time**, runs it, stores the result; the client reads the result later.

### Q28. How can Celery scale out?

**A.** Run **multiple workers**, including on different machines, so tasks execute in parallel.

### Q29. What three terminals/processes did the demo need?

**A.** `redis-server` (broker), `celery -A task worker` (worker), and the client calling `process.delay(2, 3)`.

### Q30. Why does the instructor add `sleep` to the demo task?

**A.** To simulate a heavy job (big PDF, OCR, LLM call) and make the blocking behaviour visible when run without Celery.
