from django.conf import settings
import pika
import traceback
import logging
from collections import namedtuple
from django.db import transaction,  close_old_connections

# TODO: Figure out how to  flush_transaction

log = logging.getLogger('rooibos')

# transaction management changed in django 1.6
# see http://www.realpython.com/blog/python/transaction-management-with-django-1-6/
# and https://docs.djangoproject.com/en/1.6/topics/db/transactions/#id5
def flush_transaction():
    """
    Flush the current transaction so we don't read stale data

    Use in long running processes to make sure fresh data is read from
    the database.  This is a problem with MySQL and the default
    transaction mode.  You can fix it by setting
    "transaction-isolation = READ-COMMITTED" in my.cnf or by calling
    this function at the appropriate moment
    """
    transaction.set_autocommit(False)
    try:
        logging.info("Commiting Transaction")
        transaction.commit()
    except Exception as e:
        # database connection probably closed, open a new one
        logging.exception(e)
        logging.exception("Forcing connection close")
        # close_connection()
        close_old_connections()
    finally:
        transaction.set_autocommit(True)


workers = dict()


def register_worker(id):
    def register(worker):

        def wrapped_worker(*args, **kwargs):
            flush_transaction()
            try:
                return worker(*args, **kwargs)
            except:
                log.exception(traceback.format_exc())
                raise

        workers[id] = wrapped_worker
        log.debug('Registered worker %s' % id)
        return workers[id]
    return register


def discover_workers():
    if not '_discovered' in workers:
        for app in settings.INSTALLED_APPS:
            try:
                __import__(app + ".workers")
                print('Imported workers for %s' % app)
            except ImportError, ex:
                missed = True
                #print('No workers found for %s' % app)
                #print ex
        workers['_discovered'] = True


Job = namedtuple('Job', 'arg')


def execute_handler(handler, arg):
    try:
        handler(arg)
        return True
    except Exception:
        log.exception("Exception in job execution")
        return False


def worker_callback(ch, method, properties, body):
    print('worker_callback running')
    discover_workers()
    jobname, data = body.split()
    handler = workers.get(jobname)
    if not handler:
        log.error('Received job with unknown method %s. '
                     'Known workers are %s' % (jobname, workers.keys()))
        return
    print('Running job %s %s' % (jobname, data))
    try:
        # Classic mode with Job record identifier
        identifier = int(data)
        job = Job(arg=identifier)  # for backwards compatibility
        result = execute_handler(handler, job)
        log.debug('Job %s %s completed with result %s' %
                     (job, identifier, result))
    except ValueError:
        # New mode with all data included in call
        result = execute_handler(handler, data)

    ch.basic_ack(delivery_tag=method.delivery_tag)


def run_worker(worker, arg, **kwargs):
    # TODO: Is flush transaction necessary here? Is it still needed? (if not, why not?)
    # flush_transaction()
    discover_workers()
    print("Running worker %s with arg %s" % (worker, arg))

    connection = pika.BlockingConnection(pika.ConnectionParameters(
        **getattr(settings, 'RABBITMQ_OPTIONS', dict(host='localhost'))))
    channel = connection.channel()
    channel.confirm_delivery()
    queue_name = 'rooibos-%s-jobs' % (
        getattr(settings, 'INSTANCE_NAME', 'default'))
    channel.queue_declare(queue=queue_name, durable=True)
    print('Sending message to worker process: %s' % queue_name)
    try:
        channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            body='%s %s' % (worker, arg),
            properties=pika.BasicProperties(
                delivery_mode=2,  # make message persistent
            )
        )
    except Exception:
        print('Could not publish message %s %s' % (worker, arg))
    connection.close()
