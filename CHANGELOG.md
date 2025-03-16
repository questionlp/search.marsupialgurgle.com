# Application Change Log

## Version 1.0.0

- Promoting version 1.0.0-rc3 to 1.0.0, no application or component changes

## Version 1.0.0-rc3

### Application Changes

- Added "About" page with information about the application
- Updated footer to re-add `exclude_footer_links` flag that was removed due to a previous local undo mess-up
- Updated [README.md](./README.md) to include additional mentions of dependencies

## Version 1.0.0-rc2

### Application Changes

- Fixed incorrect configuration key name when reading in the `git_repository` config key value on application initialization

## Version 1.0.0-rc1

### Application Changes

- Added `git_repository` configuration key to application settings to store the URL for the Git repository for this project
- Changed the footer to only display the link to the Git repository if the value is set

## Version 1.0.0-rc

### Application Changes

- Added "Help Page" with information about the two search modes
- Added exception handling for search-related database queries
- Added `max_query_length` configuration key to application settings with a default value of 120
- Fixed alert type for "No search query was provided." from warning to info
- Updated search text fields to use the value from `max_query_length`
- Updated the layout of the footer and added navigation links
  - Added `exclude_footer_links` flag to be used on the main landing page
- Updated how the navigation skip link is handled
- Updated test cases to reflect changes in navigation, footer and new pages

### Component Changes

- Added [flask-sanitize-escape](https://github.com/mayur19/flask-sanitize-escape) to handle some input validation

## Version 1.0.0-beta

- Initial pre-release version
