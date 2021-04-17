import json

def decodeMarketName(name):
    """Decode a name to its market code and instrument code

    Args:
        name (Str): [Name of the stock]
    """    
    # TODO: Prevent deserializing this a billion times
    with open("market_code.json") as marketNameFile:
            # Deserializing the data
            marketJSON = json.load(marketNameFile)
            try:
                return marketJSON[name]['instrument_code'], marketJSON[name]['market_code']
            except:
                raise ValueError("Stock name not found")
                print("Could not find name: " + name)