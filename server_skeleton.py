##############################################################################
# server.py
##############################################################################
import chatlib
import socket
import select


# GLOBALS
users = {}
questions = {}
logged_users = {} # a dictionary of client hostnames to usernames - will be used later

ERROR_MSG = "Error! "
SERVER_PORT = 5555
SERVER_IP = "127.0.0.1"
MAX_MSG_LENGTH = 1024

CORRECT_ANSWER_POINTS = 5
WRONG_ANSWER_POINTS = 0

PROTOCOL_CLIENT = {'login_msg':'LOGIN',
 'singup_msg':'SINGUP',
 'logout_msg':'LOGOUT',
 'getscore_msg':'MY_SCORE',
 'getlogged_msg':'LOGGED',
 'gethighscore_msg':'HIGHSCORE',}
PROTOCOL_SERVER = {'login_ok_msg':'LOGIN_OK',
 'login_failed_msg':'ERROR',
 'yourscore_msg':'YOUR_SCORE',
 'highscore_msg':'ALL_SCORE',
 'logged_msg':'LOGGED_ANSWER',
 'correct_msg':'CORRECT_ANSWER',
 'wrong_msg':'WRONG_ANSWER',
 'error_msg':'ERROR',}
# HELPER SOCKET METHODS

def build_and_send_message(conn, cmd, data):
	## copy from client
	global messages_to_send
	full_msg = chatlib.build_message(cmd, data)
	host = conn.getpeername()
	print('[SERVER] ', host, 'msg: ', full_msg)
	conn.send(full_msg.encode())
#	messages_to_send.append((conn, full_msg))	  # Debug print
def recv_message_and_parse(conn):
	## copy from client

	full_msg = conn.recv(MAX_MSG_LENGTH).decode()
	host = conn.getpeername()
	print('[CLIENT] ', host, 'msg: ', full_msg)
	cmd, data = chatlib.parse_message(full_msg)
	return (cmd, data)
# Data Loaders #

def load_user_database():
	"""
	Loads users list from file	## FILE SUPPORT TO BE ADDED LATER
	Recieves: -
	Returns: user dictionary
	"""
	users = {
			"test"		:	{"password":"test","score":0},
			"123"		:	{"password":"123","score":50},
			"master"	:	{"password":"master","score":200}
			}
	return users
# SOCKET CREATOR
def setup_socket():
	"""
	Creates new listening socket and returns it
	Recieves: -
	Returns: the socket object
	"""
	# Implement code ...

	print("Setting up server...")
	sckot = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sckot.bind((SERVER_IP, SERVER_PORT))
	sckot.listen(1)
	print("Listening for clients...")

	return sckot

def send_error(conn, error_msg):
	"""
	Send error message with given message
	Recieves: socket, message error string from called function
	Returns: None
	"""
	# Implement code ...
	build_and_send_message(conn, "ERROR", ERROR_MSG + error_msg)

def create_high_scores():
    global users
    data = ''
    users_and_scores = []
    for user in users.keys():
        users_and_scores.append((user, users[user]['score']))
    else:
        users_and_scores.sort(key=(lambda x: x[1]), reverse=True)
        for user, score in users_and_scores:
            data += '%s: %d\n' % (user, score)
        else:
            return data

##### MESSAGE HANDLING
def handle_highscore_message(conn):
	highscore_str = create_high_scores()
	build_and_send_message(conn, PROTOCOL_SERVER['highscore_msg'], highscore_str)

def handle_getscore_message(conn, username):
	global users
	# Implement this in later chapters
	score = users[username]['score']
	build_and_send_message(conn, PROTOCOL_SERVER['yourscore_msg'], str(score))
	
def handle_logout_message(conn):
	"""
	Closes the given socket (in laster chapters, also remove user from logged_users dictioary)
	Recieves: socket
	Returns: None
	"""
	global logged_users

	# Implement code ...
	client_hostname = conn.getpeername()
	if client_hostname in logged_users.keys():
		del logged_users[client_hostname]
	conn.close()

def handle_login_message(conn, data):
	"""
	Gets socket and message data of login message. Checks  user and pass exists and match.
	If not - sends error and finished. If all ok, sends OK message and adds user and address to logged_users
	Recieves: socket, message code and data
	Returns: None (sends answer to client)
	"""
	global users  # This is needed to access the same users dictionary from all functions
	global logged_users	 # To be used later

	# Implement code ...
	client_hostname = conn.getpeername()
	username, password = chatlib.split_data(data, 2)
	if username not in users.keys():
		send_error(conn, 'Username does not exist')
		return None
	if users[username]['password'] != password:
		send_error(conn, 'Password does not match!')
		return None
	logged_users[client_hostname] = username
	print(logged_users)
	build_and_send_message(conn, "LOGIN_OK", '')

def handle_singup_message(conn, data):
	"""
	Gets socket and message data of singup message. Checks  user exists.
	If yes - sends error and finished. If all ok, sends OK message and adds user and pass to users
	Recieves: socket, message code and data
	Returns: None (sends answer to client)
	"""
	global users  # This is needed to access the same users dictionary from all functions
	# Implement code ...
	username, password = chatlib.split_data(data, 2)
	if username not in users.keys():
		users[username] = {"password":password ,"score":0}
		build_and_send_message(conn, "SINGUP_OK", '')
	else:
		send_error(conn, 'Username is already used')

def handle_logged_message(conn):
    """
    Sends to the socket LOGGED message with all the logged users
    Recieves: socket and username (str)
    Returns: None (sends answer to client)
    """
    global logged_users
    all_logged_users = logged_users.values()
    logged_str = ','.join(all_logged_users)
    build_and_send_message(conn, PROTOCOL_SERVER['logged_msg'], logged_str)

def handle_client_message(conn, cmd, data):
	"""
	Gets message code and data and calls the right function to handle command
	Recieves: socket, message code and data
	Returns: None
	"""
	global logged_users	 # To be used later
	hostname = conn.getpeername()
	hostname_logged_in = hostname in logged_users.keys()
	if cmd == "LOGIN":
		handle_login_message(conn, data)
	elif cmd == "MY_SCORE":
		handle_getscore_message(conn, data)
	elif cmd == "HIGHSCORE":
		handle_highscore_message(conn)
	elif cmd == "LOGGED":
		handle_logged_message(conn)
	elif cmd == "SINGUP":
		handle_singup_message(conn, data)
	else:
		build_and_send_message(conn,"ERRORR", "there is no exsite")
	# Implement code ...
	
def print_client_sockets(client_sockets):
    for c in client_sockets:
        print("\t", c.getpeername())

def main():

	global users
	global questions
	global logged_users
	print("Welcome to Trivia Server!")
	
	# Implement code ...
	users = load_user_database()
	logged_users = {}
	server_socket = setup_socket()
	client_sockets = []
	messages_to_send = []

	while True:
		ready_to_read, ready_to_write, in_error = select.select([server_socket] + client_sockets, client_sockets, [])
		for current_socket in ready_to_read:
			if current_socket is server_socket:
				(client_socket, client_address) = current_socket.accept()
				print("New client joined!", client_address)
				client_sockets.append(client_socket)
				print_client_sockets(client_sockets)
			else:
				print("New data from client")
				try: 
					cmd, data = recv_message_and_parse(current_socket)
					if cmd == None or cmd == "LOGOUT":
						handle_logout_message(current_socket)
						client_sockets.remove(current_socket)
						print('Connection closed')
						print_client_sockets(client_sockets)
					else:
						handle_client_message(current_socket, cmd, data)
				except:
					print("===")
					handle_logout_message(current_socket)
					client_sockets.remove(current_socket)
					print('Connection closed')
					print_client_sockets(client_sockets)
#		else:
#			for message in messages_to_send:
#				current_socket, data = message
#				if current_socket in ready_to_write:
#					if current_socket in client_sockets:
#						current_socket.sendall(data.encode())
#				messages_to_send.clear()



if __name__ == '__main__':
	main()

	