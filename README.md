# AI-Powered Data Processing Agent

An intelligent full-stack application that empowers users to clean and transform datasets using **natural language instructions**.

This project leverages **Google Gemini LLM** to function as an autonomous agent. Instead of requiring users to manually select columns or write complex Regular Expressions, the system analyzes the user's intent, identifies the target column within the file context, generates the appropriate Python Regex pattern, and executes the data transformation automatically.

---

## Key Features

* **Multi-Format Support:** Handles `.csv`, `.xlsx`, and `.xls` files with automatic encoding detection and data cleaning.
* **AI Agentic Workflow:**
    * **Intent Extraction:** Automatically identifies the target column and replacement logic from a simple sentence.
    * **Regex Generation:** Converts natural language (e.g., "Mask all emails") into valid Python Regex patterns using Gemini 1.5 Flash.
    * **Context Awareness:** Validates AI suggestions against the actual file schema to prevent hallucinations.
* **Interactive UI:**
    * Real-time data preview (React Table).
    * Detailed processing statistics (Matched rows, Replaced rows).
    * Visual display of the generated Regex pattern and AI reasoning.
* **Robust Backend:** Built with Django REST Framework and Pandas for high-performance data manipulation.

---

## Tech Stack

### Backend
* **Framework:** Django 5.x, Django REST Framework (DRF)
* **Data Processing:** Pandas, NumPy, OpenPyXL, XLRD
* **AI/LLM:** Google GenAI SDK (`google-genai`), Gemini 1.5 Flash Model
* **Utilities:** Python `re` module, `python-dotenv`

### Frontend
* **Framework:** React 18, Vite
* **Styling:** CSS3, CSS Modules
* **HTTP Client:** Axios
* **Component Logic:** React Hooks (`useState`, `useEffect`)

---

## Installation & Setup

### Prerequisites
* Python 3.9+
* Node.js 16+
* A Google Gemini API Key

### 1. Backend Setup

```bash
# Clone the repository
git clone <repository_url>
cd <repository_name>

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install django djangorestframework pandas google-genai django-cors-headers python-dotenv openpyxl xlrd

# Run migrations
python manage.py makemigrations
python manage.py migrate
```

**Environment Variables:**
Create a `.env` file in the root directory:

```ini
DJANGO_SECRET_KEY=your_secure_random_string
GEMINI_API_KEY=your_google_gemini_api_key
GEMINI_MODEL_NAME=gemini-1.5-flash
DEBUG=True
```

**Start the Backend Server:**
```bash
python manage.py runserver
```
*The backend will run at `http://127.0.0.1:8000`*

### 2. Frontend Setup

Open a new terminal window and navigate to the frontend directory (or root if using a unified structure).

```bash
# Install dependencies
npm install

# Start the development server
npm run dev
```
*The frontend will run at `http://localhost:3000` (or `5173` depending on Vite version).*

---

## Usage Guide

1.  **Upload File:**
    * Drag and drop a CSV or Excel file into the upload area.
    * The system validates the file size (<10MB) and format.
    * A preview of the first 100 rows will appear.

2.  **Input Instruction:**
    * In the text area, describe what you want to do naturally. The AI will detect the column for you.
    * *Example:* "Replace all email addresses in the **email** column with 'REDACTED'."
    * *Example:* "Change the format of phone numbers in the **contact** column to ***."
    * *Example:* "Remove all numbers from the **name** column."

3.  **Process:**
    * Click **"Run Magic"**.
    * The AI analyzes your file headers and your instruction.
    * It generates a Regex pattern and applies it to the data.

4.  **Review & Download:**
    * View the "Matched Rows" and "Replaced Rows" statistics.
    * Check the generated Regex pattern displayed on the screen.
    * Click **Download Processed Data** to get the cleaned CSV.

---

## Project Structure

```text
├── api/
│   ├── migrations/
│   ├── models.py          # FileDocument model
│   ├── serializers.py     # DRF Serializers
│   ├── urls.py            # API Routes
│   ├── views.py           # Core logic (Upload & Process)
│   └── utils/
│       ├── file_parser.py     # Pandas reading logic
│       ├── llm_service.py     # Gemini AI integration
│       └── regex_processor.py # Regex substitution logic
├── src/                   # React Frontend Source
│   ├── components/
│   │   ├── FileUpload.jsx
│   │   ├── DataTable.jsx
│   │   ├── PatternInput.jsx   # AI Instruction Input
│   │   └── ResultDisplay.jsx
│   ├── services/
│   │   └── api.js         # Axios API calls
│   ├── App.jsx
│   └── main.jsx
├── config/                # Django Settings
├── manage.py
├── vite.config.js         # Vite Configuration
└── README.md
```

---

## API Documentation

### 1. Upload File
* **Endpoint:** `POST /api/upload/`
* **Body:** `Multipart/form-data` (`file`)
* **Response:** JSON containing file preview (`data`, `columns`, `row_count`).

### 2. Process Data
* **Endpoint:** `POST /api/process/`
* **Body:**
    ```json
    {
      "data": [...], // The dataset
      "natural_language_input": "Mask emails in email column"
    }
    ```
* **Response:**
    ```json
    {
      "success": true,
      "processed_data": [...],
      "state": { "matched_rows": 10, "replaced_rows": 10 },
      "ai_analysis": {
        "column_detected": "email",
        "regex_generated": "\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,7}\\b",
        "replacement_used": "REDACTED"
      }
    }
    ```

---

## Security & Limitations

* **Data Privacy:** Uploaded files are processed in memory (or temporarily stored) and should be cleaned up regularly.
* **LLM Hallucinations:** While the system validates that the identified column exists, users should verify the generated Regex pattern for critical data operations.
* **File Size:** Currently limited to 10MB for performance reasons.

---

## License

This project is created for the Rhombus AI Technical Assessment.

---

###  Future Improvements
* Add support for multiple column operations in a single request.
* Implement a "Undo" feature for data changes.
* Add unit tests for the regex generation logic.