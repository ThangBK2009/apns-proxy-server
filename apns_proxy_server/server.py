# -*- coding: utf-8 -*-
"""
APNs Proxy Server

メッセージングにはZeroMQを使っている、メッセージフレームの構造は次の通り
------------------------------------------------------------------
| Command(1) | Application ID(2) | Device Token(64) | Message(n) |
------------------------------------------------------------------
括弧内は長さ
"""

import logging
import traceback
import threading
from Queue import Queue

import zmq

import settings
from . import worker

COMMAND_LENGTH = 1
APPLICATION_ID_LENGTH = 2
DEVICE_TOKEN_LENGTH = 64

COMMAND_PING = b'1'
COMMAND_TOKEN = b'2'
COMMAND_END = b'3'

task_queues = {}


def start(address):
    context = zmq.Context()
    server = context.socket(zmq.REP)
    server.bind(address)
    try:
        while 1:
            message = server.recv()
            command = message[:COMMAND_LENGTH]
            if command == COMMAND_TOKEN:
                dispatch(message)
            elif command == COMMAND_PING:
                server.send(b"OK")
            elif command == COMMAND_END:
                server.send(b"OK")
            else:
                logging.warn("UNKNOWN COMMAND Received:%s" % command)
    except Exception, e:
        logging.error(e)
        logging.error(traceback.format_exc())
    finally:
        server.close()
        context.term()


def parse_message(message):
    """
    データフレームから各値を取り出す
    """
    pos = COMMAND_LENGTH
    application_id = message[pos:pos+APPLICATION_ID_LENGTH]

    pos += APPLICATION_ID_LENGTH
    token = message[pos:pos+DEVICE_TOKEN_LENGTH]

    pos += DEVICE_TOKEN_LENGTH
    message = message[pos:]
    return (application_id, token, message)


def dispatch(message):
    """
    Queue経由でワーカースレッドにメッセージを渡す
    """
    application_id, token, message = parse_message(message)
    if not application_id in task_queues:
        try:
            q = Queue()
            create_worker(application_id, q)
            task_queues[application_id] = q
        except ValueError, ve:
            logging.error(ve)
            return

    logging.debug("Dispatch to worker for application_id: %s" % application_id)
    task_queues[application_id].put({
        "message": message,
        "token": token
    })


def create_worker(application_id, task_queue):
    logging.info("Create worker for: %s" % application_id)
    app = get_application_config(application_id)
    for i in xrange(settings.THREAD_NUMS_PER_APPLICATION):
        thread_name = "SendWorker:%s_%i" % (app.get('name'), i)
        thread = threading.Thread(target=worker.send_worker, name=thread_name, args=(
            task_queue,
            application_id,
            app.get('sandbox'),
            app.get('cert_file'),
            app.get('key_file')
        ))
        thread.start()


def get_application_config(application_id):
    for app in settings.APPLICATIONS:
       if app.get('application_id') == application_id:
           return app
    raise ValueError('Unknown application_id given. (%s)' % application_id)