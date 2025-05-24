import argparse
import json
import os
import re
import time
from curses import wrapper

# arsenal
from . import __version__
from .modules import config
from .modules import cheat
from .modules import check
from .modules import gui as arsenal_gui


class App:

    def __init__(self):
        pass

    def get_args(self):
        examples = '''examples:
        arsenal-tmux                 # default (tmux required)
        arsenal-tmux 1               # send to tmux pane 1
        arsenal-tmux --copy
        arsenal-tmux --print
        arsenal-tmux --exec
        '''

        parser = argparse.ArgumentParser(
            prog="arsenal-tmux",
            description='arsenal-tmux v{} - Pentest command launcher'.format(__version__),
            epilog=examples,
            formatter_class=argparse.RawTextHelpFormatter
        )

        parser.add_argument(
            'pane_index', nargs='?', type=int, default=None,
            help='Optional tmux pane index to send command to')

        group_out = parser.add_argument_group('output [default = prefill]')
        group_out.add_argument('-p', '--print', action='store_true', help='Print the result')
        group_out.add_argument('-o', '--outfile', action='store', help='Output to file')
        group_out.add_argument('-x', '--copy', action='store_true', help='Output to clipboard')
        group_out.add_argument('-e', '--exec', action='store_true', help='Execute cmd')
        group_out.add_argument('-c', '--check', action='store_true', help='Check the existing commands')
        group_out.add_argument('-f', '--prefix', action='store_true', help='command prefix')
        group_out.add_argument('--no-tags', action='store_false', help='Whether or not to show the tags when drawing the cheats')
        parser.add_argument('-V', '--version', action='version', version='%(prog)s (version {})'.format(__version__))

        return parser.parse_args()

    def run(self):

        if 'TMUX' not in os.environ:
            print("Arsenal-TMUX: This tool only works inside a tmux session.")
            exit(1)

        args = self.get_args()

        # load cheatsheets
        cheatsheets = cheat.Cheats().read_files(config.CHEATS_PATHS, config.FORMATS,
                                                config.EXCLUDE_LIST)

        if args.check:
            check.check(cheatsheets)
        else:
            self.start(args, cheatsheets)

    def start(self, args, cheatsheets):
        arsenal_gui.Gui.with_tags = args.no_tags

        # create gui object
        gui = arsenal_gui.Gui()
        while True:
            # launch gui
            cmd = gui.run(cheatsheets, args.prefix)

            if cmd == None:
                exit(0)

            # Internal CMD
            elif cmd.cmdline[0] == '>':
                if cmd.cmdline == ">exit":
                    break
                elif cmd.cmdline == ">show":
                    if (os.path.exists(config.savevarfile)):
                        with open(config.savevarfile, 'r') as f:
                            arsenalGlobalVars = json.load(f)
                            for k, v in arsenalGlobalVars.items():
                                print(k + "=" + v)
                    break
                elif cmd.cmdline == ">clear":
                    with open(config.savevarfile, "w") as f:
                        f.write(json.dumps({}))
                    self.run()
                elif re.match(r"^\>set( [^= ]+=[^= ]+)+$", cmd.cmdline):
                    # Load previous global var
                    arsenalGlobalVars = load_globals()
                    # Add new glovar var
                    varlist = re.findall("([^= ]+)=([^= ]+)", cmd.cmdline)
                    for v in varlist:
                        arsenalGlobalVars[v[0]] = v[1]
                    save_globals(arsenalGlobalVars)
                    continue
                else:
                    break

            # OPT: Copy CMD to clipboard
            elif args.copy:
                try:
                    import pyperclip
                    pyperclip.copy(cmd.cmdline)
                except ImportError:
                    pass
                break

            # OPT: Only print CMD
            elif args.print:
                print(cmd.cmdline)
                break

            # OPT: Write in file
            elif args.outfile:
                with open(args.outfile, 'w') as f:
                    f.write(cmd.cmdline)
                break

            try:
                import libtmux
                server = libtmux.Server()
                session = server.list_sessions()[-1]
                window = session.attached_window
                panes = window.panes
                current_pane = window.attached_pane

                target_pane = None
                # --- Check if 'p' is set in global vars ---
                gvars = load_globals()
                p_val = gvars.pop("p", None)  # Get and remove 'p' in one step
                save_globals(gvars)
                if p_val is not None:
                    try:
                        pane_override = int(p_val)
                        if 1 <= pane_override <= 9:
                            args.pane_index = pane_override
                    except ValueError:
                        pass  # Handle invalid int conversion gracefully

                if args.pane_index is not None:
                    # User specified a pane index
                    if args.pane_index < len(panes):
                        target_pane = panes[args.pane_index]
                    else:
                        # Pane doesn't exist — create new one
                        pane_width = int(current_pane['width'])
                        pane_height = int(current_pane['height'])

                        split_vertical = pane_width >= pane_height
                        target_pane = window.split_window(attach=False, vertical=split_vertical)
                        time.sleep(0.3)

                        # Optional: Balance layout
                        window.select_layout('tiled')
                else:
                    # Determine the target pane
                    if len(panes) == 1:
                        if args.exec:
                            print(cmd.cmdline)
                            os.system(cmd.cmdline)
                        else:
                            print(cmd.cmdline)

                        return  # Exit Arsenal sending to current pane
                        
                    else:
                        # Multiple panes: prefer previous, fallback to last
                        current_index = next((i for i, p in enumerate(panes) if p.id == current_pane.id), None)
                        if current_index is not None and current_index > 0:
                            target_pane = panes[current_index - 1]
                        else:
                            target_pane = panes[-1]

                # Send the command (in either case above)
                if args.exec:
                    target_pane.send_keys(cmd.cmdline)
                else:
                    target_pane.send_keys(cmd.cmdline, enter=False)
                    target_pane.select_pane()

            except (ImportError, libtmux.exc.LibTmuxException) as e:
                print("Error using tmux:", str(e))
                return
                
def load_globals():
    if os.path.exists(config.savevarfile):
        with open(config.savevarfile, 'r') as f:
            return json.load(f)
    return {}

def save_globals(data):
    with open(config.savevarfile, 'w') as f:
        json.dump(data, f)

def main():
    try:
        App().run()
    except KeyboardInterrupt:
        exit(0)

if __name__ == "__main__":
    wrapper(main()) 