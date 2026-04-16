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

| Model | Training Accuracy | Test Accuracy | Test Recall (Attack) | Training Time |
|---|---|---|---|---|
| SVM (RBF kernel) | 99.99% | 99.97% | 1.00 | 370s |
| ANN | 88.8% | 93.1% | — | ~2160s |
| Random Forest | 100% | 84.2% | 0.00 | 11s |
| LightGBM | — | — | 0.00 | — |

**SVM** was the strongest performer, maintaining high accuracy and near-perfect precision/recall on the held-out test set.

**Random Forest and LightGBM** showed a critical failure on the test set despite high training accuracy — both models predicted all packets as normal traffic, achieving zero recall on the attack class. This is a classic symptom of class imbalance: after preprocessing, normal traffic heavily outnumbered attack samples, causing these models to learn a trivial "always predict normal" strategy that appeared accurate due to the skewed class distribution.

**ANN** achieved 93.1% test accuracy, performing better than tree-based models on this imbalanced dataset.

## Key Finding: Class Imbalance

The Edge-IIoTset dataset required significant preprocessing — many features contained missing or zero values, and after cleaning a large proportion of rows were dropped. This left a heavily imbalanced dataset where normal traffic samples substantially outnumbered attack samples. This imbalance directly caused the RF and LightGBM failures on the test set, and explains why SVM — more robust to imbalance due to its margin-based optimization — outperformed ensemble tree methods here.

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
├── ExtraExp.ipynb              # Extended experiments: SVM, RF, ANN, LightGBM, ROC curves
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

**Class imbalance:** Preprocessing significantly reduced the dataset size and left normal traffic heavily overrepresented, causing RF and LightGBM to fail on the attack class entirely. Addressing this with SMOTE or class weighting would be a clear next step.

**Deployment feature mismatch:** During real-time deployment, the server produced a high rate of false positives due to a feature alignment mismatch between the preprocessed CSV features used during training and the raw fields extracted from live packets via Scapy. Resolving this alignment is the primary blocker for a working real-time system.

## License

This project was developed as an academic senior design project at the University of Sharjah. Code is provided for educational purposes.
