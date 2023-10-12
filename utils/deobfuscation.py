import dis
import marshal
import re, lzma, codecs, base64, os


def MatchWebhook(string):
    webhookb64 = re.search(r"(aHR0cHM6Ly9kaXNjb3JkLmNvbS9hcGkvd2ViaG9va3Mv.*==)", string)
    webhook = re.search(r"(https://(.*?)discord.com/api/webhooks/[0-9]{19}/[a-zA-Z0-9\-_]{68})", string)
    telegramtokenb64 = re.search(r"zT([a-zA-Z0-9]+==)z", string)
    telegramtoken = re.search(r"([0-9]{10}:[a-zA-Z0-9]{35})", string)
    if webhookb64:
        return base64.b64decode(webhookb64.group(1)).decode()
    elif webhook:
        return webhook.group(1)
    elif telegramtokenb64:
        encoded = telegramtokenb64.group(1) + "="
        decoded = base64.b64decode(encoded).decode()
        return decoded
    elif telegramtoken:
        return telegramtoken.group(1)
    else:
        return None


class Stage3:
    def __init__(self, first, second, third, fourth):
        self.first = first
        self.second = second
        self.third = third
        self.fourth = fourth


class BlankOBF:
    @staticmethod
    def DeobfuscateStage3(assembly: bytes):
        bytestr = b"\xfd7zXZ\x00\x00" + assembly.split(b"\xfd7zXZ\x00\x00")[1]
        decompressed = lzma.decompress(bytestr)
        sanitized = decompressed.decode().replace(";", "\n")
        sanitized = re.sub(r"^__import__.*", "", sanitized, flags=re.M)
        return Stage3(
            re.search(r'^____="(.*)"$', sanitized, re.MULTILINE).group(1),
            re.search(r'^_____="(.*)"$', sanitized, re.MULTILINE).group(1),
            re.search(r'^______="(.*)"$', sanitized, re.MULTILINE).group(1),
            re.search(r'^_______="(.*)"$', sanitized, re.MULTILINE).group(1)
        )

    @staticmethod
    def DeobfuscateStage4(firstpart: str, secondpart: str, thirdpart: str, fourthpart: str):
        pythonbytes = b""
        try:
            unrot = codecs.decode(firstpart, "rot13")
            pythonbytes = base64.b64decode(unrot + secondpart + thirdpart[::-1] + fourthpart)
        except Exception as e:
            print(e)
            raise Exception(e)
        strings = codecs.decode(pythonbytes, 'ascii', errors='ignore')
        return MatchWebhook(strings)
