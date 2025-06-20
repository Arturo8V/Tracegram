import json
import requests
import time
import os
import argparse
from typing import List

script_dir = os.path.dirname(os.path.abspath(__file__))
cookies_path = os.path.join(script_dir, "instagram_cookies.json")

def load_cookies():
    if not os.path.exists(cookies_path):
        print(f"[❌] File 'instagram_cookies.json' NOT found at:\n{cookies_path}")
        exit()
    else:
        print(f"[✅] Loading cookies from:\n{cookies_path}")

    with open(cookies_path, "r", encoding="utf-8") as f:
        raw_cookies = json.load(f)

    session = requests.Session()
    for cookie in raw_cookies:
        session.cookies.set(cookie["name"], cookie["value"], domain=cookie["domain"])
    return session

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
}

def safe_get(session, url, **kwargs):
    retries = 0
    while retries < 5:
        r = session.get(url, headers=headers, **kwargs)
        if r.status_code == 429 or "Please wait" in r.text:
            wait_time = 2 ** retries
            print(f"[⏳] Rate-limit detected. Waiting {wait_time}s...")
            time.sleep(wait_time)
            retries += 1
            continue
        return r
    raise Exception("[🚫] Too many requests. Rate limit enforced.")

def get_user_id(session: requests.Session, username: str) -> str:
    url = "https://www.instagram.com/web/search/topsearch/"
    params = {"query": username}
    r = safe_get(session, url, params=params)
    if r.status_code != 200:
        raise Exception(f"Could not get user_id for @{username}")
    data = r.json()
    for user in data.get("users", []):
        if user["user"]["username"].lower() == username.lower():
            return str(user["user"]["pk"])
    raise Exception(f"User @{username} not found in search.")

def get_following(session: requests.Session, user_id: str) -> List[str]:
    query_hash = "3dec7e2c57367ef3da3d987d89f9dbc8"
    variables = {
        "id": user_id,
        "include_reel": True,
        "fetch_mutual": False,
        "first": 50
    }
    usernames = []
    has_next = True
    end_cursor = None

    while has_next:
        if end_cursor:
            variables["after"] = end_cursor

        url = f"https://www.instagram.com/graphql/query/?query_hash={query_hash}&variables={json.dumps(variables)}"
        r = safe_get(session, url)

        data = r.json()
        if "data" not in data or not data["data"].get("user"):
            print(f"   🔒 Private or inaccessible profile. Skipping...")
            break

        edges = data["data"]["user"]["edge_follow"]["edges"]
        for edge in edges:
            usernames.append(edge["node"]["username"])
        page_info = data["data"]["user"]["edge_follow"]["page_info"]
        has_next = page_info["has_next_page"]
        end_cursor = page_info["end_cursor"]
        time.sleep(2)

    return usernames

def main():
    parser = argparse.ArgumentParser(description="Find users who follow a target, among the followings of another account.")
    parser.add_argument("-o", "--origin", required=True, help="Origin account username")
    parser.add_argument("-t", "--target", required=True, help="Target account username")
    parser.add_argument("-s", "--save", default="matches.txt", help="Output file")
    args = parser.parse_args()

    session = load_cookies()

    try:
        print(f"[+] Fetching user_id for @{args.origin}...")
        origin_id = get_user_id(session, args.origin)
        print(f"[+] ID for @{args.origin}: {origin_id}")

        print(f"[+] Fetching followings of @{args.origin}...")
        level1_following = get_following(session, origin_id)
        print(f"[+] Found {len(level1_following)} users. Searching second level...")

        users_following_target = []

        for idx, username in enumerate(level1_following, 1):
            print(f"[{idx}/{len(level1_following)}] Checking @{username}...")
            try:
                user_id = get_user_id(session, username)
                followees = get_following(session, user_id)
                if args.target.lower() in [u.lower() for u in followees]:
                    print(f"   ✅ @{username} follows @{args.target}!")
                    users_following_target.append(username)
                else:
                    print(f"   ❌ Does not follow.")
            except Exception as e:
                print(f"   [!] Error accessing @{username}: {e}")
                continue

        output_path = os.path.join(script_dir, args.save)
        with open(output_path, "w", encoding="utf-8") as out:
            for user in users_following_target:
                out.write(user + "\n")

        print("\n=== FINAL RESULT ===")
        if users_following_target:
            print(f"🔥 @{args.target} is followed by:")
            for u in users_following_target:
                print(f" - @{u}")
            print(f"[💾] Results saved to '{output_path}'")
        else:
            print(f"❌ No one from @{args.origin}'s following list follows @{args.target}")

    except Exception as err:
        print(f"[ERROR] {err}")

if __name__ == "__main__":
    main()
