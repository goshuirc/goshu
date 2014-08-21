#!/usr/bin/env python3
# Goshubot IRC Bot
# written by Daniel Oaks <daniel@danieloaks.net>
# licensed under the BSD 2-clause license

import os

from gbot.modules import Module
from gbot.libs.helper import filename_escape
import sqlite3
import base64


class eggdrop(Module):

    def __init__(self):
        Module.__init__(self)
        self.events = {
            'commands': {
                'egg': [self.cmd_handler, '[-section] <suggestion> --- eggdrop'],
            },
            'in': {
                'pubmsg': [(0, self.msg_handler)],
                'privmsg': [(0, self.msg_handler)],
            },
        }

        self.db_path = 'config'+os.sep+'modules'+os.sep+filename_escape(self.name)+os.extsep+'sqlite'

        db_dir = self.db_path.rsplit(os.sep, 1)[0]
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)

        if not os.path.exists(self.db_path):
            conn = sqlite3.connect(self.db_path)

            c = conn.cursor()

            # Create table
            c.execute('create table questions (id integer primary key autoincrement, question text, answer text, requested text, approved integer)')

            conn.commit()
            c.close()

    def cmd_handler(self, event, command, usercommand):
        if len(usercommand.arguments.split()) < 1:
            return

        egg_command = usercommand.arguments.split()[0]

        if egg_command == 'add':
            if len(usercommand.arguments.split()) < 2:
                return

            qa_string = usercommand.arguments.split(' ', 1)[1]

            if len(qa_string.split('|')) < 2:
                return

            question, qa_string = qa_string.split('|', 1)
            question = question.strip().lower()

            if len(qa_string.split('|')) > 1:
                answer, qa_string = qa_string.split('|', 1)
            else:
                answer = qa_string
            answer = answer.strip()

            # database safe
            safe_question = base64.b64encode(question.encode()).decode()
            safe_answer = base64.b64encode(answer.encode()).decode()
            safe_host = base64.b64encode(event.source.encode()).decode()

            safe_approved = "0"
            useraccount = self.bot.accounts.account(event.source, event.server)
            if useraccount:
                accesslevel = self.bot.accounts.access_level(useraccount)
                if accesslevel > 4:
                    safe_approved = str(accesslevel)

            # putting values into db
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()

            query = 'insert into questions (question, answer, requested, approved) '

            query += 'values ("'
            query += safe_question
            query += '", "'
            query += safe_answer
            query += '", "'
            query += safe_host
            query += '", '
            query += safe_approved
            query += ')'

            c.execute(query)

            conn.commit()
            c.close()

    def msg_handler(self, event):
        try:
            if self.bot.irc.servers[event.server].info['connection']['nick'] in event.arguments[0].split()[0]:
                asked = True
            else:
                return
        except IndexError:
            return
        if asked:
            if len(event.arguments[0].split()) < 2:
                return

            asked_question = event.arguments[0].split(' ', 1)[1].strip().lower()
            safe_asked_question = base64.b64encode(asked_question.encode()).decode()

            # grab values from db
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()

            query = 'select answer, approved from questions '
            query += 'where question like "'
            query += safe_asked_question
            query += '"'

            c.execute(query)

            answer = None

            while not answer:
                response = c.fetchone()
                if not response:
                    break
                if int(response[1]) > 0:
                    answer = response[0]

            conn.commit()
            c.close()

            if answer:
                safe_answer = base64.b64decode(answer.encode()).decode()

                self.bot.irc.msg(event, safe_answer, 'public')
