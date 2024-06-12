
# qrcode-ijazah

## Installation
### Install modified ZBar
1. go to /pkg/zbar-master
2. run `apt-get install gettext libtool autopoint libgtk-4-dev libmagickwand-dev`
3. run `autoreconf -vfi`
4. run `./configure --prefix=/usr --with-gtk=auto --with-python=auto --disable-video`
5. run `make install`

### Install other packages
`pip install -r requirements.txt`

## Key Management
(for now)

Run `python3 src/keyGeneration.py`

copy the output value to `src/keyManagement.py`


## Run API
1. go to /src
2. run `uvicorn API:app --reload`

for test: `python3 testAPI.py`
