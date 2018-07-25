# Apps Scraper

> A really tiny scraper to extract data about mobile apps

## Setup & Running

First you need to create and to activate the `virtualenv` and install the requirements:

```sh
$ virtualenv env
$ source env/bin/activate
$ pip install -r requirements.txt
```

Then you can provide a CSV file with the URLs to parse and crawl: `$ python scraper.py input.csv`. It will generate
the following files:

* `apps.json`, a JSON array with elements in the same order as the CSV and each array element containing keys:
    - `name` - string - The name of the app
    - `app_identifier` - number - The App Store’s identifier of the app (eg. 1261357853 for Fortnite)
    - `minimum_ios_version` - string - The minimum iOS version required to run the app
    - `languages` - array of strings, sorted alphabetically - All of the languages that the app supports
* `filtered_apps.json`, a JSON dictionary, with the following keys:
    - `apps_in_spanish_and_tagalog` - array of numbers, sorted ascending - App identifiers of all apps that
    are available in both Spanish and Tagalog
    - `apps_with_insta_in_name` - array of numbers, sorted ascending - App identifiers of all apps apps that
    have “insta” in the name (case insensitive)

## License

[MIT License](http://earaujoassis.mit-license.org/) &copy; Ewerton Assis
