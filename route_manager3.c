/** @file route_manager.c
 *  @brief A small program to analyze airline routes data.
 *  @author Mike Z.
 *  @author Felipe R.
 *  @author Hausi M.
 *  @author Jose O.
 *  @author Saasha J.
 *  @author Victoria L.
 *  @author Phuong Pham
 *
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "list.h"
#include "emalloc.h"

// TODO: Make sure to adjust this based on the input files given
#define MAX_LINE_LEN 100
#define MAX_FLIGHT_INFO 500

/**
 * @brief Serves as an incremental counter for navigating the list.
 *
 * @param p The pointer of the node to print.
 * @param arg The pointer of the index.
 *
 */
void inccounter(node_t *p, void *arg)
{
    int *ip = (int *)arg;
    (*ip)++;
}

/**
 * @brief Allows to print out the content of a node.
 *
 * @param p The pointer of the node to print.
 * @param arg The format of the string.
 *
 */
void print_node(node_t *p, void *arg)
{
    char *fmt = (char *)arg;
    printf(fmt, p->subject);
}

/**
 * @brief Allows to print each node in the list.
 *
 * @param l The first node in the list
 *
 */
void analysis(node_t *l)
{
    int len = 0;

    apply(l, inccounter, &len);
    printf("Number of words: %d\n", len);

    apply(l, print_node, "%s\n");
}

typedef struct flightInfo {
    char *airlineName;
    char *airlineCode;
    char *airlineCountry;
    char *fromName;
    char *fromCity;
    char *fromCountry;
    char *fromCode;
    char *fromAltitude;
    char *toName;
    char *toCity;
    char *toCountry;
    char *toCode;
    char *toAltitude;
}flightInfo;

/**
 * @brief create: initialize the values of struct flightInfo
 *
 * @param flightNode A node type node_t.
 * @return flightInfo object.
 *
 */
flightInfo *create(node_t *flightNode) {
    char *s = flightNode->subject;
    char line[MAX_FLIGHT_INFO];
    char *tok;
    strncpy(line, s, strlen(s));
    //printf("%s\n", s);
    int i = 0;
    flightInfo *temp = (flightInfo *)emalloc(sizeof(flightInfo));

    tok = strtok(line, "\n");
    while (tok != NULL) {
        if (i == 0) {
            temp->airlineName = strdup(tok);
        
        } else if (i == 1) {
            temp->airlineCode = strdup(tok);
            
        } else if (i == 2) {
            temp->airlineCountry = strdup(tok);
            
        } else if (i == 3) { 
            temp->fromName = strdup(tok);
            
        } else if (i == 4) {
            temp->fromCity = strdup(tok);
            
        } else if (i == 5) {
            temp->fromCountry = strdup(tok);
            
        } else if (i == 6) {
            temp->fromCode = strdup(tok);
            
        } else if (i == 7) {
            temp->fromAltitude = strdup(tok);
            
        } else if (i == 8) {
            temp->toName = strdup(tok);
           
        } else if (i == 9) {
            temp->toCity = strdup(tok);
            
        } else if (i == 10) {
            temp->toCountry = strdup(tok);
            
        } else if (i == 11) {
            temp->toCode = strdup(tok);
            
        } else if (i == 12) {
            temp->toAltitude = strdup(tok);
            
        }
        
        tok = strtok(NULL, "\n");
        i++;
    }
    return temp;
}

/**
 * @brief merge: iterate through airlineList and 
 *               compare if the word exist in the Node's subject
 *
 * @param List Node.
 * @param word word to compare to the node List subject.
 * @return node_t: The node exists in the List
 *
 */
node_t *merge(node_t *List, char* word){
    // 
    node_t  *ptr = List;

    if (List == NULL) {
        return NULL;
    }
    while (ptr != NULL){
        
        if (strcmp(ptr->subject,word) == 0){
            return ptr;
        }
        ptr = ptr->next;
    }
    return NULL;
}

/**
 * @brief writeToOutput write the output to output.csv
 *
 * @param List The linkedlist of the answer responding to question.
 * @param n Top n flights responding the question.
 * @return None.
 *
 */
void writeToOutput(node_t *List, int n){
    FILE *file;
    file = fopen("output.csv", "w");
    node_t *ptr = List;
    fprintf(file, "%s,%s\n", "subject", "statistic");
    int i = 0;
    while (ptr != NULL && i < n) {
        fprintf(file, "\"%s\",%d\n", ptr->subject, ptr->statistic);
        i++;
        ptr = ptr->next;
    }
    fclose(file);
}

/**
 * @brief Answering q1: What are the top N airlines that offer the greatest 
 *        number of routes with destination country as Canada?
 *
 * @param allFlights The linkedlist of all Flights.
 * @param n Top n flights responding to q1.
 * @return None.
 *
 */
void q1(node_t* allFlights, int n){
    flightInfo *f = NULL;
    node_t *airlineList = NULL;
    node_t *sameAirline = NULL;
    node_t *temp = NULL;
    char *p;
    int patternLen;
    for ( ; allFlights->next != NULL; allFlights = temp) {
        temp = allFlights->next;
        f = create(temp);
        char *destCountry = f->toCountry;
        char airline[MAX_LINE_LEN];
        char code[MAX_LINE_LEN];
        

        if ((strncmp(destCountry, "to_airport_country: Canada", strlen("to_airport_country: Canada"))) == 0) {
            sscanf(f->airlineName, "airline_name: %[^\n]", airline);
            
            strcat(airline, " (");
            strcpy(code, f->airlineCode);
            patternLen = strlen("airline_icao_unique_code: ");
            p = &code[patternLen];
            strcpy(code, p);
            strcat(airline, code);
            strcat(airline, ")");

            sameAirline = merge(airlineList, airline);
            if (sameAirline == NULL) {
                airlineList = add_end(airlineList, new_node(airline, 1));

            } else {
                sameAirline->statistic += 1;
            }  
        }
    }
    
    node_t *sorted = NULL;
    node_t  *ptr = airlineList;
    char *su;
    int st;

    while (ptr != NULL){
        su = ptr->subject;
        st = ptr->statistic;
        sorted = add_inorder(sorted, new_node(su, st));
        ptr = ptr->next;
    }
    
    writeToOutput(sorted, n);
   
    free(f);   
    node_t  *temp_n = NULL;
    for ( ; airlineList != NULL; airlineList = temp_n) {
        temp_n = airlineList->next;
        free(airlineList->subject);
        free(airlineList);
    }

    node_t  *temp_n2 = NULL;
    for ( ; sorted != NULL; sorted = temp_n2 ) {
        temp_n2 = sorted->next;
        free(sorted->subject);
        free(sorted);
    }
}

/**
 * @brief Answering q2: What are the top N countries with least appearances 
 *        as destination country on the routes data?
 *
 * @param allFlights The linkedlist of all Flights.
 * @param n Top n flights responding to q2.
 * @return None.
 *
 */
void q2(node_t* allFlights, int n){
    flightInfo *f = NULL;
    node_t *destinationList = NULL;
    node_t *sameCountry = NULL;
    node_t *temp = allFlights;
    char *p;

    for ( ; allFlights->next != NULL; allFlights = temp) {
        temp = allFlights->next;
        f = create(temp);
        
        char country[MAX_LINE_LEN];
        sscanf(f->toCountry, "to_airport_country: %[^\n]", country);
        
        if (country[0] == '\''){
            p = &country[2];
            strcpy(country, p);
        }

        sameCountry = merge(destinationList, country);
        if (sameCountry == NULL) {
            destinationList = add_end(destinationList, new_node(country, 1));

        } else {
            sameCountry->statistic += 1;
        }  
    }

    node_t *sorted = NULL;
    node_t  *ptr = destinationList;
    char *su;
    int st;

    while (ptr != NULL){
        su = ptr->subject;
        st = ptr->statistic;
        sorted = addInAscOrder(sorted, new_node(su, st));
        ptr = ptr->next;
    }

    writeToOutput(sorted, n);

    free(f);
    node_t  *temp_n = NULL;
    for ( ; destinationList != NULL; destinationList = temp_n ) {
        temp_n = destinationList->next;
        free(destinationList->subject);
        free(destinationList);
    }

    node_t  *temp_n2 = NULL;
    for ( ; sorted != NULL; sorted = temp_n2 ) {
        temp_n2 = sorted->next;
        free(sorted->subject);
        free(sorted);
    }
}

/**
 * @brief Answering q3: What are the top N destination airports?
 *
 * @param allFlights The linkedlist of all Flights.
 * @param n Top n flights responding to q3.
 * @return None.
 *
 */
void q3(node_t* allFlights, int n){
    flightInfo *f = NULL;
    node_t *destinationList = NULL;
    node_t *sameAirport = NULL;
    node_t *temp = NULL;
    char *p;
    int patternLen = 0;

    for ( ; allFlights->next != NULL; allFlights = temp) {
        temp = allFlights->next;
        char airport[MAX_FLIGHT_INFO] = "";
        f = create(temp);

        char name[MAX_LINE_LEN];
        char code[MAX_LINE_LEN];
        char city[MAX_LINE_LEN];
        char country[MAX_LINE_LEN];
        
        sscanf(f->toName, "to_airport_name: %[^\n]", name);
        strcat(airport, name);
        strcat(airport, " (");
        
        strcpy(code, f->toCode);
        patternLen = strlen("to_airport_icao_unique_code: ");
        p = &code[patternLen];
        strcpy(code, p);
        strcat(airport, code);
        strcat(airport, "), ");
        
        strcpy(city, f->toCity);
        patternLen = strlen("to_airport_city: ");
        p = &city[patternLen];
        strcpy(city, p);
        strcat(airport, city);
        strcat(airport, ", ");

        strcpy(country, f->toCountry);
        patternLen = strlen("to_airport_country: ");
        p = &country[patternLen];
        strcpy(country, p);
        strcat(airport, country);
        
        sameAirport = merge(destinationList, airport);
        if (sameAirport == NULL) {
            destinationList = add_end(destinationList, new_node(airport, 1));
            
        } else {
            sameAirport->statistic += 1;
        }  
    }

    node_t *sorted = NULL;
    node_t  *ptr = destinationList;
    char *su;
    int st;

    while (ptr != NULL){
        su = ptr->subject;
        st = ptr->statistic;
        sorted = add_inorder(sorted, new_node(su, st));
        ptr = ptr->next;
    }

    writeToOutput(sorted, n);
    
    free(f);
    node_t  *temp_n = NULL;
    for ( ; destinationList != NULL; destinationList = temp_n ) {
        temp_n = destinationList->next;
        free(destinationList->subject);
        free(destinationList);
    }

    node_t  *temp_n2 = NULL;
    for ( ; sorted != NULL; sorted = temp_n2 ) {
        temp_n2 = sorted->next;
        free(sorted->subject);
        free(sorted);
    }
}

/**
 * @brief The main function and entry point of the program.
 *
 * @param argc The number of arguments passed to the program.
 * @param argv The list of arguments passed to the program.
 * @return int 0: No errors; 1: Errors produced.
 *
 */
int main(int argc, char *argv[])
{   
    // Read Arguments
    char inputFile[MAX_LINE_LEN];
    int question;
    int n;
    sscanf(argv[1], "--DATA=%s", inputFile);
    sscanf(argv[2], "--QUESTION=%d", &question);
    sscanf(argv[3], "--N=%d", &n);
    
    // Read Yaml File and Store each flight into linkedlist allFlights
    FILE *file;
    char line[MAX_LINE_LEN];
    char flight[MAX_FLIGHT_INFO];
    char *slice;
    node_t* allFlights = NULL;
    int i;

    file = fopen(inputFile, "r");
    while(fgets(line, MAX_LINE_LEN, file)) {
        if ((strncmp(line, "-", 1) != 0) && (i != 0)) {
            slice = &line[2];
            strcat(flight, slice);

        } else if (i != 0) {
            if (flight != NULL) {
                allFlights = add_end(allFlights, new_node(flight, 0));
            }
            slice = &line[2];
            strncpy(flight, slice, MAX_LINE_LEN);
        }
        i++;
    }
    allFlights = add_end(allFlights, new_node(flight, 0));
    
    
    // Call the Function responding to the argument
    if (question == 1){
        q1(allFlights, n);
    } else if (question == 2){
        q2(allFlights, n);
    } else if (question == 3){
        q3(allFlights, n);
    }

    
    node_t  *temp_n = NULL;
    for ( ; allFlights != NULL; allFlights = temp_n ) {
        temp_n = allFlights->next;
        free(allFlights->subject);
        free(allFlights);
    }
    exit(0);
}
