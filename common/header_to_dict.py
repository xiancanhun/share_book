from urllib.parse import parse_qsl

__author__ = 'hexl'


def print_headers_raw_to_dict(headers_raw_l):
    print("{\n    '" + ",\n    ".join(map(lambda s: "'" +"': '".join(s.strip().split(':' )) + "'", headers_raw_l))[1:-1] + "'\n}")

def print_headers_raw_to_dict_space(headers_raw_l):
    print("{\n    '" + ",\n    ".join(map(lambda s: "'" + "': '".join(s.strip().split('\t') if len(s.strip().split('\t'))>1 else [s.strip(), '']) + "'", headers_raw_l))[1:-1] + "'\n}")

def print_dict_from_copy_headers(headers_raw):
    headers_raw = headers_raw.strip()
    headers_raw_l = headers_raw.splitlines()

    if 'HTTP/1.1' in headers_raw_l[0]:
        headers_raw_l.pop(0)
    if headers_raw_l[0].startswith('Host'):
        headers_raw_l.pop(0)
    if headers_raw_l[-1].startswith('Cookie'):
        headers_raw_l.pop(-1)

    if ':' in headers_raw_l[-1]:
        print_headers_raw_to_dict(headers_raw_l)
    else:
        print_headers_raw_to_dict_space(headers_raw_l)

def print_url_params(url_params):
    s = str(parse_qsl(url_params.strip(), 1))
    print("OrderedDict(\n    " + "),\n    ".join(map(lambda s: s.strip(), s.split("),")))[1:-1] + ",\n)")

def print_url_params_new(url_params):
    l = parse_qsl(url_params.strip(), 1)
    print("{\n    " + "',\n    ".join(map(lambda s: "'"+s[0]+"': '"+s[1], l)) + "',\n}")

if __name__ == '__main__':
    text = '''
        Accept-Encoding:gzip, deflate, sdch, br
        Accept-Language:zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4
        Cache-Control:no-cache
        Connection:Upgrade
        Cookie:_octo=GH1.1.1206836797.1546841867; logged_in=yes; dotcom_user=xiancanhun; _ga=GA1.2.1780826014.1546841863
        Host:live.github.com
        Origin:https://github.com
        Pragma:no-cache
        Sec-WebSocket-Extensions:permessage-deflate; client_max_window_bits
        Sec-WebSocket-Key:HQOsEbrtREaG+7JBeuOK2w==
        Sec-WebSocket-Version:13
        Upgrade:websocket
        User-Agent:Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36
   '''
    print_dict_from_copy_headers(text)

