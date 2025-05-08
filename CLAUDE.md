# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Tool-currency is a retro-themed currency converter built with Streamlit, featuring a nostalgic 80s terminal interface. The application allows users to convert between 12 major global currencies with real-time exchange rates when available.

## Repository Structure

```
tool-currency/
├── data/
│   └── currencies.json      # JSON file containing currency data
├── mood/                    # Contains reference styling code
│   └── retro_terminal_dialogue.py
├── src/
│   ├── app.py               # Main Streamlit application
│   └── currency_utils.py    # Utility functions for currency conversion
├── run.sh                   # Convenience script to run the application
├── requirements.txt         # Python dependencies
├── LICENSE                  # MIT License
└── README.md                # Project documentation
```

## Common Development Commands

### Setup Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment (macOS/Linux)
source venv/bin/activate

# Activate virtual environment (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Application

```bash
# Using the convenience script
./run.sh

# Or directly with Streamlit
streamlit run src/app.py
```

## Development Notes

- The application uses the Open Exchange Rates API for live exchange rates when available, with a fallback to sample data.
- Styling is inspired by retro terminal interfaces, using the VT323 monospace font and a green-on-black color scheme.
- The application stores conversion history in the session state, which is cleared when the app is restarted.

## License

This project is licensed under the MIT License.