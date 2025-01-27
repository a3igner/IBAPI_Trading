# NVDA/TSM Ratio Chart

A real-time chart application that displays and monitors the price ratio between NVIDIA (NVDA) and TSMC (TSM) stocks using Interactive Brokers API.

## Features

- Real-time price ratio monitoring
- 100-minute historical data with 1-minute bars
- 20-period moving average
- Auto-updates every 10 seconds
- Statistical analysis (mean, std, min, max)
- Support for both real-time and delayed market data
- Current local time display

## Requirements

- Python 3.8 or higher
- Interactive Brokers TWS (Trader Workstation) or IB Gateway
- Market data subscriptions for NVDA and TSM

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/nvda-tsm-ratio-chart.git
cd nvda-tsm-ratio-chart
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running from Source

1. Start TWS/Gateway and log in
2. Run the script:
```bash
python stock_ratio_chart.py
```

### Building Windows Executable

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the build script:
```bash
python build_simple.py
```

3. Find the executable in the `dist` directory

### TWS/Gateway Setup

1. Open TWS/Gateway
2. Go to File -> Global Configuration (or Configure in Gateway)
3. Select "API" -> "Settings" in the left panel
4. Enable "Socket port" and ensure it's set to 7497
5. Check "Enable ActiveX and Socket Clients"
6. Click "Apply" and "OK"

## Project Structure

```
├── stock_ratio_chart.py   # Main application script
├── build_simple.py        # Build script for Windows executable
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
└── LICENSE              # MIT License
```

## Development

To contribute to this project:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Troubleshooting

1. If the chart doesn't appear:
   - Verify TWS/Gateway is running and logged in
   - Check port 7497 is enabled for API connections
   - Ensure you have market data permissions for NVDA and TSM

2. If data isn't updating:
   - Check your internet connection
   - Verify market is open (US market hours)
   - Confirm data subscriptions are active in TWS

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This software is for educational purposes only. Use at your own risk. The authors accept no responsibility for trading losses that may be incurred by using this software.
