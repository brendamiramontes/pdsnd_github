import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print("\nHello! Let's explore some USA bikeshare data!\n")
    
    # Get user input for city
    while True:
        city = input("Please Choose a City You'd Like to Analyze: Chicago, New York City, Washington ").lower()
        if city in CITY_DATA:
            break
        else:
            print("Invalid Input. Please Enter Either Chicago, New York City, or Washington")
    
    # Get user input for month
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    while True:
        month = input("\nWhich Month Would You Like to Filter by (January, February, March, April, May, June) or 'All' for No Filter? \n").lower()
        if month in months:
            break
        else:
            print("Invalid Input. Choose Either January, February, March, April, May, June, or 'All' for No Filter.")
    
    # Get user input for day of week
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    while True:
        day = input("\nWhich Day Would You Like to Filter By (Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday) or 'All' for No Filter? \n").lower()
        if day in days:
            break
        else:
            print("Invalid Input. Please Choose Either Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or 'All' for No Filter.")
    
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
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name().str.lower()
    
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]
    
    if day != 'all':
        df = df[df['day_of_week'] == day]
    
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating Total Number of Trips and The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
   #Display trip count for more insights
    number_of_trips = len(df)
    print("Number of Trips for the Month:", number_of_trips)
    
    # Display the most common month
    common_month = df['month'].mode()[0]
    print('Most Common Month:', common_month)
    
    # Display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print('Most Common Day of Week:', common_day)

    # Display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_start_hour = df['hour'].mode()[0]
    print('Most Common Start Hour:', common_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print("The Most Common Start Station Is:", common_start_station)

    # Display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print("The Most Common End Station Is:", common_end_station)

    # Display most frequent combination of start station and end station trip
    df['start_end_combination'] = df['Start Station'] + " to " + df['End Station']
    freq_startend_station = df['start_end_combination'].mode()[0]
    print('Most Common Start-End Combination:', freq_startend_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    total_travel_time = df['Trip Duration'].sum()
    #user friendly format
    total_travel_time_hours = total_travel_time // 3600
    total_travel_time_minutes = (total_travel_time % 3600) // 60
    total_travel_time_seconds = total_travel_time % 60
    print("Total Travel Time: {} hours, {} minutes, and {} seconds".format(total_travel_time_hours, total_travel_time_minutes, total_travel_time_seconds))

    # Display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    mean_travel_time_minutes = mean_travel_time // 60
    mean_travel_time_seconds = mean_travel_time % 60
    print("Mean Travel Time: {} minutes and {} seconds".format(int(mean_travel_time_minutes), int(mean_travel_time_seconds)))
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    count_user_types = df['User Type'].value_counts()
    print('User Types: ', count_user_types)
    
    # Display counts of gender
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print("Gender Counts: ", gender_counts)
    else:
        print('Gender Data Not Available for This City')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_year = int(df['Birth Year'].min())
        most_recent_year = int(df['Birth Year'].max())
        most_common_birth_year = int(df['Birth Year'].mode()[0])
        print('\nBirth Year Stats:')
        print("Earliest Year: ", earliest_year)
        print("Most Recent Year: ", most_recent_year)
        print("Most Common Birth Year: ", most_common_birth_year)

    else:
        print('\nBirth year data not available for this city.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def display_raw_data(df):
    """Displays raw data upon user request."""
    row_index = 0
    while True:
        show_data = input("\nWould You Like To See 5 Rows of Raw Data? Enter 'Yes' or 'No'.\n").lower()
        if show_data != 'yes':
            break

        print("\nRaw Data:\n")
        for i in range(row_index, min(row_index + 5, len(df))):
            print(f"Row {i + 1}:")
            for column_name, value in df.iloc[i].items():
                print(f"{column_name}: {value}")
            print("-" * 40)
        row_index += 5

        if row_index >= len(df):
            print("\nNo More Data to Display.\n")
            break
       

def main():
        while True:
            city, month, day = get_filters()
            df = load_data(city, month, day)

            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
            display_raw_data(df)

            restart = input('\nWould you like to restart? Enter yes or no.\n')
            if restart.lower() != 'yes':
                break

if __name__ == "__main__":
    main()
