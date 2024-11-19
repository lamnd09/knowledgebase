# Knowledge Base Application

This is a Streamlit-based application that serves as a knowledge base for managing and querying documents. It leverages AI capabilities for document analysis and interactive querying, designed to streamline knowledge retrieval.

---

## Features

- 📚 **Knowledge Base Management**:
- Upload and manage documents.
- AI-driven insights and analysis.
- 🔍 **Ask Your Document**:
- Query documents interactively.
- Extract specific information with ease.
- 🛠 **Customizable**:
- Supports additional pages and features for extensibility.

---

## Requirements

The application depends on Python and several Python libraries. These can be installed via the provided `requirements.txt` file.

### Dependencies

- Python 3.9 or later
- Key Python libraries (from `requirements.txt`):
- Streamlit
- Other necessary packages listed in the `requirements.txt`.

---

## Installation

### Clone the Repository

```bash

git clonehttps://github.com/your-username/knowledgebase-main.git

cd knowledgebase-main

```

### Install Dependencies

Use pip to install the required Python packages:

```bash

pip install-rrequirements.txt

```

---

## Usage

### Run the Application

Launch the application using the following command:

```bash

streamlit run1_📚_T24_Knowledge_Base.py

```

### Access the App

- Open your web browser and navigate to:

  ```

  http://localhost:8501

  ```

---

## Docker Deployment

### Build the Docker Image

To containerize the app:

```bash

docker build-tknowledgebase-app.

```

### Run the Docker Container

```bash

docker run-p8501:8501knowledgebase-app

```

---

## Folder Structure

```

knowledgebase-main/

│

├── 1_📚_T24_Knowledge_Base.py   # Main application file

├── pages/

│   └── 2_📕_Ask_Your_document.py # Additional pages for the app

├── requirements.txt             # List of Python dependencies

├── README.md                    # Documentation (this file)

├── logo.png                     # Logo for the app

└── .gitignore                   # Git ignore rules

```

---

## Contributing

Contributions are welcome! Feel free to fork this repository, make changes, and submit a pull request.

---

## License

This project is licensed under the **MIT License**. See the `LICENSE` file for details.

---
