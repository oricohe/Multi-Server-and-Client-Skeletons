import socket

# Protocol Constants

CMD_FIELD_LENGTH = 16  # Exact length of cmd field (in bytes)
LENGTH_FIELD_LENGTH = 4  # Exact length of length field (in bytes)
MAX_DATA_LENGTH = 10 ** LENGTH_FIELD_LENGTH - 1  # Max size of data field according to protocol
MSG_HEADER_LENGTH = CMD_FIELD_LENGTH + 1 + LENGTH_FIELD_LENGTH + 1  # Exact size of header (CMD+LENGTH fields)
MAX_MSG_LENGTH = MSG_HEADER_LENGTH + MAX_DATA_LENGTH  # Max size of total message
DELIMITER = "|"  # Delimiter character in protocol
DATA_DELIMITER = "#"  # Delimiter in the data part of the message
SERVER_IP = "127.0.0.1"  # Our server will run on same computer as client
SERVER_PORT = 5555

# Protocol Messages
# In this dictionary we will have all the client and server command names

PROTOCOL_CLIENT = {
    "login_msg": "LOGIN",
    "singup_msg":"SINGUP",
    "logout_msg": "LOGOUT"
}  # .. Add more commands if needed

PROTOCOL_SERVER = {
    "login_ok_msg": "LOGIN_OK",
    'singup_ok_msg':'SINGUP_OK',
    "login_failed_msg": "ERROR"
}  # ..  Add more commands if needed

# Other constants

ERROR_RETURN = None  # What is returned in case of an error


def build_message(cmd, data):
    """
    Gets command name (str) and data field (str) and creates a valid protocol message
    Returns: str, or None if error occured
    """
    # Implement code ...
    cmd = cmd + " " * (CMD_FIELD_LENGTH - len(cmd))
    LLLL = len(data)
    LLLL = str(LLLL)
    LLLL = ("0" * (4 - len(LLLL))) + LLLL
    if len(cmd) > CMD_FIELD_LENGTH:
        full_msg = None
    else:
        full_msg = (cmd + DELIMITER)
    if len(data) <= MAX_DATA_LENGTH and len(data) >= 0 and full_msg != None:
        full_msg = full_msg + (LLLL + DELIMITER + data)
    else:
        full_msg = None

    return full_msg


def parse_message(data):
    """
    Parses protocol message and returns command name and data field
    Returns: cmd (str), data (str). If some error occured, returns None, None
    """
    # Implement code ...
    split_string = data.split(DELIMITER, 2)
    if data.count(DELIMITER) != 2:
        cmd = None
        msg = None
    else:
        i = split_string[1].replace(" ", "")
        if (i.isdecimal() == True):
            if (int(i) >= 0) and (int(i) < 10000):
                cmd = split_string[0]
                msg = split_string[2]
                cmd = cmd.replace(" ", "")
            else:
                cmd = None
                msg = None
        else:
            cmd = None
            msg = None

    #	split_string = cmd.split(" ", 1)
    #	cmd = split_string[0]
    #	if 16 < len(cmd):
    #		cmd = None
    #	if 9999 < len(msg):
    #		msg = None
    #	if data.coumt('|') != 2:
    #		msg = None
    #		cmd = None

    # The function should return 2 values
    return cmd, msg


def split_data(msg, expected_fields):
    """
    Helper method. gets a string and number of expected fields in it. Splits the string
    using protocol's data field delimiter (|#) and validates that there are correct number of fields.
    Returns: list of fields if all ok. If some error occured, returns None
    """
    splitted = msg.split(DATA_DELIMITER)
    if len(splitted) == expected_fields:
        return splitted
    return


# HELPER SOCKET METHODS

def build_and_send_message(conn, code, data):
    """
    Builds a new message, wanted code and message.
    Prints debug info, then sends it to the given socket.
    Paramaters: conn (socket object), code (str), data (str)
    Returns: Nothing
    """
    # Implement Code
    msge = build_message(code, data)
    conn.send(msge.encode())

def recv_message_and_parse(conn):
    """
    Recieves a new message from given socket,
    then parses the message using chatlib.
    Paramaters: conn (socket object)
    Returns: cmd (str) and data (str) of the received message.
    If error occured, will return None, None
    """
    # Implement Code
    # ..
    full_msg = conn.recv(1024).decode()
    cmd, data = parse_message(full_msg)
    return cmd, data
	
	

def connect():
    # Implement Code
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect((SERVER_IP, SERVER_PORT))

    pass
    return conn


def error_and_exit(error_msg):
    # Implement code
    print(error_msg)
    pass


def login(conn):
    dataa = ""
    while dataa != "Bye":

        username = input("Please enter username: \n")
        password = input("Please enter password: \n")
        # Implement code

        build_and_send_message(conn, PROTOCOL_CLIENT["login_msg"], username + "#" + password)
        cmd, data = recv_message_and_parse(conn)
        if cmd == PROTOCOL_SERVER["login_ok_msg"]:
            dataa = "Bye"
        print(data)
    return username

def singup(conn):
    dataa = ""
    while dataa != "Bye":

        username = input("Please enter username: \n")
        password = input("Please enter password: \n")
        # Implement code

        build_and_send_message(conn, PROTOCOL_CLIENT["singup_msg"], username + "#" + password)
        cmd, data = recv_message_and_parse(conn)
        if cmd == PROTOCOL_SERVER["singup_ok_msg"]:
            dataa = "Bye"
        print(data)

def logout(conn):
    # Implement code
    print(PROTOCOL_CLIENT["logout_msg"])
    build_and_send_message(conn, PROTOCOL_CLIENT["logout_msg"], "")
    conn.close()
    pass

def build_send_recv_parse(conn, cmd, data):

    build_and_send_message(conn , cmd, data)
    cmd ,data = recv_message_and_parse(conn)

    return cmd , data

    '''
    full_msg = conn.recv(1024).decode()
    cmd, data = parse_message(full_msg)
    print("[CLIENT]" +full_msg)
    if full_msg == None:
        conn.close()
    else:
        return cmd, data
    '''

def get_score(conn, cmd, data):
    cmd ,data = build_send_recv_parse(conn, cmd, data)
    if cmd == None:
        print("Error with the cmd")
    else:
        print("You have " + data + " scores")

def get_highscore(conn, cmd, data):
    cmd, data = build_send_recv_parse(conn,cmd,data)
    if cmd == None:
        print("Error with the cmd")
    else:
        print(data)

def get_logged_users(conn):
    cmd, data = build_send_recv_parse(conn, "LOGGED", "")
    print(data)

def main():
    # Implement code
    conn = connect()
    print("Concted to the server successfuly.")
    if input("Do you want to sing up?(y/n)") == "y":
        singup(conn)
    user = login(conn)
    print("Login successfuly.")
    choice = ""
    while choice != "q":
        print("s    Get my score")
        print("h    Get high score")
        print("l    Get logged users")
        print("q    Quit")
        print("Please enter your choice: ")
        choice = input()
        if choice == "s":
            get_score(conn, "MY_SCORE", user)
        elif choice == "h":
            get_highscore(conn, "HIGHSCORE", "")
        elif choice == "q":
            logout(conn)
        elif choice == "l":
            get_logged_users(conn)
        else:
            print("You need to choose one of them:")

    pass

if __name__ == '__main__':
    main()
