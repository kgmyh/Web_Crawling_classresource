# https://www.delftstack.com/ko/howto/python/vpn-python/
# https://marinelifeirony.tistory.com/154
# https://coding-shop.tistory.com/384#google_vignette
import requests
import os
import sys
import tempfile
import subprocess
import base64
import time
import json
import bs4

if len(sys.argv) != 2:
    print("Enter one country at a time!")
    exit(1)
cntry = sys.argv[1]

if len(cntry) > 2:
    j = 5
elif len(cntry) == 2:
    j = 6
else:
    print("Cannot identify the country. Name is too short.")
    exit(1)

try:
    vpnServerListData = requests.get("http://www.vpngate.net/api/iphone/").text.replace(
        "\r", ""
    )
    freeServers = [line.split(",") for line in vpnServerListData.split("\n")]
    serverLabels = freeServers[1]
    serverLabels[0] = serverLabels[0][1:]
    freeServers = [srvrs for srvrs in freeServers[2:] if len(srvrs) > 1]
    print("run")
except:
    print("Something is wrong! Cannot load the VPN server's data")
    exit(1)

    availableServers = [
        srvrs for srvrs in freeServers if cntry.lower() in srvrs[j].lower()
    ]
    numOfServers = len(availableServers)
    print("We found " + str(numOfServers) + " servers for " + cntry)
    if numOfServers == 0:
        exit(1)

    supporteServers = [srvrs for srvrs in availableServers if len(srvrs[-1]) > 0]
    print(str(len(supporteServers)) + " of these servers support OpenVPN")

    bestServer = sorted(
        supporteServers,
        key=lambda srvrs: float(srvrs[2].replace(",", ".")),
        reverse=True,
    )[0]
    print("\n== Best server ==")
    labelPair = list(zip(serverLabels, bestServer))[:-1]
    for (l, d) in labelPair[:4]:
        print(l + ": " + d)
    print(labelPair[4][0] + ": " + str(float(labelPair[4][1]) / 10 ** 6) + " MBps")
    print("Country: " + labelPair[5][1])

    print("\nLaunching VPN...")
    _, path = tempfile.mkstemp()
    file = open(path, "wb")
    file.write(base64.b64decode(bestServer[-1]))
    file.write(
        b"\nscript-security 2\nup /etc/openvpn/update-resolv-conf\ndown /etc/openvpn/update-resolv-conf"
    )
    file.close()
    vpnR = subprocess.Popen(["sudo", "openvpn", "--config", path])

try:
    # time required to connect the openvpn to connect the vpn server
    time.sleep(10)
    timeS = time.time()
    nUrl = "https://www.findip.kr/"
    nRet = requests.get(nUrl)
    print(nRet.status_code)
    if nRet.status_code == 200:
        # with open("resp", "wb") as txtFile:
        #     txtFile.write(nRet.text)
        bs = bs4.BeautifulSoup(nRet.text, "html.parser")
        ip = bs.select_one('h2.w3-xxlarge').text
        print(f"Time took to check Ip address {ip}: ", (time.time() - timeS))

    vpnR.kill()

except Exception as ex:
    try:
        vpnR.kill()
    except:
        pass
    while vpnR.poll() != 0:
        time.sleep(1)
    print("\nVPN has terminated")