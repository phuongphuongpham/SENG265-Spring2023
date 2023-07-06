#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 8 14:44:33 2023
Based on: https://www.kaggle.com/datasets/arbazmohammad/world-airports-and-airlines-datasets
Sample input: --AIRLINES="airlines.yaml" --AIRPORTS="airports.yaml" --ROUTES="routes.yaml" --QUESTION="q1" --GRAPH_TYPE="bar"
@author: rivera
@author: V00980715
"""

import pandas as pd
import yaml
import sys


def sample_function(input: str) -> str:
    """Sample function (removable) that illustrations good use of documentation.
            Parameters
            ----------
                input : str, required
                    The input message.

            Returns
            -------
                str
                    The text returned.
    """
    return input.upper()


def question1(airlines_df, airports_df):
    """ question1()
            Input: None
            Output: Data Frame containing resulted data which answering question 1
                    "What are the top 20 airlines that offer the greatest number of routes with destination
                    country as Canada?"
    """
    airlines_df.columns = airlines_df.columns.str.strip()
    airlines_df.drop(airlines_df.columns[3], inplace=True, axis=1)
    airports_df.drop(['airport_name', 'airport_city', 'airport_icao_unique_code'], axis=1, errors='raise')

    #wanted_destination = airports_df[airports_df['airport_country'] == 1]

    print(airlines_df)


def question2(airlines_df, airports_df, routes_df):
    """ question2()
            Input: None
            Output: Data Frame containing resulted data which answering question 1
                    "What are the top 20 airlines that offer the greatest number of routes with destination
                    country as Canada?"
    """
    return 0


def question3(airlines_df, airports_df, routes_df):
    """ question3()
            Input: None
            Output: Data Frame containing resulted data which answering question 1
                    "What are the top 20 airlines that offer the greatest number of routes with destination
                    country as Canada?"
    """
    return 0


def question4(airlines_df, airports_df, routes_df):
    """ question4()
            Input: None
            Output: Data Frame containing resulted data which answering question 1
                    "What are the top 20 airlines that offer the greatest number of routes with destination
                    country as Canada?"
    """
    return 0


def question5(airlines_df, airports_df, routes_df):
    """ question5()
            Input: None
            Output: Data Frame containing resulted data which answering question 1
                    "What are the top 20 airlines that offer the greatest number of routes with destination
                    country as Canada?"
    """
    return 0


def main():
    """Main entry point of the program."""
    # calling the sample function

    print(sample_function(input="your code should be here."))

    # Read yaml files
    with open("airlines.yaml") as stream1:
        airlines = yaml.safe_load(stream1)
    with open("airports.yaml") as stream2:
        airports = yaml.safe_load(stream2)
    with open("routes.yaml") as stream3:
        routes = yaml.safe_load(stream3)

    airlines_df = pd.DataFrame(airlines)
    airports_df = pd.DataFrame(airports)
    routes_df = pd.DataFrame(routes)

    # Read the arguments
    question, graph = sys.argv[4], sys.argv[5]
    print(question, graph)

    if question == "--QUESTION=q1":
        question1(airlines_df, airports_df)
    elif question == "--QUESTION=q2":
        question2(airlines_df, airports_df, routes_df)
    elif question == "--QUESTION=q3":
        question3(airlines_df, airports_df, routes_df)
    elif question == "--QUESTION=q4":
        question4(airlines_df, airports_df, routes_df)
    else:
        question5(airlines_df, airports_df, routes_df)


if __name__ == '__main__':
    main()
