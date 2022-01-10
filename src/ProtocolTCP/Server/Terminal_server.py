import time
import traceback

from .Protocol_TCP_server import Protocol_TCP_server
from ..ProtocolTCP import Flag


class Terminal:
	def __init__(self, tcp: Protocol_TCP_server):
		self.tcp = tcp
		self.tcp.send_msg("pwd")
		msg = self.tcp.receive_msg()
		self.current_path = msg.strip()
		self.current_dirctory = self.current_path.split('/')[-1]
		while tcp.is_server_connected():
			try:
				command = input(f"{self.current_dirctory}$ ")
			except (EOFError, KeyboardInterrupt):
				print()
				command = "close"
			command_split = command.strip().split(' ')
			action = command_split[0].lower()
			args = command_split[1:]
			args_joined = " ".join(args)
			command = f"{action} {args_joined}"
			try:
				eval(f"self.{action}")(command)
			except (AttributeError, SyntaxError):
				print("Unknown command")
			except ParseError as error:
				print(f"Error in command {action}: {error}")
			except Exception:
				print("\n", traceback.format_exc())

	def put(self, args):
		args_split = args.split(' ')
		tmp = args_split[1:]
		file_name = " ".join(tmp)
		self.tcp.put_file(file_name, args, self.current_path)

	def get(self, args):
		self.tcp.get_file(args, self.current_path)

	def end(self, args):
		self.tcp.send_msg(args)
		time.sleep(1)
		self.tcp.disconnect_client()
		self.tcp.connect_client()

	def close(self, args):
		if self.tcp.is_client_connected():
			self.tcp.send_msg("END")
			self.tcp.disconnect_client()
		self.tcp.close_server()

	def ls(self, args):
		self.tcp.send_msg(args)
		print(self.tcp.receive_msg())

	def cd(self, args):
		if len(args) == 0:
			raise ParseError("No directory specified")
		self.tcp.send_msg(args)
		print(self.tcp.receive_msg())
		self.tcp.send_msg("pwd")
		msg = self.tcp.receive_msg()
		self.current_path = msg.strip()
		self.current_dirctory = self.current_path.split('/')[-1]

	def pwd(self, args):
		self.tcp.send_msg(args)
		print(self.tcp.receive_msg())


class ParseError(Exception):
	pass
