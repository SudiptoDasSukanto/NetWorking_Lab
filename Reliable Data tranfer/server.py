# Task 2: Implementing Reliable Data Transfer
import socket
import random
import time
import os

# Initialize variables for EWMA calculation
alpha = 0.125  # EWMA smoothing factor
EstimatedRTT = 0.4  # Initial estimated round-trip time (seconds)
DevRTT = 0  # Initial deviation of round-trip time (seconds)
TimeoutInterval = EstimatedRTT + 4 * DevRTT  # Initial timeout interval (seconds)

# Function to update timeout interval using EWMA
def update_timeout(SampleRTT):
    global EstimatedRTT, DevRTT, TimeoutInterval
    EstimatedRTT = (1 - alpha) * EstimatedRTT + alpha * SampleRTT
    DevRTT = (1 - alpha) * DevRTT + alpha * abs(SampleRTT - EstimatedRTT)
    TimeoutInterval = EstimatedRTT + 4 * DevRTT

# Function to decode packet headers
def decoding(packet):
    seq = packet[:6]
    ack = packet[6:12]
    win = packet[12:16]
    check = packet[16:20]
    return (int(seq.decode('utf-8')), int(ack.decode('utf-8')), int(win.decode('utf-8')), int(check.decode('utf-8')))

# Function to segment data into packets
def segmenting(seq, ack, window, checksum, payload):
    seq = int(seq)
    ack = int(ack)
    window = int(window)
    checksum = int(checksum)
    transport_header = f'{seq:06d}{ack:06d}{window:04d}{checksum:04d}'.encode('utf-8')[:20].ljust(20)
    
    # Build network layer header
    network_header = b'\x45\x00\x05\xdc'  # IP version 4, header length 20 bytes, total length 1500 bytes
    network_header += b'\x00\x00\x00\x00'  # Identification
    network_header += b'\x40\x06\x00\x00'  # TTL=64, protocol=TCP, checksum=0 (will be filled in by kernel)
    network_header += b'\x0a\x00\x00\x02'  # Source IP address
    network_header += b'\x0a\x00\x00\x01'  # Destination IP address
    
    # Build packet by concatenating headers and payload
    packet = network_header + transport_header + payload
    return packet

# Set up server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('', 9000))
server_socket.listen(2)

print('Server is listening for incoming connections')

# Accept a client connection
client_socket, address = server_socket.accept()
client_socket.settimeout(5)

print(f'Accepted connection from {address}')

# Set receive window size (in bytes)
receive_window_size = 1460
rwnd = 5

# Open file to be sent
file = open('sending_file.txt', 'rb')
sequence_number = random.randint(0,0)
ack_number = 0
starting_time = time.time()
file_size = os.path.getsize('sending_file.txt')

while True:
    curr_sent = 0
    stime = time.time()
    while time.time() - stime < TimeoutInterval and rwnd > curr_sent:
        payload = file.read(1460)
        payload_size = len(payload)
        print("Payload Size = {payload_size}")
        ack_number += payload_size
        if not payload:
            break
        checksum = 50
        packet = segmenting(sequence_number, ack_number, rwnd, checksum, payload)
        sequence_number += len(payload)
        client_socket.send(packet)
        curr_sent += 1
        print(f'Sent packet {sequence_number} currsent {curr_sent}')
        print()

    try:
        acknowledgment = client_socket.recv(1024)
    except socket.timeout:
        print('No acknowledgment received within timeout interval')
        break
    if acknowledgment:
        network_header = acknowledgment[:20]
        transport_header = acknowledgment[20:40]
        seq, acknowledgment_sequence_number, rwnd, checksum = decoding(transport_header)

        if acknowledgment_sequence_number == sequence_number + payload_size:
            print(f'Received acknowledgment for packet {sequence_number}')
            sequence_number += payload_size
            SampleRTT = time.time() - stime  # Calculate SampleRTT
            update_timeout(SampleRTT)  # Update TimeoutInterval using EWMA
        else:
            print(f'Received acknowledgment for packet {acknowledgment_sequence_number}, but expected {sequence_number}')
    else:
        print('Did not receive acknowledgment')

# Close file
file.close()

print(f'Throughput: {(file_size / (time.time() - starting_time)) / 1000.0} B/s')

# Close sockets
client_socket.close()
server_socket.close()
print('Done')
