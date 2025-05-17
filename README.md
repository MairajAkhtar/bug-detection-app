# 🐛 Bug Detection Analyzer (BDA)

A machine learning-powered web application for analyzing and predicting potential bugs in source code using code metrics.

## 🌟 Features

- 📊 Analyze source code files for potential bugs
- 🤖 ML-powered bug prediction
- 📁 Batch file processing support
- 📈 Detailed metric analysis
- 📑 CSV export of results
- 🔄 CI/CD integration with GitHub webhooks
- 🐋 Docker support

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- Docker (optional)
- Git

### Installation

1. **Clone the repository**
   ```cmd
   git clone <repository-url>
   cd bda
   ```

2. **Set up Python environment**
   ```cmd
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```cmd
   python app.py
   ```
   The application will be available at http://localhost:5000

### 🐋 Docker Installation

1. **Build the Docker image**
   ```cmd
   docker build -t bda-app .
   ```

2. **Run the container**
   ```cmd
   docker run -p 5000:5000 bda-app
   ```
### Environment Variables
- `FLASK_ENV`: Set to 'production' or 'development'
- `FLASK_APP`: Set to 'app.py'
- `PORT`: Default is 5000

### Model
The ML model is automatically downloaded on first run from Google Drive. Manual download link:
[📥 Download model.joblib](https://drive.google.com/file/d/1Ezi8WW3XarglXXz7PDqZalw4ps8IioAX/view?usp=sharing)