## Database Scripts

These scripts are broken into three categories: initialization scripts (init), general scripts (scripts), and testing scripts (test).

### Initialization Scripts

There are only two files in this folder: `createtables.sql` and `droptables.sql`. The first file MUST BE RUN FIRST in order to create the tables needed for proper database function. The second file will remove these tables from the database; it should only be run if the tables need to be deleted or modified. 

### General Scripts

These are example scripts that illustrate how to properly insert, remove, and query information from the database. They may also include other general tutorials.

### Test Scripts

These scripts insert dummy data into the database and allows queries on this data, in order to make sure the database works as intended. (Right now, most of the tests simply check for proper data insertion. More tests may be added to test general scripts, if required.) 