import subprocess
import os

# Variables de entorno para usar la CLI de Fabric
FABRIC_ENV = {
    "CORE_PEER_LOCALMSPID": "Org1MSP",
    "CORE_PEER_ADDRESS": "localhost:7051",
    "CORE_PEER_MSPCONFIGPATH": "/root/fabric-samples/test-network/organizations/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp",
    "CORE_PEER_TLS_ROOTCERT_FILE": "/root/fabric-samples/test-network/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt",
    "FABRIC_CFG_PATH": "/root/fabric-samples/config/"
}

ORDERER_CA = "/root/fabric-samples/test-network/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem"


def invoke_chaincode(function, args):
    # Convertimos los argumentos a cadena JSON con comillas
    json_args = ','.join(f'"{arg}"' for arg in args)

    cmd = [
        "peer", "chaincode", "invoke",
        "-o", "localhost:7050",
        "--ordererTLSHostnameOverride", "orderer.example.com",
        "--tls", "--cafile", ORDERER_CA,
        "-C", "mychannel",
        "-n", "basic",
        "--peerAddresses", FABRIC_ENV["CORE_PEER_ADDRESS"],
        "--tlsRootCertFiles", FABRIC_ENV["CORE_PEER_TLS_ROOTCERT_FILE"],
        "-c", f'{{"Args":["{function}", {json_args}]}}'
    ]

    try:
        result = subprocess.run(
            cmd,
            env={**os.environ, **FABRIC_ENV},
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return e.stderr
