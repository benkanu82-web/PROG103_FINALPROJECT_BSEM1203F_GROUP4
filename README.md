# PROG103_FINALPROJECT_BSEM1203F_GROUP4

## SRMS - Student Record Management System

A GUI-based Python application built for the PROG103: Principles of Structured Programming final project at Limkokwing University of Creative Technology, Sierra Leone Campus.

SRMS helps school administrators manage student records digitally - replacing paper registers with a searchable, visual, and reportable system. The project is aligned with **SDG 4: Quality Education**.

---

## Features

- **Secure Login** - username/password authentication with input validation and a lockout after 3 failed attempts
- **Dashboard** - live statistics (total students, gender, status, academic remarks) plus bar, pie, and line charts
- **Add Record** - form with full input validation (names, contact numbers, grades) and automatic remark calculation
- **View Records** - scrollable table showing all student records
- **Search & Filter** - filter by name, ID, gender, status, or remark
- **PDF Reports** - generate weekly, monthly, yearly, or all-time reports as downloadable PDFs
- **Light/Dark Mode** - toggle theme across the whole application

---

## Tech Stack

- **Python 3.12**
- **tkinter** - graphical user interface
- **matplotlib** - data visualisation (bar, pie, line charts)
- **reportlab** - PDF report generation
- **csv** - data storage

---

## Project Structure

```
PROG103_FINALPROJECT_BSEM1203F_GROUP4/
├── login.py          # Login window and authentication logic
├── dashboard.py       # Main application: dashboard, records, search, reports
├── students.csv       # Student record data
├── reports/            # Generated PDF reports (created automatically)
├── README.md
└── LICENSE
```

---

## How to Run

1. Make sure Python 3.12 (or later) is installed
2. Install the required libraries:
   ```
   pip install matplotlib reportlab
   ```
3. Make sure `login.py`, `dashboard.py`, and `students.csv` are in the same folder
4. Run the application:
   ```
   pytho

---

## Group Members
SEM2 BSEM1203F GROUP4
| Name | Student ID |
|------|------------|
| [Lennard Ben Kanu] | [905005868] |
| [Amadu Borboh Bah] | [905005866] |
| [Ajuno-Sesay Berick Borbordeen] | [905005872] |

**Course:** PROG103 - Principles of Structured Programming
**Examiner:** Elijah Fullah
**Semester:** 02, March – July 2026

--

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
