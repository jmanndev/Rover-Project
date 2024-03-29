# -*- coding: utf-8 -*-

#   RUNS ON ROVER
import socket
import sys
import Rover

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_name = sys.argv[1]
server_address = (server_name, 31417)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(server_address)

engine = Rover.Engine()

# Listen for incoming connections
sock.listen(5) 
while True:  
    try:
        # Wait for a connection
        print >>sys.stderr, 'waiting for a connection'
        connection, client_address = sock.accept()
        while True:
            data = connection.recv(50)
            print("received data:" + data)
            if data:
                if data == 'FORWARD':
                    engine.forward()
                elif data == 'BACKWARD':
                    engine.backward()
                elif data == 'LEFT':
                    engine.left()
                elif data == 'RIGHT':
                    engine.right()
                elif data == 'IDLE':
                    engine.idle()
                elif data == 'OFF':
                    engine.off()
                elif data == 'UP':
                    engine.up()
                elif data == 'DOWN':
                    engine.down()
                else:
                    print('Unknown Command')
                data = ''
            else:
                break
    except KeyBoardInterrupt:
        s.close()

    finally:
        connection.close()
