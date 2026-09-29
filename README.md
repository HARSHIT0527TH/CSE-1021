# Scam-URL-Checker

A small Python program that checks if a link looks like a scam. I made it in my first semester when we were learning functions, loops and if/else.

## What it does

You give it a URL. It pulls out the domain, checks that domain against a list of scam sites I put in the code, and then looks for a few suspicious things like no https, lots of hyphens or words like "login" and "verify". At the end it adds up a score out of 100 and tells you how risky the link is.

## How to run it

You only need Python 3.6 or newer, nothing else to install.

```bash
git clone https://github.com/HARSHIT0527TH/CSE-1021.git
cd CSE-1021
python main.py
```

Type the full link when it asks. It has to start with `http://` or `https://`, otherwise it shows an error and closes.

Example run:

```
Sir plz enter the string: https://amazon-account-verify.info

 Wait Sir just Analyzing URL...

Extracted domain: amazon-account-verify.info
 CRITICAL: Domain found in scam database!
Sir Now Checking blacklist...
Suspicious word found:verify
Sir Now Checking patterns...


**********************************************************************
*                                                                    *
*                  SCAM URL CHECKER - RISK REPORT                    *
*                                                                    *
**********************************************************************


----------------------------------------------------------------------
Sir the domain of URL: amazon-account-verify.info


Sir the risk sore is: 58/100'
----------------------------------------------------------------------
DETECTED FLAGS:
----------------------------------------------------------------------
  [!] Sir domain found in the scam_database
  [!] sir Suspecious key word detected: verify

----------------------------------------------------------------------
RISK LEVEL ASSESSMENT:
----------------------------------------------------------------------
 Sir Risk level is: Mid
 Sir it's a bit suspecious -- Proceed with Caution
----------------------------------------------------------------------
```

If nothing suspicious is found it just prints `✓ No flags detected - URL appears SAFE!`

## Files

Everything is in one folder:

```
scam-url-checker/
├── main.py
├── blacklist.py
├── domainextractor.py
├── patternchecker.py
└── README.md
```

- `main.py` takes the input, calls the other three files, adds up the score and prints the report
- `domainextractor.py` gets the domain out of the URL
- `blacklist.py` has the list of scam domains
- `patternchecker.py` looks for the suspicious patterns

## How it works

**Getting the domain.** The URL is messy, so first it removes `http://` or `https://` and then `www.` if there is one. After that it goes through the letters one by one and stops when it reaches `/`, `?`, `:` or `#`. Whatever it collected before that is the domain.

**Blacklist.** The domain is turned into lowercase and compared with every domain in the list (around 150). It has to match exactly. If it does, the score gets 50 points and a flag is added.

The list has fake versions of PayPal, Amazon, Google, Facebook, Instagram, WhatsApp, Apple, Microsoft and Netflix, fake bank and tax sites (SBI, HDFC, IRS, HMRC and so on), lottery and free gift scams, crypto scams, and some general "verify your account" type domains.

**Patterns.** This part adds points for each thing it finds:

- more than 2 hyphens in the domain: 10 points
- domain shorter than 5 characters: 5 points
- no `https://` in the URL: 15 points
- one of these words anywhere in the URL: 8 points (login, verify, confirm, update, secure, account, suspend, alert)
- exactly 3 dots in the domain, which I treat as an IP address: 20 points

The keyword check stops after the first word it finds, so it can only add 8 points once.

**Final score.** `calc_risk()` adds the blacklist score and the pattern score together. If the total goes above 100 it is set to 100.

## Risk levels

- 80 to 100: Critical, don't visit
- 65 to 79: High, avoid if possible
- 40 to 64: Mid, be careful
- 15 to 30: Kind of low, stay a bit alert
- 0 to 14 and 31 to 39: Very low, probably safe

Scores from 31 to 39 end up in "Very low" because of how my if/elif conditions are written. I noticed it late and haven't fixed it yet.

## Try these

```
https://google.com
score 0, very low

https://paypal-login.com
score 58, mid

http://suspicious-site.com/login
score 23, kind of low
```

## Things it can't do

- The blacklist is fixed inside the code, it doesn't update by itself
- The domain has to match the list exactly, so something like `login.paypal-login.com` is not caught by the blacklist
- The IP check only counts dots, so a normal domain with 3 dots (like `mail.example.co.uk`) also gets flagged
- Only one suspicious word is counted per URL
- It doesn't check the real SSL certificate, it only looks at whether the text `https://` is there
- No machine learning, it is only simple rules
- Terminal only, no GUI

## Ideas for later

- A GUI with buttons
- Getting the scam list from the internet so it stays updated
- Checking the actual SSL certificate
- A web app or a browser extension

## What I learned

- Writing functions and passing values between them
- Using loops to go through lists and strings
- String things like slicing and checking if something is inside another string
- Splitting a project into different files so it stays organised

## About

I'm a first year CS student at VIT Bhopal. 

## License

MIT, use it for school projects or whatever you like.

If something is broken or you find a scam domain that's missing from the list, let me know.
