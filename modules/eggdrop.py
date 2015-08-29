#!/usr/bin/env python3
# Goshu IRC Bot
# written by Daniel Oaks <daniel@danieloaks.net>
# licensed under the ISC license

import os

from gbot.modules import Module
from gbot.libs.helper import filename_escape
import sqlite3
import base64

CREATE_TABLE_SQL = '''
CREATE TABLE questions (id INTEGER PRIMARY KEY AUTOINCREMENT, question TEXT, answer TEXT, requested TEXT, approved INTEGER)
'''


class eggdrop(Module):
    """Allows for an eggdrop-like response to questions made to goshu."""

    def __init__(self, bot):
        Module.__init__(self, bot)

        db_file = '{}{}sqlite'.format(filename_escape(self.name), os.extsep)
        self.db_path = os.path.join('config', 'modules', db_file)

        db_dir = self.db_path.rsplit(os.sep, 1)[0]
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)

        if not os.path.exists(self.db_path):
            conn = sqlite3.connect(self.db_path)

            c = conn.cursor()

            # Create table
            c.execute(CREATE_TABLE_SQL)

            conn.commit()
            c.close()

    def cmd_egg(self, event, command, usercommand):
        """Eggdrop!

        @usage [-section] <suggestion>
        @view_level admin
        """
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
            safe_host = base64.b64encode(event['source'].host).decode()

            safe_approved = '0'
            useraccount = self.bot.accounts.account(event['server'], event['source'])
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

    def eggdrop_listener(self, event):
        """Responds to Eggdrop messages

        @listen in privmsg
        @listen in pubmsg
        """
        try:
            if event['message'].split()[0].startswith(event['server'].nick):
                asked = True
            else:
                return
        except IndexError:
            return
        if asked:
            if len(event['message'].split()) < 2:
                return

            asked_question = event['message'].split(' ', 1)[1].strip().lower()
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

                event['from_to'].msg(safe_answer)
