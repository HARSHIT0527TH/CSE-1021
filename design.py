# Design Document - Scam URL Checker

## Overview

This file explains how the project is put together and why I did some things the way I did.

## Structure

The project has one main file that controls everything and three small files that each do one job. All of them are in the same folder.

```
main.py (controls everything)
    |
    +-- domainextractor.py (gets the domain out of the URL)
    |
    +-- blacklist.py (checks the list of scam domains)
    |
    +-- patternchecker.py (looks for suspicious patterns)
```

`main.py` calls them one after another and combines what they return.

## Why I split it into files

- Each file has one job. `domainextractor.py` only gets the domain and `blacklist.py` only checks the list, so it's easier to find a problem.
- If I want to change how patterns are checked, I only edit `patternchecker.py` and the rest stays the same.
- I can test each function on its own without running the whole program.
- A new check (like one for SSL certificates) can be added as a new file later without touching the old ones.

## How data moves

```
User types URL
    |
    v
enter_url()       checks the URL starts with http:// or https://
    |
    v
extract_domain()  removes the protocol and www, cuts at / ? : #
    |
    v
check_blacklist() looks for the domain in the scam list
    |
    v
check_patt()      looks for suspicious patterns
    |
    v
calc_risk()       adds the two scores, keeps it between 0 and 100
    |
    v
url_risk()        prints the report
```

## The files

### main.py

This is the main file. It has four functions:

- `enter_url()` asks for the URL and checks the format
- `calc_risk()` adds the blacklist score and the pattern score
- `url_risk()` prints the report with the flags and the risk level
- `work()` runs everything in order

I made separate functions instead of one big `work()` so that each one does only one thing. If the input needs to change I only edit `enter_url()`.

### domainextractor.py

Gets the domain from a full URL.

```
Input:  https://www.amazon-account-verify.info/login?ref=email
Output: amazon-account-verify.info
```

Steps:
1. Remove `https://` or `http://`
2. Remove `www.` if it's there
3. Go through the letters and stop at the first `/`, `?`, `:` or `#`

I kept this in its own file because reading a URL is its own problem. If I want to handle subdomains differently later, I only change this file.

### blacklist.py

Has a list of about 150 scam domains and checks if the domain is in it. It turns the domain to lowercase first, and then it has to match a domain in the list exactly.

It returns two things:
- the score: 50 if it's found, 0 if not
- a list of flags that explains why it was flagged

The score is needed for the math and the flags are needed so the report can tell the user the reason. This file also prints a "CRITICAL" message on its own when it finds a match.

### patternchecker.py

Checks the domain and the URL for 5 patterns, in this order:

1. More than 2 hyphens in the domain: 10 points
2. Domain shorter than 5 characters: 5 points
3. No `https://` in the URL: 15 points
4. A suspicious word in the URL: 8 points
5. Exactly 3 dots in the domain (treated as an IP address): 20 points

The suspicious words are login, verify, confirm, update, secure, account, suspend and alert. They are searched in the whole URL, not just the domain, and the loop stops at the first one it finds, so this check can only add 8 points once.

It returns the score and the flags, same as the blacklist file.

Why these patterns? They show up a lot in phishing links:
- fake sites often use lots of hyphens to copy a real name
- very short domains look odd
- no https means the connection isn't encrypted
- words like login and verify are used to make people panic and click
- an IP address hides the real name of the site

## Decisions

**Why cap the score at 100?** If every check triggers, the points add up to 108 (50 + 10 + 5 + 15 + 8 + 20). A score over 100 doesn't make sense for "out of 100", so `calc_risk()` sets it to 100. It also sets it to 0 if it's ever below 0, but that can't really happen right now.

**Why return flags as well as the score?** With only a number the user wouldn't know what went wrong. With the flags the report can say exactly why the link looks bad.

**Why no classes?** We haven't learned them yet, and functions were enough for this.

**Why is the output like this?** The program prints each step while it works (extracting the domain, checking the blacklist, checking patterns) so you can see it running. The report at the end uses lines and spacing so it's easy to read.

## How scoring works

Every red flag adds points, so a higher score means more suspicious.

Example with `https://amazon-account-verify.info`:

```
Blacklist: domain found        = 50
Patterns:  keyword "verify"    =  8
           everything else     =  0

Total: 58, risk level Mid
```

The same link typed as `http://amazon-account-verify.info` also loses the https check:

```
50 + 15 + 8 = 73, risk level High
```

Risk levels:

| Score | Level |
|-------|-------|
| 80-100 | Critical |
| 65-79 | High |
| 40-64 | Mid |
| 15-30 | Kind of low |
| 0-14 and 31-39 | Very low |

## What the input check catches

1. URL without `http://` or `https://` is rejected with an error
2. Empty input is rejected too (see the known problems below)
3. A port number like `:8080` is dropped because the extractor stops at `:`
4. Query parameters are dropped because it stops at `?`
5. Fragments are dropped because it stops at `#`
6. Something that looks like an IP address is flagged

## Known problems

Some things in my code don't work the way they should yet:

1. Scores from 31 to 39 print "Very low" because my `elif` conditions leave a gap between "Kind of low" and "Mid". For example `http://site-with-many-hyphens-here.com/login` scores 33 (10 for hyphens, 15 for no https, 8 for the keyword) and shows "Very low".
2. The empty URL check in `enter_url()` is after the `http://` check, so it never runs. An empty input is still rejected, but with the `http://` error message.
3. The IP check just counts dots, so a normal domain with 3 dots (like `mail.example.co.uk`) is flagged as an IP address.
4. The blacklist needs an exact match, so a subdomain like `login.paypal-login.com` is not found in it.
5. The report prints "risk sore" and has an extra `'` after `/100`. That's a typo I need to fix.

## What it doesn't do

1. Doesn't check real SSL certificates, it only looks for the text `https://`
2. Doesn't check reputation scores, that would need internet access
3. No machine learning, that's too advanced for now
4. The blacklist doesn't update by itself
5. Doesn't block websites, it's only a checker

## Testing

URLs to try and the score the code gives:

| URL | Score | Level |
|-----|-------|-------|
| `https://google.com` | 0 | Very low |
| `https://github.com` | 0 | Very low |
| `https://paypal-login.com` | 58 | Mid |
| `https://amazon-account-verify.info` | 58 | Mid |
| `http://suspicious-site.com/login` | 23 | Kind of low |
| `http://a.co/verify` | 28 | Kind of low |
| `http://site-with-many-hyphens-here.com/login` | 33 | Very low (problem 1 above) |

For the `a.co` link the domain is only 4 characters, so it gets the short domain points. A domain like `sus.co` has 6 characters, so it doesn't.

## Speed

Checking about 150 domains in a loop takes almost no time, and the string operations are instant, so speed isn't a problem for a tool like this.

## A note about safety

This tool is only a helper. A low score doesn't mean a site is safe and a high score doesn't mean it's definitely a scam. It should be one of many things you use to stay safe online.

## Ideas for later

1. Get the blacklist from an API so it updates
2. A machine learning model trained on real phishing data
3. Real SSL certificate checking
4. Checking when the domain was registered (new domains are often scams)
5. Reading the page content and not only the URL
6. A browser extension
7. A GUI with Tkinter or a web page
8. Fix the known problems above

## What I learned

1. Splitting code into files so it stays organised
2. Returning more than one value from a function (score and flags)
3. Thinking about edge cases
4. Keeping things simple but still useful
5. Good variable names make the code much easier to read

## Conclusion

The design is simple but it works. Each file has one clear job and new checks can be added without breaking the old ones. It only uses functions, loops and conditionals, which is what we learned in the first semester.
