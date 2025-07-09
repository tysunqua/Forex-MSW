from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import MetaTrader5 as mt5
import pytz
from datetime import datetime, timedelta
 

# Initialize connection to MetaTrader 5
if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()


# Set the symbol using the correct name from the printed list
# For example, if the list shows "XAU/USD", then use that:
symbol = "DXY"  # Adjust based on what you see on your terminal

# Attempt to select the symbol in the Market Watch
if not mt5.symbol_select(symbol, True):
    print("Failed to select symbol", symbol)
    mt5.shutdown()
    quit()

# Define the time range for tick data: past day in this example
# utc_to = datetime.utcnow()
# utc_from = utc_to - timedelta(days=1)

# Define the time range for tick data: entire year 2025
utc_from = datetime(2020, 1, 1, 0, 0, 0)
utc_to = datetime(2025, 12, 31, 23, 59, 59)

# Retrieve tick data for the symbol (all tick types)
ticks = mt5.copy_ticks_range(symbol, utc_from, utc_to, mt5.COPY_TICKS_ALL)
if ticks is None or len(ticks) == 0:
    print("No tick data retrieved for", symbol)
    mt5.shutdown()
    quit()

# Convert tick data into a Pandas DataFrame
ticks_df = pd.DataFrame(ticks)

# Check available columns for timestamp information
print("Tick data columns:", ticks_df.columns)

# Convert the timestamp to a datetime format:
if 'time' in ticks_df.columns:
    ticks_df['time'] = pd.to_datetime(ticks_df['time'], unit='s')
elif 'time_msc' in ticks_df.columns:
    ticks_df['time'] = pd.to_datetime(ticks_df['time_msc'], unit='ms')
else:
    print("No recognizable time column found in tick data.")
    mt5.shutdown()
    quit()

# Set the datetime column as the index
ticks_df.set_index('time', inplace=True)

# Display the first few rows of the DataFrame
print(ticks_df.head())

# Save to CSV file
ticks_df.to_csv('DXY_ticks_2020_2025.csv')

# Shut down the connection to MetaTrader 5
mt5.shutdown()