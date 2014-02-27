# APNS-HTTP-Proxy

$B%G%P%$%9%H!<%/%s$r<u$1$F!"(BAPNs$B$KN.$9%5!<%P!<(B

## Requirements

- Python > 2.6

## Setup

```
# APNs$B$X$N@\B3$KMxMQ$9$k(BSSL$B>ZL@=q$NG[CV(B
cp xxxxx.certs ./certifications/
cp xxxxx.key ./certifications/

# $B@_Dj%U%!%$%k$N:n@.(B
cp settings.template.py settings.py
vim settings.py

# Python$B4D6-$N9=C[(B
make setup
```

## $B5/F0(B

```
apns-proxy-server.sh start
```

## $B3+H/MQ$N%3%^%s%I(B

Command | Description
--- | ---
make setup | Setup python environment
make lint | Check coding style using flake8. Need flake8 on your $PATH
make test | Run Tests
make live_test | Run test using server and client
make run | Run server

