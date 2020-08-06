import nsq


def handle(msg):
    print(msg)
    print(msg.body)
    return True


r = nsq.Reader(message_handler=handle, nsqd_tcp_addresses=['10.2.176.245:4150'], topic="my_topic", channel="my_channel",
               lookupd_poll_interval=15)

nsq.run()
