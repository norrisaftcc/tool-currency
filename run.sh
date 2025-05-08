#!/bin/bash

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

# Run the Streamlit app
echo "Starting the currency converter app..."
streamlit run src/app.py