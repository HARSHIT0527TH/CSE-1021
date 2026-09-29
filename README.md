# Scam-URL-Checker
IT helps U to Identify the scam URL 
# Scam URL Checker

A simple Python tool that checks if a URL is suspicious or malicious. Learned this in my first semester while studying functions, loops, and conditionals.

## What does it do

Takes a URL, extracts the domain, checks it against a list of known scam sites, and looks for suspicious patterns like missing HTTPS, weird hyphens, or sketchy keywords. Then gives you a risk score out of 100.

Basically tells you whether a link is sketchy or not.

## Installation

You need Python 3.6+ installed. That's it, no fancy dependencies.

```bash
git clone https://github.com/yourusername/scam-url-checker.git
cd scam-url-checker
python main.py
```

## How to use it

Run the program and enter a URL:

```
Sir plz enter the string: https://amazon-account-verify.info

 Wait Sir just Analyzing URL...

Extracted domain: amazon-account-verify.info
Domain found in scam database!
Sir Now Checking blacklist...
Suspicious word found: verify
Sir Now Checking patterns...

======================================================================
         SCAM URL CHECKER - DETAILED RISK REPORT
======================================================================

Domain: amazon-account-verify.info
Total Risk Score: 58/100

----------------------------------------------------------------------
DETECTED FLAGS:
----------------------------------------------------------------------
  [!] Domain found in scam database
  [!] No HTTPS encryption
  [!] Suspicious keyword: verify

----------------------------------------------------------------------
RISK LEVEL ASSESSMENT:
----------------------------------------------------------------------
WARNING: HIGH RISK - AVOID
----------------------------------------------------------------------
```

## How it works

The program has 4 main parts:

1. **URL Parser** - Takes the messy URL and extracts just the domain part
   - Strips out http:// or https://
   - Removes www. if its there
   - Gets rid of everything after the domain like /login or ?stuff

2. **Blacklist Check** - Compares the domain against 180+ known scam domains
   - If found, adds 50 points to the score

3. **Pattern Detector** - Looks for red flags
   - No HTTPS = 15 points (risky, not secure)
   - Suspicious words like "login", "verify", "confirm" = 8 points
   - Too many hyphens = 10 points (typosquatting trick)
   - Short domain name = 5 points
   - IP address instead of domain = 20 points

4. **Risk Calculator** - Adds up all the points, caps it at 100, and tells you the verdict

## Risk Levels

0-39: Low risk, probably safe
40-64: Medium risk, be careful
65-79: High risk, pretty suspicious
80-100: Critical, definitely don't visit

## File Structure

```
scam-url-checker/
├── main.py
├── modules/
│   ├── url_parser.py
│   ├── blacklist.py
│   └── patternchecker.py
└── README.md
```

main.py does the main work - it calls the other modules and shows results. Each module handles one specific thing.

## What I learned making this

- How to write functions and pass data between them
- How to use loops to check through lists
- String operations like slicing and checking if something is inside a string
- Breaking code into separate modules so its organized
- How to structure a project

## The Blacklist

Has domains that pretend to be popular sites:
- PayPal fakes (different typos and variations)
- Amazon account verification scams
- Google phishing pages
- Facebook/Instagram impersonators
- Microsoft and Apple fakes
- Fake bank sites
- Crypto and NFT scams
- Lottery and prize winning scams
- Generic "verify your account" domains

Around 180 domains total that are known to be sketchy.

## Scoring Breakdown

Blacklist match: 50 points
No HTTPS: 15 points
Suspicious keywords: 8 points
Too many hyphens: 10 points
Short domain: 5 points
IP address: 20 points
Max total: 100 points

## Test it out

Try these URLs to see it in action:

```
https://google.com
Expected: Score 0, Safe

https://paypal-login.com
Expected: Score 50+, High risk

http://suspicious-site.com/login
Expected: Score 23, Medium risk
```

## Limitations

This is a first semester project so it has some limitations:
- The blacklist is static, not updated in real time
- No machine learning or anything fancy
- Doesn't check actual SSL certificates
- Just pattern matching based on heuristics
- Terminal only, no graphical interface

## Future stuff

Could add:
- A GUI with buttons instead of terminal
- Real time updates to the scam list
- Actually verify SSL certificates
- Make it a web app
- Browser extension maybe

## Who made this

First year CS student at VIT Bhopal, learning how to actually build something useful with basic Python concepts.

## License

MIT - use it however you want for school projects or whatever.

---

If something is broken or you find a scam domain that's not on the list, let me know.
