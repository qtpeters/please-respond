# Please Respond

> Your marketing firm is tracking popularity of events around the world. You have been tasked with tracking down RSVPs for events on a popular online service that helps to organize events, Meetup.com.

## Requirements
Collect streaming RSVP data from Meetup.com and output aggregate information about the observed Event RSVPs. 

Your program should connect to the Meetup.com and collect RSVPs to Meetup Events for a configurable time period (default 60 seconds). 

The following aggregate information should be calculated:

- Total # of RSVPs received
- Date of Event furthest into the future
- URL for the Event furthest into the future
- The top 3 number of RSVPs received per Event host-country

### Input Format
Your program should connect to the Meetup.com RSVP HTTP data stream at http://stream.meetup.com/2/rsvps

- Meetup RSVP reference: https://www.meetup.com/meetup_api/docs/stream/2/rsvps/

You may assume that the input files are correctly formatted. Error handling for invalid input files may be ommitted.

### Output Format
The output will specify the aggregate calculated information in a comma-delimited format.

```
total,future_date,future_url,co_1,co_1_count,co_2,co_2_count,co_3,co_3_count
```

The program will output to screen or console (and not to a file). 

## Sample Data
The following may be used as a sample output dataset.

### Ouput

```
100,2019-04-17 12:00,https://www.meetup.com/UXSpeakeasy/events/258247836/,us,40,uk,18,jp,12
```