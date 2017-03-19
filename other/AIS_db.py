#!/usr/bin/python3.5

import argparse
import sqlite3 
import datetime
import time
import sys
import os

class ModesMessage(object):
  def __init__(self, SessionID):
    self.SessionID = SessionID
    self.AircraftID = -1
    self.RecTime = -1
    self.MsgUsTime = -0.99
    self.RSSI = -1.0
    self.Score = -1
    self.DF = -1
    self.Icao = 'FFFFFF'
    self.Alt = -1	
    self.Lat = -1
    self.Long = -1
    self.RawData = ''

class ModesParser(object):
  def __init__(self, BaseName, Position):
    self.BaseConn = sqlite3.connect(BaseName)
    print("connection open OK")	
    self.MsgCount = 0
    self.SessionID = 1
    self.Position = Position 
    self.Msg = None
    
  
  def __del__(self):
    if self.BaseConn is not None:
      print("closing connection...")
      self.BaseConn.commit()
      self.BaseConn.close()
  
  def dump_message(self): 	  
    self.Msg.RecTime = datetime.datetime.now()
    #dump message to localdb.sqb
    print(self.Msg.Icao, "RSSI:", self.Msg.RSSI, "Score:", self.Msg.Score, "Time:", self.Msg.MsgUsTime,"DF:", self.Msg.DF)
    if self.Msg.Icao == 'FFFFFF':
      return
    valcols = ":MsgID, :SessionID, :ModeS, :RecTime, :MsgUsTime, :RSSI, :Score, :DF, :RawData"
    values = {'MsgID':None,
              'SessionID':self.Msg.SessionID,
              'ModeS':self.Msg.Icao, 
              'RecTime':self.Msg.RecTime,
              'MsgUsTime':self.Msg.MsgUsTime,
              'RSSI':self.Msg.RSSI,
              'Score':self.Msg.Score,
              'DF':self.Msg.DF,
              'RawData':self.Msg.RawData}
    self.BaseConn.execute("INSERT INTO Packets VALUES( " + valcols + ");", values)
    self.MsgCount += 1
    if self.MsgCount == 256:
      self.BaseConn.commit()
      self.MsgCount = 0
    if self.Msg.Lat != -1:
      print("\tAlt:", self.Msg.Alt, "Lat:", self.Msg.Lat, "Long:", self.Msg.Long)
  
  def parse_line(self, line):
    if line == '\n' or line == '\r\n' and self.Msg is not None:
      #EndOfMessage
      self.dump_message()
      return 
    tline = line.strip(' ')
    if tline[0]=='@':
      self.Msg = ModesMessage(self.SessionID)
      self.Msg.RawData = line
    if tline[0:4] == 'RSSI' and self.Msg is not None:
      splline = tline.split(' ',3)
      self.Msg.RSSI = float(splline[1])
    if line[0:5] == 'Score' and self.Msg is not None:
      splline = tline.split(' ',2)
      self.Msg.Score = int(splline[1])
    if line[0:4] == 'Time' and self.Msg is not None:
      splline = tline.split(' ',3)
      self.Msg.MsgUsTime = float(splline[1].strip('us'))
    if line[0:2] == 'DF' and self.Msg is not None:
      splline = tline.split(' ')
      self.Msg.DF = int(splline[1].strip(':'))
    if tline[0:4] == 'ICAO' and self.Msg is not None:
      splline = tline.split(':',2)
      self.Msg.Icao = splline[1].strip(' \n\r')
    if tline[0:8] == 'Altitude' and self.Msg is not None and tline.find("not valid") == -1:
      splline = tline.split(':',3)
      self.Msg.Alt = float(splline[1].strip(' fetmrs\n\r'))
    if tline[0:8] == 'Latitude' and self.Msg is not None and tline.find("not decoded") == -1:
      splline = tline.split(' ',3)
      self.Msg.Lat = float(splline[2])
    if tline[0:9] == 'Longitude' and self.Msg is not None and tline.find("not decoded") == -1:
      splline = tline.split(' ',3)
      self.Msg.Long = float(splline[1])

def check_base(fname):
  if os.path.isfile(fname):
   return True 
  else:
    return False
    
 
def main():
  parser = argparse.ArgumentParser(description="dump1090 db filter")
  parser.add_argument('-o','--outbase', help="Output database name", default="localdb.sqb")
  parser.add_argument('-p','--position', nargs = 2, help="Receiver position (LAT, LON)", default=[-1,-1])
  args = parser.parse_args() 
  if not check_base(args.outbase):
    print("File ",args.outbase, "don't exist on filesystem, exit...")
    exit(1)
  else:
    print("OK, use ",args.outbase)
    MsgParser = ModesParser(args.outbase, args.position)
  while True:
    line = sys.stdin.readline()
    if not line:
      break
    MsgParser.parse_line(line)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting on SIGINT")
    except BaseException as e:
        print("Exiting on exception: "+str(e))
    else:
        print("Exiting on connection loss")