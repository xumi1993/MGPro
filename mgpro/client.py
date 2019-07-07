from cmd import Cmd
import readline
import sys
from mgpro import mgpro
import glob
import subprocess


def complete(text, state):
    return (glob.glob(text+'*')+[None])[state]


class Client(Cmd):
    def __init__(self):
        Cmd.__init__(self)
        self.prompt = 'MGPro>'
        self.aliases = {'c': self.do_continuation,
                        'g': self.do_gradient,
                        'p': self.do_plot,
                        'q': self.do_quit,
                        'r': self.do_read,
                        'w': self.do_write,
                        'x': self.do_dt2xa,
                        'y': self.do_dt2ya,
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
            if arg_lst[3] == 'geo':
                filename = arg_lst[0]
                dx = float(arg_lst[1])
                dy = float(arg_lst[2])
                to_geo = True
            else:
                print('Error: Specify \'geo\' to convert spherical coordinate to geo coordinate')
                return
        else:
            print('Error: Too many argumenrs')
            return
        try:
            self.mg = mgpro.mgmat(filename, dx, dy, to_geo=to_geo)
        except Exception as e:
            print('Error: Cannot read {}\n{}'.format(filename, e))

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
gradient (g): Calculare horizontal gradient or the module.
    NOTE: The unit of the input must be meter. The unit of the output has converted to km.

Syntax: gradient option
    option: Specify the parameter in [0|45|90|135|mod], which represent the \
horizontal gradient in azimuth of 0, 45, 90 or 135 or module of horizontal gradient
        '''
        if len(arg.split()) != 1:
            print('Error: Only 1 argument required, but {} arguments got'.format(arg.split()))
            return
        elif arg not in ['0', '90', '45', '135', 'mod']:
            print('Error: Degree or module must be in 0, 45, 90, 135 and \'mod\'')
            return
        self.result = self.mg.gradient(arg)

    def do_dt2za(self, arg):
        '''
dt2za (z): Vertical magnetization

Syntax: dt2za i0 d0 ['mem']
    i0: Magnetic dip of the region
    d0: Magnetic declination of the region
    mem: Switch for saving Za to memory and replacing the data read before
        '''
        if len(arg.split()) == 2:
            i0, d0 = [float(value) for value in arg.split()]
            self.result = self.mg.dt2za(i0, d0)
        elif len(arg.split()) == 3:
            if arg.split()[2].lower() == 'mem':
                i0, d0 = [float(value) for value in arg.split()[0:2]]
                self.result = self.mg.dt2za(i0, d0, replace=True)
            else:
                print('Error: \'mem\' should be specified to save Za to memory')
                return
        else:
            print('Two or three argumrnts required')

    def do_dt2xa(self, arg):
        '''
dt2xa (x): Horizontal magnetization along x direction

Syntax: dt2xa i0 d0 ['mem']
    i0: Magnetic dip of the region
    d0: Magnetic declination of the region
    mem: Switch for saving Xa to memory and replacing the data read before
        '''
        if len(arg.split()) == 2:
            i0, d0 = [float(value) for value in arg.split()]
            self.result = self.mg.dt2xa(i0, d0)
        elif len(arg.split()) == 3:
            if arg.split()[2].lower() == 'mem':
                i0, d0 = [float(value) for value in arg.split()[0:2]]
                self.result = self.mg.dt2xa(i0, d0, replace=True)
            else:
                print('Error: \'mem\' should be specified to save Xa to memory')
                return
        else:
            print('Two or three argumrnts required')

    def do_dt2ya(self, arg):
        '''
dt2xa (y): Horizontal magnetization along y direction

Syntax: dt2ya i0 d0 ['mem']
    i0: Magnetic dip of the region
    d0: Magnetic declination of the region
    mem: Switch for saving Ya to memory and replacing the data read before
        '''
        if len(arg.split()) == 2:
            i0, d0 = [float(value) for value in arg.split()]
            self.result = self.mg.dt2ya(i0, d0)
        elif len(arg.split()) == 3:
            if arg.split()[2].lower() == 'mem':
                i0, d0 = [float(value) for value in arg.split()[0:2]]
                self.result = self.mg.dt2ya(i0, d0, replace=True)
            else:
                print('Error: \'mem\' should be specified to save Ya to memory')
                return
        else:
            print('Two argumrnts required')

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

    def do_plot(self, arg):
        '''
plot (p): Preview the result.

Syntax: plot [data|result]
    Specify 'data' or 'result' to draw map view of the raw data or the result (default)
        ''' 
        if arg.lower() == 'data':
            self.mg.pltmap(self.mg.data_expand[self.mg.row_begin: self.mg.row_end + 1, self.mg.col_begin: self.mg.col_end + 1])
        elif  arg.lower() == 'result' or arg == '':
            self.mg.pltmap(self.result)
        else:
            print('Error: argument should be in \'data\' and \'result\'')

    def completedefault(self, *args):
        readline.set_completer_delims(' \t\n;')
        readline.parse_and_bind("tab: complete")
        readline.set_completer(complete)

    def default(self, line):
        cmd, arg, line = self.parseline(line)
        if cmd in self.aliases:
            self.aliases[cmd](arg)
        else:
            try:
                subprocess.call(line, shell=True)
            except:
                print('Command not found')


def main():
    Client().cmdloop()


if __name__ == "__main__":
    main()
