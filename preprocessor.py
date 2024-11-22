import re
import pandas as pd
from io import StringIO

def preprocess(data):
    # Regex pattern to match both 12-hour and 24-hour time formats
    message_pattern = re.compile(r"(\d{1,2}/\d{1,2}/\d{2}),\s*(\d{1,2}:\d{2})(?:\s*[apAP][mM])?\s*-\s*(.+?):\s*(.+)")
    continuation_pattern = re.compile(r"^\s*(.+)$")

    # List to store matched lines and their details
    results = []

    # Use StringIO to simulate file reading from a string
    file = StringIO(data)
    previous_entry = None

    for line in file:
        # Check for message pattern
        message_match = message_pattern.match(line)
        if message_match:
            # If there's a previous entry, append it to results
            if previous_entry:
                results.append(previous_entry)

            # Create a new entry for the current line
            date, time, user, message = message_match.groups()
            previous_entry = {
                'Date': date,
                'Time': time,
                'User': user,
                'Message': message
            }
        else:
            # Check for continuation pattern
            continuation_match = continuation_pattern.match(line)
            if continuation_match and previous_entry:
                # Append continuation message to the previous entry
                previous_entry['Message'] += ' ' + continuation_match.group(1)

    # Append the last entry if there is one
    if previous_entry:
        results.append(previous_entry)

    # Convert list of results to DataFrame
    df = pd.DataFrame(results)

    # Convert 'Date' to datetime, inferring the format
    df['Date'] = pd.to_datetime(df['Date'], dayfirst=True, errors='coerce')
    # Convert 'Time' to datetime, handling both 12-hour and 24-hour formats
    df['Time'] = pd.to_datetime(df['Time'], format='%I:%M %p', errors='coerce').fillna(pd.to_datetime(df['Time'], format='%H:%M', errors='coerce'))

    # Extract additional time and date components
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month_name()
    df['DayName'] = df['Date'].dt.day_name()
    df['Day'] = df['Date'].dt.day
    df['Hour'] = df['Time'].dt.hour
    df['Minute'] = df['Time'].dt.minute
    df['monthNum'] = df['Date'].dt.month
    df['Date'] = df['Date'].dt.date
    # Drop the original 'Date' and 'Time' columns
    df = df.drop(['Time'], axis=1)

    period = []
    for hour in df['Hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))
    df['Period'] = period

    return df
