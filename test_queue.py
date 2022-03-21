import os , sys

from kombu import Connection,Exchange, Queue,Producer

sys.path.append("/apps/djezzy/interfaces/control")

os.environ["DJANGO_SETTINGS_MODULE"] = "interfaces.control.settings"


from django.conf import settings

from django.conf import global_settings


conn=Connection([
              # 'amqp://epramxx:Monday1@mqueue1:5672//'
              "amqp://{}:{}@{host}/".format(
                  *settings.MQ_USER_PASSWORD,
                  host=settings.MQ_HOST_CLUSTER[0],
                  ssl=settings.MQ_SSL)
               for host in settings.MQ_HOST_CLUSTER
              ])

channel = conn.channel()

exchange = Exchange("test-exchange", type="direct")

producer = Producer(exchange=exchange, channel=channel, routing_key="test-key")

queue = Queue(name="test-queue", exchange=exchange, routing_key="test-key")

queue.maybe_bind(conn)

queue.declare()

producer.publish("This is test message")
print ("--------------- finish ---------------")

