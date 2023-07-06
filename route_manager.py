#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 8 14:44:33 2023
Based on: https://www.kaggle.com/datasets/arbazmohammad/world-airports-and-airlines-datasets
Sample input: --AIRLINES="airlines.yaml" --AIRPORTS="airports.yaml" --ROUTES="routes.yaml" --QUESTION="q1" --GRAPH_TYPE="bar"
@author: rivera
@author: V00980715
         Phuong Pham
"""
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import yaml
import sys
import csv


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


def output_to_file(output_file, list_of_element) -> None:
    """ output_to_file(output_file, list_of_element)
            Input:
            ----------
                output_file
                list_of_element: list of data for each row in the output

            Output:
            ----------
                None
                Write to output csv file
    """
    output = csv.writer(output_file)
    header = ["subject", "statistic"]
    output.writerow(header)

    for element in list_of_element:
        output.writerow(element)


def question1(airlines_df: pd.DataFrame, airports_df: pd.DataFrame, routes_df: pd.DataFrame, f1) -> dict:
    """ question1(airlines_df, airports_df, routes_df, f1)
            Input:
            ----------
                airlines_df, airports_df, routes_df, f1

            Output:
            ----------
                dict: A dictionary of lists of "subject" and "statistic" (will be used to display graph)
                "What are the top 20 airlines that offer the greatest number of routes with destination
                country as Canada?"
    """
    q1_airlines_df = airlines_df.copy()
    q1_airports_df = airports_df.copy()
    q1_routes_df = routes_df.copy()
    q1_airlines_df.drop(['airline_country'], inplace=True, axis=1)
    q1_airports_df.drop(['airport_name',
                         'airport_city',
                         'airport_icao_unique_code',
                         'airport_altitude'], inplace=True, axis=1)

    q1_airports_df = q1_airports_df[q1_airports_df['airport_country'] == "Canada"]

    q1_routes_df = q1_routes_df[q1_routes_df['route_to_airport_id'].isin(q1_airports_df['airport_id'])]
    q1_routes_df = q1_routes_df[q1_routes_df['route_airline_id'] != '\\N']
    q1_airlines_df = q1_airlines_df[q1_airlines_df['airline_id'].isin(q1_routes_df['route_airline_id'])]

    result: pd.DataFrame = q1_routes_df.groupby(['route_airline_id'],
                                                as_index=False).size().sort_values(by='size',
                                                                                   ascending=False).head(40)
    id_size = []
    for index, row in result.iterrows():
        id_size.append([row["route_airline_id"], row["size"]])

    id_name_code = []
    for index, row in q1_airlines_df.iterrows():
        id_name_code.append([row["airline_id"], row["airline_name"], row["airline_icao_unique_code"]])

    list_of_name = []
    list_of_code = []
    for id1, size in id_size:
        for id2, name, code in id_name_code:
            if id1 == id2:
                list_of_name.append(name)
                list_of_code.append(code)

    result['airline_name'] = pd.Series(list_of_name, index=result.index)
    result['airline_code'] = pd.Series(list_of_code, index=result.index)

    result = result.sort_values(by=['size', 'airline_name'], ascending=[False, True]).head(20)

    name_code_size = []
    subject = []
    statistic = []

    for index, row in result.iterrows():
        name_code = row["airline_name"] + " (" + row["airline_code"] + ")"
        name_code_size.append([name_code, row["size"]])
        subject.append(name_code)
        statistic.append(row["size"])

    d = {"subject": subject, "statistic": statistic}
    output_to_file(f1, name_code_size)

    return d


def question2(airlines_df: pd.DataFrame, airports_df: pd.DataFrame, routes_df: pd.DataFrame, f2) -> dict:
    """ question2(airlines_df: pd.DataFrame, airports_df: pd.DataFrame, routes_df: pd.DataFrame, f2)
            Input:
            ----------
                airlines_df, airports_df, routes_df, f2

            Output:
            ----------
                dict: A dictionary of lists of "subject" and "statistic" (will be used to display graph)
                What are the top 30 countries with the least appearances as destination country
                on the routes' data?

    """
    q2_airlines_df = airlines_df.copy()
    q2_airports_df = airports_df.copy()
    q2_routes_df = routes_df.copy()

    q2_airports_df.drop(['airport_name',
                         'airport_city',
                         'airport_icao_unique_code',
                         'airport_altitude'], inplace=True, axis=1)

    q2_routes_df = q2_routes_df[q2_routes_df['route_to_airport_id'] != '1']
    q2_routes_df = q2_routes_df[q2_routes_df['route_to_airport_id'] != '\\N']
    q2_airports_df = q2_airports_df[q2_airports_df['airport_id'].isin(q2_routes_df['route_to_airport_id'])]

    to_from = []
    for index, row in q2_routes_df.iterrows():
        to_from.append([row["route_to_airport_id"], row["route_from_airport_id"]])

    id_country = []
    for index, row in q2_airports_df.iterrows():
        id_country.append([row["airport_id"], row["airport_country"]])

    list_of_country = []
    for to_country_id, from_country_id in to_from:
        for airport_id, airport_country in id_country:
            if (airport_id == to_country_id) and (airport_country != " Santiago Island"):
                list_of_country.append(airport_country)

    data = {'country_name': list_of_country}
    df = pd.DataFrame(data)
    result: pd.DataFrame = df.groupby(['country_name'],
                                      as_index=False).size().sort_values(by=['size', 'country_name'],
                                                                         ascending=[True, True]).head(30)
    country_size = []
    subject = []
    statistic = []

    for index, row in result.iterrows():
        country_size.append([row["country_name"], row["size"]])
        subject.append(row["country_name"])
        statistic.append(row["size"])

    d = {"subject": subject, "statistic": statistic}
    output_to_file(f2, country_size)

    return d

def question3(airlines_df: pd.DataFrame, airports_df: pd.DataFrame, routes_df: pd.DataFrame, f3) -> dict:
    """ question3(airlines_df: pd.DataFrame, airports_df: pd.DataFrame, routes_df: pd.DataFrame, f3)
            Input:
            ----------
                airlines_df, airports_df, routes_df, f3

            Output:
            ----------
                dict: A dictionary of lists of "subject" and "statistic" (will be used to display graph)
                "What are the top 10 destination airports?"
    """
    q3_airlines_df = airlines_df.copy()
    q3_airports_df = airports_df.copy()
    q3_routes_df = routes_df.copy()

    q3_airports_df.drop(['airport_altitude'], inplace=True, axis=1)

    q3_routes_df = q3_routes_df[q3_routes_df['route_to_airport_id'] != '1']
    q3_routes_df = q3_routes_df[q3_routes_df['route_to_airport_id'] != '\\N']
    q3_airports_df = q3_airports_df[q3_airports_df['airport_id'].isin(q3_routes_df['route_to_airport_id'])]

    to_from = []
    for index, row in q3_routes_df.iterrows():
        to_from.append([row["route_to_airport_id"], row["route_from_airport_id"]])

    id_name_city_country_code = []
    for index, row in q3_airports_df.iterrows():
        id_name_city_country_code.append([row["airport_id"], row["airport_name"], row["airport_city"],
                                          row["airport_country"], row["airport_icao_unique_code"]])

    list_of_airport = []

    for to_country_id, from_country_id in to_from:
        airport = ""
        for i, name, city, country, code in id_name_city_country_code:
            if i == to_country_id:
                airport = name + " (" + code + "), " + city + ", " + country
        list_of_airport.append(airport)

    data = {'airport': list_of_airport}
    df = pd.DataFrame(data)
    result: pd.DataFrame = df.groupby(['airport'],
                                      as_index=False).size().sort_values(by=['size', 'airport'],
                                                                         ascending=[False, True]).head(10)

    airport_size = []
    subject = []
    statistic = []

    for index, row in result.iterrows():
        airport_size.append([row["airport"], row["size"]])
        subject.append(row["airport"])
        statistic.append(row["size"])

    d = {"subject": subject, "statistic": statistic}
    output_to_file(f3, airport_size)

    return d


def question4(airlines_df: pd.DataFrame, airports_df: pd.DataFrame, routes_df: pd.DataFrame, f4) -> dict:
    """ question4(airlines_df: pd.DataFrame, airports_df: pd.DataFrame, routes_df: pd.DataFrame, f4)
            Input:
            ----------
                airlines_df, airports_df, routes_df, f4

            Output:
            ----------
                dict: A dictionary of lists of "subject" and "statistic" (will be used to display graph)
                "What are the top 15 destination cities?"
    """
    q4_airlines_df = airlines_df.copy()
    q4_airports_df = airports_df.copy()
    q4_routes_df = routes_df.copy()

    q4_airports_df.drop(['airport_altitude'], inplace=True, axis=1)

    q4_routes_df = q4_routes_df[q4_routes_df['route_to_airport_id'] != '1']
    q4_routes_df = q4_routes_df[q4_routes_df['route_to_airport_id'] != '\\N']
    q4_airports_df = q4_airports_df[q4_airports_df['airport_id'].isin(q4_routes_df['route_to_airport_id'])]

    to_from = []
    for index, row in q4_routes_df.iterrows():
        to_from.append([row["route_to_airport_id"], row["route_from_airport_id"]])

    id_city_country = []
    for index, row in q4_airports_df.iterrows():
        id_city_country.append([row["airport_id"], row["airport_city"], row["airport_country"]])

    list_of_city = []
    for to_country_id, from_country_id in to_from:
        c = ""
        for i, city, country in id_city_country:
            if i == to_country_id:
                c = city + ", " + country
        list_of_city.append(c)

    data = {'city': list_of_city}
    df = pd.DataFrame(data)
    result: pd.DataFrame = df.groupby(['city'],
                                      as_index=False).size().sort_values(by=['size', 'city'],
                                                                         ascending=[False, True]).head(15)

    city_size = []
    subject = []
    statistic = []
    for index, row in result.iterrows():
        city_size.append([row["city"], row["size"]])
        subject.append(row["city"])
        statistic.append(row["size"])

    d = {"subject": subject, "statistic": statistic}
    output_to_file(f4, city_size)

    return d


def question5(airlines_df: pd.DataFrame, airports_df: pd.DataFrame, routes_df: pd.DataFrame, f5) -> dict:
    """ question5(airlines_df: pd.DataFrame, airports_df: pd.DataFrame, routes_df: pd.DataFrame, f5)
            Input:
            ----------
                airlines_df, airports_df, routes_df, f5

            Output:
            ----------
                dict: A dictionary of lists of "subject" and "statistic" (will be used to display graph)
                "What are the unique top 10 Canadian routes (i.e., if CYYJ-CYVR is included, CYVR-CYYJ
                should not) with most difference between the destination altitude and the origin altitude?"
    """

    q5_airlines_df = airlines_df.copy()
    q5_airports_df = airports_df.copy()
    q5_routes_df = routes_df.copy()

    q5_airports_df.drop(['airport_name', 'airport_city'], inplace=True, axis=1)
    q5_airports_df['airport_altitude'] = pd.to_numeric(q5_airports_df['airport_altitude'])
    q5_airports_df = q5_airports_df[q5_airports_df['airport_icao_unique_code'] != "\\N"]
    q5_airports_df = q5_airports_df[q5_airports_df["airport_country"] == "Canada"]

    q5_routes_df = q5_routes_df[q5_routes_df['route_to_airport_id'] != '1']
    q5_routes_df = q5_routes_df[q5_routes_df['route_to_airport_id'] != '\\N']
    q5_routes_df = q5_routes_df[q5_routes_df['route_from_airport_id'] != '1']
    q5_routes_df = q5_routes_df[q5_routes_df['route_from_airport_id'] != '\\N']

    q5_routes_df = q5_routes_df[q5_routes_df['route_from_airport_id'].isin(q5_airports_df["airport_id"])]
    q5_routes_df = q5_routes_df[q5_routes_df['route_to_airport_id'].isin(q5_airports_df["airport_id"])]

    from_to = []
    for index, row in q5_routes_df.iterrows():
        from_to.append([row["route_from_airport_id"], row["route_to_airport_id"]])

    id_code_altitude = []
    for index, row in q5_airports_df.iterrows():
        id_code_altitude.append([row["airport_id"], row["airport_icao_unique_code"], row["airport_altitude"]])

    origin_destination_alt = []
    for fr, to in from_to:
        origin = ""
        destination = ""
        origin_alt = 0
        destination_alt = 0
        for i, code, alt in id_code_altitude:
            if fr == i:
                origin = code
                origin_alt: int = alt
        for i, code, alt in id_code_altitude:
            if to == i:
                destination = code
                destination_alt: int = alt

        if origin_alt >= destination_alt:
            alt_diff = origin_alt - destination_alt
        else:
            alt_diff = destination_alt - origin_alt

        if origin != "" and destination != "" and alt_diff != 0:
            origin_destination_alt.append([origin, destination, alt_diff])

    list_of_origin = []
    list_of_destination = []
    list_of_altitude = []
    for ori1, dest1, alt1 in origin_destination_alt:
        highest_diff: int = alt1
        od1: str = dest1 + "-" + ori1
        unique = []
        for ori2, dest2, alt2 in origin_destination_alt:
            a: int = alt2
            od2: str = ori2 + "-" + dest2
            if od1 == od2 and a >= highest_diff:
                highest_diff = a
                unique = [ori2, dest2, alt2]
            else:
                unique = [ori1, dest1, alt1]
        list_of_origin.append(unique[0])
        list_of_destination.append(unique[1])
        list_of_altitude.append(unique[2])

    data = {"origin": list_of_origin, "destination": list_of_destination, "altitude_difference": list_of_altitude}
    df = pd.DataFrame(data)
    result: pd.DataFrame = df.groupby(['origin', 'destination', 'altitude_difference'],
                                      as_index=False).size().sort_values(by='altitude_difference',
                                                                         ascending=False).head(10)

    route_altitude = []
    subject = []
    statistic = []
    for index, row in result.iterrows():
        route = row["origin"] + "-" + row["destination"]
        route_altitude.append([route, row["altitude_difference"]])
        subject.append(route)
        statistic.append(row["altitude_difference"])

    d = {"subject": subject, "statistic": statistic}
    output_to_file(f5, route_altitude)

    return d


def graph_type(d: dict, title: str, graph: str, x: str, y: str, output_pdf: str) -> None:
    """graph_type(d: dict, title: str, graph: str, x: str, y: str, output_pdf: str) -> None:
        Input:
         ----------
            d: dictionary from calling question<>() functions
            title: title of the graph
            graph: graph type from given argument
            x: x-axis name
            y: y-axis name
            output_pdf: pdf output file

        Output:
        ----------
            None
            Call the plotting_pie or plotting_bar function
    """
    df = pd.DataFrame(d)
    if graph == "--GRAPH_TYPE=pie":
        plotting_pie(df, title, output_pdf)
    else:
        plotting_bar(df, title, x, y, output_pdf)


def plotting_pie(input_df, title: str, output_pdf: str) -> None:
    """plotting_pie(input_df, title: str, output_pdf: str) -> None:
         Input:
         ----------
            input_df: Data frame generated from graph_type() function
            title: title of the graph
            output_pdf: pdf output file

        Output:
        ----------
            None
            Show the graph and Save it to output_pdf file
    """
    colors = ['#ffcaca', '#ffedc1', '#feffb8', '#c4ffcb', '#c8e5ff', '#e0d6ff', '#d2d4dc']
    fig = plt.figure(figsize=(24, 14))
    plt.pie(input_df['statistic'], labels=input_df['subject'], colors=colors, autopct='%1.1f%%')
    plt.title(title, fontsize=18, weight='bold')
    plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9)
    plt.show()
    plt.savefig(output_pdf, format="pdf")


def plotting_bar(input_df, title: str, x: str, y: str, output_pdf: str) -> None:
    """plotting_pie(input_df, title: str, output_pdf: str) -> None:
            Input:
             ----------
                input_df: Data frame generated from graph_type() function
                title: title of the graph
                x: x-axis name
                y: y-axis name
                output_pdf: pdf output file

            Output:
            ----------
                None
                Show the graph and Save it to output_pdf file
    """
    new_color = (255/255, 154/255, 141/255)
    fig = plt.figure(figsize=(24, 14))
    x_values = input_df["subject"]
    y_values = input_df["statistic"]

    plt.barh(x_values, y_values, color=new_color)
    plt.xlabel(y, weight='bold', fontsize=14)
    plt.ylabel(x, weight='bold', fontsize=14)
    plt.title(title, weight='bold', fontsize=18)
    plt.show()
    plt.savefig(output_pdf, format="pdf")


def main():
    """Main entry point of the program."""
    # calling the sample function

    print(sample_function(input="your code should be here."))

    # Read yaml files using numpy into DataFrame
    with open("airlines.yaml", 'r') as stream1:
        airlines = yaml.safe_load(stream1)
    with open("airports.yaml", 'r') as stream2:
        airports = yaml.safe_load(stream2)
    with open("routes.yaml", 'r') as stream3:
        routes = yaml.safe_load(stream3)

    airlines_dict = np.array(airlines)
    airports_dict = np.array(airports)
    routes_dict = np.array(routes)

    airlines_arr = airlines_dict[()]['airlines']
    airports_arr = airports_dict[()]['airports']
    routes_arr = routes_dict[()]['routes']

    airlines_df = pd.DataFrame(airlines_arr)
    airports_df = pd.DataFrame(airports_arr)
    routes_df = pd.DataFrame(routes_arr)

    # Create stream to output csv files
    f1 = open('q1.csv', 'w', encoding='UTF8', newline='')
    f2 = open('q2.csv', 'w', encoding='UTF8', newline='')
    f3 = open('q3.csv', 'w', encoding='UTF8', newline='')
    f4 = open('q4.csv', 'w', encoding='UTF8', newline='')
    f5 = open('q5.csv', 'w', encoding='UTF8', newline='')

    # Read the arguments
    question, graph = sys.argv[4], sys.argv[5]

    # Generate the answer responding to question argument
    if question == "--QUESTION=q1":
        dictionary = question1(airlines_df, airports_df, routes_df, f1)
        graph_type(dictionary, "Top 20 Airlines that offer The Greatest Number of Routes with Destination Country as Canada",
                   graph, "Airlines", "Number of Routes with Destination Country as Canada", "q1.pdf")
    elif question == "--QUESTION=q2":
        dictionary = question2(airlines_df, airports_df, routes_df, f2)
        graph_type(dictionary, "Top 30 Countries with Least Appearances as Destination Country on the Routes Data",
                   graph, "Country", "Number of Appearances as Destination Country", "q2.pdf")
    elif question == "--QUESTION=q3":
        dictionary = question3(airlines_df, airports_df, routes_df, f3)
        graph_type(dictionary, "Top 10 Destination Airports",
                   graph, "Airport", "Number of Appearances as Destination Airport", "q3.pdf")
    elif question == "--QUESTION=q4":
        dictionary = question4(airlines_df, airports_df, routes_df, f4)
        graph_type(dictionary, "Top 15 Destination Cities",
                   graph, "City", "Number of Appearances as Destination City", "q4.pdf")
    else:
        dictionary = question5(airlines_df, airports_df, routes_df, f5)
        graph_type(dictionary, "The Unique Top 10 Canadian Routes with Greatest Altitude Difference",
                   graph, "Routes", "Altitude Difference", "q5.pdf")

    f1.close()
    f2.close()
    f3.close()
    f4.close()
    f5.close()


if __name__ == '__main__':
    main()
