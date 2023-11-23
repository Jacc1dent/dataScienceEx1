#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Student Name: Jack Fitzgerald

Student ID: R00205373

Cohort: CS-3

"""
import pandas as pd
import matplotlib.pyplot as plt


def task1():

    # Create Dataframe
    df = pd.read_csv("Movies-1.csv", encoding="ISO-8859-1")

    # Finding the total number of unique genres
    uniqueGenres = pd.unique(df["main_Genre"])
    totalUniqueGenres = len(uniqueGenres)
    print(f"Total number of unique main genres: {totalUniqueGenres}")

    # Finding the most popular genre
    mostPopularGenre = df["main_Genre"].value_counts()
    popularGenrePrint = mostPopularGenre.head(1)
    print(f"Most popular genre: {popularGenrePrint}")
    # print(mostPopularGenre.head(1))

    # Finding the least popular genre
    leastPopularPrint = mostPopularGenre.tail(1)
    print(f"Least popular genre: {leastPopularPrint}")

    # Find the top 8 most popular genres
    topGenres = df["main_Genre"].value_counts()
    topGenresPrint = topGenres.head(8)

    # Plotting bar chart for the top 8 popular genres
    plt.figure(figsize=(12, 8))
    topGenresPrint.plot(kind="bar", color="black")
    plt.title("Top 8 Most Popular Genres")
    plt.xlabel("Genre")
    plt.ylabel("Popularity")
    # Setting tick locations and labels
    plt.xticks(rotation=45)
    plt.grid(axis="y", linestyle="--")
    plt.tight_layout()
    plt.show()


# task1()


def task2():

    # Creating the dataframe
    df = pd.read_csv("Movies-1.csv", encoding="ISO-8859-1")
    # Splitting the genres and exploding them into separate rows.
    genres = df["Genre"].str.split(",").explode().str.strip()

    # Finding the most common genre
    mostCommon = genres.mode()[0]

    # Finding the least common genre
    # The least common genre is the first element of the sorted index
    leastCommon = genres.value_counts().sort_values().index[0]

    print(f"Most Common Genre: {mostCommon}")
    print(f"Least Common Genre: {leastCommon}")

    
# task2()
    

def task3():

    # Creating the dataframe
    df = pd.read_csv("Movies-1.csv", encoding="ISO-8859-1")
    # Extract only the numerical values
    # Specifies any errors during conversion, to be replaced with NaN
    df["Runtime"] = pd.to_numeric(df["Runtime"].str.extract("(\d+)", expand=False), errors="coerce")
    # Removes missing values, Column label
    df = df.dropna(subset=["Runtime"])

    # Creating the boxplot with a size of the figure(plot)
    plt.figure(figsize=(12, 8))
    plt.boxplot(df["Runtime"], vert=False, showfliers=False)  # Horizontally, for the runtime column in the DataFrame.

    # Calculating the first and third quartiles.
    q1 = df["Runtime"].quantile(0.25)
    q3 = df["Runtime"].quantile(0.75)

    # Calculating the interquartile range
    iqr = q3 - q1

    # Identifying outliers using the IQR method.
    outliers = df[(df["Runtime"] < q1 - 1.5 * iqr) | (df["Runtime"] > q3 + 1.5 * iqr)]
    # Creates a list of 1s with equal length of outliers
    plt.scatter(outliers["Runtime"], [1]*len(outliers), color="red", label="Outliers", marker="x")

    # Printing titles of Outliers
    # Getting the titles of movies considered outliers + printing the titles
    outliersTitle = outliers["Title"].unique()

    print("These are the movies with runtimes that are outliers: ")
    # Printing the titles of movies
    for title in outliersTitle:
        print(title)
    print("Total Outliers: ", len(outliers))

    # Printing the Box Plot
    # Setting the title
    plt.title("Movie Runtimes with Outliers")

    # Labelling the x-axis
    plt.xlabel("Runtime")
    # Removes the y-axis labels
    plt.yticks([])
    plt.legend()

    # Print plot
    plt.show()

    
# task3()
    

def task4():

    # Creating the dataframe
    df = pd.read_csv("Movies-1.csv", encoding="ISO-8859-1")

    # Check for null values
    nullVotes = df["Number of Votes"].isnull().sum()
    nullRatings = df["Rating"].isnull().sum()

    # Print the number of null values
    print(f"Number of null values in 'Number of Votes': {nullVotes}")
    print(f"Number of null values in 'Rating': {nullRatings}")

    # Fill null values with the mean for each attribute
    # Inplace replaces the original DataFrame without reassignment
    df["Number of Votes"].fillna(df["Number of Votes"].mean(), inplace=True)
    df["Rating"].fillna(df["Rating"].mean(), inplace=True)

    # Check if there are any more null values
    nullVotesAfter = df["Number of Votes"].isnull().sum()
    nullRatingsAfter = df["Rating"].isnull().sum()

    # Print the number of null values
    print(f"\nNumber of null values in 'Number of Votes' after filling: {nullVotesAfter}")
    print(f"Number of null values in 'Rating' after filling: {nullRatingsAfter}")

    # Visualising with the scatter plot
    plt.figure(figsize=(12, 8))
    plt.scatter(df["Number of Votes"], df["Rating"], color="Black")
    plt.title("Relationship between Number of Votes and Rating")
    plt.xlabel("Number of Votes")
    plt.ylabel("Rating")
    # True enables grid lines
    plt.grid(True, linestyle="--")
    plt.tight_layout()
    plt.show()

    """
    
    Null Values might come up in datasets due to missing data during the collection of the data.
    Filling null values with the mean is a common strategy to handle missing data and in order to maintain
    integrity of the dataset.
    
    """


# task4()

    
def task5():

    # Creating the dataframes
    genreDf = pd.read_csv("main_genre.csv", encoding="ISO-8859-1")
    movieDf = pd.read_csv("Movies-1.csv", encoding="ISO-8859-1")

    # Converting column names to lowercase
    genreDf.columns = genreDf.columns.str.lower()

    # Convert column to lowercase and replacing certain characters
    movieDf["Synopsis"] = movieDf["Synopsis"].str.lower().replace(["\.", ",", "'", "-"], "", regex=True)

    # New dataframe for storing results
    df = pd.DataFrame(columns=["main_Genre", "most_frequent_related_genre"])

    # Iterating through main genres and selecting the movies with synopses containing main genres
    for main_genre in genreDf.columns:
        movie = movieDf[movieDf["Synopsis"].str.contains(main_genre)]

        # Checking if there are any movies
        if not movie.empty:
            count = movie["main_Genre"].value_counts()

            # Getting the frequency
            # Returns the index corresponding to the max value
            relatedGenre = count.idxmax()

            # Append the results to the dataframe
            # Resets index and forms range of integers
            df = pd.concat([df, pd.DataFrame({"main_Genre": [main_genre], "most_frequent_related_genre": [relatedGenre]})],
                       ignore_index=True)

    # Printing the results
    # Iterates through each row, index being the current row and row containing the values of the row

    for index, row in df.iterrows():
        print(f"{row['main_Genre']}: {row['most_frequent_related_genre']}")

    
# task5()

    
def task6():

    # Creating the dataframe
    df = pd.read_csv("Movies-1.csv", encoding="ISO-8859-1")

    # Converting runtime to a string and extracting numeric values
    df["Runtime"] = df["Runtime"].astype(str)
    # [0] selects only the first column of the dataframe
    df["Runtime"] = pd.to_numeric(df["Runtime"].str.extract("(\d+)")[0], errors="coerce")

    # Calculate the mean of the runtime and filling in any null values with the mean
    mean = df["Runtime"].mean()
    df["Runtime"].fillna(mean, inplace=True)

    # Creating a scatter plot to visualise the relationship between runtime and rating
    plt.figure(figsize=(12, 8))
    plt.scatter(df["Runtime"], df["Rating"], color="Black")
    plt.title("Relationship Between Runtime and Rating")
    plt.xlabel("Runtime (minutes)")
    plt.ylabel("Rating")
    plt.grid(True, linestyle="--")
    plt.tight_layout()
    plt.show()


# task6()
