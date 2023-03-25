#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MATCH_THRESHOLD 0.5

struct Incident {
    const char *host;
    const char *type;
    const char *name;
    const char *time;
    const char *user;
    const char *severity;
    const char *payload;
};

double ratcliff_obershelp(const char *str1, const char *str2) {
    int len1 = strlen(str1);
    int len2 = strlen(str2);

    if (len1 == 0 || len2 == 0) {
        return 0.0;
    }

    int max_len = (len1 > len2) ? len1 : len2;
    int vector1[max_len];
    int vector2[max_len];
    memset(vector1, 0, max_len * sizeof(int));
    memset(vector2, 0, max_len * sizeof(int));

    int i, j;
    for (i = 0; i < len1; i++) {
        for (j = 0; j < len2; j++) {
            if (str1[i] == str2[j]) {
                int k, l;
                for (k = i, l = j; k < len1 && l < len2 && str1[k] == str2[l]; k++, l++);
                if (k > i) {
                    int len = k - i;
                    for (k = i; k < i + len; k++) {
                        vector1[k] = 1;
                    }
                    for (l = j; l < j + len; l++) {
                        vector2[l] = 1;
                    }
                    i += len - 1;
                    j += len - 1;
                }
            }
        }
    }

    int matches = 0;
    for (i = 0; i < max_len; i++) {
        if (vector1[i] && vector2[i]) {
            matches++;
        }
    }

    double ratio = (2.0 * matches) / (len1 + len2);

    return ratio;
}


struct IncidentList {
    struct Incident *incidents;
    int size;
};
// create a function that returns a list of Incidents
// that are in the last X days

struct IncidentList search_incidents(const struct IncidentList *incident_list, const char *search, int num_incidents) {
    struct IncidentList results = {NULL, 0};

    char *term_copy = strdup(search);
    char **search_terms = NULL;
    int num_terms = 0;

    char *tok = strtok(term_copy, " ");
    while (tok != NULL) {
        search_terms = realloc(search_terms, sizeof(char*) * ++num_terms);
        search_terms[num_terms-1] = tok;
        tok = strtok(NULL, " ");
    }

    for (int i = 0; i < num_incidents; i++) {
        for (int j = 0; j < num_terms; j++) {
            struct Incident *incident = &incident_list->incidents[i];
            if (MATCH_THRESHOLD < ratcliff_obershelp(search_terms[j], incident->name) ||
                MATCH_THRESHOLD < ratcliff_obershelp(search_terms[j], incident->user) ||
                MATCH_THRESHOLD < ratcliff_obershelp(search_terms[j], incident->host) ||
                MATCH_THRESHOLD < ratcliff_obershelp(search_terms[j], incident->type) ||
                MATCH_THRESHOLD < ratcliff_obershelp(search_terms[j], incident->time) ||
                MATCH_THRESHOLD < ratcliff_obershelp(search_terms[j], incident->severity) ||
                MATCH_THRESHOLD < ratcliff_obershelp(search_terms[j], incident->payload)) {
                results.incidents = realloc(results.incidents, sizeof(*results.incidents) * (results.size+1));
                results.incidents[results.size++] = *incident;
                break;
            }
        }
    }

    free(search_terms);
    free(term_copy);

    return results;
}


