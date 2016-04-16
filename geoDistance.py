import urllib
#import urllib.request ->python 3.5 method
import socket
import math
#import xml.dom.minidom as dom

"""
Measure the geographical distance between my computer to destination hosts.
Using http://freegeoip.net
"""
def geoDistance(desthost):
    print ("Measure the geographical distance between this computer to " + desthost)
    #get the ip address of destination
    destaddr = socket.gethostbyname(desthost)
    #get the ip address of my computer
    myname = socket.getfqdn(socket.gethostname())
    myaddr = socket.gethostbyname(myname)
    #gather the latitude and longitude of hosts
    #we will use a default coordination
    #(mylatitude, mylongitude) = getcoord(2, myaddr)
    #cannot get the geographical coordination of my computer using its current address, maybe because the computer is used within a NAT network.
    mylatitude = 41.5074
    mylongitude = -81.6053
    (destlatitude, destlongitude) = getcoord(1, destaddr)
    destlatitude = float(destlatitude)
    destlongitude = float(destlongitude)
    distance = caldist(mylatitude, mylongitude, destlatitude, destlongitude)
    print ("Distance between this computer and %s is %1.1f km" %(desthost, distance))
    


def getcoord(a, addr):
    #get the latitude and longitude of a given ip address
    host = 0
    if a == 1:
        host = "Destination host"
    if a == 2:
        host = "My computer"
    #send the http get request to http://freegeoip.net
    url = "http://freegeoip.net/xml/" + addr
    #print ("request url is " + url)
    #reply = urllib.request.urlopen(url) ->python3.5 methods
    reply = urllib.urlopen(url)
    contents = reply.read()
    #decode the receiving data and parse it to find the latitude and longitude
    contents = contents.decode("utf-8")
    lines = contents.splitlines()
    country = 0
    region = 0
    city = 0
    latitude = 0
    longitude = 0
    for line in lines:
        a = line.find("<RegionCode>") + 1
        if a:
            region = line[(a+len("<RegionName>")-1) : (len(line) - len("</RegionName>"))]
            #print (region)
            
        a = line.find("<CountryName>") + 1
        if a:
            country = line[(a+len("<CountryName>")-1) : (len(line) - len("</CountryName>"))]
            #print (country)
            
        a = line.find("<City>") + 1
        if a:
            city = line[(a+len("<City>")-1) : (len(line) - len("</City>"))]
            #print (city)
            
        a = line.find("<Latitude>") + 1
        if a:
            latitude = line[(a+len("<Latitude>")-1) : (len(line) - len("</Latitude>"))]
            #print (latitude)

        a = line.find("<Longitude>") + 1
        if a:
            longitude = line[(a+len("<Longitude>")-1) :(len(line) - len("</Longitude>"))]
            #print (longitude)
    
    print (host +" locates in: %s, %s, %s" %(country, region, city))
    return latitude, longitude

def caldist(mylatitude, mylongitude, destlatitude, destlongitude):
    #calculating the geographical distance using the latiude and longitude of both my computer and destination
    #the earth is abstracted in to a sphere
    distance = 0
    earthR = 6371.0 #the radius of earth is abstracted t o 6371 kilometers in this program
    myla = math.radians(mylatitude)
    mylo = math.radians(mylongitude)
    destla = math.radians(destlatitude)
    destlo = math.radians(destlongitude)
    deltaphi = myla - destla
    deltalambda = mylo - destlo
    phim = (myla + destla)/2
    distance = earthR*math.sqrt(math.pow(deltaphi,2) + (math.cos(phim)*math.pow(deltalambda,2)))
    return distance


def main():
    #reading targets.txt file to get all the websites needed to be measured
    f = open("targets.txt", "r")
    targets = f.readlines()
    for target in targets:
        target = target.split("\n")[0]
        geoDistance(target)


if __name__ == "__main__":
    main()
    
    
    
