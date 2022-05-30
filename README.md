# Expired Domain Finder
Python command-line tool to find expired domains attached to open source projects (currently PyPi only, Author e-mail address metadata). Idea based on the repo [scovetta/expired-domain-finder](https://github.com/scovetta/expired-domain-finder).

The tool uses two methods of evaluating if a domain is expired:
- the package [psf/requests](https://github.com/psf/requests) to send a HEAD request to the domain and wait for the response
- the package [DannyCork/python-whois](https://github.com/DannyCork/python-whois) to look up domain registration records

False-positive results can happen.

## Bugs
If you find any bugs, please open an issue or submit a pull request.

## Security
If you find a security vulnerability, please report it to me privately at luigi[-dot-]gubello[-at-]protonmail.com.
