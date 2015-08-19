# Echo client program

import clientServer


if __name__ == '__main__':
	client=clientServer.ClientServer(MODE=1)
	client.clientConnect()