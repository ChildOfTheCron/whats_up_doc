## What's Up Doc?
What's Up Doc is a command line tool that aggregates multiple different AWS RSS feeds into a single summary table. The table can be sorted between the different columns.

![HiMum](./images/whatsupDoc.jpg?raw=true)

## Purpose
The generated table attempts to summarise the most up-to-date RSS releases for the specific service and lists them by date.

Please note that The app is supposed to show the latest updates to be consumed in a quick glance, rather than be an in-depth analysis of each RSS feed. Because of this only one update per service will be listed. This update will be the latest amongst all the updates parsed for the service (amongst all the RSS feeds given). What this means is that if an AWS feature for the service was released, after, say, a security bulletin, then the new AWS feature will be listed, but the security bulletin will not. If this behaviour is not desired, then you should list specific RSS feed URLs to constrain the list to updates you are interested in. 

I made this tool to assist me in staying up to date with the latest changes to the various AWS services. As there are so many, it is difficult to keep up with them all. This tool *should* cover all different AWS services, I compiled a list using their service catalogue but I did find a service that was unlisted. I'm happy to accept any PRs or issues logged for missing services.

## Usage
    usage: whats_up_doc.py [-h] [-f FUZZ] [-n] [-u URL]

    options:

      -h, --help            show this help message and exit
      -f FUZZ, --fuzz FUZZ  Fuzziness level. Select 1, 2 or 3. Default is 1.
      -n, --nocache         Generate new json from template ignoring previous runs. All previous data will be lost!
      -u URL, --url URL     Specify specific rss feed url to parse. Must belong to an AWS RSS feed.
  

Examples:

    python3 whats_up_doc.py -n -f 1
    python3 whats_up_doc.py -f 2
    python3 whats_up_doc.py -n -f 1 -u 'https://aws.amazon.com/security/security-bulletins/feed/'
Once a run is complete the generated html file can be found in ./output/

## Fuzziness Level
You can set 3 different fuzziness levels (-f 1/2/3)

**Level 1** - This level will check to see if the service is mentioned in any of the RSS feed titles. If it is, it'll be updated in the table.

**Level 2** - Similar to one, it'll check for both service name and also any tags. If either of these are found in the title of the RSS feed then it'll match.

**Level 3** - Similar to levels 1 and 2 but includes both the RSS feeds title and summary section of the article.

Note: The higher the level the less accurate results may be. Keep this in mind when setting.

## Installation
Not much is needed to run the app. Just install the requirements.txt file:
    pip install -r requirements.txt

