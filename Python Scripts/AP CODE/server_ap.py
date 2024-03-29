# -*- coding: utf-8 -*-

#   RUNS ON AP
import socket
import sys
import json
import sqlite3

DATABASE_ENABLED = False    

    
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_name = sys.argv[1]
server_address = (server_name, 31415)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(server_address)

# Connecetion to DB
if DATABASE_ENABLED:
    sqlconnection = sqlite3.connect("rover.sqlite3")
    cursor = sqlconnection.cursor()



# message must be a json string
def saveDataToSQL(message, curs):
    data = json.loads(message)
    print("save: " + message)
    
    format_str = """INSERT INTO roverapp_datareceived (sendTime, heading, roll, pitch, tempC, leftState, rightState, propellorState, distance) VALUES ("{sendTime}", "{heading}", "{roll}", "{pitch}", "{tempC}", "{leftState}", "{rightState}", "{propellorState}", "{distance}");"""
    sql_command = format_str.format(sendTime=data["time"], heading=data["heading"], roll=data["roll"], pitch=data["pitch"], tempC=data["tempC"], leftState=data["left"], rightState=data["right"], propellorState=data["propellor"], distance=data["distance"])
    
    curs.execute(sql_command)
    sqlconnection.commit()  # do not delete this line


# Listen for incoming connections
sock.listen(5)   
try:
    while True:
        # Wait for a connection
        print >>sys.stderr, 'waiting for a connection'
        connection, client_address = sock.accept()
        newData = ''

        while True:
            
            data = connection.recv(50)
            
            if data:
                newData += data
                if data.endswith('☢'):
                    newData = newData.strip('☢')
                    print("received data:" + newData)
                    if DATABASE_ENABLED:
                        saveDataToSQL(newData, cursor)
                    newData = ''
            else:
                break

finally:
    connection.close()
    if DATABASE_ENABLED:
        sqlconnection.commit()
        cursor.close()
        sqlconnection.close()
