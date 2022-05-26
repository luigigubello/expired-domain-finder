import os
import sys
import json
import re
import requests
import click
import whois

packages = []
json_response = []
well_known_domains = ['gmail.com', 'outlook.com', 'hotmail.com']


def list_packages_python(path_file):
    if path_file.isalnum():
        return
    if not os.path.isfile(path_file):
        error = {"error": "file not exist or not accessible"}
        print("Error: {}".format(error['error']))
        sys.exit(1)
    with open(path_file) as f:
        try:
            for line in f:
                spl = re.split('>|<|=|\n', line)
                # Missing error handling, too tired today sorry
                if str(spl[0]).isalnum():
                    packages.append(str(spl[0]))
        except:
            error = {"error": "empty file"}
            print("Error: {}".format(error['error']))
            sys.exit(1)


def pypi_domain(package, verbose):
    pypi_url = 'https://pypi.org/project/' + package + '/'
    r = requests.get(pypi_url)
    if not r.ok:
        # print("Error\nStatus code: {}".format(r.status_code))
        return
    source_code = r.text
    result = re.findall(r'<a href="mailto:(.*?)">', source_code)
    result = list(set(result))
    if result:
        json_response.append({"package": package, "url": pypi_url, "domains": {}})
        for item in result:
            email_domain = str(item).split('@')[-1]
            if '&gt;' in email_domain:  # fix some wrong domains
                email_domain = email_domain.replace('&gt;', '')
            if email_domain in well_known_domains:
                json_response[-1]['domains'][email_domain] = 'Not expired'
                continue
            if url_ping(email_domain):
                json_response[-1]['domains'][email_domain] = 'Not expired'
                continue
            domain = whois_query(email_domain)
            if not domain:
                json_response[-1]['domains'][email_domain] = 'Could be expired'
                continue
            if expiration_date_check(domain):
                json_response[-1]['domains'][email_domain] = 'Not expired'
                continue
            if status_check(domain):
                json_response[-1]['domains'][email_domain] = 'Not expired'
            else:
                json_response[-1]['domains'][email_domain] = 'Probably expired'
        if verbose:
            print(json_response[-1])


def beautiful_print(json_response):
    for item in json_response:
        print("Package: {}".format(item['package']))
        print("PyPi URL: {}".format(item['url']))
        print("Domains")
        for key in item['domains'].keys():
            print("  {} --> {}".format(key, item['domains'][key]))


def url_ping(url):
    try:
        site_ping = requests.head('https://' + url, timeout=10)
        if site_ping.status_code < 400:
            return True  # Not expired
        else:
            return False
    except:
        try:
            site_ping = requests.head('http://' + url, timeout=10)
            if site_ping.status_code < 400:
                return True  # Not expired
            else:
                return False
        except:
            return False


def expiration_date_check(domain):
    try:
        if domain.expiration_date:
            return True  # Not expired
        else:
            return False
    except:
        return False


def status_check(domain):
    try:
        status_list = ['connect', 'active']
        status = domain.status
        for item in status_list:
            if item in str(status).lower():
                return True  # Not expired
        return False
    except:
        return False


def whois_query(url):
    try:
        domain = whois.query(url)
        if domain is None:
            return False
        else:
            return domain
    except:
        return False


@click.command()
@click.argument('path')
@click.option('--json', 'json_dict', is_flag=True, help='Optional. Print JSON result.')
@click.option('--verbose', 'verbose', is_flag=True, help='Optional. Good for long lists.')
def pypi_edf(path, json_dict, verbose):
    """
    🌸 PyPi expired domain finder\n
    https://github.com/luigigubello/expired-domain-finder
    """
    list_packages_python(path)
    if packages:
        if verbose:
            for item in packages:
                pypi_domain(item, True)
        else:
            for item in packages:
                pypi_domain(item, False)
    else:
        pypi_domain(path, False)
    if json_dict:
        print(json.dumps(json_response))
    else:
        beautiful_print(json_response)


if __name__ == "__main__":
    pypi_edf()
