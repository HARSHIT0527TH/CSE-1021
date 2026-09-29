#{Sir} -- Harshit Sir
from blacklist import check_blacklist
from domainextractor import extract_domain
from patternchecker import check_patt


def enter_url():
    url = input("Sir plz enter the string: ")
    # for http:// and etc
    if "http://" not in url and "https://" not in url:
        print("Error: Link must start with \"http://\" and \"https://\",plz check the link")
        return None
    #for blank
    if url == "":
        print("Error: Sir ulc can't be empty")
        return None
    return url

def calc_risk(blacklist_score,patt_score):
    t_score= blacklist_score + patt_score

    if t_score < 0:
        t_score = 0

    if t_score > 100:
        t_score = 100

    return t_score

def url_risk(domain,score,flag):
    print("\n")
    print("*"*70)
    print("*" + " " * 68 + "*")
    print("*" + "SCAM URL CHECKER - RISK REPORT".center(68) + "*")
    print("*" + " " * 68 + "*")
    print("*"*70)
    print("\n"*2)
    print("-"*70)
    print("Sir the domain of URL: "+ domain)
    print("\n")
    print("Sir the risk sore is: " + str(score) + "/100\'")
    print("-" * 70)
    print("DETECTED FLAGS:")
    print("-" * 70)
    
    if len(flag) == 0:
        print("✓ No flags detected - URL appears SAFE!")
    else:
        for flag in flag:
            print("  [!] " + flag)
    print("\n" + "-" * 70)
    print("RISK LEVEL ASSESSMENT:")
    print("-" * 70)
    
    if score >= 80:
        print(" Sir Risk level is: Critical ")
        print(" Sir I recommend u to not visit this side")
    elif score <= 80 and score >= 65:
        print(" Sir Risk level is: High ")
        print(" Sir it's very suspecious -- AVOID IF POSSIBLE")
    elif score <= 65 and score >= 40:
        print(" Sir Risk level is: Mid ")
        print(" Sir it's a bit suspecious -- Proceed with Caution")
    elif score <= 30 and score >= 15:
        print(" Sir Risk level is: KIND OF LOW")
        print(" Sir it's kind of suspecious -- Proceed but be a bit alert")
    else:
        print(" Sir Risk level is: Very Low")
        print("Sir it's likely safe -- NO Need to Worry")
    print("-"*70 + "\n")

def work():
    url = enter_url()
    if url is None:
        return
    print("\n Wait Sir just Analyzing URL...\n")

    # domain dalna hai
    domain = extract_domain(url)
    print("Extracted domain: " + domain)

    blacklist_score,blacklist_flag = check_blacklist(domain)
    print("Sir Now Checking blacklist...")
    
    patt_score , patt_flag= check_patt(domain, url)
    print("Sir Now Checking patterns...")
    all_flag = blacklist_flag+patt_flag

    final_score = calc_risk(blacklist_score,patt_score)
    url_risk(domain, final_score,all_flag)


if __name__ == "__main__":
    work()
