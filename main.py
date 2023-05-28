import csv
import tkinter
from tkinter import ttk
from pprint import pprint
from operator import itemgetter

DLC_FILE = r"C:\Users\Jank\Documents\sims 4 dlc.csv"

def treeview_sort_column(tv, col, reverse):
    l = [(tv.set(k, col), k) for k in tv.get_children('')]
    l.sort(reverse=reverse)

    # rearrange items in sorted positions
    for index, (val, k) in enumerate(l):
        tv.move(k, '', index)

    # reverse sort next time
    tv.heading(col, command=lambda: \
               treeview_sort_column(tv, col, not reverse))

class Dlc:
    def __init__(self, name, tier, rank):
        self.name = name
        self.tier = tier
        self.rank = rank
    
    def __iter__(self):
        yield self.name
        yield self.tier
        yield self.rank

    def __len__(self):
        return 3
    
    def __str__(self):
        return f"{self.name},{self.tier},{self.rank}"

class Table:
    def __init__(self, root, tree: ttk.Treeview, lst: list):
        self.root = root
        self.tree = tree
        self.max = []
        self.max.append(len(max(lst, key=lambda x: len(x.name)).name))
        self.max.append(len(max(lst, key=lambda x: len(x.tier)).tier))
        self.max.append(len(max(lst, key=lambda x: len(x.rank)).rank))

        self.tree.heading("name", text="NAME", command=lambda: \
                     treeview_sort_column(self.tree, "name", False))
        self.tree.heading("tier", text="TIER", command=lambda: \
                     treeview_sort_column(self.tree, "tier", False))
        self.tree.heading("rank", text="RANK", command=lambda: \
                     treeview_sort_column(self.tree, "rank", False))
         
        # code for creating table
        for i, item in enumerate(lst):
            self.create_entry(i, item)
    
    def create_entry(self, i, dlc: Dlc):
        self.tree.insert('', tkinter.END, values=list(dlc))
            

def get_dlc_from_file():
    with open(DLC_FILE) as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        ret = []
        for row in reader:
            ret.append(Dlc(*row))
        return ret

def main():
    root = tkinter.Tk()
    columns = ('name', 'tier', 'rank')
    tree = ttk.Treeview(root, columns=columns, show="headings")
    contents = get_dlc_from_file()
    # dlc_sorted = sorted(contents, key=lambda x: x.tier)
    Table(root, tree, contents)
    tree.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
    root.mainloop()

if __name__ == "__main__":
    main()