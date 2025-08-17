# **Deduplication Tool**

## **Description**
This application deduplicates records in a JSON dataset based on unique identifiers (`_id` and `email`). It keeps the most recent occurrence of each record, maintaining the original order of the data. The tool also validates JSON records before processing and provides detailed logging throughout the operation.

---

## **Table of Contents**
- [Prerequisites](#prerequisites)
- [Setting Up the Virtual Environment](#setting-up-the-virtual-environment)
- [Installing Dependencies](#installing-dependencies)
- [Usage](#usage)
- [Running the Application](#running-the-application)
- [Command Line Options](#command-line-options)
- [Examples](#examples)
- [Output](#output)
- [Testing](#testing)
- [Project Structure](#project-structure)
- [License](#license)

---

## **Prerequisites**

Before starting with the setup, ensure you have the following installed:

1. **Python 3.x** – The latest version of Python (3.7 or higher recommended).
2. **pip** – Python's package installer (usually comes with Python).
3. **git** – To clone the repository (if applicable).

---

## **Setting Up the Virtual Environment**

To isolate the dependencies and avoid conflicts with other projects, we'll use a virtual environment.

### 1. **Clone the repository (if applicable)**

```bash
git clone https://your-repository-url.git
cd your-project-directory
```

### 2. **Create a virtual environment**

For **Windows**:
```bash
python -m venv venv
```

For **macOS/Linux**:
```bash
python3 -m venv venv
```

### 3. **Activate the virtual environment**

For **Windows**:
```bash
# Command Prompt
venv\Scripts\activate

# PowerShell
venv\Scripts\Activate.ps1

# Git Bash
source venv/Scripts/activate
```

For **macOS/Linux**:
```bash
source venv/bin/activate
```

You should see `(venv)` at the beginning of your command prompt, indicating that the virtual environment is active.

### 4. **Deactivate the virtual environment (when done)**

To deactivate the virtual environment when you're finished working:
```bash
deactivate
```

---

## **Installing Dependencies**

With the virtual environment activated, install the required dependencies:

```bash
pip install -r requirements.txt
```

If `requirements.txt` doesn't exist, create it with the following content:
```txt
# Add any external dependencies here
# Currently, the tool uses only Python standard library modules
```

---

## **Usage**

The deduplication tool is a command-line application that processes JSON files containing lead data. It validates records, removes duplicates, and saves the processed data to a new file.

### **Basic Usage**
```bash
python main.py --input-file input.json --output-file output.json
```

### **With Custom Log File**
```bash
python main.py --input-file data.json --output-file processed.json --log-file custom.log
```

---

## **Running the Application**

### **Step 1: Prepare Your Input File**

Ensure your input JSON file follows this structure:
```json
{
  "leads": [
    {
      "_id": "unique_id_1",
      "email": "user1@example.com",
      "firstName": "John",
      "lastName": "Doe",
      "address": "123 Main St",
      "entryDate": "2024-01-15T10:30:00Z"
    },
    {
      "_id": "unique_id_2",
      "email": "user2@example.com",
      "firstName": "Jane",
      "lastName": "Smith",
      "address": "456 Oak Ave",
      "entryDate": "2024-01-16T14:20:00Z"
    }
  ]
}
```

### **Step 2: Run the Application**

```bash
python main.py --input-file your_data.json --output-file deduplicated_data.json
```

### **Step 3: Follow the Interactive Prompts**

If invalid records are found, the application will:
1. Display validation results
2. Ask if you want to continue with only valid records
3. Wait for your response (y/n)

### **Step 4: Review Results**

The application will display:
- Total number of original records
- Number of valid/invalid records
- Number of final records after deduplication
- Number of duplicates removed
- Output file location

---

## **Command Line Options**

| Option | Required | Description | Default |
|--------|----------|-------------|---------|
| `--input-file` | Yes | Path to the input JSON file | None |
| `--output-file` | Yes | Path to save the processed JSON file | None |
| `--log-file` | No | Path to save the log file | `processing.log` |

---

## **Examples**

### **Example 1: Basic Deduplication**
```bash
python main.py --input-file leads.json --output-file clean_leads.json
```

### **Example 2: Custom Log File**
```bash
python main.py --input-file data/leads.json --output-file data/processed_leads.json --log-file logs/deduplication.log
```

### **Example 3: Processing Large Dataset**
```bash
python main.py --input-file large_dataset.json --output-file cleaned_dataset.json --log-file large_dataset.log
```

---

## **Output**

### **Console Output**
The application provides real-time feedback:
```
Validation Results:
Total records: 1000
Valid records: 995
Invalid records: 5

Warning: 5 invalid records found.
Continue with only valid records? (y/n): y

Final Results:
Original records: 1000
Final records: 850
Removed duplicates: 150
Processed data saved to: output.json
```

### **Log File**
Detailed logging is saved to the specified log file:
```
2024-08-17 10:30:00 - Starting JSON processing
2024-08-17 10:30:00 - Input file: leads.json
2024-08-17 10:30:00 - Output file: clean_leads.json
2024-08-17 10:30:01 - Step 1: Validating records
2024-08-17 10:30:02 - Step 2: Deduplicating records
2024-08-17 10:30:03 - Processing completed successfully
```

### **Output JSON File**
The processed file maintains the same structure as input:
```json
{
  "leads": [
    {
      "_id": "unique_id_1",
      "email": "user1@example.com",
      "firstName": "John",
      "lastName": "Doe",
      "address": "123 Main St",
      "entryDate": "2024-01-15T10:30:00Z"
    }
  ]
}
```

---

## **Testing**

### **Test with Sample Data**

1. Create a test file `test_data.json`:
```json
{
  "leads": [
    {
      "_id": "1",
      "email": "test1@example.com",
      "firstName": "Test",
      "lastName": "User",
      "address": "123 Test St",
      "entryDate": "2024-01-01T00:00:00Z"
    },
    {
      "_id": "1",
      "email": "test1@example.com",
      "firstName": "Test",
      "lastName": "User",
      "address": "123 Test St",
      "entryDate": "2024-01-02T00:00:00Z"
    }
  ]
}
```

2. Run the deduplication:
```bash
python main.py --input-file test_data.json --output-file test_output.json
```

3. Verify the output contains only one record (the most recent one).

### **Error Testing**

Test error handling by:
- Running with non-existent input file
- Using invalid JSON format
- Testing with empty files

---

## **Project Structure**

```
deduplication-tool/
│
├── main.py                 # Main application entry point
├── json_handler.py         # JSON processing and deduplication logic
├── logger.py              # Logging configuration and utilities
├── requirements.txt       # Python dependencies
├── README.md             # This documentation
│
├── data/                 # Sample data files (optional)
│   └── sample_leads.json
│
├── logs/                 # Log files directory
│   └── processing.log
│
└── tests/                # Test files (optional)
    └── test_deduplication.py
```

---

## **Troubleshooting**

### **Common Issues**

1. **"Input file does not exist"**
   - Verify the file path is correct
   - Use absolute paths if relative paths don't work

2. **"Permission denied"**
   - Ensure you have read access to input file
   - Ensure you have write access to output directory

3. **"Invalid JSON format"**
   - Validate your JSON using an online JSON validator
   - Check for trailing commas or syntax errors

4. **"Module not found"**
   - Ensure virtual environment is activated
   - Verify all required files are present in the project directory

---