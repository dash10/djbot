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

			# filter time remaining
                        while True:
                                line = stream.readline()
                                if line:
					if line.find('#') == -1:
                                        	queue.put(line)
                                else:
					break

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
