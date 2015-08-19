# Echo server program

import clientServer


if __name__ == '__main__':
	server=clientServer.ClientServer(MODE=1)
	server.serverStartup()
