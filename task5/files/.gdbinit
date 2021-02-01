set pagination off
file gpslogger
b main.setup_cipher
b main.generate_key
b main.generate_iv
b strings.Repeat
b runtime.concatstring2
commands
