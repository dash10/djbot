from threading import Thread
from Queue import Queue, Empty

class NonBlockingStreamReader:

        def __init__(self, stream):
                '''
                stream: the stream to read from.
                        usually stdout or stderr
                '''

                self._s = stream
                self._q = Queue()

                def _populateQueue(stream, queue):
                        '''
                        Collect lines from 'stream' and put the in 'queue'
                        '''

                        while True:
                                line = stream.readline()
                                if line:
                                        queue.put(line)
                                else:
					# ordinarily this should error
                                        pass # we don't care if it cuts off

                self._t = Thread(target = _populateQueue,
                        args = (self._s, self._q))
                self._t.daemon = True
                self._t.start() # start collecting lines from stream

        def readline(self, timeout = None):
                try:
                        return self._q.get(block = timeout is not None,
                                timeout = timeout)
                except Empty:
                        return None
