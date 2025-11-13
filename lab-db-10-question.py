import pandas as pd
import matplotlib.pyplot as plt

# Load the data
df = pd.read_csv('trade-data.csv')
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['date'] = df['timestamp'].dt.date


def q_1():
    """Count rows from March 15-31, 2024"""
    result = df.query('timestamp >= "2024-03-15" and timestamp < "2024-04-01"')
    return len(result)


def q_2():
    """Count daily rows in March, filling missing days with -1"""
    # Query for March 2024
    march_data = df.query('timestamp >= "2024-03-01" and timestamp < "2024-04-01"')

    # Count rows per day
    daily_counts = march_data.groupby('date').size()

    # Create a full range of dates for March 2024
    full_march = pd.date_range(start='2024-03-01', end='2024-03-31', freq='D')
    full_march_dates = full_march.date

    # Reindex to include all days in March, fill missing with -1
    result = daily_counts.reindex(full_march_dates, fill_value=-1)

    return result.values


def q_3():
    """Calculate daily sum of amount column, filling missing days with 0, rounded to integers"""
    # Query for March 2024
    march_data = df.query('timestamp >= "2024-03-01" and timestamp < "2024-04-01"')

    # Sum amount per day
    daily_sums = march_data.groupby('date')['amount'].sum()

    # Create a full range of dates for March 2024
    full_march = pd.date_range(start='2024-03-01', end='2024-03-31', freq='D')
    full_march_dates = full_march.date

    # Reindex to include all days in March, fill missing with 0
    result = daily_sums.reindex(full_march_dates, fill_value=0)

    # Round to integers
    result = result.round().astype(int)

    return result.values


def q_4():
    """Generate weekly counts separated by side value, displayed as a stacked bar chart"""
    # Query for March 2024
    march_data = df.query('timestamp >= "2024-03-01" and timestamp < "2024-04-01"')

    # Add week column
    march_data = march_data.copy()
    march_data['week'] = march_data['timestamp'].dt.isocalendar().week

    # Count by week and side
    weekly_side_counts = march_data.groupby(['week', 'side']).size().unstack(fill_value=0)

    # Create stacked bar chart
    fig, ax = plt.subplots(figsize=(10, 6))
    weekly_side_counts.plot(kind='bar', stacked=True, ax=ax)

    ax.set_xlabel('Week')
    ax.set_ylabel('Count')
    ax.set_title('Weekly Trade Counts by Side')
    ax.legend(title='Side', labels=['Side 0', 'Side 1'])

    plt.tight_layout()
    plt.savefig('weekly_trade_counts.png')
    plt.close()

    return weekly_side_counts


if __name__ == '__main__':
    print("Q1 - Count rows from March 15-31, 2024:")
    print(q_1())
    print("\n" + "="*50 + "\n")

    print("Q2 - Daily row counts in March (missing days = -1):")
    print(q_2())
    print("\n" + "="*50 + "\n")

    print("Q3 - Daily sum of amount in March (missing days = 0):")
    print(q_3())
    print("\n" + "="*50 + "\n")

    print("Q4 - Weekly counts by side (saved as PNG):")
    print(q_4())
    print("\nChart saved as 'weekly_trade_counts.png'")
