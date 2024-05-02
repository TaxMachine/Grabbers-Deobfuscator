import re, lzma, codecs, base64

WEBHOOK_REGEX = r"(https://((ptb\.|canary\.|development\.)?)discord(app)?\.com/api/webhooks/[0-9]{19}/[a-zA-Z0-9\-_]{68})"
WEBHOOK_REGEX_BASE64 = r"(aHR0cHM6Ly9[\d\w]+==)"
TELEGRAM_REGEX = r"([0-9]{10}:[a-zA-Z0-9]{35})"
TELEGRAM_REGEX_BASE64 = r"zT([a-zA-Z0-9]+==)z"

def MatchWebhook(string):
    webhookb64 = re.findall(WEBHOOK_REGEX_BASE64, string)
    webhook = re.findall(WEBHOOK_REGEX, string)
    telegramtokenb64 = re.search(TELEGRAM_REGEX_BASE64, string)
    telegramtoken = re.search(TELEGRAM_REGEX, string)
    if webhookb64:
        decoded = []
        for w in webhookb64:
            w = base64.b64decode(w).decode()
            if w not in decoded and re.fullmatch(WEBHOOK_REGEX, w) is not None:
                decoded.append(w)
        return decoded if len(decoded) > 1 else decoded[0]
    elif webhook:
        webhooks = []
        for w in webhook:
            if w[0] not in webhooks:
                webhooks.append(w[0])
        return webhooks if len(webhooks) > 1 else webhooks[0]
    elif telegramtokenb64:
        encoded = telegramtokenb64.group(1) + "="
        decoded = base64.b64decode(encoded).decode()
        return decoded
    elif telegramtoken:
        return telegramtoken.group(1)
    else:
        return None


class BlankStage3Obj:
    def __init__(self, first, second, third, fourth):
        self.first = first
        self.second = second
        self.third = third
        self.fourth = fourth


def BlankStage3(assembly: bytes):
    bytestr = b"\xfd7zXZ\x00\x00" + assembly.split(b"\xfd7zXZ\x00\x00")[1]
    decompressed = lzma.decompress(bytestr)
    sanitized = decompressed.decode().replace(";", "\n")
    sanitized = re.sub(r"^__import__.*", "", sanitized, flags=re.M)
    return BlankStage3Obj(
        re.search(r'^____="(.*)"$', sanitized, re.MULTILINE).group(1),
        re.search(r'^_____="(.*)"$', sanitized, re.MULTILINE).group(1),
        re.search(r'^______="(.*)"$', sanitized, re.MULTILINE).group(1),
        re.search(r'^_______="(.*)"$', sanitized, re.MULTILINE).group(1)
    )

def BlankStage4(stage3Obj: BlankStage3Obj):
    pythonbytes = b""
    try:
        unrot = codecs.decode(stage3Obj.first, "rot13")
        pythonbytes = base64.b64decode(unrot + stage3Obj.second + stage3Obj.third[::-1] + stage3Obj.fourth)
        # this is just for testing, you can uncomment it if you want to see the deobfuscated binary object
        f = open("dump.bin", "wb")
        f.write(pythonbytes)
        f.close()
    except Exception as e:
        print(e)
        raise Exception(e)
    strings = codecs.decode(pythonbytes, 'ascii', errors='ignore')
    return MatchWebhook(strings)
