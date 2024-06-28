import feedparser
import json
import os
import argparse
from datetime import datetime
from time import mktime
from prettytable.colortable import ColorTable, Themes

# Security Bulletin RSS feed = https://aws.amazon.com/security/security-bulletins/feed/
# What’s New RSS feed = https://aws.amazon.com/about-aws/whats-new/recent/feed/
# AWS Blog feed = https://aws.amazon.com/blogs/aws/feed/

#dict_keys(['links', 'link', 'id', 'guidislink', 'title', 'title_detail', 'summary', 'summary_detail', 'published', 'published_parsed', 'tags', 'authors', 'author', 'author_detail'])
#time.struct_time(tm_year=2023, tm_mon=3, tm_mday=22, tm_hour=17, tm_min=6, tm_sec=44, tm_wday=2, tm_yday=81, tm_isdst=0)

def normalize_date(date):
    "dd/mm/yy"
    dt = datetime.fromtimestamp(mktime(date))
    dt = dt.strftime('%d-%m-%Y')

    return dt

def normalize_time(time):
    tm = datetime.fromtimestamp(mktime(time))
    tm = tm.strftime('%H:%M:%S')

    return tm

def is_newer(date_one, date_two):
    dt_obj1 = datetime.strptime(date_one, "%d-%m-%Y")
    dt_obj2 = datetime.strptime(date_two, "%d-%m-%Y")
    if dt_obj2 > dt_obj1:
        #print(date_two + " is newer than " + date_one)
        return True
    else:
        return False

def build_html(data):
    html_top = """
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8" />
    <title>What's Up Doc?</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
  </head>

  <body>
    <h2 class="header-style"><span style="color: #FF9900">W</span>hat's <span style="color: #FF9900">U</span>p <span style="color: #FF9900">D</span>oc?</h2>
    <p style="text-align: center; font-family: arial;">AWS RSS feed aggregator, click to sort and have a great day!</p>

    <style>
        .header-style {
            font-size: 5em;
            font-family: arial;
            text-align: center;
            height: 0.5em;
        }
        .styled-table {
            border-collapse: collapse;
            margin: 25px 0;
            font-size: 0.9em;
            font-family: sans-serif;
            min-width: 400px;
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
            margin-left: auto;
            margin-right: auto;
        }
        .styled-table thead tr {
            background-color: #009879;
            color: #ffffff;
            text-align: left;
        }
        .styled-table th {
            cursor: pointer;
            height: 70px;
        }
        .styled-table td {
            padding: 12px 15px;
        }
        .styled-table tbody tr {
            border-bottom: 1px solid #dddddd;
        }
        .styled-table tbody tr:nth-of-type(even) {
            background-color: #f3f3f3;
        }
        .styled-table tbody tr:last-of-type {
            border-bottom: 2px solid #FF9900;
        }
        .styled-table tbody tr.active-row {
            font-weight: bold;
            color: #009879;
        }
        th:hover {background-color: #FF9900;}
    </style>

    <script>
    """
    html_json = "var myJSON = ['" + json.dumps(data) + "']"
    html_bot = """
    document.write('<input type="text" id="myInput" onkeyup="searchFunc()" placeholder="Search Summary for text..." title="Type in a string">');
    document.write('<table class="styled-table", id="myTable2">');
    document.write('<tbody>');
    document.write("<tr>");
    document.write('<th onclick="sortTable(0)"> Service <i class="fa fa-sort" style="font-size:12px"></i></th>');
    document.write('<th onclick="sortTable(1)"> Tag <i class="fa fa-sort" style="font-size:12px"></i></th>');
    document.write('<th onclick="sortTable(2)"> Date <i class="fa fa-sort" style="font-size:12px"></i></th>');
    document.write('<th onclick="sortTable(3)"> Time <i class="fa fa-sort" style="font-size:12px"></i></th>');
    document.write('<th onclick="sortTable(4)"> Summary <i class="fa fa-sort" style="font-size:12px"></i></th>');
    document.write('<th onclick="sortTable(5)"> Source <i class="fa fa-sort" style="font-size:12px"></i></th>');
    document.write("</tr>");

    const myObj = JSON.parse(myJSON[0]);
    var test = "blah"
    for (key in myObj) {
        test = myObj[key];

        for (x in test) {
            document.write("<tr>");
            document.write('<td>' + JSON.stringify(test[x]['Name']).replace(/^"(.*)"$/,'$1') + '</td>');
            document.write('<td>' + JSON.stringify(test[x]['Tag']).replace(/"/g,'') + '</td>');
            document.write('<td>' + JSON.stringify(test[x]['Date']).replace(/^"(.*)"$/,'$1') + '</td>');
            document.write('<td>' + JSON.stringify(test[x]['Time']).replace(/^"(.*)"$/,'$1') + '</td>');
            document.write('<td>' + JSON.stringify(test[x]['Summary']).replace(/^"(.*)"$/,'$1') + '</td>');
            document.write('<td>' + JSON.stringify(test[x]['Link']).replace(/^"(.*)"$/,'$1') + '</td>');
            document.write("</tr>");
        }
    }
    document.write('</tbody>');
    document.write("</table>");

    function searchFunc() {
      var input, filter, table, tr, td, i, txtValue;
      input = document.getElementById("myInput");
      filter = input.value.toUpperCase();
      table = document.getElementById("myTable2");
      tr = table.getElementsByTagName("tr");
      for (i = 0; i < tr.length; i++) {
          td = tr[i].getElementsByTagName("td")[4];
          if (td) {
              txtValue = td.textContent || td.innerText;
              if (txtValue.toUpperCase().indexOf(filter) > -1) {
                  tr[i].style.display = "";
              } else {
                  tr[i].style.display = "none";
              }
          }
      }
    }

    function sortTable(n) {
      var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
      table = document.getElementById("myTable2");
      switching = true;
      // Set the sorting direction to ascending:
      dir = "asc";
      /* Make a loop that will continue until
      no switching has been done: */
      while (switching) {
        // Start by saying: no switching is done:
        switching = false;
        rows = table.rows;
        /* Loop through all table rows (except the
        first, which contains table headers): */
        for (i = 1; i < (rows.length - 1); i++) {
          // Start by saying there should be no switching:
          shouldSwitch = false;
          /* Get the two elements you want to compare,
          one from current row and one from the next: */
          x = rows[i].getElementsByTagName("TD")[n];
          y = rows[i + 1].getElementsByTagName("TD")[n];
          /* Check if the two rows should switch place,
          based on the direction, asc or desc: */
          if (dir == "asc") {
            if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
              // If so, mark as a switch and break the loop:
              shouldSwitch = true;
              break;
            }
          } else if (dir == "desc") {
            if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
              // If so, mark as a switch and break the loop:
              shouldSwitch = true;
              break;
            }
          }
        }
        if (shouldSwitch) {
          /* If a switch has been marked, make the switch
          and mark that a switch has been done: */
          rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
          switching = true;
          // Each time a switch is done, increase this count by 1:
          switchcount ++;
        } else {
          /* If no switching has been done AND the direction is "asc",
          set the direction to "desc" and run the while loop again. */
          if (switchcount == 0 && dir == "asc") {
            dir = "desc";
            switching = true;
          }
        }
      }
    }
    </script>
  </body>
</html>
    """
    return(html_top + html_json + html_bot)

def print_table(data):
    table = [['Service', 'Date', 'Summary']]
    table_source = data
    #tab = PrettyTable(table[0])
    tab = ColorTable(table[0], theme=Themes.OCEAN)
    tab.add_rows(table[1:])
    for element in table_source:
        for item in table_source[element]:
            if len(item["Name"]) > 17:
               item["Name"] = item["Name"].replace("Amazon","")
               item["Name"] = item["Name"].replace("AWS","")
               item["Name"] = item["Name"].replace(" ","") if len(item["Name"]) > 17 else item["Name"]
            #print(item["Name"], item["Tag"], item["Date"], item["Time"], item["Summary"], item["Link"])
            if "NO DATA" not in item["Summary"]:
                meh = [[item["Name"], item["Date"], item["Summary"]]]
                tab.add_rows(meh)
    print(tab)

# Todo - a lot of code duplication need to clean up
# Todo - add try catches
def update(url, fuzz):
    #Todo use get to get data not direct key access
    feed = feedparser.parse(url)
    for entry in feed.entries:
        for x in services_list:
            for y in services_list[x]:
                name = y.get("Name")
                if name in entry.title:
                    if is_newer(y.get("Date"), normalize_date(entry.published_parsed)):
                        y["Date"] = normalize_date(entry.published_parsed)
                        y["Time"] = normalize_time(entry.published_parsed)
                        y["Summary"] = entry.title
                        y["Link"] = entry.link
                elif (int(fuzz) == 2) or (int(fuzz) == 3):
                    if type(y["Tag"]) == list:
                        for tag in y["Tag"]:
                            if tag in entry.title:
                                if is_newer(y.get("Date"), normalize_date(entry.published_parsed)):
                                    y["Date"] = normalize_date(entry.published_parsed)
                                    y["Time"] = normalize_time(entry.published_parsed)
                                    y["Summary"] = entry.title
                                    y["Link"] = entry.link
                    else:
                        if y["Tag"] in entry.title:
                            if is_newer(y.get("Date"), normalize_date(entry.published_parsed)):
                                y["Date"] = normalize_date(entry.published_parsed)
                                y["Time"] = normalize_time(entry.published_parsed)
                                y["Summary"] = entry.title
                                y["Link"] = entry.link
                else:
                    continue

                if int(fuzz) == 3:
                    if name in entry.summary:
                        if is_newer(y.get("Date"), normalize_date(entry.published_parsed)):
                            y["Date"] = normalize_date(entry.published_parsed)
                            y["Time"] = normalize_time(entry.published_parsed)
                            y["Summary"] = entry.title
                            y["Link"] = entry.link
                        else:
                            if type(y["Tag"]) == list:
                                for tag in y["Tag"]:
                                    if tag in entry.summary:
                                        if is_newer(y.get("Date"), normalize_date(entry.published_parsed)):
                                            y["Date"] = normalize_date(entry.published_parsed)
                                            y["Time"] = normalize_time(entry.published_parsed)
                                            y["Summary"] = entry.title
                                            y["Link"] = entry.link
                            else:
                                if y["Tag"] in entry.summary:
                                    if is_newer(y.get("Date"), normalize_date(entry.published_parsed)):
                                        y["Date"] = normalize_date(entry.published_parsed)
                                        y["Time"] = normalize_time(entry.published_parsed)
                                        y["Summary"] = entry.title
                                        y["Link"] = entry.link

def write_output(services_list):

    if not os.path.exists('output'):
        os.makedirs('output')

    f = open("output/index.html", "w")
    f.write(build_html(services_list))
    f.close()

    with open('services.json', "w") as json_file:
        json.dump(services_list, json_file)

def main(fuzz):

    if specific_url:
        update(specific_url, fuzz)
    else:
        rss_urls = ["https://aws.amazon.com/blogs/aws/feed/","https://aws.amazon.com/security/security-bulletins/feed/","https://aws.amazon.com/about-aws/whats-new/recent/feed/"]
        for url in rss_urls:
            update(url, fuzz)

if __name__ == "__main__":

    argParser = argparse.ArgumentParser()
    argParser.add_argument("-f", "--fuzz", help="Fuzziness level. Select 1, 2 or 3. Default is 1.")
    argParser.add_argument("-n", "--nocache", action='store_true', help="Generate new json from template ignoring previous runs. All previous data will be lost!")
    argParser.add_argument("-u", "--url", help="Specify specific rss feed url to parse. Must belong to an AWS RSS feed.")
    argParser.add_argument("-t", "--table", action='store_true', help="Print summary table to terminal.")
    args = argParser.parse_args()
    fuzziness = str(1) if args.fuzz is None else args.fuzz
    no_cache_run = args.nocache
    specific_url = args.url
    services_list = []

    if (no_cache_run) or not (os.path.isfile("services.json")):
        with open('template.json', "r") as json_file:
            services_list = json.load(json_file)
    else:
        with open('services.json', "r") as json_file:
            services_list = json.load(json_file)

    main(fuzziness)
    write_output(services_list)

    if args.table:
        print_table(services_list)
