# ContackGen

Contextual Network Traffic Generator

## Scapy privilege

Scapy needs root privileges to create raw sockets because it uses the Python socket library. 

Only processes with an effective user ID of 0 or the CAP_NET_RAW capability are allowed to open raw sockets.

```bash
sudo setcap cap_net_raw=eip $(readlink -f $(which python))
```

after u ran the program you may want to get back to default:
```bash
sudo setcap -r $(readlink -f $(which python))
```
NB : On kali this line may not needed

## Usage

```bash
chmod +x main.py && sudo ./main.py -h
```

## Test

```bash
python -m pytest test/test_pcap.py
```