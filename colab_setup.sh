# setup script for google colab

# install graph-tool: https://colab.research.google.com/github/count0/colab-gt/blob/master/colab-gt.ipynb#scrollTo=GQ18Kd5F3uKe
echo "deb http://downloads.skewed.de/apt focal main" >> /etc/apt/sources.list
apt-key adv --keyserver keyserver.ubuntu.com --recv-key 612DEFB798507F25
apt-get update
apt-get install python3-graph-tool python3-matplotlib python3-cairo

# Colab uses a Python install that deviates from the system's! Bad collab! We need some workarounds.
apt purge python3-cairo
apt install libcairo2-dev pkg-config python3-dev
pip install --force-reinstall pycairo
pip install zstandard

pip install -r requirements.txt

pip install -e .

cd src/analysis/orca
g++ -O2 -std=c++11 orca orca.cpp