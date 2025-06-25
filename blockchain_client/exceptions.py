class BlockchainAPIError(Exception):
    def __init__(self, message, response=None):
        super().__init__(message)
        self.status_code = response.status_code if response else None
        self.response_text = response.text if response else None



