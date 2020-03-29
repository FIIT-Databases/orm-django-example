from logging import FileHandler


class Utf8FileHandler(FileHandler):

    def emit(self, record):
        msg = self.format(record)
        stream = self.stream

        try:
            stream.write(msg)
            stream.write(self.terminator)
            self.flush()
        except Exception:
            try:
                stream.write(str(msg.encode('utf-8'))[2:-1])
                stream.write(self.terminator)
                self.flush()
            except Exception:
                self.handleError(record)
