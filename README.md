# immunizationSJ

The current implementation uses [DataTables](http://www.datatables.net/) for displaying the data on a web page in a way that is easy to search and sort.

The data comes as an Excel file which needs to be prepared for conversion to a CSV file, which is then placed as JSON to be read by the web page.

A demonstration of this in action is available on [this project's GitHub Page](http://codeforsanjose.github.io/immunizationSJ/).

## Preparing the Excel file for export to CSV

The provided Excel spreadsheets contain headers which span multiple columns. They also contain Unicode characters which do not readily transfer over to JSON or HTML without additional work or configuration.

The column headers and title information leading up to the actual rows of data should be removed, in addition to the symbol legend which is at the very bottom of the data set.

The file can then be saved or exported as a CSV that is ready for the next step.


## Converting the CSV into JSON

Two problems with the provided data set become apparent when trying to convert it into JSON.

* The school codes sometimes start with a 0, making these values come up as `undefined` when interpreted as JSON (making the JSON invalid and therefore unusable by DataTables).

* There are some holes present in the data for some schools. The field is left blank, resulting in a null array value which is also invalid for JSON (results in two consecutive commas: `,,` instead of some value like `,0,` or `,"",`)

A quick and dirty way of doing this is to use a CSV->JSON converter which handles these issues. One such converter is the [Convert CSV to JSON](http://www.convertcsv.com/csv-to-json.htm) site.

In order for the data to be usable by DataTables, the JSON must be a "JSON Array", that is, only the values are present for each row in the Excel file as a two-dimensional array. An example of a working CSV file and JSON file are available in the `data` and `data_html` folders, respectively.


## TODO:

* programmatically convert the CSV file into usable JSON, properly handling the null values and any school codes having a leading zero

* implement a partial load mechanism so that the entire data set does not need to be loaded at each use