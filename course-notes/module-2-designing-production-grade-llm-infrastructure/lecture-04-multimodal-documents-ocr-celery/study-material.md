# Lecture 04: Multimodal Document Processing, OCR, and Celery

**Course:** AI-Enabled Software Engineering · **Module 2:** Designing Production-Grade LLM Infrastructure  
**Instructor:** Professor, CSE, IIT Kharagpur (name garbled in the transcript)  
**TA / demos:** Salma  
**Running example:** Generic file and image demos (test PDF, CSV/Excel stock sheets, a passport and a PAN card for vision OCR, a `x² + y²` Celery task) - no KaryaSetu code this week  
**Workshop path:** none for this lecture

> **Transcript note:** Source is an auto-captioned transcript (`lecture-04-multimodal-documents-ocr-celery.txt`) with many mis-hearings. Read “Ï PDF / PDF Pamlar / Ï MU PDF” as **pypdf / pdfplumber / PyMuPDF**, “first API” as **FastAPI**, “salary / certainty” as **Celery**, “Pytaselect / pythesilate” as **pytesseract**, “inotion / emotion” as **erosion**, “Unicorn” as **Uvicorn**, “Talker” n/a. The “Sam Watson / Sam Altman” name in the Excel demo is just placeholder text.

---

## Learning outcomes (exam-ready)

By the end of this session you should be able to:

- Compare **pypdf, pdfplumber, PyMuPDF** and pick one for text, tables, images, metadata, rendering, annotation.
- Read and write **CSV** and **Excel** with **pandas** (`read_csv`, `to_csv`, `read_excel`, `to_excel`) using the key parameters.
- Explain the **two-stage OCR pipeline**: preprocess (Pillow / OpenCV) then recognise (pytesseract).
- Describe OpenCV preprocessing: **invert, grayscale, binarise (threshold), erode, dilate, noise removal (median blur)**.
- Run OCR with a **vision LLM** (chat UI and API): base64 image, multimodal message, JSON output, refusal handling, token cap.
- Explain why FastAPI `async` is **not parallelism**, and how **Celery + broker + worker** offloads heavy work.
- Name the three Celery components, the role of `.delay()`, and the result store.

---

## Session map

| Block | Lecture focus | Demo |
|-------|---------------|------|
| **1 - File processing** | PDF (3 libraries), CSV, Excel | Salma: text/table/image extraction, highlight, metadata, pandas read/write |
| **2 - OCR** | Pillow, OpenCV, pytesseract | Rotate, invert; pipeline walkthrough |
| **3 - Vision-model OCR** | OpenAI chat UI and Python API | PAN card to JSON file |
| **4 - APIs and Celery** | FastAPI limits, task queue, workers, Redis | Slow `process(x, y)` blocking vs `.delay()` with Redis + worker |

**Not covered (deferred):** Celery demos with other brokers - **RabbitMQ** next class; prompt versioning for vision prompts also next class.

---

## Part 1: File processing

### PDF libraries at a glance

| Library | Text | Tables | Images | Render page as image | Metadata |
|---------|:----:|:------:|:------:|:--------------------:|:--------:|
| **pypdf** | Yes | Weak | Yes | No | Yes |
| **pdfplumber** | Yes | **Best** | Possible, not preferred | Possible, not preferred | - |
| **PyMuPDF** (`fitz`) | Yes | - | Yes | **Yes** | Yes, plus links, annotation |

Instructor’s framing: pypdf = most basic; pdfplumber = layout and tables; PyMuPDF = most extensive.

### pypdf

```python
from pypdf import PdfReader
reader = PdfReader("test_file.pdf")
len(reader.pages)                 # page count
page = reader.pages[0]            # one page
page.extract_text()               # plain text
for img in page.images:           # images on page
    open(f"page0_image{i}.png", "wb").write(img.data)   # binary data
```

- Loop over `reader.pages` to read the whole document.
- `page.images` returns a **list** (a page can hold several images); write `img.data` in **`wb`** mode.

### pdfplumber

```python
import pdfplumber
with pdfplumber.open("test_file.pdf") as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        tables = page.extract_tables()
```

- `extract_tables()` returns a **nested list**: tables, each a list of rows (row 0 is usually the header).
- A page with no table returns an **empty list** (seen in the demo).

### PyMuPDF (`fitz`)

| Task | API |
|------|-----|
| Open | `doc = fitz.open(path)`; `doc.page_count` |
| Load page | `doc.load_page(i)` or `doc[i]` |
| Text | `page.get_text()` |
| Images | `page.get_images()` gives metadata incl. **`xref`** (reference number, not necessarily 0,1,2) |
| Extract one image | `doc.extract_image(xref)` gives dict with `image` (bytes) and `ext` |
| Render page to PNG | `page.get_pixmap()` then `.save("page0.png")` |
| Links | `page.get_links()` |
| Metadata | `doc.metadata` (title, author, creation date, ...) |
| Highlight text | `page.search_for("term")` returns bounding boxes (`Rect`); `page.add_highlight_annot(rect)` for each; `doc.save(out.pdf)` |

Highlight colour defaults to yellow and can be changed.

### pandas and the DataFrame

- A **DataFrame** is a 2-D tabular structure held in **RAM**. Reading a file loads it into a DataFrame; writing saves it back.
- pandas adds an automatic **row index** (0, 1, 2 ...) with no column name.

### CSV

| Direction | Call | Useful parameters |
|-----------|------|-------------------|
| Read | `pd.read_csv(path)` | `skiprows`, `header=None`, `names=[...]`, `nrows`, `na_values`, `usecols` |
| Write | `df.to_csv(path)` | `columns`, `header=False`, `index=False`, `na_rep` |

| Parameter | Effect |
|-----------|--------|
| `skiprows=n` | Skip first *n* rows |
| `header=None` | First row is **data**, not column names |
| `names=[...]` | Assign your own column names |
| `nrows=n` | Read only the first *n* rows |
| `na_values=[...]` | Treat strings like `"N/A"`, `-1`, `-999` as **NaN** (can be set per column with a dict) |
| `usecols=[...]` | Load only selected columns |
| `index=False` (write) | Do not write the auto index |

Inspecting a DataFrame: `df.head()`, `df.tail()`, `df.info()` (rows, dtypes, non-null counts, memory), `df.describe()` (mean, std, min, max), `df.shape` (tuple of rows, columns), `df.dtypes`.

### Excel

| Direction | Call | Notes |
|-----------|------|-------|
| Read | `pd.read_excel(path, sheet_name=...)` | Same ideas as CSV, plus `sheet_name` and `dtype` |
| Write | `df.to_excel(path, sheet_name=..., header=True/False, index=False)` | |

- `dtype={"account_number": str, "zip": str}` forces string columns (keeps leading zeros).
- **`converters={"col": func}`** runs a function on **every cell** of a column while loading. Demo: replace missing `people` cells with a placeholder name and missing `EPS` cells with `None`.
- Lecture caveat: `header=None` vs `header=0/1` controls whether the first row is treated as column names (in pandas `header=0` is the usual “first row is header”).

---

## Part 2: Classical OCR (preprocess then recognise)

**OCR** = given an image, return machine-readable text. Two steps:

1. **Read and preprocess** the image - Pillow and/or OpenCV.
2. **Recognise** text - **pytesseract** (Python wrapper for Tesseract).

> Skipping preprocessing makes Tesseract perform “severely poorly” on real scans (instructor emphasis).

### Pillow (basic)

| Task | API |
|------|-----|
| Open | `Image.open(path)` |
| Metadata | `img.format`, `img.size` (width, height), `img.mode` (RGB, L, 1) |
| Show | `img.show()` |
| Rotate | `img.rotate(angle)` (counter-clockwise) |
| Resize | `img.resize((800, 600))` |
| Greyscale | `img.convert("L")` |
| Crop | `img.crop((left, upper, right, lower))` |
| Save | `img.save(path)` |

Pillow is simple and limited.

### OpenCV (`cv2`) - richer preprocessing

| Step | API / idea | Purpose |
|------|-----------|---------|
| Read / write | `cv2.imread`, `cv2.imwrite` | I/O (OpenCV loads as **BGR**) |
| Shape | `img.shape` | Height, width |
| **Invert** | `cv2.bitwise_not(img)` | White-on-black swap |
| **Greyscale** | `cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)` | One channel |
| **Binarise** | `cv2.threshold(gray, thresh, maxval, type)` | Each pixel becomes low or high |
| **Erode** (thin font) | invert, `cv2.erode(img, kernel, iterations=n)`, invert back | Shrinks strokes |
| **Dilate** (thick font) | invert, `cv2.dilate(img, kernel, iterations=n)`, invert back | Grows strokes |
| **Noise removal** | dilate then erode (or `morphologyEx`), then `cv2.medianBlur` | Remove speckles |

**Threshold parameters:** source image, threshold, max value, type. Example: `threshold=210`, `maxval=230`, `THRESH_BINARY` - pixel above 210 becomes 230, otherwise 0. Result has only two values.

**Kernel:** small matrix (e.g. `np.ones((2, 2), np.uint8)`) slid over the image like a CNN filter. Bigger kernel or more iterations means stronger effect.

| Operation | Effect on text |
|-----------|----------------|
| Erosion | Thinner strokes |
| Dilation | Thicker strokes |

Why invert first? Morphology operates on **white foreground**; text is normally dark on light, so invert, process, invert back.

**Noise removal logic:** dilating thickens a stroke so it **absorbs nearby specks**; eroding returns the stroke to its original width while the specks are gone. `medianBlur` replaces each pixel with the **median of its neighbourhood**, smoothing remaining noise.

### Recognise with pytesseract

```python
import pytesseract
from PIL import Image
text = pytesseract.image_to_string(Image.open("no_noise.jpg"))
```

Returns a plain string (OCR result). Install Tesseract itself as well as the Python package.

---

## Part 3: Vision-model OCR (OpenAI)

Same input (image) and output (text), but a **multimodal LLM** does the recognition. Benefits shown: reads **handwriting**, understands layout, infers context (e.g. identifies a document as an Indian passport without being told), and returns **structured JSON**.

### Two ways

| Way | Steps |
|-----|-------|
| **Chat UI** | Upload image, prompt e.g. “extract the text from the image and tell me what type of document this is” |
| **Python API** | Encode image, build message, call model, parse response |

### API recipe

1. **Create an API key** in the OpenAI platform (name it, copy once, keep secret).
2. **Base64-encode** the image (`base64.b64encode(...).decode()`) - binary cannot go straight into a prompt.
3. Create the client: `OpenAI(api_key=...)` or rely on the **`OPENAI_API_KEY` environment variable** (do not hard-code keys).
4. Call chat completions with:
   - `model` (a GPT vision-capable model; lecture mentions GPT-4 family)
   - `messages`: `role: "user"`, `content` = list of parts: `{"type": "text", "text": prompt}` and `{"type": "image_url", "image_url": {"url": "data:image/jpeg;base64,..."}}`
   - `response_format={"type": "json_object"}` for JSON output
   - **`max_completion_tokens`** to cap cost (billing is per token)
5. **Handle the response** defensively:
   - If `message.refusal` is set: model refused (blurred image, bad prompt).
   - If `message.content` is `None`: nothing returned.
   - Else `json.loads(content)` and save to a `.json` file.

Demo: PAN card image to a structured JSON file of all fields.

### Classical OCR vs vision-LLM OCR

| | Pillow/OpenCV + Tesseract | Vision LLM |
|---|---|---|
| Preprocessing | **Required** for good results | Mostly not needed |
| Output | Raw string | Can be **structured JSON** with understanding |
| Cost | Free, local | **Per-token** API cost |
| Privacy | Local | Image sent to a third party |
| Failure modes | Garbled text | Refusal, null, hallucinated fields |

---

## Part 4: FastAPI limits and Celery

### Sync vs async recap

- **Synchronous:** client sends a request and waits; slow work (large PDF, big image, LLM call) blocks the caller.
- **Asynchronous (FastAPI `async`):** while request A awaits Gemini/OpenAI, the event loop can start request B (database) and C (processing). Good for **I/O waits**.

### The bottleneck

FastAPI async **switches between tasks; it does not parallelise** them. It runs in **one process on one machine**, so **CPU-bound or long-running tasks block** the others. Fine for short, lightweight work; not for heavy jobs.

### Celery - offload heavy work

Celery is a **distributed task queue**. The web app **enqueues** work and returns immediately; separate **workers** execute it.

| Component | Role | In the demo |
|-----------|------|-------------|
| **Client / producer** | Triggers tasks | The FastAPI app or `client.py` |
| **Broker (task queue / message queue)** | Holds pending tasks | **Redis** (RabbitMQ next class) |
| **Worker (consumer)** | Takes **one task at a time**, executes it | `celery -A task worker` |
| **Result store / backend** | Stores returned results for the client to fetch | Same message system |

**Flow:**

1. Client calls `task.delay(args)` - **enqueues** instead of running inline.
2. Client gets an **immediate response** and moves on (no blocking).
3. A worker dequeues, executes, writes the result to the result store.
4. Client fetches the result when ready.

Key facts:

- **`.delay()`** = “put on the queue”; calling the function directly runs it synchronously.
- Many workers can run, even on **different machines** - horizontal scaling and a distributed system.
- Workers run **in parallel** with the client and with each other.
- Benefits: **scalability, reliability, no user waiting**.

### Demo walk-through

```python
from celery import Celery
app = Celery("task", broker="redis://localhost:6379/0")

@app.task
def process(x, y):
    time.sleep(...)          # fake heavy work
    return x**2 + y**2
```

| Terminal | Command | Observation |
|----------|---------|-------------|
| 1 | `redis-server` | Broker/queue is up |
| 2 | `celery -A task worker` | Worker connects to Redis, waits for tasks |
| 3 | `process.delay(2, 3)` | **Returns instantly**; worker prints progress, finishes, stores result |

Without Celery, `process(2, 3)` **blocks the terminal** until the sleep ends.

---

## Key takeaways

1. Pick the PDF tool by job: **pdfplumber for tables, PyMuPDF for images, rendering, links, annotation, pypdf for simple text**.
2. pandas treats CSV and Excel the same way: load into a **DataFrame**, tune with `na_values`, `usecols`, `dtype`, `converters`, write with `index=False`.
3. Classical OCR = **preprocess (grey, threshold, erode/dilate, denoise) then pytesseract**; skipping preprocessing wrecks accuracy.
4. Vision LLMs do OCR plus understanding and JSON, but cost tokens - **cap tokens, check refusal and null, never hard-code keys**.
5. FastAPI async handles waiting, not heavy compute; **Celery + broker + worker + `.delay()`** gives real background execution.
