# StepMania 5 Songs to Sheet

An export facility for StepMania songs to Google Sheets.
Python 3.9.4, Windows

## Installation

Place the Songs to Sheet folder in your StepMania top level directory (the one with _Songs_).

## Usage

### Run "Songs to Sheet.exe"

* Data files (CSV) will be placed in a folder called "output" (eg. "Songs to Sheet/output/Singles.csv")

### Import selected data file into Google sheets

1. Open your [Google Drive](https://drive.google.com)
2. Open a spreadsheet (or create new, _New_ -> _Google Sheet_)
3. _File_ -> _Import_ -> _Upload_
   * Navigate to your selected CSV file ("Songs to Sheet/output") and select it for import.
4. In the _Import file_ window
__NOTE__: Google Drive will leave a copy of the CSV file laying around, it can be removed after import

   * Choose _Import location_
   * Change _Separator type_ to __Custom__ and __;__ (semi-colon)
   * Check _Convert text to numbers, dates and formulas_
   * _Import Data_
   * Repeat for each selected file

### Use the provided macro to format your sheet
__NOTE__: The macro is deemed "unsafe" by Google because it hasn't passed through their verification process.
If you're unsure about using it, skip it and format the sheet manually.

1. Open your Google Sheet you wish to format
2. _Tools_ -> _Script Editor_
   * Click __Untitled Project__ at the top and rename the project to something memorable
   * On the left, rename __code.gs__ to __macros.gs__ (click the 3 dots on hover)
   * Copy the text from "Songs to Sheet/Google Sheets Macro.txt"
   * Replace the auto-generated code ("function myFunction() ...") with the copied text and _Save_
   * Return to your Google Sheet
3. _Tools_ -> _Macros_ -> _Import_
   * Click _Add function_ to the right of _formatSongSheet_ and close the window
4. _Tools_ -> _Macros_ -> _formatSongSheet_
   * Authorise the macro
   * _Continue_ -> Select/login to your account
   * A window will popup, "Google hasn’t verified this app"
   * _Advanced_ -> _Go to YourProjectName (unsafe)_ -> _Allow_
5. _Tools_ -> _Macros_ -> _formatSongSheet_ (to run the macro for reals this time)
6. Repeat for each sheet
