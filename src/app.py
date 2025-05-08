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

# Initialize session state for theme preference
if "theme" not in st.session_state:
    st.session_state.theme = "retro"  # Default to retro theme

# Set page configuration with meaningful title and layout
st.set_page_config(
    page_title="RetroComputer 8000 - Currency Converter",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def apply_retro_style():
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
        overflow-x: auto;
        max-width: 100%;
    }
    
    /* Table wrapper */
    .table-wrapper {
        overflow-x: auto;
        max-width: 100%;
        margin-bottom: 10px;
    }
    
    /* Currency table */
    .currency-table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 2px;
        font-family: 'VT323', monospace;
        font-size: 18px;
        margin-top: 20px;
        table-layout: fixed;
        overflow: hidden;
    }
    
    .currency-table th, .currency-table td {
        border: 1px solid #33ff33;
        padding: 8px;
        text-align: left;
        background-color: rgba(0, 0, 0, 0.8);
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }
    
    .currency-table th {
        background-color: #004400;
        position: sticky;
        top: 0;
        z-index: 1;
    }
    
    .currency-table tr:hover {
        background-color: #004400;
    }
    
    .currency-table tr:hover td {
        background-color: #004400;
        box-shadow: 0 0 5px #33ff33;
    }
    
    /* Theme toggle switch */
    .theme-toggle {
        position: absolute;
        top: 20px;
        right: 20px;
        z-index: 1000;
    }
    
    .toggle-label {
        display: inline-block;
        margin-right: 10px;
        font-family: 'VT323', monospace;
        color: #33ff33;
        font-size: 16px;
    }
    </style>
    """, unsafe_allow_html=True)

def apply_standard_style():
    """
    Apply a clean, professional standard theme styling.
    Uses a light color scheme with modern UI elements.
    """
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500&display=swap');
    
    /* Global modern styling */
    .main {
        background-color: #f8f9fa;
        color: #212529;
        font-family: 'Roboto', sans-serif;
    }
    
    /* Main container styling */
    .block-container {
        border: 1px solid #dee2e6;
        border-radius: 8px;
        padding: 20px;
        box-shadow: 0 0 15px rgba(0, 0, 0, 0.05);
        max-width: 1000px !important;
        background-color: #ffffff;
    }
    
    /* Buttons */
    .stButton>button {
        background-color: #0d6efd;
        color: white;
        border: none;
        border-radius: 4px;
        font-family: 'Roboto', sans-serif;
        width: 100%;
        text-align: center;
        padding: 10px;
        font-size: 16px;
        margin-bottom: 10px;
        transition: all 0.2s;
    }
    
    .stButton>button:hover {
        background-color: #0b5ed7;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    
    /* Text inputs */
    .stTextInput>div>div>input, .stNumberInput>div>div>input {
        background-color: #ffffff;
        color: #212529;
        border: 1px solid #ced4da;
        border-radius: 4px;
        font-family: 'Roboto', sans-serif;
        padding: 10px;
    }
    
    /* Dialog text box styling */
    .dialog-text {
        background-color: #f8f9fa;
        color: #212529;
        border: 1px solid #dee2e6;
        padding: 15px;
        font-family: 'Roboto', sans-serif;
        margin-bottom: 20px;
        font-size: 16px;
        position: relative;
        border-radius: 8px;
    }
    
    .dialog-header {
        color: #0d6efd;
        margin-bottom: 10px;
        font-weight: 500;
        font-size: 18px;
    }
    
    /* Header */
    .standard-header {
        padding: 20px;
        margin-bottom: 30px;
        text-align: center;
        background-color: #ffffff;
        border-bottom: 1px solid #dee2e6;
    }
    
    /* For select boxes */
    .stSelectbox>div>div>div {
        background-color: #ffffff !important;
        color: #212529 !important;
        border: 1px solid #ced4da !important;
        border-radius: 4px !important;
    }
    
    /* System stats display */
    .system-stats {
        font-family: 'Roboto', sans-serif;
        font-size: 14px;
        color: #6c757d;
        border-top: 1px solid #dee2e6;
        margin-top: 20px;
        padding-top: 10px;
    }
    
    /* Result box */
    .result-box {
        background-color: #e9ecef;
        color: #212529;
        border: 1px solid #dee2e6;
        padding: 20px;
        margin: 20px 0;
        font-family: 'Roboto', sans-serif;
        font-size: 18px;
        text-align: center;
        border-radius: 8px;
    }
    
    /* Chart container */
    .chart-container {
        background-color: #ffffff;
        border: 1px solid #dee2e6;
        padding: 15px;
        margin-top: 20px;
        border-radius: 8px;
        overflow-x: auto;
        max-width: 100%;
    }
    
    /* Table wrapper */
    .table-wrapper {
        overflow-x: auto;
        max-width: 100%;
        margin-bottom: 10px;
    }
    
    /* Currency table */
    .currency-table {
        width: 100%;
        border-collapse: collapse;
        font-family: 'Roboto', sans-serif;
        font-size: 14px;
        margin-top: 20px;
        table-layout: fixed;
        overflow: hidden;
    }
    
    .currency-table th, .currency-table td {
        border: 1px solid #dee2e6;
        padding: 8px;
        text-align: left;
        background-color: #ffffff;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }
    
    .currency-table th {
        background-color: #f8f9fa;
        position: sticky;
        top: 0;
        z-index: 1;
        font-weight: 500;
    }
    
    .currency-table tr:hover {
        background-color: #f1f3f5;
    }
    
    .currency-table tr:hover td {
        background-color: #f1f3f5;
    }
    
    /* Theme toggle switch */
    .theme-toggle {
        position: absolute;
        top: 20px;
        right: 20px;
        z-index: 1000;
    }
    
    .toggle-label {
        display: inline-block;
        margin-right: 10px;
        font-family: 'Roboto', sans-serif;
        color: #212529;
        font-size: 14px;
    }
    </style>
    """, unsafe_allow_html=True)

def apply_theme_style():
    """Apply styling based on the current theme setting"""
    if st.session_state.theme == "retro":
        apply_retro_style()
    else:
        apply_standard_style()

def display_system_info():
    """
    Display a system information box with current date and time.
    Style depends on the current theme setting.
    
    Returns:
        str: Formatted system information
    """
    now = datetime.now()
    
    if st.session_state.theme == "retro":
        # Retro-styled ASCII art box
        system_info = f"""
        ╔═══════════════════════════════════════════════════╗
        ║ RETRO-COMPUTER 8000 | CURRENCY v1.0               ║
        ║ DATE: {now.strftime('%Y-%m-%d')} | TIME: {now.strftime('%H:%M:%S')} ║
        ║ MEMORY: 64K RAM SYSTEM  38911 BASIC BYTES FREE    ║
        ╚═══════════════════════════════════════════════════╝
        """
    else:
        # Modern info display
        system_info = f"""
        Currency Converter v1.0
        Date: {now.strftime('%Y-%m-%d')} | Time: {now.strftime('%H:%M:%S')}
        © 2025 Modern Systems Inc.
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
    <div class="table-wrapper">
    <table class="currency-table">
        <thead>
            <tr>
                <th style="width: 25%;">Timestamp</th>
                <th style="width: 15%;">From</th>
                <th style="width: 20%;">Amount</th>
                <th style="width: 15%;">To</th>
                <th style="width: 25%;">Result</th>
            </tr>
        </thead>
        <tbody>
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
    
    table_html += """
        </tbody>
    </table>
    </div>
    """
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
    <div class="table-wrapper">
    <table class="currency-table">
        <thead>
            <tr>
                <th style="width: 60%;">Currency</th>
                <th style="width: 40%;">Rate</th>
            </tr>
        </thead>
        <tbody>
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
    
    table_html += """
        </tbody>
    </table>
    </div>
    """
    return table_html

def toggle_theme():
    """Toggle between retro and standard themes"""
    if st.session_state.theme == "retro":
        st.session_state.theme = "standard"
    else:
        st.session_state.theme = "retro"
    st.rerun()  # Rerun the app to apply the new theme

def main():
    """
    Main application function that sets up the Streamlit interface and handles user interactions.
    """
    # Apply styling based on current theme
    apply_theme_style()
    
    # Initialize session state for conversion history
    if "conversion_history" not in st.session_state:
        st.session_state.conversion_history = []
    
    # Theme toggle
    col_toggle, col_spacer = st.columns([1, 5])
    with col_toggle:
        theme_label = "🌙 Retro" if st.session_state.theme == "retro" else "☀️ Standard"
        if st.button(f"Switch to {theme_label}", key="theme_toggle"):
            toggle_theme()
    
    # Header with styling based on theme
    if st.session_state.theme == "retro":
        st.markdown("""
        <div class='retro-header'>
            <h1 class='title-neon' style='color: #33ff33; font-size: 36px;'>CURRENCY CONVERTER v1.0</h1>
            <p style='color: #33ff33; font-size: 20px;'>INTERNATIONAL TRADING SYSTEM</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class='standard-header'>
            <h1 style='color: #0d6efd; font-size: 32px;'>Currency Converter</h1>
            <p style='color: #6c757d; font-size: 18px;'>International Currency Exchange Tool</p>
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
            if st.session_state.theme == "retro":
                st.markdown(f"<pre style='color: #33ff33; font-family: VT323, monospace;'>{display_system_info()}</pre>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='color: #6c757d; font-family: Roboto, sans-serif; background-color: #f8f9fa; padding: 10px; border-radius: 4px; border: 1px solid #dee2e6;'>{display_system_info()}</div>", unsafe_allow_html=True)
            
            # Theme-appropriate footer
            if st.session_state.theme == "retro":
                st.markdown("""
                <div class="system-stats">
                    <p>SYSTEM PERFORMANCE: NOMINAL</p>
                    <p>EXCHANGE DATA: ONLINE</p>
                    <p>CONNECTION: SECURE</p>
                    <p>(C) RETRO SYSTEMS INC. 2025</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="system-stats">
                    <p>System Status: Online</p>
                    <p>Data Source: Open Exchange Rates API</p>
                    <p>© 2025 Modern Systems Inc.</p>
                </div>
                """, unsafe_allow_html=True)
            
        except Exception as error:
            # Handle any unexpected errors in the sidebar
            st.error(f"Error displaying exchange rates: {str(error)}")

# Run the application
if __name__ == "__main__":
    main()