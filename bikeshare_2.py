import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTH_NAMES = ['January','Feburary','March','April','May','June','July','August','September','Octuber','November','December']

DAY_OF_WEEK_NAMES = ['Monday','Thurday','Wednesday','Tuesday','Friday','Saturday','Sunday']

"""
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
"""
def get_filters():
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while( True ):
        print('Choose a number that represents a city of interest (1-3):')
        print('1- Chicago')
        print('2- New York City')
        print('3- Washington')
        city = ''
        input_str = input()
        if input_str.isdigit():
            cityIndex = int(input_str)
        else:
            print('Your selection is not an integer. Please try again...')
            continue
        if cityIndex >=1 and cityIndex <= 3:
            city = list(CITY_DATA)[cityIndex-1]
            break
        else:
            print('Your selection is out of range. Please try again...')
    print('Selected City:', city.capitalize())
    # get user input for month (all, january, february, ... , june)
    while( True ):
        print('Choose a number that represents a month of interest (1-12) or all months (13):')
        for idx, m in enumerate(MONTH_NAMES):
            print( str(idx+1) + '- ' + m)
        print('13- All')
        input_str = input()
        if input_str.isdigit():
            monthIndex = int(input_str)
        else:
            print('Your selection is not an integer. Please try again...')
            continue
        if monthIndex >=1 and monthIndex <= 13:
            month = monthIndex
            break
        else:
            print('Your selection is out of range. Please try again...')
    if(month < 13):
        print('Selected Month:', MONTH_NAMES[month-1])
    else:
        print('Selected all months')
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while( True ):
        print('Choose a number that represents a day of week (1-7) or the full week (8):')
        for idx, dow in enumerate(DAY_OF_WEEK_NAMES):
            print( str(idx+1) + '- ' + dow)
        print('8- All')
        input_str = input()
        if input_str.isdigit():
            dayIndex = int(input_str)
        else:
           print('Your selection is not an integer. Please try again...')
           continue 
        if dayIndex >=1 and dayIndex <= 8:
            day = dayIndex
            break
        else:
            print('Your selection is out of range. Please try again...')
    if(day < 8):
        print('Selected Day Of Week:', DAY_OF_WEEK_NAMES[day-1])
    else:
        print('Selected all the week')
    print('-'*40)
    return city, month, day


"""
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
"""
def load_data(city, month, day):
    print('City', city)
    print('Month', month)
    print('Day', day)

    df = pd.read_csv(CITY_DATA[city])

    # validation
    missing_columns = []
    if not 'Start Time' in df:
        missing_columns.append('Start Time')
    if not 'End Time' in df:
        missing_columns.append('End Time')
    if missing_columns:
        print('load_data _ Missing the following mandatory columns:', ','.join(missing_columns)+'.', 'Unable to continue.')
        return df

    # setup
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # filter months
    if month < 13:
        df = df[df['Start Time'].dt.month == month]
        df = df[df['End Time'].dt.month == month]

    # filter week days
    if day < 8:
        dt_day = day-1
        df = df[df['Start Time'].dt.day_of_week == dt_day]
        df = df[df['End Time'].dt.day_of_week == dt_day]
    return df

"""Displays statistics on the most frequent times of travel."""
def time_stats(df):

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # validation

    #setup
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Start Month'] = df['Start Time'].dt.month
    df['Start Day Of Week'] = df['Start Time'].dt.day_of_week
    df['Start Hour'] = df['Start Time'].dt.hour

    # display the most common month
    cm = df['Start Month'].mode()
    print('The most common month of travel is', MONTH_NAMES[cm[0]-1])

    # display the most common day of week
    cdow = df['Start Day Of Week'].mode()
    print('The most common day of week for travel is on', DAY_OF_WEEK_NAMES[cdow[0]])
    
    # display the most common start hour
    csh = df['Start Hour'].mode()
    print('The most common start hour is', csh[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

"""Displays statistics on the most popular stations and trip."""
def station_stats(df):
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # validation
    missing_columns = []
    if not 'Start Station' in df:
        missing_columns.append('Start Station')
    if not 'End Time' in df:
        missing_columns.append('End Station')
    if missing_columns:
        missing_columns.append('.')
        print('station_stats _ Missing the following mandatory columns:', ','.join(missing_columns)+'.','Skipping processing.')
        print('-'*40)
        return

    # setup
    df['Stations Combined'] = df['Start Station'] + ' - ' + df['End Station']

    # display most commonly used start station
    print('The most commonly used start station is', df['Start Station'].mode()[0])

    # display most commonly used end station
    print('The most commonly used end station is', df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    print('The most frequent combination of start station and end station trip is', df['Stations Combined'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

"""Displays statistics on the total and average trip duration."""
def trip_duration_stats(df):
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # validation
    missing_columns = []
    if not 'Trip Duration' in df:
        missing_columns.append('Trip Duration')
    if missing_columns:
        print('trip_duration_stats _ Missing the following mandatory columns:', ','.join(missing_columns) + '.','Skipping processing.')
        print('-'*40)
        return

    # display total travel time
    print('Total travel time is', df['Trip Duration'].sum())

    # display mean travel time
    print('Mean travel time is', df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

"""Displays statistics on bikeshare users."""
def user_stats(df):
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # validation
    missing_columns = []
    if not 'Birth Year' in df:
        missing_columns.append('Birth Year')
    if not 'User Type' in df:
        missing_columns.append('User Type')
    if not 'Gender' in df:
        missing_columns.append('Gender')
    
    # Display counts of user types
    if 'User Type' in missing_columns:
        print('user_stats _ Missing column User Type. Unable to count user types.')
    else:
        print('Counts of user types')
        cout = df.groupby('User Type').size()
        print(cout, '\n')

    # Display counts of gender
    print('Counts of gender')
    if 'Gender' in missing_columns:
        print('user_stats _ Missing column Gender . Unable to process counts of gender.')
    else:
        cog = df.groupby('Gender').size()
        print(cog, '\n')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in missing_columns:
        print('user_stats _ Missing column Birth Year. Unable to process earliest, recent and common year of birth.')
    else:
        maby = df['Birth Year'].max()
        miby = df['Birth Year'].min()
        moby = df['Birth Year'].mode()
        print('Most realiest year of birth',int(miby))
        print('Most recent year of birth',int(maby))
        print('Most common year of birth',int(moby[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or y to continue\n')
    start_loc = 0
    while (view_data == 'yes' or view_data == 'y'):
        print(df.iloc[start_loc:start_loc+5])
        start_loc += 5
        view_data = input("Do you wish to continue? (yes or y): ").lower()
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        if df.empty:
            print('Dataframe empty. No data found for the selected input.') 
        else:
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
            display_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes' and restart.lower() != 'y':
            break


if __name__ == "__main__":
	main()
