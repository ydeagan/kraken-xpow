import requests
import hashlib
import os
import time


def byte_array_to_hex(byte_array):
    return ''.join(format(x, '02x') for x in byte_array)


def hex_to_byte_array(hex_string):
    return bytes.fromhex(hex_string)


def double_sha256(byte_array):
    return hashlib.sha256(hashlib.sha256(byte_array).digest()).digest()


def solve_challenge(challenge_data):
    difficulty = challenge_data['difficulty']
    randomness = challenge_data['randomness']
    data = hex_to_byte_array(challenge_data['data'])

    random_buffer = bytearray(randomness)
    combined_data = bytearray(len(data) + len(random_buffer))
    combined_data[:len(data)] = data

    start_time = time.time()

    while True:
        random_bytes = os.urandom(randomness)
        combined_data[len(data):] = random_bytes

        hash_result = double_sha256(combined_data)
        if int.from_bytes(hash_result[:4], 'big') >> (32 - difficulty) == 0:
            return {
                "solution": byte_array_to_hex(random_bytes),
                "attempts": 0,
                "time": time.time() - start_time
            }


def get_slid_cookie():
    url = 'https://iapi.kraken.com/api/internal/slid'
    headers = {
        'Accept': 'application/json',
        'Accept-Language': 'en-US,en;q=0.5',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://www.kraken.com/',
        'X-Korigin': '2081',
        'Origin': 'https://www.kraken.com',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'Priority': 'u=4',
        'Te': 'trailers'
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    cookies = response.cookies.get_dict()
    return cookies


def get_challenge(context):
    url = 'https://iapi.kraken.com/api/internal/session'
    headers = {
        'Accept': 'application/json',
        'Accept-Language': 'en-US,en;q=0.5',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://www.kraken.com/',
        'X-Korigin': '2081',
        'Origin': 'https://www.kraken.com',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'Priority': 'u=4',
        'Te': 'trailers'
    }

    cookies = context['cookies']

    cookies.update({
        'SLID': context['slid'],
        'dev': cookies.get('dev'),
        'asid': cookies.get('asid'),
        '__cf_bm': cookies.get('__cf_bm'),
        '_cfuvid': cookies.get('_cfuvid'),
    })

    response = requests.get(url, headers=headers, cookies=cookies)
    response.raise_for_status()
    cookies = response.cookies.get_dict()
    context['sessid'] = cookies.get('SESSID')

    response_data = response.json()
    context['challenge_data'] = response_data.get(
        'result', {}).get('challenge2', {})


def main():
    context = {}
    context['cookies'] = get_slid_cookie()
    context['slid'] = context['cookies'].get('SLID')

    if not context['slid']:
        print("SLID cookie not found in response")
        return

    get_challenge(context)

    if not context.get('challenge_data'):
        print("Challenge data not found in response")
        return

    solution = solve_challenge(context['challenge_data'])
    context['x_pow_solution'] = solution['solution']

    print(f"X-Pow Solution: {context['x_pow_solution']}")


if __name__ == "__main__":
    main()
