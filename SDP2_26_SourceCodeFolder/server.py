import socket
import threading
import numpy as np
import joblib
from scapy.all import *

# Load the trained model from the file
loaded_model = joblib.load('/home/sarrag/Desktop/SDP/svm_model.joblib')

# Revised function to extract features from the packet
def extract_features(packet):
    # Check if the packet has an IP layer and a TCP layer
    if not (packet.haslayer(IP) and packet.haslayer(TCP)):
        return None  # Skip packets that do not have both IP and TCP layers
    # Extract relevant fields from the packet
    frame_time = packet.time
    src_host = packet[IP].src
    dst_host = packet[IP].dst
    # The following TCP attributes need to be safely accessed as well
    tcp_layer = packet[TCP]
    tcp_ack = tcp_layer.ack
    tcp_ack_raw = tcp_layer.ack_raw
    tcp_connection_rst = tcp_layer.flags.R
    tcp_connection_syn = tcp_layer.flags.S
    tcp_flags_ack = tcp_layer.flags.A
    tcp_dstport = tcp_layer.dport
    tcp_seq = tcp_layer.seq
    tcp_srcport = tcp_layer.sport
   
    # Create a feature vector
    feature_vector = [frame_time, src_host, dst_host, tcp_ack, tcp_ack_raw, tcp_connection_rst,
                      tcp_connection_syn, tcp_flags_ack, tcp_dstport, tcp_seq, tcp_srcport]
   
    return feature_vector

# Function to process incoming packets
def process_packet(packet):
    features = extract_features(packet)
    # If the packet doesn't have the right layers, skip it
    if features is None:
        return
    # Convert the features to a NumPy array
    data_array = np.array(features).reshape(1, -1)
    # Perform prediction using the loaded SVM model
    prediction = loaded_model.predict(data_array)
    return prediction

# Function to handle client connections
def handle_client(conn, addr):
    print(f'Connected by: {addr}')
    try:
        while True:
            # Receive data from the client
            data = conn.recv(1024)
            if not data:
                break
            # Process the received packet data
            packet = Ether(data)
           
            # Extract features from the packet
            features = extract_features(packet)
            # If the packet doesn't have the right layers, skip it
            if features is None:
                continue
           
            # Convert the features to a NumPy array
            data_array = np.array(features).reshape(1, -1)
            # Perform prediction using the loaded SVM model
            prediction = loaded_model.predict(data_array)
            # Send the prediction back to the client
            conn.sendall(prediction.tobytes())
    finally:
        # Close the connection
        conn.close()

# Function to continuously capture and process packets
def capture_and_process():
    # Capture packets from the network interface
    sniff(prn=process_packet)

# Create a socket object
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
tcp_socket.bind(("127.0.0.1", 9090))

# Start listening for incoming connections
tcp_socket.listen(5)

print("Server started. Listening for connections...")

# Start capturing and processing packets in a separate thread
capture_thread = threading.Thread(target=capture_and_process)
capture_thread.start()

try:
    while True:
        # Accept incoming connections
        conn, addr = tcp_socket.accept()
        # Handle the connection in a separate thread
        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.start()
except KeyboardInterrupt:
    print("\nServer stopped.")

# Close the server socket
tcp_socket.close()