import time
import pandas as pd
import numpy as np
# create a dictionary for city data
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington).
    while True:
        city = input('\nWhich city would you like to explore?\n \
    \nChicago, New york city, or Washington?\n').lower()
        if city in ['chicago', 'new york city', 'washington']:
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input('\nWhich month would you like to choose?\n \
    \nAll, January, February, March, April, May, or June?\n').lower()
        if month in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('\nWhich day of week would you like to explore?\n \
    \nAll, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?\n').lower()
        if day in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            break

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

    # load city data
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month from the Start Time column to create a month column
    df['month'] = df['Start Time'].dt.month

    # extract day from the Start Time column to create a 'day-of-week' column
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    print('\nMost common month:', popular_month)

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('\nMost common day of week:', popular_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('\nMost common start hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_Start_Station = df['Start Station'].mode()[0]
    print('\nMost commonly used start station:', popular_Start_Station)

    # display most commonly used end station
    popular_End_Station = df['End Station'].mode()[0]
    print('\nMost commonly used end station:', popular_End_Station)

    # display most frequent combination of start station and end station trip
    # create a trip column including start station and end station
    df['trip'] = 'from ' + df['Start Station'] + ' to ' + df['End Station']
    # print value counts for each trip
    trip_count = df['trip'].value_counts()
    # find the most popular trip
    popular_trip = trip_count.index[0]
    print('\nMost frequent trip:', popular_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('\nTotal travel time: {} seconds'.format(total_travel_time))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('\nAverage travel time: {} seconds'.format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # display counts of user types
    user_types = df['User Type'].value_counts()
    print('\nUser Types:\n', user_types)

    # display counts of gender
    # note that no genda data or birth year data for Washington
    try:
        genders = df['Gender'].value_counts()
        print('\nGenders:\n', genders)
    # display earliest, most recent, and most common year of birth
        earliest_birth_year = df['Birth Year'].min()
        recent_birth_year = df['Birth Year'].max()
        common_birth_year = df['Birth Year'].mode()[0]
        print('\nEarliest birth year:', int(earliest_birth_year))
        print('\nMost recent birth year:', int(recent_birth_year))
        print('\nMost common birth year:', int(common_birth_year))
    except:
        print('\nNo genda data or birth year data for Washington.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
