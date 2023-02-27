import pandas as pd
import matplotlib.pyplot as plt

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib
import numpy as np
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

plt.rcParams['lines.linewidth'] = 2
plt.rcParams['axes.facecolor']='white'
plt.rcParams['figure.facecolor']='white'
plt.rcParams['figure.edgecolor']='white'
plt.rcParams['savefig.facecolor']='white'
plt.rcParams['savefig.edgecolor']='white'
plt.rcParams['axes.labelsize']=12
plt.rcParams['xtick.labelsize']=12
plt.rcParams['ytick.labelsize']=12
plt.rcParams['axes.titlesize']=12
plt.rcParams['legend.framealpha']=1
plt.rcParams['legend.fontsize']=11
plt.rcParams['axes.xmargin']=0
plt.rcParams['axes.ymargin']=0
plt.rcParams['axes.autolimit_mode']='round_numbers'
matplotlib.rcParams['pdf.fonttype']=42
matplotlib.rcParams['ps.fonttype']=42

import random
import argparse
import numpy as np

random.seed(0)

parser = argparse.ArgumentParser()

args = parser.add_argument_group('')
args.add_argument('--in_path', type=str, default="NAR")
args.add_argument('--fig_path', type=str, default="NAR")
args.add_argument('--eps', type=float, default=0.3)
args.add_argument('--N_classes', type=int, default=2)
args = parser.parse_args()


in_path = args.in_path
fig_path = args.fig_path
eps = args.eps

def pltcolor(n):
    return plt.rcParams['axes.prop_cycle'].by_key()['color'][n]



df = pd.read_csv(f"{in_path}/node_{1}_{eps}.csv")

for cls in range(0,N_classes):
    df_ = df[df["class"] == cls]
    plt.plot(df_['round'],df_['made_accepted']/df_['made'], marker=markers[cls], markevery=200,label=f"Class {cls}")
plt.legend()
plt.grid()
plt.xlim(0,100000)
plt.xlabel("Time")
plt.ylabel("NAR")
plt.ylim(0,1)
plt.legend(ncol=1,labelspacing=0.2, loc="lower left", bbox_to_anchor=(0.735, 0.65))
plt.savefig(f"{fig_path}/eps_{eps}.png",bbox_inches="tight")
plt.show()