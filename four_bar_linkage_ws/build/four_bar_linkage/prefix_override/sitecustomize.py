import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/mayank/Downloads/2022101094/four_bar_linkage_ws/install/four_bar_linkage'
