## Database Scripts

These scripts are broken into three categories: initialization scripts (init), general scripts (scripts), and testing scripts (test).

### Initialization Scripts

These scripts create the tables needed for the database to work properly. They also include deconstructor scripts if the database needs to be removed.

### General Scripts

These are useful scripts that the backend will likely have to use in order to properly query information from the database. They may also include general tutorials. (There are not many of these right now, but more should be added soon.)

### Test Scripts

These scripts insert dummy data into the database after initialization and allow you to run sample queries on the data, in order to make sure the database works as intended. (Right now, most of the tests simply check for proper data insertion. More tests should be added to test any general scripts added into the directory above.) 