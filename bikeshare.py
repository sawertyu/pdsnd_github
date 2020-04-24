import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS = ["january","february","march","april","may","june"]
DAYS = ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]
invalid_message = "\nInvalid input. Please, try again."

def month_filter():
    while True:
        month = input("\nPlease, specify the full name of the month: \n").lower()
        if month in MONTHS:
            break
        else:
            print(invalid_message)
    return month


def day_filter():
    while True:
        day = input("\nPlease, specify the day (Monday, Tuesday, etc.): \n").lower()
        if day in DAYS:
            break
        else:
            print(invalid_message)
    return day    
       

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print("Hello! Let's explore some US bikeshare data for Chicago, New York City, and Washington!")
    
    while True:
        city = input("\nEnter the city you'd like to get data for: \n").lower()
        if city in CITY_DATA.keys():
            break
        else:
            print(invalid_message)

    time_condition = ["month", "day", "both", "none"]   
    time_filter = ""
    month = "all"
    day = "all"
    while time_filter not in time_condition:
        time_filter = input("\nEnter how you would like to filter the data by: month, day, both, or none: \n").lower()
        if time_filter == time_condition[0]:
            month = month_filter()
        elif time_filter == time_condition[1]:
            day = day_filter()
        elif time_filter == time_condition[2]:
            month = month_filter()
            day = day_filter()
        elif time_filter == time_condition[-1]:
            pass
        else:
            print(invalid_message)
        
    print("\nYou've selected: {}, {}, {}".format(city, month, day))    
    print("-"*40)
    
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
    df["Start Time"] = pd.to_datetime(df["Start Time"])
    df["month"] = df["Start Time"].dt.month
    df["day_of_week"] = df["Start Time"].dt.dayofweek

    
    if month != "all":
        months = MONTHS
        month = months.index(month) + 1
        df = df[df["month"] == month]
    
    if day != "all":
        days = DAYS
        day = days.index(day)
        df = df[df["day_of_week"] == day]
 
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
  
    # displays the most popular month
    df["month"] = df["Start Time"].dt.month_name()
    popular_month = df["month"].mode()[0]
    print("\nThe Most Popular Month of Renting:\n", popular_month)

    # displays the most popular day of week
    df["day_of_week"] = df["Start Time"].dt.day_name()
    popular_day = df["day_of_week"].mode()[0]
    print("\nThe Most Popular Day of Renting:\n", popular_day)

    # displays the most common start hour
    df["hour"] = df["Start Time"].dt.hour
    popular_start_hour = df["hour"].mode()[0]
    print("\nThe Most Popular Start Hour of Renting:\n", popular_start_hour)
      
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Displays the most commonly used start station
    popular_start_station = df["Start Station"].mode()[0]
    print("\nThe Most Popular Start Station:\n", popular_start_station)

    # Displays the most commonly used end station
    popular_end_station = df["End Station"].mode()[0]
    print("\nThe Most Popular End Station:\n", popular_end_station)

    # Displays the most frequent combination of start station and end station trip
    df["Full Route"] = "from " + df["Start Station"] + " to " + df["End Station"]
    popular_route = df["Full Route"].mode()[0]
    print("\nThe most popular route:\n", popular_route)
    
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Displays total travel time
    total_travel_time = int(df["Trip Duration"].sum())
    print("\nThe total travel duration is {} minutes.".format(total_travel_time))

    # Displays mean travel time
    mean_travel_time = int(df["Trip Duration"].mean())
    print("\nThe average travel duration is {} minutes.".format(mean_travel_time))   
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    df_columns = list(df.columns.values)
        
    # Displays counts of user types
    user_types = df["User Type"].value_counts()
    print("\nThe total number of users by user type:\n"+ str(user_types))
    
    # Displays counts of gender   
    if "Gender" in df_columns:
        gender_count = df["Gender"].value_counts()
        print("\nThe total number of users by gender:\n"+ str(gender_count))
    else:
        pass

    # Displays earliest, most recent, and most common year of birth 
    if "Birth Year" in df_columns:
        popular_birthyear = int(df["Birth Year"].mode()[0])
        youngest_user = int(df["Birth Year"].max())
        oldest_user = int(df["Birth Year"].min())
        print("\nThe most popular year of birth is {}.\n".format(popular_birthyear))
        print("\nThe youngest user was born in {}.\n".format(youngest_user))
        print("\nThe oldest user was born in {}.\n".format(oldest_user))
    else:
        pass  

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

        restart = input("\nWould you like to restart? Enter yes or no.\n")
        if restart.lower() != "yes":
            break


if __name__ == "__main__":
	main()
