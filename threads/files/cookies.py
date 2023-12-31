import requests


user_agent_key = "User-Agent"
user_agent_value = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
headers = {user_agent_key: user_agent_value}


def get_yahoo_cookie():
    response = requests.get("https://fc.yahoo.com", headers=headers, allow_redirects=True)

    if not response.cookies:
        raise Exception("Failed to obtain Yahoo auth cookie.")

    cookie = list(response.cookies)[0]

    return cookie


def get_yahoo_crumb(cookie):
    crumb_response = requests.get(
        "https://query1.finance.yahoo.com/v1/test/getcrumb",
        headers=headers,
        cookies={cookie.name: cookie.value},
        allow_redirects=True,
    )
    crumb = crumb_response.text

    if crumb is None:
        raise Exception("Failed to retrieve Yahoo crumb.")

    return crumb


def get_handler(crumb, cookie):
    # url = f"https://query1.finance.yahoo.com/v8/finance/chart/quote?symbols=SPY&crumb={crumb}"
    url = f'https://query1.finance.yahoo.com/v10/finance/quoteSummary/NVDA?modules=price&crumb={crumb}'

    response = requests.get(
        url,
        headers=headers,
        cookies={cookie.name: cookie.value}
    )
    return response.json()


if __name__ == '__main__':
    cookies = get_yahoo_cookie()
    crumbs = get_yahoo_crumb(cookies)
    get_handler(crumbs, cookies)
