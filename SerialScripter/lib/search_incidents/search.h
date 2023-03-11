// incident_search.h

#ifndef INCIDENT_SEARCH_H
#define INCIDENT_SEARCH_H

struct Incident {
  char Host[256];
  char Name[256];
  char User[256];
  char Process[256];
  char RemoteIP[256];
  char Cmd[256];
};

struct Host {
  char name[256];
};

int search_incidents(struct Incident *incidents, int num_incidents,
  char *search_string, struct Host *hosts, int max_hosts);

#endif