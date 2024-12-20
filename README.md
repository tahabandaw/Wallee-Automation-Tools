# README for "Wallee Transaction Export Tool"

This repository contains a Python-based desktop application that integrates with the Wallee API to retrieve and export transaction data. The app allows users to specify date ranges for querying settled bank transactions and supports both "Charge" and "Refund" transaction types. The output is saved as a CSV file for further use.

## Features

- **Interactive GUI**: Built using `tkinter` for ease of use.
- **Wallee API Integration**: Fetches settled bank transactions for a given date range.
- **Data Validation**: Ensures accurate and valid input data through a robust validation system.
- **Export Functionality**: Outputs transaction details to a CSV file.
- **Multi-threaded Execution**: Ensures smooth UI interaction by running API requests in a separate thread.

---

## Prerequisites

To run this application, you need:

1. **Python 3.7+** installed on your machine.
2. The following Python libraries:
   - `wallee`
   - `pandas`
   - `tkinter` (comes pre-installed with Python)

Install required dependencies using:

```bash
pip install wallee pandas
```

---

## How to Run

1. Clone this repository:

```bash
git clone https://github.com/your-username/wallee-transaction-export.git
```

2. Navigate to the project directory:

```bash
cd wallee-transaction-export
```

3. Run the application:

```bash
python wallee_transaction_tool.py
```

---

## Usage

1. Enter the **start date** and **end date** for the transaction query in the respective fields.
2. Click **Export** to fetch and save the transaction data.
3. The results are saved in `C:/Users/Public/` with a filename based on the end date.

---

## Folder Structure

```plaintext
.
|-- README.md           # Documentation
|-- wallee_transaction_tool.py  # Main application script
```

---

## Key Considerations

- Ensure your Wallee API credentials (`user_id` and `api_secret`) are set up in the code.
- Check for write permissions in the output directory.
- Handle sensitive data (e.g., API secrets) securely.

---

## Contributing

Feel free to fork this repository and submit pull requests. Contributions are always welcome!

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.
