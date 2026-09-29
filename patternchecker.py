#{Sir} -- Harshit Sir
def check_patt(domain,url):
    score = 0
    flag = []
    count = 0
    for char in domain:
        if char == "-":
            count += 1

    if count > 2:
        print(" Sir something is wrong \"_SUSPECIOUS_\"")
        score += 10
        flag.append("Sir there are too many Hypens'-' in domain")

    if len(domain) < 5:
        print("Sir it didn't seems like a real Domain")
        score += 5
        flag.append("Sir the domain is too short then usual")

    if "https://" not in url:
        print("sir here is no \"https://\" here")
        score += 15
        flag.append("Sir it didn't had the correct order")

    suspicious_words = ["login", "verify", "confirm", "update", "secure", "account", "suspend", "alert"]
    url_lower = url.lower()

    for word in suspicious_words:
        if word in url_lower:
            print("Suspicious word found:" + word)
            score += 8
            flag.append("sir Suspecious key word detected: " + word)
            break

    dot_c = 0
    for char in domain:
        if char == ".":
            dot_c += 1

    if dot_c == 3:
        print("Sir it's not domain it's the \'I.P ADRESS\'")
        flag.append("Sir Domain is IP address is not normal")
        score += 20

    return score,flag
