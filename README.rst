======================
CalDAV roundtrip check
======================

This packages creates a test event in a CalDAV calendar, and checks that it can
be read back.


Usage
=====

Create a configuration file::

    [default]
    url = https://caldav.example.com/
    calendar = testcalendar
    username = test@example.com
    password = secret
    # loglevel = WARNING  # This default means no output for a successful run.

Now run ``caldav-check-roundtrip example.conf``. It will create an event in the
given calendar ``testcalendar`` with a random string in the
``X-Mailcheck-Token`` header, check if an event with that string exists, and
then delete the event. The exit status is 0 if sucessful, 1 on errors (e.g.
connection failed) and 2 if the event could not be found.
