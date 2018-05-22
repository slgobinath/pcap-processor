# Pcap Processor
Read and process pcap files using this nifty tool.

This tool can read pcap files, process them internally and write them to one or more sinks.
Currently there are mappers written for pcap length conversion and protocol normalization.
I also have written sinks to write the pcap file to console, csv file or http endpoint.

```text
usage: pcap-processor [-h] [--map {length,protocol}]
                      [--sink {console,kafka,http,csv,grpc}] [--version]
                      file [file ...]

Read and process pcap files using this nifty tool.

positional arguments:
  file                  pcap file to read

optional arguments:
  -h, --help            show this help message and exit
  --map {length,protocol}
                        enable a mapper with the given name. You can use this
                        option multiple times to enable more than one mappers
  --sink {console,kafka,http,csv,grpc}
                        enable a sink with the given name. You can use this
                        option multiple times to enable more than one sinks
  --version             show program's version number and exit
```

## Requirements

pcap-reader relies on external command line tool: `tshark` and some Python modules.

Install `tshark` using the following command in Ubuntu and its derivatives:

```bash
sudo apt install tshark
```

Install Python dependencies using the following command:

```bash
pip3 install -r requirements.txt
```

## Research Work
This tool is developed as part of my research project. If you are using this tool in your research,
please cite the following paper:

**Citation:**

```text
Loganathan, G., Samarabandu, J., & Wang, X. (2018). Sequence to Sequence Pattern Learning Algorithm for Real-time Anomaly Detection in Network Traffic. In 2018 IEEE Canadian Conference on Electrical & Computer Engineering (CCECE) (CCECE 2018). Quebec City, Canada.
```

**BibTex**

```bibtex
@INPROCEEDINGS{Loga1805:Sequence,
AUTHOR="Gobinath Loganathan and Jagath Samarabandu and Xianbin Wang",
TITLE="Sequence to Sequence Pattern Learning Algorithm for Real-time Anomaly
Detection in Network Traffic",
BOOKTITLE="2018 IEEE Canadian Conference on Electrical \& Computer Engineering (CCECE)
(CCECE 2018)",
ADDRESS="Quebec City, Canada",
DAYS=13,
MONTH=may,
YEAR=2018,
KEYWORDS="Seq2Seq; Anomaly Detection",
ABSTRACT="Network intrusions can be modeled as anomalies in network traffic in which
the expected order of packets and their attributes deviate from regular
traffic. Algorithms that predict the next sequence of events based on
previous sequences are a promising avenue for detecting such anomalies. In
this paper, we present a novel multi-attribute model for predicting a
network packet sequence based on previous packets using a
sequence-to-sequence (Seq2Seq) encoder-decoder model. This model is trained
on an attack-free dataset to learn the normal sequence of packets in TCP
connections and then it is used to detect anomalous packets in TCP traffic.
We show that in DARPA 1999 dataset, the proposed multi-attribute Seq2Seq
model detects anomalous raw TCP packets which are part of intrusions with
97\% accuracy. Also, it can detect selected intrusions in real-time with
100\% accuracy and outperforms existing algorithms based on recurrent
neural network models such as LSTM."
}
```

## Use Cases

Read a pcap file and send all packets to Apache Kafka:

```bash
python3 -m pcap_processor --sink kafka input.pcap 
```

Read a pcap file, map protocols and write them to a CSV file:

```bash
python3 -m pcap_processor --map protocol --sink csv input.pcap 
```

Mappers and sinks have their own properties. Please modify them in the relevant `plugins/<file>.py`.

For example, to change the output CSV file location, modify the `self.path = "packets.csv"` in `pcap_processor/plugins/csv_sink.py`.