import clint.textui
import os.path
import requests

"""How do you monitor the download progress of a very large file?
"""

# Instead of using urllib etc., I used the requests library
# I also used clint, which is created by the same guy that made requests

# Check out Requests: http://docs.python-requests.org/en/master/
# You can install using pip

url = "https://dl.google.com/chrome/mac/stable/GGRO/googlechrome.dmg"
# Streaming, so we can iterate over the response.
r = requests.get(url, stream=True)

# takes the file name from the url and joins it to the user's desktop path
path = [os.path.expanduser('~'), "Desktop", url.split("/")[-1]]
download_location = os.path.join(*path)


with open(download_location, 'wb') as f:
    total_length = int(r.headers.get('content-length'))

    for chunk in clint.textui.progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1):
        if chunk:
            f.write(chunk)
            f.flush()
