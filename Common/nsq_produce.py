import nsq
import tornado.ioloop
import time


class nsq_tcp_client:
    def __init__(self, nsqd_tcp_addresses='10.2.176.245:4150'):
        self.writer = nsq.Writer(nsqd_tcp_addresses=nsqd_tcp_addresses)

    def finish_pub(self, conn, data):
        print(data)

    def pub_message(self):
        self.writer.pub('my_topic', time.strftime('%H:%M:%S').encode("utf-8"), self.finish_pub)

    def nsq_run(self):
        tornado.ioloop.PeriodicCallback(callback=self.pub_message, callback_time=1000).start()
        nsq.run()


# # writer = nsq.Writer(nsqd_tcp_addresses='10.2.176.245:4150')
# writer = nsq.Writer(nsqd_tcp_addresses='10.2.176.245:4150')
# tornado.ioloop.PeriodicCallback(callback=pub_message, callback_time=1000).start()
# tip.start()
# nsq.run()

if __name__ == '__main__':
    nsq_tcp_client().nsq_run()
