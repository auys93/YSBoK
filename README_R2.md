**Scenario**

  - Assume you have log data of the following form:
  
  - Keys = values of on each line.
  
  - The values are quoted strings, unquoted strings or integers in an unsorted manner.
  
  - The data has strings with the value of timestamp, message, ID, and field_#

**Prompt**

  - Using any programming or scripting language of your choice, parse this data into a table
  
  - The CSV has a header row formatted: as ID, Timestamp (YYYY-MM-DD), Message, Field_1, Field_2, Field_3,Field_4,Field_5_Field_6, Field_9
  
  - The CSV is sorted by the ID field.
  
  - Fields and their respective values are persevered
  
  - Create a header in the column to the right of the timestamp called timezone, and insert the timezone in there.
