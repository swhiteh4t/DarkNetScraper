from .colors import ColoredText

def print_generic(data=None, key=None):
    keys = {
        'email' : 'Emails',
        'crypto' : 'Crypto',
        'ip4' : 'IPv4',
        'ip6' : 'IPv6',
        'cloud': 'Cloud domains',
        'phone': 'Phone Numbers'
    }
    if key in keys:
        print(ColoredText("[ * ] " + keys[key], 'green'))
        if len(data) > 0:
            for v in data:
                print(ColoredText("[ - ] " + v, 'white'))
        else: 
            print(ColoredText("[ - ] No " + keys[key] + " found ", 'white'))
        print("\n")

def handle_response_code(code):
    if code >= 300 and code < 400:
        print(ColoredText("[ - ] Moved to a new location", 'white'))
    elif code == 404:
        print(ColoredText("[ - ] Requested site not found", 'red'))
    elif code == 401:
        print(ColoredText("[ - ] Unauthorized", 'red'))
    elif code == 400:
        print(ColoredText("[ - ] Bad request", 'red'))
    else:
        print(ColoredText("[ - ] Request failed", 'red'))
    print(ColoredText("[ - ] Status code: " + str(code), 'white'))