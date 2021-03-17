# pwmfan
Python script to control a PWM fan

## Usage
```
python pwmfan.py
```

## Systemd service
Edit the path in `pwmfan.service`.
Then run:
```
sudo cp pwmfan.service /etc/systemd/system/.
sudo systemctl start pwmfan.service
sudo systemctl enable pwmfan.service
```

Adopted from https://github.com/DriftKingTW/Raspberry-Pi-PWM-Fan-Control

