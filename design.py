# Design Document - Scam URL Checker

## Overview

This document explains how the project is structured and why I made certain design choices.

## Architecture

The project uses a modular design with a central orchestrator. Here's how it's organized:

```
main.py (Orchestrator)
    |
    +-- modules/url_parser.py (Domain Extraction)
    |
    +-- modules/blacklist.py (Database Check)
    |
    +-- modules/patternchecker.py (Pattern Detection)
```

Each module does one specific job. main.py calls them in order and combines the results.

## Why Modular Design

I separated the code into modules for a few reasons:

1. Each module has one responsibility. url_parser.py only extracts domains. blacklist.py only checks the database. This makes it easy to understand and fix.

2. If I want to change how patterns are detected, I only need to edit patternchecker.py. The rest of the code doesn't break.

3. It's easier to test. I can test each module independently without running the whole program.

4. Someone else can easily add a new module later (like for SSL certificate checking) without touching existing code.

## Data Flow

Here's how data moves through the program:

```
User Input (URL)
    |
    v
enter_url() - Validates the URL format
    |
    v
extract_domain() - Strips protocol, removes www
    |
    v
check_blacklist() - Checks against known scam domains
    |
    v
check_patt() - Looks for suspicious patterns
    |
    v
calc_risk() - Combines scores and caps at 100
    |
    v
url_risk() - Displays results with flags
    |
    v
User sees risk report
```

## Module Details

### main.py

This is the control center. It orchestrates everything.

Functions:
- enter_url(): Gets input from user and validates format
- calc_risk(): Adds the two scores together, ensures it doesn't exceed 100
- url_risk(): Displays the final report with flags
- work(): The main flow that calls everything in order

Why separate these functions instead of having one big work function? Because each function does one thing. If I need to change how the input works, I just edit enter_url(). Easier to debug, easier to understand.

### modules/url_parser.py

Extracts the clean domain from a full URL.

```
Input:  https://www.amazon-account-verify.info/login?ref=email
Output: amazon-account-verify.info
```

How it works:
1. Remove https:// or http://
2. Remove www. if present
3. Stop at the first delimiter (/, ?, :, or #)

Why a separate module? Parsing URLs is its own problem. Later if I want to handle subdomains differently or support more URL formats, I can change just this module.

### modules/blacklist.py

Maintains a list of 180+ known scam domains and checks if the input domain matches.

Returns two things:
- score: 50 if found in blacklist, 0 if safe
- flags: A list of why it's flagged (for the report)

Why return both? The score is needed for the calculation, and the flags are needed to explain to the user why it's suspicious.

### modules/patternchecker.py

Analyzes the domain and URL for 5 types of suspicious patterns.

Pattern checks (in order):
1. Too many hyphens in domain (more than 2) = 10 points
2. Domain too short (less than 5 chars) = 5 points
3. No HTTPS encryption = 15 points
4. Suspicious keywords in URL = 8 points
5. Domain is actually an IP address = 20 points

Each check adds points if the condition is met. Returns both score and flags.

Why these patterns? They're common tactics used in phishing:
- Hyphens look similar to domain separators (typosquatting)
- Short domains are less memorable and more suspicious
- No HTTPS means data isn't encrypted
- Keywords like "login" and "verify" are used to trick people
- Using IP instead of domain name hides the real identity

## Design Decisions Explained

### Why cap score at 100?

A risk can't be more than 100% risky. If somehow all checks trigger, the score could go over 100, but that doesn't make sense. Capping ensures the score stays meaningful.

### Why return flags from each module?

I could have just returned the score, but then main.py wouldn't know which checks triggered. By returning flags, the user sees exactly why something is flagged. This is way more helpful than just showing a number.

### Why use lowercase variable names?

I'm following Python conventions (PEP 8). Makes the code look professional and matches what other Python code looks like.

### Why not use classes?

Classes are more advanced. Since this is a first semester project, I stuck with functions because that's what we learned. The modular approach with functions works fine.

### Why is the output formatted this way?

Simple formatting makes it easy to read. The program outputs step by step so users can see the analysis happening. The final report uses lines and spacing to organize information.

## How Scoring Works

The program awards points for each red flag found. Higher score = more suspicious.

Example: amazon-account-verify.info

```
Blacklist check: Domain found = 50 points
Pattern check:
  - HTTPS missing = 15 points
  - Keyword "verify" found = 8 points
  - (Other checks pass with 0 points)
  
Total: 50 + 15 + 8 = 73 points
Risk Level: HIGH (65-79 range)
```

The scoring isn't perfect, but it works well for most cases. A domain with multiple red flags gets a higher score than one with just one issue.

## Edge Cases Handled

1. Empty URL input - rejected immediately
2. URL without protocol - rejected (must have http:// or https://)
3. URL with port number - handled by stopping at the : delimiter
4. URL with query parameters - handled by stopping at the ? delimiter
5. URL with fragments - handled by stopping at the # delimiter
6. IP address as domain - detected and flagged

## What's Not Handled

Some things the program doesn't do (and why):

1. Doesn't verify actual SSL certificates - would need external libraries
2. Doesn't check reputation scores - would need internet connection
3. Doesn't use machine learning - too advanced for first semester
4. Doesn't update blacklist in real time - would need database/API
5. Doesn't block websites - this is just a checker, not a blocker

## Testing Strategy

Manual testing was done with:

Safe domains:
- google.com
- github.com

Scam domains (in blacklist):
- paypal-login.com
- amazon-account-verify.info

Suspicious patterns:
- http://site-with-many-hyphens-here.com/login (missing HTTPS, hyphens, keyword)
- http://sus.co/verify (short domain, keyword, no HTTPS)

Each was tested to verify correct scoring and flag detection.

## Performance

The program is fast. Checking 180 domains in a loop takes milliseconds. String operations are instant. No performance issues for a tool like this.

## Security Notes

This tool is for checking URLs, not a security guarantee. A low score doesn't mean a site is 100% safe. A high score doesn't mean it's definitely malicious. Use it as one of many tools to stay safe online.

## Future Improvements

If I were to expand this:

1. Real-time updates using an API for the blacklist
2. Machine learning model trained on real phishing data
3. Actual SSL certificate verification
4. Check domain registration details (new domains are often scams)
5. Analyze page content, not just the URL
6. Browser extension for easy checking while browsing
7. GUI with Tkinter or web interface
8. Keep statistics on which patterns are most common

## Lessons Learned

Making this project taught me:

1. How to organize code into modules for clarity
2. The importance of returning multiple values (score and flags)
3. How to think about edge cases
4. The balance between simplicity and functionality
5. That good variable names matter a lot for readability

## Conclusion

The design is simple but effective. Using functions and modules keeps the code organized. Each part has a clear job. New features can be added without breaking existing code.

For a first semester project using only basic Python concepts (functions, loops, conditionals), this structure works well.
