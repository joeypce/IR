import urllib.request as urllib2

with open('football_and_teams_final.json', encoding='utf-8-sig') as f_input:
    for line in f_input:
        print(line)
        url = 'http://localhost:8983/solr/footballtweets/update/json?commit=true&wt=json'
        y = "[" + line + "]"
        y = y.encode("utf-8")
        req = urllib2.Request(url, y)
        req.add_header('Content-type', 'application/json')
        response = urllib2.urlopen(req)
        the_page = response.read()
        print(the_page.decode("utf-8"))
