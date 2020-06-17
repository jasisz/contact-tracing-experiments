import sys

from exposure_keys.keys_pb2 import TEKSignatureList, TemporaryExposureKeyExport


def decode_key_from_file(file_name: str) -> TemporaryExposureKeyExport:
    with open(file_name, mode="rb") as f:
        content = f.read()
    content = content.strip(b"EK Export v1    ")
    export = TemporaryExposureKeyExport()
    export.ParseFromString(content)
    return export


def decode_signature_from_file(file_name: str) -> TEKSignatureList:
    with open(file_name, mode="rb") as f:
        content = f.read()
    signature = TEKSignatureList()
    signature.ParseFromString(content)
    return signature


if __name__ == "__main__":
    """
    Usage:
        python ./decode_keys.py /1591142400-00001/
    """
    print(decode_key_from_file(sys.argv[1] + "export.bin"))
    print(decode_signature_from_file(sys.argv[1] + "export.sig"))
