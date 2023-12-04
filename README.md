
# qrcode-ijazah

## Installation

install packages in `/pkg` directory 

 #### Pyquirc

 1. go to `pyquirc-main` folder
 2. run `python3 -m pip install .`

 #### IBS
 1. go to `IBS` folder
 2. run `python3 -m pip install .`
 
 #### QRDataHiding

 1. go to `QRDataHiding` folder
 2. run `python3 -m pip install .`


## Key Management
(for now)

Run `python3 src/keyGeneration.py`

copy the output value to `src/keyManagement.py`


## Run API
1. go to /src
2. run `uvicorn API:app --reload`

for test: `python3 testAPI.py`
