class Register:
    def __init__(self, name):
        self.value = None
        self.name = name

    def __str__(self):
        return "{}({})".format(self.name, self.value)


eax = Register('eax')
ebx = Register('ebx')
ecx = Register('ecx')
edx = Register('edx')


WRITE = 4
READ = 3
STDOUT = 1

SYSCALL32 = 0x80


def ADD(adr_1, adr_2):
    adr_2.value = adr_1.value + adr_2.value


def MOV(adr_1, adr_2):
    adr_2.value = adr_1


def INT(call):
    if call != 0x80:
        return
    if eax.value == 3 and ebx.value == 1:
        print(str(ecx.value)[:edx.value])


if __name__ == '__main__':
    script = ["MOV(5, ecx)",
              "MOV(6, edx)",
              "ADD(edx, ecx)",
              "MOV(READ, eax)",
              "MOV(STDOUT, ebx)",
              "MOV(2, edx)",
              "INT(SYSCALL32)"]

    for line in script:
        eval(line)
