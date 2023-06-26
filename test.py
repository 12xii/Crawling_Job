from matplotlib import font_manager as fm
import matplotlib as mpl
from matplotlib import pyplot as plt

print ('버전: ', mpl.__version__)
print ('설치 위치: ', mpl.__file__)
print ('설정 위치: ', mpl.get_configdir())
print ('캐시 위치: ', mpl.get_cachedir())

print ('설정파일 위치: ', mpl.matplotlib_fname())

font_list = fm.findSystemFonts(fontpaths=None, fontext='ttf')

print([(f.name, f.fname) for f in fm.fontManager.ttflist if 'Nanum' in f.name])

print('# 설정 되어있는 폰트 사이즈')
print (plt.rcParams['font.size'] ) 
print('# 설정 되어있는 폰트 글꼴')
print (plt.rcParams['font.family'] )

plt.rcParams["font.family"] = 'NanumGohticOTF'

print(plt.rcParams['font.family'])