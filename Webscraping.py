

import bs4
import requests
from bs4 import BeautifulSoup#

def requestTrains(departStation, destintationStation, departDate, departTime, returnDate=None, returnTime=None):
    site = "https://ojp.nationalrail.co.uk/service/timesandfares/" + departStation + "/" + destintationStation + "/" + departDate + "/" + departTime + "/dep"
    if not (returnDate == None and returnTime == None):
        site = site + "/" + returnDate + "/" + returnTime + "/dep"

    print("Site Requested: " + site)
    return requests.get(site)


def extractJourneys(request):
    requestBody = request.text
    parser = BeautifulSoup(requestBody, 'html.parser')
    outboundlist = parser.find(id="oft").find_all("tr", attrs={'class': "mtx"})
    returnlist = parser.find(id="ift").find_all("tr", attrs={'class': "mtx"})

    outboundoutput = [[0 for columns in range(15)] for rows in range(len(outboundlist))]

    for i, item in enumerate(outboundlist):
        itemparser = BeautifulSoup(str(item), 'html.parser')
        columns = itemparser.find_all("td")
        # Departure Time
        departtime = itemparser.find("div", class_="dep").text.strip();
        outboundoutput[i][0] = departtime.split(":")[0]
        outboundoutput[i][1] = departtime.split(":")[1]
        # Departure Station
        outboundoutput[i][2] = itemparser.find("span", class_="result-station").text
        # Departure Station Abbreviation
        outboundoutput[i][3] = itemparser.find("div", class_="from").find("abbr").text
        # Departure Platform
        outboundoutput[i][4] = itemparser.find("span", class_="ctf-plat").text.replace("Platform", "").replace("\n",
                                                                                                               "").replace(
            "\t", "")
        # Journey Duration
        duration = itemparser.find("div", class_="dur").text.replace("\t", "").replace("\n", "").replace("m", "")
        if ("h" in duration):
            outboundoutput[i][5] = duration.split("h")[0]
            outboundoutput[i][6] = duration.split("h")[1]
        else:
            outboundoutput[i][5] = "00"
            outboundoutput[i][6] = duration
        # Changes During Journey
        outboundoutput[i][7] = itemparser.find("div", class_="chg").text.replace(" change(s)", "").strip()
        # Arrival Time
        arrivetime = itemparser.find("div", class_="arr").text.strip()
        outboundoutput[i][8] = arrivetime.split(":")[0]
        outboundoutput[i][9] = arrivetime.split(":")[1]
        # Destination Station
        outboundoutput[i][10] = itemparser.find("div", class_="to").find("span", class_="result-station").text
        # Destination Station Abbreviation
        outboundoutput[i][11] = itemparser.find("div", class_="to").find("abbr").text
        # Destination Station Platform
        platform = itemparser.find("div", class_="to").find("span", class_="ctf-plat")
        if (hasattr(platform, "text")):
            outboundoutput[i][12] = platform.text.replace("Platform", "").replace("\n", "").replace("\t", "")
        else:
            outboundoutput[i][12] = None
        # Journey Fare
        if ("£" in columns[4].find_all("div")[1].text):
            outboundoutput[i][13] = columns[4].find_all("div")[1].text.split("£")[1].split("\n")[0]
        else:
            outboundoutput[i][13] = None
        # Link to Buy Ticket
        outboundoutput[i][14] = None

    returnoutput = [[0 for columns in range(15)] for rows in range(len(returnlist))]

    for i, item in enumerate(returnlist):

        itemparser = BeautifulSoup(str(item), 'html.parser')
        columns = itemparser.find_all("td")
        # Departure Time
        departtime = itemparser.find("div", class_="dep").text.strip();
        returnoutput[i][0] = departtime.split(":")[0]
        returnoutput[i][1] = departtime.split(":")[1]
        # Departure Station
        returnoutput[i][2] = itemparser.find("span", class_="result-station").text
        # Departure Station Abbreviation
        returnoutput[i][3] = itemparser.find("div", class_="from").find("abbr").text
        # Departure Platform
        returnoutput[i][4] = itemparser.find("span", class_="ctf-plat").text.replace("Platform", "").replace("\n",
                                                                                                             "").replace(
            "\t", "")
        # Journey Duration
        duration = itemparser.find("div", class_="dur").text.replace("\t", "").replace("\n", "").replace("m", "")
        if ("h" in duration):
            returnoutput[i][5] = duration.split("h")[0]
            returnoutput[i][6] = duration.split("h")[1]
        else:
            returnoutput[i][5] = "00"
            returnoutput[i][6] = duration
        # Changes During Journey
        returnoutput[i][7] = itemparser.find("div", class_="chg").text.replace(" change(s)", "").strip()
        # Arrival Time
        arrivetime = itemparser.find("div", class_="arr").text.strip()
        returnoutput[i][8] = arrivetime.split(":")[0]
        returnoutput[i][9] = arrivetime.split(":")[1]
        # Destination Station
        returnoutput[i][10] = itemparser.find("div", class_="to").find("span", class_="result-station").text
        # Destination Station Abbreviation
        returnoutput[i][11] = itemparser.find("div", class_="to").find("abbr").text
        # Destination Station Platform
        platform = itemparser.find("div", class_="to").find("span", class_="ctf-plat")
        if (hasattr(platform, "text")):
            returnoutput[i][12] = platform.text.replace("Platform", "").replace("\n", "").replace("\t", "")
        else:
            returnoutput[i][12] = None
        # Journey Fare
        if ("£" in columns[4].find_all("div")[1].text):
            returnoutput[i][13] = columns[4].find_all("div")[1].text.split("£")[1].split("\n")[0]
        else:
            returnoutput[i][13] = None
        # Link to Buy Ticket
        returnoutput[i][14] = None

    return [outboundoutput, returnoutput]

def getJourneys(departStation, destintationStation, departDate, departTime, returnDate = None, returnTime = None):
    return extractJourneys(requestTrains(departStation, destintationStation, departDate, departTime, returnDate, returnTime))

def delays(station, outbound = True):
    # https://ojp.nationalrail.co.uk/service/ldbboard/dep/Norwich
    # https://ojp.nationalrail.co.uk/service/ldbboard/arr/Norwich
    site = "https://ojp.nationalrail.co.uk/service/ldbboard/"
    if(outbound):
        site += "dep/" + station
    else:
        site += "arr/" + station

    delaypage = BeautifulSoup(requests.get(site).text, 'html.parser')
    journeys = delaypage.find("div", class_="tbl-cont").find("tbody").find_all("tr")

    output = [[None for columns in range(3)] for rows in range(len(journeys))]

    for i, journey in enumerate(journeys):
        columns = journey.find_all("td")
        output[i][0] = columns[0].text.strip()
        output[i][1] = columns[1].text.strip()
        output[i][2] = columns[2].text.strip()

    print(output)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    request = requestTrains("Bristol", "Great Yarmouth", "250121", "1530", "270121", "1745")
    # requestTrains("KTH", "London", "250121", "1530", "270121", "1745")
    # requestTrains("LST", "NRW", "250121", "1500")
    # print(request.text)
    requestBody = request.text
    # print(requestBody)

    journeys = extractJourneys(request)

    for i in range(5):
        print(journeys[0][i])

    for i in range(5):
        print(journeys[1][i])

    print("departhour")
    print(journeys[0][0][0])
    print("departmin")
    print(journeys[0][0][1])
    print("departstation")
    print(journeys[0][0][2])
    print("departstationabbriviation")
    print(journeys[0][0][3])
    print("departplatform")
    print(journeys[0][0][4])
    print("journeytimehours")
    print(journeys[0][0][5])
    print("journeytimemins")
    print(journeys[0][0][6])
    print("numberofchanges")
    print(journeys[0][0][7])
    print("arrivaltimehours")
    print(journeys[0][0][8])
    print("arrivaltimeminutes")
    print(journeys[0][0][9])
    print("destinationstation")
    print(journeys[0][0][10])
    print("destinationstationabbriviation")
    print(journeys[0][0][11])
    print("destinationplatform")
    print(journeys[0][0][12])
    print("ticketprice")
    print(journeys[0][0][13])
    print("linktobuy")
    print(journeys[0][0][14])

    print("--------------------------------------------")
    delayInfo = delays("Norwich")
    print("--------------------------------------------")
    delayInfo2 = delays("Norwich", False)