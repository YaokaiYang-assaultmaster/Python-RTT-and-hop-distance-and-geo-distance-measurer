import time 
import socket 
import os 
import struct
import select


def distMeasurement(desthost):

    print ("Measure the hop distance and RTT of " + desthost)
    destaddr = socket.gethostbyname(desthost) #get the ip address for a given hsot
    #print (destaddr)
    port = 33435 #port used in the destination port field in udp packet
    udp = socket.getprotobyname("udp")
    icmp = socket.getprotobyname("icmp")
    ttl = 32 #the initial TTL in the ip header will be this
    
    #use UDP segment to test a host, the UDP segment is send to a port that is unlikely to be used in destination host
    #create a sending socket using udp protocol
    sendsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, udp)
    sendsocket.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl) #set the ttl field in IP header
    #create a receiving socket as a raw socket, using icmp protocol, in order to receive all the IP datagram
    recvsocket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
    sendtime = send(destaddr, sendsocket, port) 
    TTL, arrivedtime = getreply(recvsocket, destaddr, port)
    if TTL:
        delay = arrivedtime - sendtime
        delay = 1000*delay #delay is going to be showed in the unit of ms.
        TTL = 32 - TTL #subtracting 32 with the remaining TTL in the header field to get the hop distance
        print ("Destination host: %s, Hop distance: %s, RTT: %1.1fms" %(desthost, TTL, delay))
    sendsocket.close()
    recvsocket.close()
    

def send(destaddr, sendsocket, port):
    #send the artificial to a port that is unlikely to be used on the remote host
    try:
        a = sendsocket.sendto(struct.pack("d", time.time()), (destaddr,port))
        #print (a)
    except socket.error, e:
        print ("failed. (socket error: '%s')" % e[1])
        return
    sendtime = time.time()
    #recording the send time and return it for calculating RTT
    #print (sendtime)
    return sendtime

def getreply(recvsocket, destaddr, port):
    #use the raw socket to receive the icmp packet in order to parse it.
    #timeout = 10s
    start = time.time()
    timeout = 10.0
    who = None
    packet = None
    myname = socket.getfqdn(socket.gethostname())
    myaddr = socket.gethostbyname(myname) #get the ip address for my own computer 
    #print ("start to listen")
    while 1:
        rd, wt, er = select.select([recvsocket], [], [], timeout)
        if rd:
            try:
                packet, who = recvsocket.recvfrom(4096)
            except Exception:
                pass
            #print (who)
            #(daddr, dport) = who
            #print (daddr)
            #print (packet)
            arrivedtime = time.time()
            #record the arriving time of ICMP packet and return it for calculating RTT

            #parsing thr receiving IP datagram
            icmpheader = packet[20:24]
            #print (icmpheader)
            icmpdata = packet[28:]
            type, code, checksum = struct.unpack("bbH", icmpheader)
            print ("received ICMP packet of " + "type: %d code: %d" %(type, code))
            origipheader = icmpdata[ :20]
            (TTL, )= struct.unpack("b", origipheader[8])
            #print (TTL)
            saddr = origipheader[12:16]
            (saddr, ) = struct.unpack("4s", saddr)
            saddr = socket.inet_ntoa(saddr)
            #print (saddr)
            daddr = origipheader[16:20]
            (daddr, ) = struct.unpack("4s", daddr)
            daddr = socket.inet_ntoa(daddr)
            #print (daddr)
            udpheader = icmpdata[20:28]
            # sport = struct.unpack("H", udpheader[ :2])
            # print (sport)
            # dport = struct.unpack("H", udpheader[2:4])
            # print (dport)
            #the source port and destination port seems to be changed from the original value, cannot use them to match the packet.

            #if the packet belongs to our distMeasutrement tool
            if daddr == destaddr:
                #if saddr == myaddr:
                #cannot use source address to match the packet if the computer is used within a NAT network
                #since the source address will be changed when passing the NAT-enabled router
                if type == 3:
                    if code == 3:
                        return TTL, arrivedtime
        timeout = (start + timeout) - time.time()
        if timeout < 0:
            print ("failed! timeout within 10.0 seconds")
            return None, None
            


def main():
    #reading txt file
    f = open("targets.txt", "r")
    targets = f.readlines()
    #print targets
    for target in targets:
        target = target.split("\n")[0]
        print target
        distMeasurement(target)


if __name__ == "__main__":
    main()


            







