from ib_insync import *
import pandas as pd
from datetime import datetime
import pytz
import matplotlib.pyplot as plt
import numpy as np
import time

def get_historical_data(ib, symbol, exchange='NASDAQ'):
    """Fetch historical minute bar data for a given symbol"""
    contract = Stock(symbol, exchange, 'USD')
    end_time = datetime.now(pytz.timezone('US/Eastern'))
    
    try:
        print(f"\nFetching historical data for {symbol}...")
        bars = ib.reqHistoricalData(
            contract,
            endDateTime=end_time,
            durationStr='6000 S',  # 100 minutes in seconds (100 * 60)
            barSizeSetting='1 min',
            whatToShow='TRADES',
            useRTH=True,
            formatDate=1,
            timeout=30
        )
        
        if bars is None or len(bars) == 0:
            print(f"No data received for {symbol}")
            return None
            
        df = util.df(bars)
        print(f"Received {len(df)} bars for {symbol}")
        return df
        
    except Exception as e:
        print(f"Error fetching data for {symbol}: {str(e)}")
        return None

def process_data(nvda_data, tsm_data):
    """Process OHLC data and return DataFrame with ratios"""
    if nvda_data is None or tsm_data is None:
        print("Failed to get data for one or both stocks")
        return None
        
    try:
        result_df = pd.DataFrame({
            'Time': nvda_data['date'],
            'NVDA_Close': nvda_data['close'],
            'TSM_Close': tsm_data['close']
        })
        
        result_df['Ratio'] = result_df['NVDA_Close'] / result_df['TSM_Close']
        return result_df
        
    except Exception as e:
        print(f"Error processing data: {str(e)}")
        return None

class RatioChart:
    def __init__(self):
        plt.style.use('dark_background')
        self.fig, self.ax = plt.subplots(figsize=(12, 8))
        self.fig.canvas.manager.set_window_title('NVDA/TSM Ratio Chart (Auto-refresh: 10s)')
        plt.ion()  # Enable interactive mode
        
    def update(self, result_df):
        """Update the chart with new data"""
        try:
            self.ax.clear()
            
            # Plot ratio
            self.ax.plot(result_df['Time'], result_df['Ratio'], 'g-', label='NVDA/TSM Ratio')
            
            # Calculate and plot moving average
            ma_window = min(20, len(result_df))
            ma = result_df['Ratio'].rolling(window=ma_window).mean()
            self.ax.plot(result_df['Time'], ma, 'r--', label=f'MA({ma_window})', alpha=0.8)
            
            # Format plot
            self.ax.set_title('NVDA/TSM Price Ratio (1-minute bars)', fontsize=14)
            self.ax.set_xlabel('Time')
            self.ax.set_ylabel('Ratio')
            self.ax.grid(True, alpha=0.3)
            self.ax.legend()
            
            # Rotate x-axis labels
            plt.xticks(rotation=45)
            
            # Add statistics text
            stats_text = f'Statistics:\n'
            stats_text += f'Mean: {result_df["Ratio"].mean():.4f}\n'
            stats_text += f'Std: {result_df["Ratio"].std():.4f}\n'
            stats_text += f'Min: {result_df["Ratio"].min():.4f}\n'
            stats_text += f'Max: {result_df["Ratio"].max():.4f}'
            
            self.ax.text(0.02, 0.98, stats_text,
                        transform=self.ax.transAxes,
                        verticalalignment='top',
                        bbox=dict(boxstyle='round', facecolor='black', alpha=0.8))
            
            # Add current local time at bottom
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S %Z')
            self.ax.text(0.99, 0.02, f'Last Update: {current_time}',
                        transform=self.ax.transAxes,
                        horizontalalignment='right',
                        verticalalignment='bottom',
                        bbox=dict(boxstyle='round', facecolor='black', alpha=0.8))
            
            plt.tight_layout()
            self.fig.canvas.draw()
            self.fig.canvas.flush_events()
            
            print(f"Chart updated at {current_time}")
            
        except Exception as e:
            print(f"Error updating chart: {str(e)}")

def main():
    ib = IB()
    try:
        print("Connecting to TWS...")
        ib.connect('127.0.0.1', 7497, clientId=1, readonly=True)
        
        if not ib.isConnected():
            print("Failed to connect to TWS")
            return
            
        print("Connected successfully")
        
        # Initialize chart
        chart = RatioChart()
        
        # Main loop for continuous updates
        while True:
            try:
                # Get historical data
                nvda_data = get_historical_data(ib, 'NVDA')
                tsm_data = get_historical_data(ib, 'TSM')
                
                # Process and update chart
                result_df = process_data(nvda_data, tsm_data)
                if result_df is not None:
                    chart.update(result_df)
                
                # Check if window is still open
                if not plt.get_fignums():
                    print("Chart window closed. Exiting...")
                    break
                
                # Wait for next update
                for _ in range(10):  # 10 second refresh interval
                    plt.pause(1)  # Check for window close every second
                    if not plt.get_fignums():
                        break
                
            except Exception as e:
                print(f"Error in update loop: {str(e)}")
                plt.pause(1)  # Wait before retrying
        
    except KeyboardInterrupt:
        print("\nStopping monitoring...")
    except Exception as e:
        print(f"Fatal error: {str(e)}")
    finally:
        plt.close('all')
        ib.disconnect()

if __name__ == "__main__":
    main()
