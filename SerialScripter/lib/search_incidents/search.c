#include <stdio.h>
#include <string.h>
#include <stdlib.h>

// Ratcliff-Obershelp algorithm for string similarity
int ratcliff_obershelp(char *s1, char *s2) {
    int len1 = strlen(s1), len2 = strlen(s2);
    if (len1 == 0 || len2 == 0) {
        return 0;
    }
    int max_len = (len1 > len2) ? len1 : len2;
    int lcs_len = 0;
    int i, j, k;
    for (i = 0; i < len1; i++) {
        for (j = 0; j < len2; j++) {
            for (k = 0; i + k < len1 && j + k < len2 && s1[i + k] == s2[j + k]; k++);
            if (k > lcs_len) {
                lcs_len = k;
            }
        }
    }
    return (2 * lcs_len * 100) / max_len;
}

// Struct definition
struct Incidents {
    char host[50];
    char name[50];
    char user[50];
    char process[50];
    char remoteIP[50];
    char cmd[100];
};

// Function to find matching incidents
struct Incidents* find_matching_incidents(struct Incidents* incidents, int num_incidents, char* search_string, double threshold, int* num_matches) {
    // Allocate memory for the matches array
    struct Incidents* matches = (struct Incidents*) malloc(num_incidents * sizeof(struct Incidents));
    if (matches == NULL) {
        fprintf(stderr, "Memory allocation error\n");
        exit(EXIT_FAILURE);
    }

    // Search for similar strings
    int count = 0;
    for (int i = 0; i < num_incidents; i++) {
        int similarity = ratcliff_obershelp(search_string, incidents[i].host);
        similarity = (similarity > ratcliff_obershelp(search_string, incidents[i].name)) ? similarity : ratcliff_obershelp(search_string, incidents[i].name);
        similarity = (similarity > ratcliff_obershelp(search_string, incidents[i].user)) ? similarity : ratcliff_obershelp(search_string, incidents[i].user);
        similarity = (similarity > ratcliff_obershelp(search_string, incidents[i].process)) ? similarity : ratcliff_obershelp(search_string, incidents[i].process);
        similarity = (similarity > ratcliff_obershelp(search_string, incidents[i].remoteIP)) ? similarity : ratcliff_obershelp(search_string, incidents[i].remoteIP);
        similarity = (similarity > ratcliff_obershelp(search_string, incidents[i].cmd)) ? similarity : ratcliff_obershelp(search_string, incidents[i].cmd);

        if ((double) similarity / 100 > threshold) {
            matches[count++] = incidents[i];
        }
    }

    // Update the number of matches
    *num_matches = count;

    // Return the matches array
    return matches;
}