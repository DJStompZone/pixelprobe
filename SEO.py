import httpx
import json
import asyncio
import datetime
import os
import time
from time import time as TIME
from googlesearch import search
from urllib.parse import urlparse
from base64 import b64decode as d6
from math import inf
from tqdm import tqdm
from requests.exceptions import HTTPError

from dotenv import load_dotenv
load_dotenv()

DEBUG_MODE = DEBUGMODE = True
LOGFILE = "logfile.txt"
TIMETRIAL = False
GLOBALQCAP = 50
NUM_SVCS = 2

BING_API_ENDPOINT = "https://api.bing.microsoft.com/v7.0/search"
BING_API_KEY = os.environ.get("bing_api_key")
if not any([os.path.isfile('./.env') or BING_API_KEY, DEBUGMODE]):
    raise ValueError(f"[WARN] You do not appear to have a bing api key set\nPlease create a .env file and re-run this script")


searches = [
    "chat",
    "tools",
    "image generator",
    "character",
    "assistant",
    "platform",
    "software",
    "text generator",
    "conversational agent",
    "research tools",
    "training data",
    "for business",
    "language processing",
    "voice assistant",
    "for gaming",
    "framework",
    "libraries",
    "innovations",
    "trends",
    "solutions",
    "analytics",
    "predictions",
    "use cases",
    "for healthcare",
    "for finance",
]

prep_queries = lambda inpt: [
    f"ai {ea}"
    for ea in (
        []
        if (type(inpt) not in [str, set, list])
        else ([inpt] if type(inpt) is str else inpt)
    )
]

l5, l2 = [[67, 103, 111, 75, 67, 103, 111, 61], [67, 103, 111, 61]]


_rb = lambda inp: print(d6("".join([chr(ea) for ea in inp])).decode())

bnr=[73,67,65,103,73,67,65,103,73,67,65,103,73,67,65,103,73,67,65,103,73,67,65,103,73,67,65,103,73,67,65,103,73,67,65,103,73,67,65,103,73,67,65,103,73,67,65,103,73,67,65,103,73,67,65,103,73,67,65,103,73,67,65,103,73,67,65,103,73,67,65,103,73,67,65,103,73,67,65,103,73,67,65,103,73,67,65,103,73,67,65,103,73,67,65,103,73,67,65,103,67,105,65,103,73,67,65,103,73,67,65,103,73,67,65,103,73,67,65,115,76,67,65,103,73,67,65,103,73,67,65,103,73,67,65,103,73,67,65,103,73,67,65,103,73,67,65,103,73,67,65,115,76,67,65,103,73,67,65,103,73,67,65,103,73,67,65,103,73,67,65,103,73,67,65,103,73,67,65,103,73,67,65,103,73,67,65,103,73,67,65,103,73,67,65,115,76,67,65,103,73,67,65,103,73,67,65,103,73,67,65,103,73,67,65,103,73,67,65,103,67,109,65,51,84,85,48,105,73,105,74,78,99,83,52,103,73,67,66,107,89,105,65,103,73,67,65,103,73,67,65,103,73,67,65,103,73,67,65,103,73,67,65,103,73,67,65,103,89,68,100,78,84,83,65,103,89,68,100,78,84,83,73,105,73,107,49,120,76,105,65,103,73,67,65,103,73,67,65,103,73,67,65,103,73,67,65,103,73,67,65,103,73,67,112,78,84,83,65,103,73,67,65,103,73,67,65,103,73,67,65,103,73,67,65,103,73,67,65,103,67,105,65,103,84,85,48,103,73,67,66,103,84,85,48,117,73,67,65,103,73,67,65,103,73,67,65,103,73,67,65,103,73,67,65,103,73,67,65,103,73,67,65,103,73,67,65,103,73,67,66,78,84,83,65,103,73,67,66,78,84,83,65,103,73,71,66,78,84,83,52,103,73,67,65,103,73,67,65,103,73,67,65,103,73,67,65,103,73,67,65,103,73,67,66,78,84,83,65,103,73,67,65,103,73,67,65,103,73,67,65,103,73,67,65,103,73,67,65,103,67,105,65,103,84,85,48,103,73,67,65,115,84,84,107,103,89,68,100,78,84,83,65,103,89,68,100,78,74,121,65,103,73,71,66,78,82,105,99,117,90,49,65,105,87,87,69,103,73,67,66,78,84,83,65,103,73,67,66,78,84,83,65,103,73,67,120,78,79,83,66,103,78,48,49,105,76,71,57,107,79,67,65,115,99,70,99,105,86,51,69,117,73,67,66,78,84,83,120,107,84,85,49,105,76,105,65,103,73,67,53,110,85,67,74,90,89,83,65,103,67,105,65,103,84,85,49,116,98,87,82,78,79,83,65,103,73,67,66,78,84,83,65,103,73,67,66,103,86,107,69,103,76,70,89,110,73,67,120,78,74,121,65,103,73,70,108,105,73,67,66,78,84,83,65,103,73,67,66,78,84,87,49,116,90,69,48,53,73,67,65,103,73,69,49,78,74,121,65,105,74,122,90,88,74,121,65,103,73,71,66,88,89,105,66,78,84,83,65,103,73,67,66,103,84,87,73,103,76,69,48,110,73,67,65,103,87,87,73,103,67,105,65,103,84,85,48,103,73,67,65,103,73,67,65,103,73,67,66,78,84,83,65,103,73,67,65,103,73,70,104,78,87,67,65,103,73,68,104,78,73,105,73,105,73,105,73,105,73,67,66,78,84,83,65,103,73,67,66,78,84,83,65,103,73,67,65,103,73,67,65,103,73,69,49,78,73,67,65,103,73,68,104,78,73,67,65,103,73,67,66,78,79,67,66,78,84,83,65,103,73,67,65,103,84,84,103,103,79,69,48,105,73,105,73,105,73,105,73,103,67,105,65,103,84,85,48,103,73,67,65,103,73,67,65,103,73,67,66,78,84,83,65,103,73,67,65,115,86,105,99,103,86,107,69,117,73,70,108,78,76,105,65,103,73,67,65,115,73,67,66,78,84,83,65,103,73,67,66,78,84,83,65,103,73,67,65,103,73,67,65,103,73,69,49,78,73,67,65,103,73,70,108,66,76,105,65,103,73,67,120,66,79,83,66,78,84,83,52,103,73,67,65,115,84,84,107,103,87,85,48,117,73,67,65,103,73,67,119,103,67,105,53,75,84,85,49,77,76,105,65,103,73,67,65,103,76,107,112,78,84,85,119,117,76,107,70,78,76,105,65,103,73,67,53,78,81,83,53,103,84,87,74,116,98,87,81,110,76,107,112,78,84,85,119,117,76,107,112,78,84,85,119,117,73,67,65,103,73,67,65,117,83,107,49,78,84,67,52,103,73,67,66,103,87,87,74,116,90,68,107,110,73,67,66,81,88,108,108,105,98,87,82,81,74,121,65,103,73,71,66,78,89,109,49,116,90,67,99,103,]
bnrline=[76,83,48,116,76,83,48,116,76,83,48,116,76,83,48,116,76,83,48,116,76,83,48,116,76,83,48,116,76,83,48,116,76,83,48,116,76,83,48,116,76,83,48,116,76,83,48,116,76,83,48,116,76,83,48,116,76,83,48,116,76,83,48,116,76,83,48,116,76,83,48,116,76,83,48,116,76,83,48,116,76,83,48,116,76,83,48,116,76,83,48,116,76,83,48,116,76,83,48,116,76,81,61,61,]
bnr_intro=[73,67,65,103,73,67,65,103,86,50,86,115,89,50,57,116,90,83,66,48,98,121,66,81,97,88,104,108,98,70,66,121,98,50,74,108,73,67,48,103,101,87,57,49,99,105,66,107,97,87,100,112,100,71,70,115,73,70,78,70,84,121,66,108,101,72,66,115,98,51,74,104,100,71,108,118,98,105,66,48,98,50,57,115,73,83,65,103,73,67,65,103,73,65,61,61,]
bnr_intro2=[73,67,65,103,73,67,65,103,73,67,65,103,73,67,66,69,83,105,66,84,100,71,57,116,99,67,65,121,77,68,73,122,73,67,65,103,73,67,65,103,76,83,65,103,73,67,65,103,73,69,53,118,73,70,74,112,90,50,104,48,99,121,66,83,90,88,78,108,99,110,90,108,90,67,65,103,73,67,65,103,73,67,65,103,73,67,65,103,73,67,65,103,73,65,61,61,]
bnrs = [l5, bnr, l2, bnrline, bnr_intro, bnr_intro2, bnrline]


def d_bnr(_b=bnrs):
    __ = [ _rb(ea) for ea in _b]


def dprint(*args, **kwargs):
    global DEBUGMODE
    if not DEBUGMODE:
        return
    print(" ".join(map(str, args)), **kwargs)
    try:
      if not os.path.isfile(LOGFILE):
        dprint("[WARN] No log file present")
      msg = str(" ".join(map(str, args)))+str(**kwargs)
      with open(LOGFILE, "a") as f:
          timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
          f.write(f"[{timestamp}] {msg}\n")
    except Exception as e:
        print(f"Uh-oh, dprint threw an exception:", e)



def listify(srch) -> list:
    ls = []
    while True:
        try:
            ls.append(next(srch))
        except Exception as e:
            if getattr(e, "__class__") is StopIteration:
                return ls if type(ls) is list else list(ls)
    raise ValueError("This should never execute")


async def get_matches(gs=None, q=None, kwd="deepai"):
    if q is not None:
        _gs = await do_gs(q=q)
    else:
        _gs = await do_gs()
    gs = _gs
    return [{i: url} for i, url in enumerate(gs) if kwd in url]


async def get_lowest_match(_ml=None):
    if _ml is None:
        _ml = (
            lambda gs=None, kwd="deepai": [
                {"position": i, "url": url}
                for i, url in enumerate(gs if bool(gs) else do_gs())
                if kwd in url
            ]
        )()
    lowest_match = inf
    if type(_ml) is not list:
        raise TypeError("Not a list!")
    winner = None
    for each in _ml:
        if (
            type(each) is dict
            and bool(each.get("position"))
            and bool(each.get("url"))
            and each["position"] < lowest_match
        ):
            lowest_match = int(each.get("position"))
            winner = each
            dprint(f"DEBUG: Found a new winner with score: {lowest_match}")
    if lowest_match != inf:
        dprint(
            f"DEBUG: Done checking! Our winner was {winner} with score: {lowest_match}"
        )
    else:
        dprint(f"DEBUG: 0/{len(_ml)} matches found", "\n", _ml)
    if lowest_match == inf:
        return -1
    return int(lowest_match)

async def do_gs(q="ai chat", num_results=50, sleep_interval=10, timeout=None) -> list:
    try:
        return listify(
            search(
                q, num_results=num_results, sleep_interval=sleep_interval, timeout=timeout
            )
        )
    except Exception as e:
        if "429" in str(e):
          print("[ERR] Uh oh, we are being rate limited. Please visit this url to resolve: ", str(e).split("url: ")[-1])
          aborted = input("Press enter when ready to continue (or input 'a' to abort)").lower() == 'a'
          if aborted:
              return []
          try:
              return listify(
                    search(
                        q, num_results=num_results, sleep_interval=sleep_interval, timeout=timeout
                    )
              )
          except Exception as e:
              dprint("[ERR] Exception: ", e)
              return []

async def do_gs_kw(search_query: str, depth: int, kw: str):
    try:
        __srch = await do_gs(q=search_query, num_results=depth, timeout=None)
        for i, url in enumerate(__srch):
            if kw.lower() in url.lower():
                return i
        return -1
    except Exception as e:
        print(f"Error in do_gs_kw: {e}")
        return -1

async def do_bs_kw(kw: str, depth: int, search_query: str):
    if BING_API_KEY == None:
        raise ValueError("You do not seem to have a `BING_API_KEY` set\nThis program is unlikely to work properly without one")
    headers = {"Ocp-Apim-Subscription-Key": BING_API_KEY}
    params = {"q": search_query, "count": depth}
    async with httpx.AsyncClient(timeout=None) as client:
        response = await client.get(BING_API_ENDPOINT, headers=headers, params=params, timeout=None)
        if response.status_code > 399:
            dprint(f"[{TIME()}] Got error status {response.status_code}")
            return -1
        data = response.json()
        web_pages = data.get("webPages", {}).get("value", [])
        for i, page in enumerate(web_pages):
            name = page.get("name", "").lower()
            url = page.get("url", "").lower()
            if kw.lower() in name or kw.lower() in url:
                return i
        return -1


async def do_kw_all(kw="deepai", depth=50, search_queries=[], pbar=None, timeout=None):
    results = {}
    try:
        for query in search_queries:
            dprint(f'[INFO] Checking {depth} results for query: "{query}" matching keyword "{kw}"')
            bing_position = await do_bs_kw(kw, depth, query)
            if pbar:  # Update the progress bar after the Bing request
                pbar.update(GLOBALQCAP)
            google_position = await do_gs_kw(query, depth, kw)
            if pbar:  # Update the progress bar after the Google request
                pbar.update(GLOBALQCAP)
            results[query] = {"bing": bing_position, "google": google_position}
            for service in ["bing", "google"]:
                if results[query][service] > -1:
                    results[query][service] += 1
        dprint(f"[INFO] processed {depth*len(search_queries)} items, matched {len(results)}")
    except KeyboardInterrupt:
        dprint("KeyboardInterrupt detected, pretty-printing current results and exiting...")
    finally:
        dprint(f"Finished fetching data, rendering {sum([len(results[ea]) for ea in results.keys()])} results...")
        return results



def _pp(results):
    print('\n'.join([f"{'Query':<25} | Bing Ranking | Google Ranking (WIP)", "-" * 65]))
    for query, positions in results.items():
        bing_rank = "N/A" if positions["bing"] == -1 else positions["bing"]
        google_rank = "N/A" if positions["google"] == -1 else positions["google"]
        print(f"{query:<25} | {bing_rank:<14}| {google_rank}")
pp=_pp

def main_routine(_QCAP: int|None=None):
    QCAP = GLOBALQCAP if not _QCAP else _QCAP
    dprint("Starting up...")
    import asyncio
    queries = prep_queries(searches)
    num_q = len(queries) * NUM_SVCS * GLOBALQCAP
    dprint(f"Queued {num_q} operations")
    pbar = tqdm(total=num_q)  # Initialize the tqdm progress bar here
    outcome = asyncio.run(do_kw_all("deepai", GLOBALQCAP, queries, pbar))
    pbar.close()  # Close the tqdm progress bar
    pp(outcome)
    return num_q

def _TIME_script(prcs=None):
    b4 = TIME()
    _ = (main_routine if not bool(prcs) else prcs)()
    print(
        f"Collected {_ if type(_) is int else len(_)} results in ~{int(TIME() - b4)} seconds"
    )


if __name__ == "__main__":
    d_bnr()
    if all([DEBUG_MODE, TIMETRIAL]):
        print(_TIME_script())
    elif DEBUG_MODE and not TIMETRIAL:
        main_routine()
    else:
        while True:
            input("What're you doing in mah swamp?")
