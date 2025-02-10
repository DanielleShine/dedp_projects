import calendar
from datetime import datetime
import numpy as np
import pandas as pd
import time

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def display_data(df):
    """
    Asks the user if they want to see 5 rows of data and keeps iterating until the user says 'no'.
    """
    start_row = 0
    while True:
        show_data = input("\nWould you like to see 5 rows of data? Enter 'yes' or 'no': ").strip().lower()
        if show_data == 'yes':
            # display(df.iloc[start_row:start_row+5])  # Display next 5 rows
            # print(df.head(start_row:start_row+5))
            print(df[start_row:start_row+5].head())
            start_row += 5
            if start_row >= len(df):  # Stop if there are no more rows to display
                print("\n🚀 End of data reached.")
                break
        elif show_data == 'no':
            print("\n✅ Data display stopped.")
            break
        else:
            print("❌ Invalid input. Please enter 'yes' or 'no'.")


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # get user input for city (chicago, new york city, washington)
    while True:
        city = input('Would you like to see data for Chicago, New York City, or Washington?').lower()
        if city in ['chicago', 'new york city', 'washington']:
            break
        else:
            print('❌ Invalid input. Please enter a valid city name.')

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input('Which month - January, February, March, April, May, June, or All?').lower()
        if month in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
            break
        else:
            print('❌ Invalid input. Please enter a valid month name.')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or All?').lower()
        if day in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            break
        else:
            print('❌ Invalid input. Please enter a valid day of the week.')

    print('-'*40)
    
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    df.drop('Unnamed: 0', axis=1, inplace=True)
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]
        
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
        
    return df

def station_stats(df):
    """Displays statistics on the most popular stations and trip.
    
    Returns and prints:
        (str) most_common_start_station - The most common start station
        (str) most_common_end_station - The most common end station
        (str) most_common_combination - The most common trip combination
    
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    try:
        # display most commonly used start station, end station and most frequent combination of start station and end station trip
        most_common_start_station = df['Start Station'].mode()[0]
        most_common_end_station = df['End Station'].mode()[0]
        df['Start End Station'] = df['Start Station'] + ' to ' + df['End Station']
        most_common_combination = df['Start End Station'].mode()[0]
        
        # Print most common start station, end station, and combination
        print("Most common start station is: ", most_common_start_station, "\nMost common end station is: ", most_common_end_station, "\nMost common combination is: ", most_common_combination)
    
    except KeyError:
        print("The 'Start Station' or 'End Station' columns are not present in the dataset.")
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    return most_common_start_station, most_common_end_station, most_common_combination


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0]
    common_month_name = calendar.month_name[common_month]  # Convert month number to month name

    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    common_hour_12hr = datetime.strptime(str(common_hour), "%H").strftime("%I %p")  # Convert to 12-hour format

    # print the most common month, day of week, and start hour
    print("Common month is: ", common_month_name, "\nCommon day is: ", common_day, "\nAnd finally common hour is: ", common_hour_12hr)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration.
    
    Returns and prints:
        (int) total_travel_time - The total travel time
        (int) mean_travel_time - The mean travel time
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    try:

        # display total travel time
        total_travel_time = df['Trip Duration'].sum()
        total_minutes = total_travel_time // 60 + (total_travel_time % 60)
        
        total_hours = total_minutes // 60
        total_days = total_hours // 24
        rounded_total_travel_time = np.round(total_days, 2)

        # display mean travel time
        mean_travel_time = df['Trip Duration'].mean()
        mean_minutes = mean_travel_time // 60 + (mean_travel_time % 60)
        rounded_mean_travel_time = np.round(mean_minutes, 2)

        # Print total and mean travel time
        print(f"Total travel time is: {rounded_total_travel_time} days\nMean travel time is: {rounded_mean_travel_time} minutes")

    except KeyError:
        print("The 'Trip Duration' column is not present in the dataset.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    return rounded_total_travel_time.item(), rounded_mean_travel_time.item()

def user_stats(df):
    """Displays statistics on bikeshare users."""
    
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("User types are: ", user_types, "\n")
    
    # For the Birth Year Information
    print("For the Birth Year Information:")
    try:
        # Display earliest, most recent, and most common year of birth
        earliest_birth_year = int(df['Birth Year'].min())
        most_recent_birth_year = int(df['Birth Year'].max())
        most_common_birth_year = int(df['Birth Year'].mode()[0])

        # Print user types and birth year stats
        print("Earliest birth year is: ", earliest_birth_year)
        print("Most recent birth year is: ", most_recent_birth_year)
        print("Most common birth year is: ", most_common_birth_year)

    except KeyError:
        print("The 'Birth Year' column is not present in the dataset.")

    # Gender Distribution
    print("\nGender Distribution:")
    try:
        gender_counts = df['Gender'].value_counts()
        print("Counts of each gender: ", gender_counts)
    except KeyError:
        print("The 'Gender' column is not present in the dataset.")

    # Age Distribution
    print("\nAge Distribution:")
    try:
        current_year = pd.to_datetime('now').year
        df['Age'] = current_year - df['Birth Year']
        age_distribution = np.round(df['Age'].describe(), 2)
        print(age_distribution)
    except KeyError:
        print("The 'Birth Year' column is not present in the dataset.")
    
    # User Type Comparison
    print("\nUser Type Comparison:")
    try:
        subscriber_duration = np.round(df[df['User Type'] == 'Subscriber']['Trip Duration'].mean(), 2)
        customer_duration = np.round(df[df['User Type'] == 'Customer']['Trip Duration'].mean(), 2)
        print(f"Average trip duration for Subscribers: {subscriber_duration} seconds")
        print(f"Average trip duration for Customers: {customer_duration} seconds")
    except KeyError:
        print("The 'User Type' or 'Trip Duration' columns are not present in the dataset.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    return 

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        display_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)
        
        while True:
            restart = input('\nWould you like to restart? Enter yes or no.\n').lower()
            if restart == 'yes':
                # Code to restart the process
                break
            elif restart == 'no':
                # Code to exit the process
                print("✅ Thank you for using the Bikeshare Data Analysis tool.\nStopping the program")
                exit()
            else:
                print("Please enter a valid response: 'yes' or 'no'.")


if __name__ == "__main__":
	main()
