NVDA/TSM Ratio Chart Application
==============================

This application displays a real-time chart of the NVDA/TSM price ratio with 1-minute historical data.

Requirements:
------------
1. Interactive Brokers TWS (Trader Workstation) or IB Gateway must be running
2. TWS/Gateway must be configured to accept API connections on port 7497
3. Market data subscriptions for NVDA and TSM

Setup in TWS/Gateway:
-------------------
1. Open TWS/Gateway
2. Go to File -> Global Configuration (or Configure in Gateway)
3. Select "API" -> "Settings" in the left panel
4. Enable "Socket port" and ensure it's set to 7497
5. Check "Enable ActiveX and Socket Clients"
6. Click "Apply" and "OK"

Usage:
------
1. Start TWS/Gateway and log in
2. Double-click NVDA_TSM_Ratio_Chart.exe
3. The chart will automatically:
   - Display 100 minutes of historical 1-minute data
   - Update every 10 seconds
   - Show current local time
4. Close the chart window to exit the application

Features:
--------
- 100-minute historical data with 1-minute bars
- NVDA/TSM price ratio plot
- 20-period moving average
- Real-time statistics (mean, std, min, max)
- Auto-updates every 10 seconds
- Current local time display

Troubleshooting:
--------------
1. If the chart doesn't appear:
   - Verify TWS/Gateway is running and logged in
   - Check port 7497 is enabled for API connections
   - Ensure you have market data permissions for NVDA and TSM

2. If data isn't updating:
   - Check your internet connection
   - Verify market is open (US market hours)
   - Confirm data subscriptions are active in TWS

Note: This application requires an active Internet connection and proper market data subscriptions in your Interactive Brokers account.
