def dump(kcode):
	offset = 6
	for i in range(0, len(kcode.opname)):
		macro = ''
		macro += '#define '
		macro += kcode.name
		macro += '_'
		macro += kcode.opname[i]
		macro += '('
		macro += 'op'
		macro += ')   '
		macro += 'MASK('
		macro += 'op'
		macro += ', '
		macro += str(offset)
		offset += kcode.opsize[i]
		macro += ', '
		macro += str(kcode.opsize[i])
		macro += ')'
		print macro
def encode(kcode):
	offset = 6
	macro = 'int '
	macro += kcode.name
	macro += '(op'
	for i in range(0, len(kcode.opname)):
		macro += ', '
		macro += kcode.opname[i]
	macro += ') { \n   int opcode = ( '
	macro += '(op << '
	macro += str(offset)
	macro += ')'
	for i in range(0, len(kcode.opname)):
		macro += ' | (' 
		macro += kcode.opname[i]
		macro += ' << '
		offset += kcode.opsize[i]
		macro += str(offset)
		macro += ')'
	macro += ' );\n   return opcode;\n }'	
	print macro
	print ''
class KCODE:
	def __init__(self, opcode, line):     #constructer
		self.tokens = line.split()
		self.name = self.tokens[0].replace('@', '').split(':')[0]
		self.NAME = self.name.upper()
		self.opname = []                #declaration opname array
		self.optype = []                #declaration optype array
		self.opsize = []                #declaration opsize array
		self.opcode = opcode
		self.OPCODE = 'OPCODE_%s' % self.name
		self.OPLABEL = 'L_%s' %self.name
		self.ifdef = 'CASE'
		self.size = '%d' % len(self.tokens[1:])
		for a in self.tokens[1:]:
			if a.startswith('#') :
				self.ifdef = a[1:]
				self.size = '%d' % len(self.tokens[1:]) - 1
				continue
			if len(a.split(':')) == 1: print line
			t = a.split(':')
			self.opname.append(t[0])
			self.optype.append(t[1])
			self.opsize.append(int(t[2]))


KCODE_LIST = []

c = 0
for line in open('genvmrobo.txt', 'r'):
	if line.startswith('#') or len(line) == 0: continue
	if len(line.split()) > 1:
		kc = KCODE(c ,line)
		KCODE_LIST.append(kc)
		c += 1
print '#define MASK(op, x, y) ((op >> x) & ((1 << y)-1))'
print ''
for kcode in KCODE_LIST:
	dump(kcode)
	encode(kcode)
