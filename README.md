# Tool-Currency

A retro-themed currency converter built with Streamlit, featuring a nostalgic 80s terminal interface.

## Features

- Convert between 12 major global currencies
- Real-time exchange rates (when available)
- Retro-styled terminal interface
- Conversion history tracking
- Current exchange rates display

## Simplified for ARM Compatibility

This application has been simplified to work well on ARM architectures:
- Minimal dependencies: only requires Streamlit and Requests
- No heavy data processing libraries required
- Uses native HTML for tables instead of DataFrames
- Optimized for compatibility across platforms

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/tool-currency.git
   cd tool-currency
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```
   - On Windows:
     ```
     venv\Scripts\activate
     ```

4. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Start the application:
   ```
   ./run.sh
   ```
   or
   ```
   streamlit run src/app.py
   ```

2. Open your web browser and navigate to `http://localhost:8501`

3. Use the interface to:
   - Enter the amount to convert
   - Select source and target currencies
   - View conversion results
   - Track conversion history
   - Monitor current exchange rates

## Deployment

### Local Deployment

For local deployment (beyond the development server):

1. **Docker Deployment** (recommended for production):

   Create a `Dockerfile` in the project root:
   ```dockerfile
   FROM python:3.9-slim

   WORKDIR /app

   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt

   COPY . .

   EXPOSE 8501

   CMD ["streamlit", "run", "src/app.py"]
   ```

   Build and run the Docker container:
   ```bash
   docker build -t tool-currency .
   docker run -p 8501:8501 tool-currency
   ```

2. **SystemD Service** (for Linux systems):

   Create a service file at `/etc/systemd/system/tool-currency.service`:
   ```
   [Unit]
   Description=Tool Currency Converter
   After=network.target

   [Service]
   User=<your-user>
   WorkingDirectory=/path/to/tool-currency
   ExecStart=/path/to/tool-currency/venv/bin/streamlit run src/app.py

   [Install]
   WantedBy=multi-user.target
   ```

   Enable and start the service:
   ```bash
   sudo systemctl enable tool-currency
   sudo systemctl start tool-currency
   ```

### Streamlit Community Cloud Deployment

To deploy to [Streamlit Community Cloud](https://streamlit.io/cloud) (free hosting):

1. Push your repository to GitHub:
   ```bash
   git remote add origin https://github.com/yourusername/tool-currency.git
   git push -u origin main
   ```

2. Sign up for a free account at [share.streamlit.io](https://share.streamlit.io/)

3. Deploy your app:
   - Click "New app" in the Streamlit Cloud dashboard
   - Enter your GitHub repository URL
   - Set the main file path to `src/app.py`
   - Click "Deploy"

4. Your app will be available at a URL like: `https://yourusername-tool-currency-src-app-xyz123.streamlit.app`

5. **Important Configuration**:
   - If your app needs secrets (like API keys), add them via the Streamlit Cloud dashboard:
     1. Go to your app in the dashboard
     2. Click on "Advanced settings" > "Secrets"
     3. Add your secrets in TOML format:
       ```toml
       [openexchangerates]
       api_key = "your_api_key_here"
       ```

## Data Sources

The application uses:
- Sample exchange rates for demonstration
- Open Exchange Rates API when connectivity is available

## Troubleshooting

If you encounter any issues:
- Make sure you have the latest version of Streamlit installed
- The application requires only basic libraries for maximum compatibility
- For ARM-based systems, this version has been specifically optimized to avoid dependency issues

## Version History

- **v1.3 (Current)** - Significant code quality and robustness improvements:
  - Added comprehensive documentation and docstrings
  - Implemented caching for better performance
  - Enhanced error handling and security features
  - Improved startup scripts with better environment detection

- **v1.2** - Simplified dependencies for ARM compatibility:
  - Removed pandas dependency for improved compatibility
  - Added native HTML table generation
  - Reduced external library dependencies

- **v1.1** - Added presentation mode:
  - Created HTML presentation view
  - Added project structure documentation

- **v1.0** - Initial release:
  - Basic currency conversion functionality
  - Retro terminal styling
  - Exchange rate display

## License

This project is licensed under the MIT License - see the LICENSE file for details.