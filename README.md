![Gemini API](https://docs.gemini.com)

Unofficial and open-source Python 3 module for [Gemini API](https://gemini.com/).

Maneet Khaira

Dependencies
========
- Python >= 3.0
- Requests >= 2.10.0

Usage
========
    
    First, install requests.
    ```
    pip install requests
    ```


    ```
    import gemini

    # Set third argument to True if you are experimenting on api.sandbox.gemini.com
    session = GeminiSession("my_api_key", "my_api_secret", True)

    # Buy .01 BTC at $575/BTC and print the response
    print(sesh.new_order("btcusd", ".01", "575","buy"))
    ```

API Reference
========

## TODO: Finish this section. 

For now, see docstrings in gemini.py

Donations
========

If this has been useful to you, please donate so I can keep on making stuff.

**- BTC: [1HYdvp9AtQWaebcSSEk55PKp12HmpKTdz4](http://puu.sh/pihQ2/af88def653.png)**

Contribute
========

If you are interested in adding any new features or functionality, feel free to send a pull request!