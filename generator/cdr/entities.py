class Customer:
    def __init__(self, customer_type: str, msisdn: str, imsi: str, imei: str):
        """
        Initializes a Customer entity with customer_type, MSISDN, IMSI, and IMEI.

        Args:
            customer_type (str): Type of customer (e.g., "regular", "premium").
            msisdn (str): The MSISDN as a string.
            imsi (str): The IMSI as a string.
            imei (str): The IMEI as a string.
        """
        self.customer_type = customer_type
        self.msisdn = msisdn  
        self.imsi = imsi  
        self.imei = imei 

    def __str__(self):
        return f"Customer(customer_type={self.customer_type}, msisdn={self.msisdn}, imsi={self.imsi}, imei={self.imei})"

    def __eq__(self, other):
        if not isinstance(other, Customer):
            return False
        return self.msisdn == other.msisdn and self.imsi == other.imsi and self.imei == other.imei

    def __hash__(self):
        return hash((self.customer_type, self.msisdn, self.imsi, self.imei))


    def to_dict(self):
        return {
            "customer_type": self.customer_type,
            "msisdn": str(self.msisdn),  
            "imsi": str(self.imsi),      
            "imei": str(self.imei)      
        }


class Node:
    def __init__(self, network_type: str, rnc_id: str, lac: str, cell_id: str, tac: str, gNB_ID: str,
                 NR_Cell_ID: str, MSC_Address: str = None, SGSN_Address: str = None, GGSN_Address: str = None,
                 plmn: str = "", SGW_Address: str = None, PGW_Address: str = None, MME_Address: str = None):
        """
        Initializes a Node entity with relevant parameters based on network type.
        """
        self.network_type = network_type
        self.rnc_id = rnc_id
        self.lac = lac
        self.cell_id = cell_id
        self.tac = tac
        self.gNB_ID = gNB_ID
        self.NR_Cell_ID = NR_Cell_ID
        self.MSC_Address = MSC_Address
        self.SGSN_Address = SGSN_Address
        self.GGSN_Address = GGSN_Address
        self.plmn = plmn
        self.SGW_Address = SGW_Address
        self.PGW_Address = PGW_Address
        self.MME_Address = MME_Address

    def __str__(self):
        return f"Node(network_type={self.network_type}, rnc_id={self.rnc_id}, lac={self.lac}, cell_id={self.cell_id}, " \
               f"tac={self.tac}, gNB_ID={self.gNB_ID}, NR_Cell_ID={self.NR_Cell_ID}, MSC_Address={self.MSC_Address}, " \
               f"SGSN_Address={self.SGSN_Address}, GGSN_Address={self.GGSN_Address}, plmn={self.plmn}, " \
               f"SGW_Address={self.SGW_Address}, PGW_Address={self.PGW_Address}, MME_Address={self.MME_Address})"

    def to_dict(self):
        """
        Converts the Node object to a dictionary representation.

        Returns:
            dict: A dictionary representing the Node object.
        """
        return {
            "network_type": self.network_type,
            "rnc_id": self.rnc_id,
            "lac": self.lac,
            "cell_id": self.cell_id,
            "tac": self.tac,
            "gNB_ID": self.gNB_ID,
            "NR_Cell_ID": self.NR_Cell_ID,
            "MSC_Address": str(self.MSC_Address) if self.MSC_Address else None,
            "SGSN_Address": str(self.SGSN_Address) if self.SGSN_Address else None,
            "GGSN_Address": str(self.GGSN_Address) if self.GGSN_Address else None,
            "plmn": self.plmn,
            "SGW_Address": str(self.SGW_Address) if self.SGW_Address else None,
            "PGW_Address": str(self.PGW_Address) if self.PGW_Address else None,
            "MME_Address": str(self.MME_Address) if self.MME_Address else None,
        }

