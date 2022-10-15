# Serial Scripter API Guide

## General endpoint structure

```
serialscripter.com/
	wingoEDR/
		GET updateconfig
		systemhealth/
			POST diskspace
			POST diskusage // Maybe make an alert??
		POST activeshares
		POST generalinfo
		POST errors

	gomemento/

	common/
		POST heartbeat
		GET ipblacklist
		POST incidentalert
		GET ipwhitelist
```

## wingoEDR Endpoints

#### GET updateconfig:

This should just return the config for wingoEDR stored on the server

#### POST diskspace

Endpoint for posting the dispace of a given device

```
    {
    	"ip": {}
    	"maxdiskspace": {}
    	"remaningdiskspace": {}
    }
```

#### POST diskusage

Gives the disk active time for the past minute

```
	{
		"ip": {}
		"diskactivepercent": {}
	}
```

#### POST activeshares

Returns a list of active shares on a system. This is returned to the server because it is an operation that requires human intervention

```
	{
	  "ip": {},
	  "shares": [
	    {
	      "name": {},
	      "fullpath": {},
	      "permissions": [
	        {
	          "users": [
	            {
	              "username": {},
	              "SID": {}
	            }
	          ]
	        }
	      ],
	      "SMBversion": {}
	    }
	  ]
	}
```

#### POST generalinfo

This is the endpoint that will receive the basic info about the host on startup

```
	{
	  "ip": {},
	  "hostname": {},
	  "OS": {
	    "name": {},
	    "version": {},
	    "config": {},
	    "hotfixes": []
	  },
	  "registeredOwner": {},
	  "registeredOrganization": {},
	  "domain": {},
	  "logonServer": {}
	}
```

#### POST errors

An endpoint to recieve non-fatal errors
