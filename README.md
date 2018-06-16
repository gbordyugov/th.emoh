## Case 1

The supplied Python script generates test data for all three tables
and saves it in the `csv` directory.

The supplied SQL query refreshes tables, loads the data from the csv
files and offers two different solutions to Case 1 question
 1. The first solution additionally checks if the user ids have been
    registered as part of attributions before counting them in the
    button click and bank details tables
 2. The second solution is a bit more simple-minded and just counts
    the number of distinct user in all three tables.

I assumed that the app counts as installed if the corresponding
`anonymous_user_id` appears in the attributions table (please correct
me if I'm wrong here).

All scripts should be runnable out of the box, the only things that
need adjustment is the paths to the csv files in the COPY statements
in the SQL code.

In the test case uploaded, there are 10000 attributions, 5000 user
register events (not all of them are from unique users, your mileage
may vary depending on the result of the random sampling with
replacement from them) and 1000 bank account events (a smaller number
of unique events too).

## Case 2

I would suggest having a master event table with rows representing
events. A single event would be a single row, characterised by the
landlord id, event type, event source, property id, etc.

Additionally, if you anticipate many event types (such as price
change, maintenance performed in the property, acquiring / getting rid
of a property as in Case 3, etc.) I would suggest having a separate
table for those event types - it's a standard DB normalization
practice.

The same for the event sources - if you're anticipating new possible
event sources in future, it would come in handy to have a separate
table holding that information.

Going back to the master table with events, I would suggest it to  have
 - user_id identifying the user
 - a field referencing an event type from the corresponding table as
   described above
 - event source referencing the table with event sources, as describe
   above.

All of this can be realized using common tools. For example, Google
Analytics offers the so-called "Custom Dimensions" for single events
that can hold any additional information and which can be used to
reference the auxiliary tables (event type, event source).

Another advantage of Google Analytics would that that it exports most
of the data into the designated tables on Google BigQuery, which can
be queried using user-defined SQL queries (supplied either from their
front end client or public API), thus allowing for virtually unlimited
additional analytics logic. Additionally, the users of Google
Analytics can create their own auxiliary tables using the BigQuery
infrastructure and use them in parallel to the GA export tables, thus
allowing performing all analytics in the cloud without the need of
downloading the data.

Note on anonymous users: Google Analytics (and probably many other
tracking systems) has its own user tracking system, based on cookies.
So if an anonymous user then should log-in later or create an account,
their history can be tracked before log-in/sign-in based on that
cookie.


## Case 3

I would introduce here a new event type "Change in number of
apartments" (or even a pair "Acquired new apartment" / "Sold
apartment"), which would be just another event type in the table
layout, which I described above.

Then querying for the number of apartments that a certain landlord
possesses would be realized by
 1. taking only events of that type for the given user and
 2. aggregating over them with the suitable choice of aggregator
    (depends on the particular representation of that
    acquire/get-rid-of event type).
