# StepMania 5 Songs to Sheet

An export facility for StepMania songs to Google Sheets.

### Installation

Place _Songs to Sheet_ in your StepMania top level directory (the one with _Songs_).

### Usage

1. Run _Songs to Sheet.exe_. Data files (CSV) will be created and placed in _output_ (eg. _Songs to Sheet/output/Singles.csv_)

2. Import selected CSV file into Google sheets
* Open your [Google Drive](https://drive.google.com).
* Open an existing spreadsheet. (or create and open a new spreadsheet, _New_ -> _Google Sheet_)
* _File_ -> _Import_ -> _Upload_
* Navigate to your selected CSV file (_Songs to Sheet/output_) and select it for import.
* In the _Import file_ window
   * Choose your _Import location_
   * Set the _Separator type_ to _Custom_ and _semi-colon_ (;)
   * Check _Convert text to numbers, dates and formulas_
   * Click _Import Data_
   * Repeat for each selected CSV
   * NOTE: Google Drive will leave a copy of the CSV laying around, it can be removed after import

3. Use the provided macro to format your sheet
* NOTE: The macro is deemed "unsafe" by Google because it hasn't passed through their verification process.
         If you're unsure about using it, feel free to skip this.
* Open your Google Sheet to format
* _Tools_ -> _Script Editor_
* Click _Untitled Project_ at the top to rename the project to something memorable
* On the left, rename _code.gs_ to _macros.gs_ (click the 3 dots on hover)
* Copy the text from _Songs to Sheet/Google Sheets Macro.txt_
* Replace the auto-generated code (_function myFunction() {}_) with the copied text and _Save_
* Return to your Google Sheet
* _Tools_ -> _Macros_ -> _Import_
* In the _Import_ window, click _Add function_ to the right of _formatSongSheet_ and close the _Import_ window
* _Tools_ -> _Macros_ -> _formatSongSheet_
* You'll need to authorise the macro
   * _Continue_ -> Select/login to your account
   * A window will popup, "Google hasn’t verified this app"
   * _Advanced_ -> _Go to {something memorable} (unsafe)_ -> _Allow_
* _Tools_ -> _Macros_ -> _formatSongSheet_ (to run the macro for reals this time)
* Repeat for each sheet
