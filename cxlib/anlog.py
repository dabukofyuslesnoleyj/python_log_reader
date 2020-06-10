import os
import json
import datetime
import glob

class Anlog:
    def __init__(self, level, cate, dt, msg):
        self.level = level
        self.cate = cate
        self.dt = dt
        self.msg = msg
        self.data_log = (msg.startswith('@') or msg.startswith('#'))
        self._data = None
        self._data_msg = None
        self._tags = None

    def data(self):
        if self.data_log and self._data == None:
            if self._data_msg == None:
                self._parse_data_and_tags()
            self._data = json.loads(self._data_msg)

        return self._data

    def tags(self):
        if self.data_log and self._tags == None:
            self._parse_data_and_tags()
            
        return self._tags

    def _parse_data_and_tags(self):
        if self.data_log:
            entries = self.msg.split('#json', 1)
            text = entries[0]
            if text.startswith('@'):
                self._tags = text[1:].split(';')
            else:
                self._tags = []

            self._data_msg = entries[1].strip()

    def __str__(self):
        return ','.join([self.level, self.cate, self.dt.strftime('%Y-%m-%d %H:%M:%S'), self.msg])

    @staticmethod
    def parse_time(text):
        # Use self crafted code to parse time to improve performance.

        # TODO: supports time zone
        e = text.split(' ')
        dd = e[0].split('-')
        tt = e[1].split(':', 2)

        return datetime.datetime(
            int(dd[0]),
            int(dd[1]),
            int(dd[2]),
            int(tt[0]),
            int(tt[1]),
            int(tt[2][0:2]),
            int(tt[2][3:6])*1000)

    @staticmethod
    def parse_log(line, skipError=True):
        # TODO: supprots sub_tags
        line = line.strip()
        items = line.split(',', 3)

        try:
            level = items[0]
            cate = items[1]
            dt = Anlog.parse_time(items[2])
            msg = items[3]

            return Anlog(level, cate, dt, msg)
        except Exception as e:
            if not skipError:
                return Anlog(level, cate, dt, msg)
            else:
                print('ERROR: ' + str(e) + '\nlog msg: ' + line)
                return Anlog('ERROR', 'LogDataParseError', datetime.datetime.now(), str(e) + '; log msg: ' + line)

    @staticmethod
    def parse_point(text):
        """
        PointD(X: <x>, Y: <y>)
        """
        obj = Anlog.parse_object(text)
        if obj['__type__'] == 'PointD':
            return float(obj['X']), float(obj['Y'])
        else:
            return 0, 0

    @staticmethod
    def parse_object(text):
        li = text.find('(')
        ri = text.rfind(')')

        type_name = text[:li]
        entries = text[li+1:ri].split(',')

        d = dict()
        for e in entries:
            kv = e.split(':')
            if len(kv) > 0:
                d[kv[0].strip()] = kv[1].strip()

        d['__type__'] = type_name

        return d

    @staticmethod
    def get_paths(glob_pattern, sorting = True):
        paths = glob.glob(glob_pattern)
        if sorting:
            Anlog._sort_paths(paths)
        return paths

    @staticmethod
    def read_all_lines(glob_pattern):
        for p in Anlog.get_paths(glob_pattern):
            if not os.path.isfile(p):
                continue

            with open(p, 'r', encoding = 'utf8') as fp:
                for line in fp.readlines():
                    yield line

    @staticmethod
    def read_all_logs(glob_pattern):
        lines = Anlog.read_all_lines(glob_pattern)
        for line in lines:
            yield Anlog.parse_log(line)

    @staticmethod
    def _sort_paths(paths):
        # A tricky extract log timestamp and supports no-stamp log.
        def _key(v):
            if len(v) > 15:
                return v[-15:]
            else:
                return '999999999999999'

        paths.sort(key = _key)

    @staticmethod
    def get_paths_with_dt(glob_pattern, stdt, endt):
        """
        v2k.log
        v2k.log.YYYYmmddHHMMSSf
        """
        paths = Anlog.get_paths(glob_pattern)
        keep = ''
        tail = datetime.datetime(1911, 1, 1, 0, 0)
        lists = []
        mfn, mfext = os.path.splitext(os.path.basename(max(paths)))
        mFullFn = mfn + mfext
        if len(mFullFn.split('.')) == 3:
            tail = datetime.datetime.strptime(mFullFn.split('.')[2], '%Y%m%d%H%M%S%f')
            tail = datetime.datetime(tail.year, tail.month, tail.day, tail.hour)
        for p in paths:
            fn, fext = os.path.splitext(os.path.basename(p))
            fullFn = fn + fext 
            name = fullFn.split('.')
            if len(name) == 2:
                keep = p
                continue
            t = datetime.datetime.strptime(name[2], '%Y%m%d%H%M%S%f')
            t = datetime.datetime(t.year, t.month, t.day, t.hour)
            if t >= stdt and t <= endt:
                lists.append(p)
                
        if keep != '' and (lists.count == 0 or tail <= endt):   
            lists.append(keep)

        return lists

    @staticmethod
    def read_dt_range_lines(glob_pattern, stdt, endt):
        for p in Anlog.get_paths_with_dt(glob_pattern, stdt, endt):
            if not os.path.isfile(p):
                continue

            with open(p, 'r', encoding = 'utf8') as fp:
                for line in fp.readlines():
                    yield line

    @staticmethod
    def read_dt_range_logs(glob_pattern, stdt, endt):
        lines = Anlog.read_dt_range_lines(glob_pattern, stdt, endt)
        for line in lines:
            yield Anlog.parse_log(line)

class LineCounter:
    def __init__(self):
        self.count = 0

    def counter(self, line):
        self.count = self.count + 1
        if self.count % 10000 == 0:
            print(self.count)
        return line

    @staticmethod
    def new():
        lt = LineCounter()
        return lt.counter

def example1():
    start = datetime.datetime.now()
    count = 0
    for line in Anlog.read_all_lines("logs/v2k.log*"):
        l = Anlog.parse_log(line)
        count = count + 1
        if l.data_log:
            print(l.tags())
            print(l.data())
    print((datetime.datetime.now() - start))
    print(count)

def example2():
    logs = Anlog.read_all_logs("logs/v2k.log*")

    dt = datetime.datetime.now()
    dt = dt - datetime.timedelta(days=50)
    #start = datetime.datetime.now()
    #end = datetime.datetime.now()

    logs = filter(LineCounter.new(), logs)
    #logs = filter(lambda l: l.dt > dt, logs)
    # logs = filter(lambda l: l.dt > start and l.dt < end, logs)
    logs = filter(lambda l: l.cate == 'AdjustmentRecognizer', logs)
    logs = filter(lambda l: l.data_log, logs)

    for log in logs:
        data = log.data()
        #print(log.data()['capture_image_uid'])

# example2()