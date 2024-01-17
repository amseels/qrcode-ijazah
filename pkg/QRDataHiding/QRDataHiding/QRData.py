from dataclasses import dataclass

@dataclass
class QRData:
    """

    A dataset of QR. ??? 

    Attributes:
        payload: ???
        payload_no_ecc: 
        payload_after_ecc: 
        version: 
        data_type: 
        eci:
        ecc_level:
        mask:
    
    #TO_DO_LIST: fill the description above
    """
    payload: bytes
    payload_no_ecc: bytes
    payload_after_ecc: bytes
    version: int
    mask: int
    
    def __init__(self, config):
        # self.payload = config.payload
        # self.payload_no_ecc = config.payload_no_ecc
        # self.payload_after_ecc = config.payload_after_ecc
        # self.version = config.version
        # self.data_type = config.data_type
        # self.eci = config.eci
        # self.ecc_level = config.ecc_level
        # self.mask = config.mask

        # ZBAR
        self.payload = config.data
        self.payload_no_ecc = None
        self.payload_after_ecc = config.payload_after_ecc
        self.version = config.version
        self.data_type = None
        self.eci = config.eci
        self.ecc_level = config.ecc_level
        self.mask = None
    
    def __str__(self):
        return f'QRData(  payload = {self.payload!r}' \
        f',\n\t payload_no_ecc = {self.payload_no_ecc!r}'\
        f',\n\t payload_after_ecc = {self.payload_after_ecc!r}' \
        f',\n\t version = {self.version}' \
        f',\n\t data_type = {self.data_type}' \
        f',\n\t eci = {self.eci}' \
        f',\n\t ecc_level = {self.ecc_level}' \
        f',\n\t mask = {self.mask}' \
        '\n\t )'