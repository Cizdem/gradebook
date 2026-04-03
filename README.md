# Gradebook

A command-line gradebook manager written in Python.

---

## Setup

### 1. Clone / download the project

```bash
git clone github.com/Cizdem/gradebook
cd gradebook
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows
.venv\Scripts\activate
```

### 3. Install dependencies

There are no third-party dependencies. The project uses only the Python standard library.

---

## Seed sample data

Run the seed script to populate `data/gradebook.json` with sample students, courses, enrollments, and grades:

```bash
python scripts/seed.py
```

**Expected output:**

```
Added students: Alice (1), Bob (2), Carol (3)
Added courses: CS101, MA201
Enrolled students in courses.
Added grades.
Saved to data/gradebook.json
```

---

## CLI Usage

All commands are run via `python main.py <subcommand> [options]`.

### Add a student

```bash
python main.py add-student --name "Diana Prince"
# Student added with ID 4: 'Diana Prince'
```

### Add a course

```bash
python main.py add-course --code CS101 --title "Intro to CS"
# Course added: [CS101] Intro to CS
```

### Enroll a student

```bash
python main.py enroll --student-id 1 --course CS101
# Student 1 enrolled in course 'CS101'.
```

### Add a grade

```bash
python main.py add-grade --student-id 1 --course CS101 --grade 95
# Grade 95.0 added for student 1 in 'CS101'.
```

### List students / courses / enrollments

```bash
python main.py list students
python main.py list courses
python main.py list enrollments
```

### Compute average grade

```bash
python main.py avg --student-id 1 --course CS101
# Average for student 1 in 'CS101': 90.00
```

### Compute GPA

```bash
python main.py gpa --student-id 1
# GPA for student 1: 84.00
```

---

## Running Tests

```bash
python -m pytest tests/
# or with the built-in runner:
python -m unittest discover -s tests
```

---

## Project Structure

```
gradebook/
├── gradebook/
│   ├── __init__.py       # Package init; re-exports key symbols
│   ├── models.py         # Student, Course, Enrollment data classes
│   ├── storage.py        # JSON persistence (load_data / save_data)
│   ├── service.py        # Business logic (pure functions)
│   └── validators.py     # Input validation helpers (parse_grade, etc.)
├── tests/
│   └── test_service.py   # Unit tests (unittest)
├── scripts/
│   └── seed.py           # Sample-data seeder
├── data/
│   └── gradebook.json    # Persisted data (auto-created)
├── logs/
│   └── app.log           # Application log (auto-created)
├── main.py               # CLI entry point (argparse)
└── README.md
```

---

## Design Decisions & Limitations

### Design decisions

- **Flat JSON file** — chosen for simplicity and zero dependencies. The entire dataset is loaded into memory on every CLI invocation and written back atomically. This is fast enough for small gradebooks (hundreds of students/courses).
- **Pure service functions** — `service.py` receives the in-memory `data` dict and returns values or raises `ValueError`. This makes unit-testing trivial (no patching of globals) and keeps I/O out of business logic.
- **Model objects in memory, dicts on disk** — `Student`, `Course`, and `Enrollment` provide validation and a clean API; `to_dict` / `from_dict` handle (de)serialisation without a third-party library.
- **Relative imports inside the package** — `storage.py` uses `from .models import …` to demonstrate relative imports, as required.
- **Logging to file only** — console output is kept clean (friendly messages only); all INFO/ERROR records go to `logs/app.log`.

### Limitations

- **No concurrent access safety** — two processes writing simultaneously will corrupt the JSON file.
- **Full reload on every command** — unsuitable for very large datasets; a database back-end (SQLite) would be the natural next step.
- **No authentication** — any user with file access can read/modify all data.
- **Integer student IDs only** — IDs are assigned sequentially and never reused; deleting a student leaves a gap.
