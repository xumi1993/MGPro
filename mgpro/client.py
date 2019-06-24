from cmd import Cmd
import readline
import sys
import mgpro
import glob


def complete(text, state):
    return (glob.glob(text+'*')+[None])[state]


class Client(Cmd):
    def __init__(self):
        Cmd.__init__(self)
        self.prompt = 'MGPro>'
        self.aliases = {'c': self.do_continuation,
                        'g': self.do_gradient,
                        'q': self.do_quit,
                        'r': self.do_read,
                        'w': self.do_write,
                        'z': self.do_dt2za,
                        'h': self.do_help}
        self.result = None

    def do_quit(self, arg):
        'Close MGPro'
        print('Bye...')
        sys.exit(0)

    def do_read(self, arg):
        '''
read (r): read a raw data file with 3 columns (x, y, value)

Syntax: read filename dx dy [\'geo\']
    filename: Path to the raw data file
    dx: sampling interval along x directory in meter
    dy: sampling interval along y directory in meter
    geo: Specify this keyword to convert spherical coordinate to geo coordinate
        '''
        arg_lst = arg.split()
        if len(arg_lst) < 3:
            print('Error: Not enough arguments')
            return
        elif len(arg_lst) == 3:
            filename = arg_lst[0]
            dx = float(arg_lst[1])
            dy = float(arg_lst[2])
            to_geo = False
        elif len(arg_lst) == 4:
            if arg_lst[4] == 'geo':
                to_geo = True
            else:
                print('Error: Specify \'geo\' to convert spherical coordinate to geo coordinate')
                return
        # elif 3 < len(arg_lst) < 7:
        #     print('The region must be in 4 args')
        #     return
        # elif len(arg_lst) == 7:
        #     filename = arg_lst[0]
        #     dx = float(arg_lst[1])
        #     dy = float(arg_lst[2])
        #     xy_limit = [float(pos) for pos in arg_lst[3:]]
        else:
            print('Error: Too many argumenrs')
            return
        self.mg = mgpro.mgmat(filename, dx, dy, to_geo)

    def do_continuation(self, arg):
        '''
continuation (c): Calculate continuation and derivative for the data read

Syntax: continuation h order
    h: continuation in h km
    order: derivative order
        '''
        if len(arg.split()) != 2:
            print('Error: Two arguments required')
            return
        h, order = [float(value) for value in arg.split()]
        self.result = self.mg.continuation(h, order)

    def do_gradient(self, arg):
        '''
gradient (g): Calculare horizontal gradient or the module

Syntax: gradient option
    option: Specify the parameter in [0|45|90|135|mod], which represent the \
horizontal gradient in azimuth of 0, 45, 90 or 135 or module of horizontal gradient
        '''
        if len(arg.split()) != 1:
            print('Error: Too many arguments')
            return
        elif arg not in ['0', '90', '45', '135', 'mod']:
            print('Error: Degree or module must be in 0, 45, 90, 135 and \'mod\'')
            return
        self.result = self.mg.gradient(arg)

    def do_dt2za(self, arg):
        if len(arg.split()) != 2:
            i0, d0 = [float(value) for value in arg.split()]
            self.result = self.mg.dt2za(i0, d0)

    def do_write(self, arg):
        '''
write (w): Write any result to a txt file

Syntax: write filename [\'lalo\']
    filename: path to txt file you want to write
    lalo: Specify the keyword to convert geo coordinate to spherical coordinate'
        '''
        if self.result is None:
            print('Error: No result in the memery')
            return
        if len(arg.split()) > 2:
            print('Error: Too many arguments')
        elif len(arg.split()) == 1:
            filename = arg
            to_latlon = False
        elif len(arg.split()) == 2:
            filename = arg.split()[0]
            if arg.split()[1] == 'lalo':
                to_latlon = True
            else:
                print('Error: Specify \'lalo\' to convert geo coordinate to spherical coordinate')
        try:
            self.mg.savetxt(filename, self.result, to_latlon)
        except Exception as e:
            print('{}'.format(e))
            return

    def completedefault(self, *args):
        readline.set_completer_delims(' \t\n;')
        readline.parse_and_bind("tab: complete")
        readline.set_completer(complete)

    def default(self, line):
        cmd, arg, line = self.parseline(line)
        if cmd in self.aliases:
            self.aliases[cmd](arg)
        else:
            print('Command not found')


if __name__ == "__main__":
    Client().cmdloop()