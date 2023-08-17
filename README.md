## PixelProbe
<img src="https://i.imgur.com/FGrjNM4.jpg">

### Overview

PixelProbe is a script developed for querying AI-related terms on Bing using the Bing API. It enables users to quickly search for different facets of AI, from tools to innovations and use cases. This script combines multiple libraries and tools to efficiently gather and process search data.

### Prerequisites

1. Python 3.x
2. Libraries:
   - httpx
   - asyncio
   - googlesearch
   - tqdm
   - dotenv
   - requests

### Setup

1. Install the necessary libraries:
    ```bash
    pip install httpx asyncio googlesearch tqdm python-dotenv requests
    ```

2. Create a `.env` file in the same directory as your script and set your Bing API key:
    ```plaintext
    bing_api_key=YOUR_API_KEY_HERE
    ```

### Usage

1. Run the script:
    ```bash
    python SEO.py
    ```

2. The script will start by searching for a predefined set of AI-related terms on Bing.
3. As the results come in, they will be processed and logged.
4. If any errors or exceptions occur, they will be logged in a `logfile.txt`.

### Customization

1. Modify the `searches` list to add or remove terms you want to query.
2. Adjust the `GLOBALQCAP` to change the number of queries you'd like to send.
3. If you'd like to run a time trial, set `TIMETRIAL = True`.

### Debugging

- Set `DEBUG_MODE = True` to activate debugging mode.

### Contributing

Contributions of any size are encouraged. Please open a new Pull Request if you'd like to contribute to the PixelProbe project.
If you have any issues, feel free to create a new Github Issue or join the [StompZone Discord](https://discord.gg/stompzone)
  
### Contributing

Feel free to fork the project and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

### License

[MIT License](https://opensource.org/license/mit/)

### Disclaimer

Ensure you have permission from Bing and that you adhere to the API's usage limits and terms of service. 
The author(s) of this software accept no responsibility or liability for misuse of this product.
