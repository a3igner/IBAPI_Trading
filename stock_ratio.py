from ib_insync import *
import pandas as pd
from datetime import datetime, timedelta
import pytz
import time

class StockPairMonitor:
    def __init__(self, ib, symbols, exchange='NASDAQ'):
        self.ib = ib
        self.symbols = symbols
        self.exchange = exchange
        self.contracts = {sym: Stock(sym, exchange, 'USD') for sym in symbols}
        self.last_update = {sym: None for sym in symbols}
        self.last_prices = {sym: None for sym in symbols}
        
    def start_price_monitoring(self):
        """Start real-time price monitoring for all symbols"""
        for contract in self.contracts.values():
            # Request delayed market data if real-time is not available
            self.ib.reqMktData(contract, '', False, False)  # snapshot=False, regulatorySnapshot=False
            
    def on_price_change(self, tickers):
        """Called when price updates are received"""
        for ticker in tickers:
            if hasattr(ticker, 'contract') and ticker.contract.symbol in self.symbols:
                if hasattr(ticker, 'last') and ticker.last is not None:
                    self.last_update[ticker.contract.symbol] = datetime.now()
                    self.last_prices[ticker.contract.symbol] = ticker.last
            
    def should_refresh_data(self):
        """Check if any symbol has new price data"""
        current_time = datetime.now()
        return any(
            last_update is not None and (current_time - last_update).seconds < 5
            for last_update in self.last_update.values()
        )

def get_historical_data(ib, symbol, exchange='NASDAQ'):
    """
    Fetch historical minute bar data for a given symbol
    """
    contract = Stock(symbol, exchange, 'USD')
    
    # Calculate end time as current time
    end_time = datetime.now(pytz.timezone('US/Eastern'))
    
    try:
        # Request historical data with proper duration format
        bars = ib.reqHistoricalData(
            contract,
            endDateTime=end_time,
            durationStr='10800 S',  # Last 3 hours (3 * 60 * 60 seconds)
            barSizeSetting='1 min',  # 1-minute bars
            whatToShow='TRADES',
            useRTH=True,
            formatDate=1,
            timeout=10  # Add timeout to prevent hanging
        )
        
        if bars is None or len(bars) == 0:
            print(f"No data received for {symbol}")
            return None
            
        return util.df(bars)
    except Exception as e:
        print(f"Error fetching data for {symbol}: {str(e)}")
        return None

def process_and_display_data(nvda_data, tsm_data):
    """Process and display OHLC data and ratios"""
    if nvda_data is None or tsm_data is None:
        print("Failed to get data for one or both stocks")
        return
        
    # Create a DataFrame with OHLC prices for both stocks
    result_df = pd.DataFrame({
        'Time': nvda_data['date'],
        'NVDA_Open': nvda_data['open'],
        'NVDA_High': nvda_data['high'],
        'NVDA_Low': nvda_data['low'],
        'NVDA_Close': nvda_data['close'],
        'TSM_Open': tsm_data['open'],
        'TSM_High': tsm_data['high'],
        'TSM_Low': tsm_data['low'],
        'TSM_Close': tsm_data['close']
    })
    
    # Calculate NVDA/TSM ratios for each price type
    result_df['Open_Ratio'] = result_df['NVDA_Open'] / result_df['TSM_Open']
    result_df['High_Ratio'] = result_df['NVDA_High'] / result_df['TSM_High']
    result_df['Low_Ratio'] = result_df['NVDA_Low'] / result_df['TSM_Low']
    result_df['Close_Ratio'] = result_df['NVDA_Close'] / result_df['TSM_Close']
    
    # Clear screen and display updated data
    print("\033[H\033[J")  # Clear screen
    print(f"\nData updated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\nLast 10 entries of price data and ratio:")
    print(result_df.tail(10))
    
    # Calculate statistics for each ratio type
    print("\nCurrent Ratios:")
    print(f"Open Ratio:   {result_df['Open_Ratio'].iloc[-1]:.4f}")
    print(f"High Ratio:   {result_df['High_Ratio'].iloc[-1]:.4f}")
    print(f"Low Ratio:    {result_df['Low_Ratio'].iloc[-1]:.4f}")
    print(f"Close Ratio:  {result_df['Close_Ratio'].iloc[-1]:.4f}")
    
    print("\nRatio Statistics (based on Close Ratio):")
    print(f"Mean Ratio: {result_df['Close_Ratio'].mean():.4f}")
    print(f"Max Ratio:  {result_df['Close_Ratio'].max():.4f}")
    print(f"Min Ratio:  {result_df['Close_Ratio'].min():.4f}")

def main():
    # Connect to IB TWS
    ib = IB()
    try:
        # Connect in read-only mode
        ib.connect('127.0.0.1', 7497, clientId=1, readonly=True)
        
        # Check if connected
        if not ib.isConnected():
            print("Failed to connect to TWS. Please make sure TWS or IB Gateway is running and properly configured.")
            return
            
        print("Connected to TWS successfully")
        
        # Initialize stock pair monitor
        monitor = StockPairMonitor(ib, ['NVDA', 'TSM'])
        
        # Set up price update callback
        ib.pendingTickersEvent += monitor.on_price_change
        
        # Start price monitoring
        monitor.start_price_monitoring()
        
        print("Starting continuous monitoring. Press Ctrl+C to exit.")
        
        # Main loop for continuous updates
        while True:
            ib.sleep(1)  # Allow time for price updates
            
            # Check if we should refresh the data
            if monitor.should_refresh_data():
                nvda_data = get_historical_data(ib, 'NVDA')
                tsm_data = get_historical_data(ib, 'TSM')
                process_and_display_data(nvda_data, tsm_data)
            
    except KeyboardInterrupt:
        print("\nStopping monitoring...")
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        ib.disconnect()

if __name__ == "__main__":
    main()
