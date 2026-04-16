# ML-Based Intrusion Detection System for IoT Networks

**Senior Design Project — University of Sharjah, Spring 2023/2024**  
Department of Computer Engineering

## Contributors

- Sarra Ghali
- Meera Hassan Ali Mohamad Safar
- Sara Majid Humaid Majid Alshamsi

**Supervisor:** Dr. Ala' Altaweel

## Overview

This project develops a Machine Learning-based Intrusion Detection System (IDS) for IoT networks, trained to detect DDoS TCP SYN flood attacks. The system was built and validated on a physical testbed consisting of a Raspberry Pi 4 Model B, multiple IoT sensors, and a server, generating real network traffic for testing.

The ML models were trained on the [Edge-IIoTset dataset](https://doi.org/10.1109/ACCESS.2022.3165809), a comprehensive IoT/IIoT network traffic dataset containing both normal and attack traffic from 11 attack categories.

## Results

| Model | Training Accuracy | Testing Accuracy | Training Time |
|---|---|---|---|
| Random Forest | 100% | 100% | — |
| SVM (RBF kernel) | 99.9% | 99.9% | 282s |

Both models achieved near-perfect classification on the preprocessed dataset. Random Forest showed complete robustness to feature removal, while SVM accuracy dropped to 99% when the `tcp.connection.rst` feature was excluded, highlighting its importance for attack classification.

## Repository Structure

```
├── Data_preprocessing.py       # Feature selection, cleaning, sampling from Edge-IIoTset
├── RF_Train_Test.py            # Random Forest training and evaluation
├── SVM_Train_Test.py           # SVM (RBF) training and evaluation
├── server.py                   # Server-side deployment with real-time SVM classification
├── operating_the_sensors.py    # RPi GPIO sensor management (IR, Ultrasonic, Water, Temp)
├── Collect_and_send.py         # Sensor data collection and TCP transmission to server
├── legitimate_client.py        # Simulated legitimate client traffic
├── client.sh                   # Shell script to run 100,000 client connections
├── FinalExp.ipynb              # Extended experiments: ANN, LightGBM, SHAP, ROC curves
└── SDP2_26_FinalReport.pdf     # Full project report
```

## System Architecture

The testbed consists of:
- **Raspberry Pi 4 Model B** — manages sensors and transmits data wirelessly to the server
- **Sensors** — IR, Ultrasonic, Water Level, Temperature & Humidity
- **Alfa AWUS036ACM sniffer** — captures network traffic in promiscuous mode
- **Server** — runs the deployed ML model and classifies incoming packets in real time

Attack simulation was performed using `hping3` to generate TCP SYN flood packets targeting the server, while `tcpdump` captured traffic for analysis in Wireshark.

## Dataset

The [Edge-IIoTset dataset](https://doi.org/10.1109/ACCESS.2022.3165809) was used for training and testing. Preprocessing steps included:

- Selecting relevant TCP and IP header features
- Sampling 5% of rows per file
- Converting timestamps to epoch format and IP addresses to integer format
- Dropping zero-value rows in key TCP columns
- Removing nulls and duplicates

Features used: `frame.time`, `ip.src_host`, `ip.dst_host`, `tcp.ack`, `tcp.ack_raw`, `tcp.connection.rst`, `tcp.connection.syn`, `tcp.flags.ack`, `tcp.dstport`, `tcp.seq`, `tcp.srcport`

## Known Limitations

During real-time deployment, the server produced a high rate of false positives. This is attributed to a feature alignment mismatch between the training data (preprocessed CSV features) and live packet captures (raw Scapy fields). Resolving this alignment is identified as the primary next step for improving deployment reliability.

## Extended Experiments (FinalExp.ipynb)

The notebook includes additional experiments beyond the submitted project:
- **ANN** — 90% training accuracy, 93% testing accuracy
- **LightGBM** — trained and evaluated with feature importance analysis
- **SHAP** — explainability analysis on Random Forest
- **ROC and Precision-Recall curves** for all models

## License

This project was developed as an academic senior design project at the University of Sharjah. Code is provided for educational purposes.
