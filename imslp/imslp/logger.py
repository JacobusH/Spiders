class Logger(object):

    def __init__(self):
        now = datetime.datetime.now()
        self.leDate = now.strftime("%Y-%m-%d %H")

    def LogToFile(self, toWrite):
        filename = "LogFile_%s.txt" % self.leDate
        fh = open(filename, "a")
        fh.write(toWrite + '\n')
        fh.close