"""
Tool-Currency Converter Application

A retro-themed currency converter built with Streamlit, featuring a
nostalgic 80s terminal interface and real-time currency conversion.
"""
import streamlit as st
from datetime import datetime
import json
import os
import sys

# Add the parent directory to sys.path to import from src
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.currency_utils import (
    load_currencies, 
    get_currency_codes, 
    get_currency_name, 
    get_currency_symbol,
    get_exchange_rates, 
    convert_currency
)

# Set page configuration with meaningful title and layout
st.set_page_config(
    page_title="RetroComputer 8000 - Currency Converter",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def apply_terminal_style():
    """
    Apply retro-themed styling with VT323 font and green-on-black theme.
    
    Uses custom CSS with various retro effects like glowing text, scanlines,
    and terminal-style UI elements.
    """
    # CSS for enhanced 80s retro terminal look
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=VT323&display=swap');
    
    /* Global retro styling */
    .main {
        background-color: #000;
        color: #33ff33;
        font-family: 'VT323', monospace;
    }
    
    /* Main container styling with terminal border */
    .block-container {
        border: 2px solid #33ff33;
        border-radius: 5px;
        padding: 20px;
        box-shadow: 0 0 10px #33ff33;
        max-width: 1000px !important;
    }
    
    /* Buttons */
    .stButton>button {
        background-color: #000;
        color: #33ff33;
        border: 2px solid #33ff33;
        border-radius: 0;
        font-family: 'VT323', monospace;
        width: 100%;
        text-align: left;
        padding: 15px;
        font-size: 20px;
        margin-bottom: 10px;
        box-shadow: 0 0 5px #33ff33;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        background-color: #33ff33;
        color: #000;
        transform: translateX(5px);
    }
    
    /* Text inputs */
    .stTextInput>div>div>input, .stNumberInput>div>div>input {
        background-color: #000;
        color: #33ff33;
        border: 2px solid #33ff33;
        border-radius: 0;
        font-family: 'VT323', monospace;
        padding: 10px;
        box-shadow: 0 0 5px #33ff33;
    }
    
    /* Sidebar styling */
    .css-1kyxreq, .css-1d391kg, .css-1oe6wy4 {
        background-color: #000;
        color: #33ff33;
    }
    
    .css-1kyxreq a, .css-1d391kg a, .css-1oe6wy4 a {
        color: #33ffff !important;
    }
    
    /* Dialog text box styling */
    .dialog-text {
        background-color: #000;
        color: #33ff33;
        border: 2px solid #33ff33;
        padding: 15px;
        font-family: 'VT323', monospace;
        margin-bottom: 20px;
        font-size: 20px;
        position: relative;
        box-shadow: 0 0 5px #33ff33;
    }
    
    .dialog-header {
        color: #ffffff;
        margin-bottom: 10px;
        font-weight: bold;
        font-size: 22px;
        text-shadow: 0 0 5px #33ff33;
    }
    
    /* Blinking cursor */
    .terminal-cursor {
        display: inline-block;
        background-color: #33ff33;
        width: 10px;
        height: 20px;
        animation: blink 1s step-end infinite;
    }
    
    @keyframes blink {
        50% { opacity: 0; }
    }
    
    /* Header with scanlines effect */
    .retro-header {
        position: relative;
        padding: 20px;
        margin-bottom: 30px;
        text-align: center;
        overflow: hidden;
    }
    
    .retro-header::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: repeating-linear-gradient(
            transparent 0px,
            transparent 2px,
            rgba(0, 0, 0, 0.3) 3px,
            rgba(0, 0, 0, 0.3) 3px
        );
        pointer-events: none;
    }
    
    /* For select boxes */
    .stSelectbox>div>div>div {
        background-color: #000 !important;
        color: #33ff33 !important;
        border: 2px solid #33ff33 !important;
    }
    
    /* Simple system stats display */
    .system-stats {
        font-family: 'VT323', monospace;
        font-size: 16px;
        color: #33ff33;
        border-top: 1px dashed #33ff33;
        margin-top: 20px;
        padding-top: 10px;
    }
    
    /* Neon flicker animation for the title */
    .title-neon {
        animation: neon-flicker 3s infinite alternate;
        text-shadow: 0 0 10px #33ff33, 0 0 20px #33ff33;
    }
    
    @keyframes neon-flicker {
        0%, 19%, 21%, 23%, 25%, 54%, 56%, 100% {
            text-shadow: 0 0 10px #33ff33, 0 0 20px #33ff33;
        }
        20%, 24%, 55% {
            text-shadow: none;
        }
    }
    
    /* Result box */
    .result-box {
        background-color: #000;
        color: #33ff33;
        border: 2px solid #33ff33;
        padding: 20px;
        margin: 20px 0;
        font-family: 'VT323', monospace;
        font-size: 24px;
        text-align: center;
        box-shadow: 0 0 10px #33ff33;
    }
    
    /* Chart container */
    .chart-container {
        background-color: #000;
        border: 2px solid #33ff33;
        padding: 15px;
        margin-top: 20px;
        box-shadow: 0 0 5px #33ff33;
    }
    
    /* Currency table */
    .currency-table {
        width: 100%;
        border-collapse: collapse;
        font-family: 'VT323', monospace;
        font-size: 18px;
        margin-top: 20px;
    }
    
    .currency-table th, .currency-table td {
        border: 1px solid #33ff33;
        padding: 8px;
        text-align: left;
    }
    
    .currency-table th {
        background-color: #004400;
    }
    
    .currency-table tr:hover {
        background-color: #004400;
    }
    </style>
    """, unsafe_allow_html=True)

def display_system_info():
    """
    Display a retro-styled system information box with current date and time.
    
    Returns:
        str: Formatted ASCII art box with system information
    """
    now = datetime.now()
    
    system_info = f"""
    ╔═══════════════════════════════════════════════════╗
    ║ RETRO-COMPUTER 8000 | CURRENCY v1.0               ║
    ║ DATE: {now.strftime('%Y-%m-%d')} | TIME: {now.strftime('%H:%M:%S')} ║
    ║ MEMORY: 64K RAM SYSTEM  38911 BASIC BYTES FREE    ║
    ╚═══════════════════════════════════════════════════╝
    """
    
    return system_info

def create_history_table(conversion_history):
    """
    Create an HTML table displaying conversion history.
    
    Args:
        conversion_history (list): List of conversion records
        
    Returns:
        str: HTML table markup for the conversion history
    """
    table_html = """
    <table class="currency-table">
        <tr>
            <th>Timestamp</th>
            <th>From</th>
            <th>Amount</th>
            <th>To</th>
            <th>Result</th>
        </tr>
    """
    
    # Add rows for each conversion
    for conv in conversion_history:
        # Add simple XSS protection by escaping values
        timestamp = conv["timestamp"].replace("<", "&lt;").replace(">", "&gt;")
        from_currency = conv["from_currency"].replace("<", "&lt;").replace(">", "&gt;")
        to_currency = conv["to_currency"].replace("<", "&lt;").replace(">", "&gt;")
        
        table_html += f"""
        <tr>
            <td>{timestamp}</td>
            <td>{from_currency}</td>
            <td>{conv["amount"]:.2f}</td>
            <td>{to_currency}</td>
            <td>{conv["result"]:.2f}</td>
        </tr>
        """
    
    table_html += "</table>"
    return table_html

def create_rates_table(rates, currency_codes):
    """
    Create an HTML table displaying current exchange rates.
    
    Args:
        rates (dict): Dictionary of exchange rates
        currency_codes (list): List of valid currency codes
        
    Returns:
        str: HTML table markup for the exchange rates
    """
    table_html = """
    <table class="currency-table">
        <tr>
            <th>Currency</th>
            <th>Rate</th>
        </tr>
    """
    
    # Add rows for each currency rate
    for code, rate in rates.items():
        if code in currency_codes:  # Only show rates for our defined currencies
            # Get symbol with fallback to empty string
            symbol = get_currency_symbol(code) or ""
            # Add simple XSS protection
            code_safe = code.replace("<", "&lt;").replace(">", "&gt;")
            symbol_safe = symbol.replace("<", "&lt;").replace(">", "&gt;")
            
            table_html += f"""
            <tr>
                <td>{code_safe} ({symbol_safe})</td>
                <td>{rate:.4f}</td>
            </tr>
            """
    
    table_html += "</table>"
    return table_html

def main():
    """
    Main application function that sets up the Streamlit interface and handles user interactions.
    """
    # Apply styling
    apply_terminal_style()
    
    # Initialize session state for conversion history
    if "conversion_history" not in st.session_state:
        st.session_state.conversion_history = []
    
    # Terminal header with retro styling
    st.markdown("""
    <div class='retro-header'>
        <h1 class='title-neon' style='color: #33ff33; font-size: 36px;'>CURRENCY CONVERTER v1.0</h1>
        <p style='color: #33ff33; font-size: 20px;'>INTERNATIONAL TRADING SYSTEM</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Get all available currencies - do this once at the beginning
    currency_codes = get_currency_codes()
    
    # Check if we have any currencies
    if not currency_codes:
        st.error("ERROR: No currency data available. Please check the data files.")
        return
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    # Currency converter section
    with col1:
        st.markdown("<h2 style='color: #33ff33;'>CURRENCY EXCHANGE TERMINAL</h2>", unsafe_allow_html=True)
        
        # Input for amount
        amount = st.number_input(
            "ENTER AMOUNT:", 
            min_value=0.01, 
            value=100.00, 
            step=10.0,
            help="Enter the amount you want to convert"
        )
        
        # Select boxes for currencies
        col1a, col1b = st.columns(2)
        with col1a:
            from_currency = st.selectbox(
                "FROM CURRENCY:", 
                currency_codes, 
                index=0,
                help="Select the source currency"
            )
        with col1b:
            # Default to a different currency than the 'from' currency if possible
            default_to_index = 1 if len(currency_codes) > 1 else 0
            to_currency = st.selectbox(
                "TO CURRENCY:", 
                currency_codes, 
                index=default_to_index,
                help="Select the target currency"
            )
        
        # Convert button
        if st.button("CONVERT CURRENCY"):
            # Get the conversion result
            result = convert_currency(amount, from_currency, to_currency)
            
            if result is not None:
                # Format the result
                from_symbol = get_currency_symbol(from_currency) or ""
                to_symbol = get_currency_symbol(to_currency) or ""
                
                # Display the result
                st.markdown(f"""
                <div class='result-box'>
                    {from_symbol}{amount:.2f} {from_currency} = {to_symbol}{result:.2f} {to_currency}
                </div>
                """, unsafe_allow_html=True)
                
                # Add to conversion history (limit to last 10 for performance)
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                st.session_state.conversion_history.append({
                    "timestamp": timestamp,
                    "from_currency": from_currency,
                    "to_currency": to_currency,
                    "amount": amount,
                    "result": result
                })
                
                # Keep only the last 10 conversions
                if len(st.session_state.conversion_history) > 10:
                    st.session_state.conversion_history = st.session_state.conversion_history[-10:]
            else:
                st.error("CONVERSION ERROR: Could not retrieve exchange rate.")
        
        # Conversion History Section
        if len(st.session_state.conversion_history) > 0:
            st.markdown("<h3 style='color: #33ff33;'>CONVERSION HISTORY</h3>", unsafe_allow_html=True)
            
            # Display conversion history as a simple table
            st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
            
            # Create HTML table
            table_html = create_history_table(st.session_state.conversion_history)
            st.markdown(table_html, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Add clear history button
            if st.button("CLEAR HISTORY"):
                st.session_state.conversion_history = []
                st.rerun()
    
    # Sidebar with exchange rates and settings
    with col2:
        try:
            # Get exchange rates for USD
            rates, last_update = get_exchange_rates("USD")
            
            st.markdown("<h3 style='color: #33ff33;'>CURRENT EXCHANGE RATES</h3>", unsafe_allow_html=True)
            st.markdown(f"<p style='color: #33ff33;'>Base: USD | Last Update: {last_update}</p>", unsafe_allow_html=True)
            
            # Display exchange rates in a styled table
            st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
            
            # Create rates table
            table_html = create_rates_table(rates, currency_codes)
            st.markdown(table_html, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
            # System information display
            st.markdown(f"<pre style='color: #33ff33; font-family: VT323, monospace;'>{display_system_info()}</pre>", unsafe_allow_html=True)
            
            # Add a retro "system stats" footer
            st.markdown("""
            <div class="system-stats">
                <p>SYSTEM PERFORMANCE: NOMINAL</p>
                <p>EXCHANGE DATA: ONLINE</p>
                <p>CONNECTION: SECURE</p>
                <p>(C) RETRO SYSTEMS INC. 2025</p>
            </div>
            """, unsafe_allow_html=True)
            
        except Exception as error:
            # Handle any unexpected errors in the sidebar
            st.error(f"Error displaying exchange rates: {str(error)}")

# Run the application
if __name__ == "__main__":
    main()