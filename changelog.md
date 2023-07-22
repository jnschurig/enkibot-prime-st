#### 0.4.0 2023-07-22

- Added world page anchors for quicker navigation to each world section (1, 2, and 3)
- Added !Blue section for blue magic. Select `Blue-Mage` from the selector to enable it.
- Also added a dedicated !Blue tab for detailed reading.
- Moved class resource files into a separate directory to prevent cluttering.
- Changed file-system lookups to fully-qualified vs relative.

#### 0.3.0 2023-07-16

- Added Mix section in the sidebar. Select `Chemist` from the selector to enable it.
- Added experimental `Reset Session` button to `Additional Options` expander. 
- Changed default expander behavior. Previous: open. Current: closed.
- Numerous tiny tweaks.

#### 0.2.2 2023-07-14

- Fixed the data fetch so it will grab a copy from `https://enkibot-prime.herokuapp.com/debug/`.
- It will cache the result for minimal hits to the website.
- In the event a non-200 http result, it will use a local copy of the data.

#### 0.2.1 2023-07-11

- Fixed a minor issue with filenames when no jobs/classes are selected.

#### 0.2.0 2023-07-11

- Implemented versioning and changelog.
- Added tabs bar for additional pages.
- Added tab for unformatted text.
- Added download button for unformatted text (as .md file).
- Renamed the "Show Original Markdown" button to "Simplified Display".
- Other minor formatting and spacing changes.

#### 0.1.1 2023-07-10

- Fixed a bug with searching that caused every character to display on its own row.

#### 0.1.0 2023-07-09

- Officially created Enkibot-Prime-ST.
- Added `pandas` as a requirement for creating and manipulating dataframes.
