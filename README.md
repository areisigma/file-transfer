# file-transfer
Simple python3 socket tool to transfer file between two endpoints.

### Modes
This software has two classes. First is transmitter mode and second is receiver mode. Run program with no arguments, usage will print.

### Change addresses
Change IP address in transmitter class to connect computer, that is running this program with `-r` argument.
Change IP address in receiver class to bind this address to your socket. This is necesery to run receiver mode.

#### Note that the program does not always work properly. It has not any anti-byte-loss system. While transfering big files you will get many bugs yet.
