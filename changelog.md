#### 1.0.0 2024-04-30

- Added extra usable sections in each expander.
- Added a popover for Big Bridge encounter chart in the Bridgamesh section.
- Added a popover image for the Neo Exdeath image reference.
- Improved the code layout as relating to !Mix resources.
- Added !Mix as a tab. Sidebar !Mix will remain available when Chemist class is selected.
- Checking the Debug box will enable !Blue and !Mix resources.
- Checking the Debug box will enable the NOT job class hints.
- Fixed a significant bug in which `Shield`, `Rod`, and other such job
  tags were not being used, so relevant hints were either always on or
  never on.
- Added more detail to the README.
- Job query parameters enabled!
  - Now the selected jobs can be changed as part of a url using `job=job-name`.
  - Link directly to the selected classes.
- Improved data parser fetches hint data from source repository.
- Added multiple output formats for raw data.
<!-- - Replaced boss_resources and incorporated it into the Enkibot class. -->
<!-- - Replaced blue_resources and incorporated it into the Enkibot class. -->
- todo: fix the search
- Added "UNKNOWN ADVANCE" option to job list to show all advance job hints.
<!-- - Query params for searches (maybe just the main one) -->

#### 0.6.0 2023-08-04

- Renamed the `Boss Compendium` tab to `Bosses` in order to reduce tab crowding.
- Renamed the `!Blue Grimoire` tab to `!Blue` in order to reduce tab crowding.
- Minor corrections to many of the boss detail yaml files.
- Additional detail added to stats (HP, MP, Types, and more Statuses)
- Implemented a default order on the boss data to generally be in encounter order.
- Minor code organization changes to support more kinds of data.

#### 0.5.0 2023-08-01

- Updated the About text to be a little more clear and descriptive.
- Added certain boss stats (level, status vulnerabilities, and elemental weaknesses) 
  to relevant sections to help users have a better grasp of what options are available 
  in each fight.
- Hover over Status and Element column names to see an icon legend.
- Full boss breakdown available in the a dedicated `Boss Compendium` tab.

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

- Fixed a minor issue with export filenames when no jobs/classes are selected.

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
