# My Piano Site — crawler laboratory

1. Open PowerShell in this folder and run `python server.py`.
2. Open http://127.0.0.1:8000/ in your browser.
3. In a second PowerShell, run:
   `pip install requests beautifulsoup4`
4. Then run `python crawler.py`.

The site contains four synthetic piano lessons. Each has a WAV audio file and a PDF.
The next experiment will hide the media URLs behind a JSON API so we can study how a crawler discovers resources that are not present directly in the HTML.
