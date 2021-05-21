# StepMania Songs to Sheet

An export facility for StepMania songs to Google Sheets.

* Compiles your installed songs' data into CSVs file for each mode which can be imported into any spreadsheeting software.
* Detects errors in your songs' installations, including missing files and bad song definitions.
* A macro is provided to quickly format your data cleanly in Google Sheets.

Only supports __Singles__ and __Double__ modes, and is __Windows__ only.

Contact me on Discord: __Fishlips13#1467__

## Installation

1. Download the latest zip from __Releases__
2. Extract to your StepMania top level folder (the one with the "Songs" folder)

## Usage

### Run "Songs to Sheet.exe"

* Data files (CSV) will be placed in the __output__ folder (eg. "Songs to Sheet/output/Singles.csv")
* Refer to the log file generated in __output__ for details on any errors encountered

### Import selected data file into Google sheets

__NOTE__: After import, Google Drive will leave a copy of the data file laying around. It can be removed after import.

1. Open your [Google Drive](https://drive.google.com)
2. Open a spreadsheet or create new (_New_ -> _Google Sheet_)
3. _File_ -> _Import_
   * __Upload__ or navigate to your selected data file ("Songs to Sheet/output") and select it for import
   * Choose your __Import location__
   * Change __Separator type__ to __Custom__ and "__;__" (semi-colon)
   * Check __Convert text to numbers, dates and formulas__ (checked by default)
   * Click __Import Data__
   * Repeat for each selected file (make sure to change your __Import location__ if you want multiple sheets in the same file)

### Use the provided macro to format your sheet

__NOTE__: The macro is deemed "unsafe" by Google because it hasn't passed through their verification process.
If you're unsure about using it, skip it and format the sheet manually.

1. Open your Google Sheet you wish to format
2. _Tools_ -> _Script Editor_
   * Click __Untitled Project__ at the top and rename the project to something memorable
   * On the left, rename __code.gs__ to __macros.gs__ (click the 3 dots on hover)
   * Copy the text from "Songs to Sheet/Google Sheets Macro.txt"
   * Replace the auto-generated code (function myFunction() ...) with the copied text and __Save__
   * Return to your Google Sheet
3. _Tools_ -> _Macros_ -> _Import_
   * Click __Add function__ to the right of __formatSongSheet__
   * Return to your Google Sheet
4. _Tools_ -> _Macros_ -> _formatSongSheet_
   * _Continue_ -> Select/login to your account
   * A window will popup, "Google hasn’t verified this app"
   * _Advanced_ -> _Go to YourProjectName (unsafe)_ -> _Allow_
      * Visit your [Google Permissions](https://myaccount.google.com/permissions) to remove the permission for a third-party app
   * Return to your Google Sheet
5. _Tools_ -> _Macros_ -> _formatSongSheet_ (to run the macro for reals this time)
6. Repeat for each sheet
