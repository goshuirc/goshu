#!/usr/bin/env python3
#
# Copyright 2011 Daniel Oakley <danneh@danneh.net>
# Goshubot IRC Bot	-	http://danneh.net/goshu

from .libs import helper
import hashlib
import json

class Manager():
	"""Manages info/settings; to be subclassed."""
	
	name = 'Manager'
	
	def __init__(self, bot, path=None):
		self.bot = bot
		self.path = path
		self._store = {}
	
	def ret(paths, store=None):
		if store:
			value = store
		else:
			value = self._store
		paths = paths.split('.')
		for path in paths:
			value = value[path]
		return value
	
	def use_file(self, path, load=True, update=False):
		"""Sets the storage file to use."""
		self.path = path
		
		if load:
			try:
				self.load()
			except IOError:
				self.save()
		
		if update:
			self.update()
		
		self.save() # make sure we can save to the file
	
	def load(self, path=None):
		"""Load data file from `path`, or `self.path`."""
		if path:
			file = open(path, 'r')
			try:
				self._store = json.loads(file.read())
			except ValueError:
				self._store = {}
			file.close()
		elif self.path:
			file = open(self.path, 'r')
			try:
				self._store = json.loads(file.read())
			except ValueError:
				self._store = {}
			file.close()
		else:
			self._store = {}
			if self.bot.DEBUG:
				print(self.name+'.load : no path to load from')
	
	def save(self, path=None):
		"""Save `self.store` in file at `path`, or `self.path`."""
		if path:
			file = open(path, 'w')
			file.write(json.dumps(self._store, sort_keys=True, indent=4))
			file.close()
		elif self.path:
			file = open(self.path, 'w')
			file.write(json.dumps(self._store, sort_keys=True, indent=4))
			file.close()
		else:
			if self.bot.DEBUG:
				print(self.name+'.save : no path to save to')
	
	def update(self):
		"""Update the current data file, to be overwritten by subclass."""
		...
	
	def _encrypt(self, password):
		"""Returns hashed password."""
		return hashlib.sha512(password).hexdigest()


class Info(Manager):
	"""Manages goshubot IRC info."""
	
	name = 'Info'
	
	def update(self):
		"""Make sure servers are correct, etc."""
		old_store = self._store
		new_store = {}
		
		if len(old_store) < 1:
			self._update_server(new_store, None)
		
		for server in old_store:
			prompt = ' '
			prompt += server + ' '
			prompt += old_store[server]['connection']['address'] + ':'
			prompt += str(old_store[server]['connection']['port']) + ' '
			prompt += '- ok? [y]: '
			if helper.is_ok(prompt, True, True):
				new_store[server] = old_store[server]
			else:
				if self._update_server(old_store, server):
					new_store[server] = old_store[server]
		
		self._store = new_store
	
	def _update_server(self, store, server):
		if server:
			old_server = store[server]
			del store[server]
			if helper.is_ok(' delete server? [n]: ', False, True):
				return False
		else:
			old_server = {}
		new_server = {}
		
		if server:
			new_server_name = ''
			while new_server_name == '':
				try:
					new_server_name = helper.new_input(' server nickname[%s]: ' % server, False, False, True).split()[0].strip()
				except IndexError:
					new_server_name = ''
		else:
			new_server_name = ''
			while new_server_name == '':
				try:
					new_server_name = helper.new_input(' server nickname: ', False, False, True).split()[0].strip()
				except IndexError:
					new_server_name = ''
		
		new_server['connection'] = {}
		self._update_attribute(old_server, new_server, 'connection.address', 'server address')
		self._update_attribute(old_server, new_server, 'connection.ssl', 'ssl', truefalse=True)
		if new_server['connection']['ssl']:
			assumed_port = 6679
		else:
			assumed_port = 6667
		self._update_attribute(old_server, new_server, 'connection.port', 'port', old_value=assumed_port)
		self._update_attribute(old_server, new_server, 'nickserv_pass', 'nickserv password')
		
		store[new_server_name] = new_server
		
		return True
	
	def _update_attribute(self, old_server, new_server, attribute, display_name, old_value=None, truefalse=False):
		attribute = attribute.split('.')
		(paths, attribute_name) = (attribute[:-1], attribute[-1])
		
		if not old_value:
			try:
				old_path = old_server
				for path in paths:
					old_path = old_path[path]
				old_value = str(old_path[attribute_name])
			except KeyError:
				old_value = None
		
		
		if old_value != None:
			if truefalse:
				new_value = helper.is_ok('  %s [%s]' % (display_name, str(old_value)), old_value, True)
			else:
				new_value = helper.new_input('  %s [%s]: ' % (display_name, str(old_value)), False, False, True).strip()
			if new_value == '':
				new_value = old_value
		else:
			new_value = ''
			while new_value == '':
				try:
					if truefalse:
						new_value = helper.is_ok('  %s: ' % display_name, '', True)
					else:
						new_value = helper.new_input('  %s: ' % display_name, False, False, True).strip()
				except IndexError:
					new_value = ''
		
		new_path = new_server
		for path in paths:
			new_path = new_path[path]
		new_path[attribute_name] = new_value

class Settings(Manager):
	"""Manages goshubot settings."""
	
	name = 'Settings'
	
	def update(self):
		"""Update the current data file."""
		old_store = self._store
		new_store = {}
		
		new_store['nick'] = self._update_attribute('nick', old_store)
		new_store['passhash'] = self._update_attribute('passhash', old_store, password=True, display_name='password')
		new_store['prefix'] = self._update_attribute('prefix', old_store, display_name='bot command prefix')
		
		self._store = new_store
	
	def _update_attribute(self, name, store, password=False, display_name=None):
		"""Return updated single piece of data."""
		if not display_name:
			display_name = name
		if password:
			try:
				old_data = store[name]
				if password:
					new_data = helper.new_input(' %s [*****]: ' % display_name, newline=False, clearline=True, password=password).strip()
					if new_data != '':
						return self._encrypt(new_data.encode('utf8'))
					else:
						return old_data
			except KeyError:
				data = ''
				while data == '':
					data = helper.new_input(' %s: ' % display_name, newline=False, clearline=True, password=password).strip()
				return self._encrypt(data.split()[0].encode('utf8'))
			
		else:
			try:
				old_data = store[name]
				new_data = helper.new_input(' %s [%s]: ' % (display_name, old_data), newline=False, clearline=True).strip()
				if new_data != '':
					return new_data
				else:
					return old_data
			except KeyError:
				data = ''
				while data == '':
					data = helper.new_input(' %s: ' % display_name, newline=False, clearline=True).strip()
				return data.split()[0]