Put standalone executables in here (can be any programs, not just python).

CoinTrader can load these as External Plugins and send and receive data from them,

Or you can have them executed periodically (like every 30 seconds, or 20 minutes or hour or whatever)

The output from the command can be returned into the interactive CoinTrader workbench to alert users
to potential good buys, market dumps or whatever your app does.

For structure, put all your development code in a subdirectory and
just the executable and config files in the Externals directory
proper. 