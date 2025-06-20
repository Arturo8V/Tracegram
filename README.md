# 🕵️ Tracegram – Instagram OSINT CLI Tool


**Tracegram** te permite saber si un usuario es seguido por los seguidos de otro. Útil para OSINT, análisis de redes o curiosidad investigadora.

**Tracegram** lets you identify whether a given target user is followed by any of the accounts that a source user follows. Perfect for OSINT, social graph analysis, or investigative curiosity.


## ⚙️ Requirements

- Python 3.8+
- Valid Instagram session cookies (exported manually)
- A logged-in Instagram account (to generate cookies)

🍪 How to Export Your Instagram Cookies (Required)
Tracegram uses your browser session cookies to authenticate with Instagram. This is necessary because Instagram does not provide a public API for follower data, and most endpoints require you to be logged in.
Without valid cookies, the tool won’t work.

🧭 How to Get the Cookies
  Open https://www.instagram.com in your desktop browser (Chrome recommended).

  Make sure you're logged in with the Instagram account you want to use.

  Press F12 or right-click → Inspect to open Developer Tools.

  Go to the tab: Application → expand Cookies → click https://www.instagram.com

  In the list of cookies shown, locate:

  sessionid

  ds_user_id

Your cookie file should be placed in:

```bash
  tracegram/cookies/instagram_cookies.json
  I've included a template file. Just replace the "value" fields with your actual Instagram session cookies.



## 📦 Installation

```bash
git clone https://github.com/youruser/tracegram.git
cd tracegram
pip install -e .
tracegram -o origin_user -t target_user
