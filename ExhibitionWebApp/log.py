import sys
from browser import document, alert, window, html

document <= html.TEXTAREA('',Id='log',Rows='20',Cols='60')
def write(data):
    document['log'].value += data
sys.stdout.write = sys.stderr.write = write
