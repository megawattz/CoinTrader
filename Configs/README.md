Put your JSON config in here. It will be loaded automatically by the framework and referenced by its filename,
like Config.Get("MyPlugin")

That will return a python structure to your plugin with the JSON in the file, converted to a python dictionary.

If you subclass from a known CoinTrader base class the Config loading
is done for you and you can reference with the Config object in your
code, like this.

