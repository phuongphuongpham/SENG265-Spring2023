/** @file route_manager.c
 *  @brief A pipes & filters program that uses conditionals, loops, and string processing tools in C to process airline routes.
 *  @author Felipe R.
 *  @author Hausi M.
 *  @author Jose O.
 *  @author Saasha J.
 *  @author Victoria L.
 *  @author Phuong Pham
 *
 */
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

/**
 * Function: main
 * --------------
 * @brief The main function and entry point of the program.
 *
 * @param argc The number of arguments passed to the program.
 * @param argv The list of arguments passed to the program.
 * @return int 0: No errors; 1: Errors produced.
 *
 */

#define MAX_CHAR_LENGTH 1024
#define NUM_LINE        69964
#define CATEGORIES      13

// Indexes each Categories
#define AIR_NAME        0
#define AIR_CODE        1
#define AIR_COUNTRY     2

#define FROM_NAME       3
#define FROM_CITY       4
#define FROM_COUNTRY    5
#define FROM_CODE       6

#define TO_NAME         8
#define TO_CITY         9
#define TO_COUNTRY      10
#define TO_CODE         11


/* void flight_details
 * Purpose: Tokenize inputLine and Store the Categories into an array
 * Output: void
 */
void flight_details(char* inputLine, char details[CATEGORIES][MAX_CHAR_LENGTH]){
     int c = 0;

     char* tok;
     char line[MAX_CHAR_LENGTH];

     strcpy(line, inputLine);
     
     tok = strtok(line, ",");
     
     
     while (tok != NULL) {	   
           strcpy(details[c], tok);
	   tok = strtok(NULL, ",");
           c++;
     }
    
}




/* int check_flight()
 * Purpose: Based on the filter (arguments), Check if any flights exist
 * Input: char* inputLine, int argc, char filter[argc-1][MAX_CHAR_LENGTH] <- Array of Arguments
 * Output: return 1 if the flight matches the filter
 *                0 otherwise
 */

int check_flight(char* inputLine, int argc, char filter[argc-1][MAX_CHAR_LENGTH]) {
     char details[CATEGORIES][MAX_CHAR_LENGTH]; 

     
     flight_details(inputLine, details);
     //printf("%s\n", details[AIR_CODE]);
     if (argc - 1 == 3) {
	 int s1 = 0;
	 int s2 = 0;
         char airline[MAX_CHAR_LENGTH];
	 char dest_country[MAX_CHAR_LENGTH];
	 strcpy(airline, filter[1]);
	 strcpy(dest_country, filter[2]);
	 while (airline[s1] != '\0') {
		 s1++;
	 }
	 airline[s1] = '\0';
	 
	 while (dest_country[s2] != '\0') {
                 s2++;
         }
         dest_country[s2] = '\0';

	 if (details[AIR_CODE] != NULL && details[TO_COUNTRY] != NULL){
	    //printf("%s, %s\n", dest_country, details[TO_COUNTRY]);
	    //printf("%s, %s\n", airline, dest_country);
            int a = strcmp(details[AIR_CODE], airline);
	    int b = strcmp(details[TO_COUNTRY], dest_country);
	    if (a == 0 && b == 0) {
		return 1;
	    }  	
	 }		
     } else if (argc - 1 == 4) {
	 int s1, s2, s3;
         char src_country[MAX_CHAR_LENGTH];
	 char dest_city[MAX_CHAR_LENGTH];
	 char dest_country[MAX_CHAR_LENGTH];
	 strcpy(src_country, filter[1]);
	 strcpy(dest_city, filter[2]);
	 strcpy(dest_country, filter[3]);
	 while (src_country[s1] != '\0') {
                 s1++;
         }
         src_country[s1] = '\0';

         while (dest_city[s2] != '\0') {
                 s2++;
         }
         dest_city[s2] = '\0';

	 while (dest_country[s3] != '\0') {
		 s3++;
	 }
	 dest_country[s3] = '\0';

         if (details[FROM_COUNTRY] != NULL && details[TO_CITY] != NULL && details[TO_COUNTRY] != NULL){
            int a = strcmp(details[FROM_COUNTRY], src_country);
	    int b = strcmp(details[TO_CITY], dest_city);
            int c = strcmp(details[TO_COUNTRY], dest_country);
            if (a == 0 && b == 0 && c == 0) {
                return 1;
            }
         }
     } else {
	 int s0, s1, s2, s3, s4;
	 char src_city[MAX_CHAR_LENGTH];
     	 char src_country[MAX_CHAR_LENGTH];
	 char dest_city[MAX_CHAR_LENGTH];
	 char dest_country[MAX_CHAR_LENGTH];
	 strcpy(src_city, filter[1]);
	 strcpy(src_country, filter[2]);
	 strcpy(dest_city, filter[3]);
	 strcpy(dest_country, filter[4]);

	 while (src_city[s0] != '\0') {
		 s0++;
	 }
	 src_city[s0] = '\0';

	 while (src_country[s1] != '\0') {
                 s1++;
         }
         src_country[s1] = '\0';

         while (dest_city[s2] != '\0') {
                 s2++;
         }
         dest_city[s2] = '\0';

         while (dest_country[s3] != '\0') {
                 s3++;
         }
         dest_country[s3] = '\0';

         if (details[FROM_CITY] != NULL && details[FROM_COUNTRY] != NULL && details[TO_CITY] != NULL && details[TO_COUNTRY] != NULL){
            int a = strcmp(details[FROM_CITY], src_city);
	    int b = strcmp(details[FROM_COUNTRY], src_country);
            int c = strcmp(details[TO_CITY], dest_city);
            int d = strcmp(details[TO_COUNTRY], dest_country);
            if (a == 0 && b == 0 && c == 0 && d == 0) {
                return 1;
            }
         }
     }
	  
     	 
     return 0;
}




int main(int argc, char *argv[])
{
    // TODO: your code.
    FILE *input;
    FILE *output;   



    /* Store Arguments (3 Cases)
     * Case 1: DATA, AIRLINE, DEST_COUNTRY
     * Case 2: DATA, SRC_COUNTRY, DEST_CITY, DEST_COUNTRY
     * Case 3: DATA, SRC_CITY, SRC_COUNTRY, DEST_CITY, DEST_COUNTRY
     */

    char filter[argc-1][MAX_CHAR_LENGTH];
    if (argc == 4) { //Case 1
       int total_read1, total_read2, total_read3;

       total_read1 = sscanf(argv[1], "--DATA=%s", filter[0]);
       total_read2 = sscanf(argv[2], "--AIRLINE=%s", filter[1]);
       total_read3 = sscanf(argv[3], "--DEST_COUNTRY=%s", filter[2]);

      
    } else if (argc == 5) { //Case 2
       int total_read1, total_read2, total_read3, total_read4;

       total_read1 = sscanf(argv[1], "--DATA=%s", filter[0]);
       total_read2 = sscanf(argv[2], "--SRC_COUNTRY=%s", filter[1]);
       total_read3 = sscanf(argv[3], "--DEST_CITY=%s", filter[2]);
       total_read4 = sscanf(argv[4], "--DEST_COUNTRY=%s", filter[3]);
    } else if (argc == 6) { //Case 3
       int total_read1, total_read2, total_read3, total_read4, total_read5;

       total_read1 = sscanf(argv[1], "--DATA=%s", filter[0]);
       total_read2 = sscanf(argv[2], "--SRC_CITY=%s", filter[1]);
       total_read3 = sscanf(argv[3], "--SRC_COUNTRY=%s", filter[2]);
       total_read4 = sscanf(argv[4], "--DEST_CITY=%s", filter[3]);
       total_read5 = sscanf(argv[5], "--DEST_COUNTRY=%s", filter[4]);

    }

   

    // Open input file and Check if file exists
    input = fopen(filter[0], "r");
    
    if (input == NULL) {
	printf("%s", "Failed to open file");
    }
    



    // Read and Store input file into char array line by line
    static char arr[NUM_LINE][MAX_CHAR_LENGTH]; 
    
    int row = 0;
    while(fgets(arr[row], MAX_CHAR_LENGTH, input)) {
  	  row++;
    } 
    
     

    // Filter and Print out List of Flights match the Filter 
    int exist = 0;
    char flight[MAX_CHAR_LENGTH];
    //char result_list[NUM_LINE][MAX_CHAR_LENGTH];
    //int v = 0;
    for (int r = 1; r < row; r++) {
	strcpy(flight, arr[r]);
	//printf("%s\n", flight);
	exist = check_flight(flight, argc, filter);
	if (exist == 1){
	   printf("%s\n", arr[r]);
	   //strcpy(result_list[v], arr[r]);
	}	
    }


    output = fopen("output.txt", "w");
    fputs("NO RESULTS FOUND.\n", output);    

    fclose(output); 



    
    exit(0);
}


