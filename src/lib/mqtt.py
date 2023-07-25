import machine
from ubinascii import hexlify
from drivers.mqtt import MQTTClient

def puback_cb(msg_id):
  print('PUBACK ID = %r' % msg_id)

def suback_cb(msg_id, qos):
  print('SUBACK ID = %r, Accepted QOS = %r' % (msg_id, qos))
  
def con_cb(connected):
  if connected:
    pass
    #client.subscribe('subscribe/topic')

def msg_cb(topic, pay):
  print('Received %s: %s' % (topic.decode("utf-8"), pay.decode("utf-8")))


class Mqtt():
    def __init__(self):

        # host,port,username and password of the mqtt broker

        self.hostname='cbb90cade46d4ff38fdf18a5dc12c4be.s2.eu.hivemq.cloud'
        self.port=8883 
        self.user="test1"
        self.password="TestPass"
        self.client_id = hexlify(machine.unique_id())
        self.client = None

    def connect(self):

        # load the private key for TLS aka mqtts
        with open('cert/key.der','rb') as f:
            key = f.read()
        # load the certificate for TLS aka mqtts
        with open('cert/cert.der','rb') as f:
            cert = f.read()

        ssl_params={
            "key": key, 
            "cert": cert, 
            "server_hostname":self._hostname
        }    

        self.client = MQTTClient(self.hostname, port=self.port, reconnect_retry_time=10, keep_alive=0 ,ssl=True, ssl_params=ssl_params )

        self.client.set_connected_callback(con_cb)
        self.client.set_puback_callback(puback_cb)
        self.client.set_suback_callback(suback_cb)
        self.client.set_message_callback(msg_cb)

        self.client.connect(self.client_id, user=self.user, password=self.password, clean_session=True, will_topic=None, will_qos=0, will_retain=False, will_payload=None)

