import sqlite3
import subprocess

if __name__ == '__main__':
    tables = ['daily_history_price', 'fruit', 'fruit_location', 'fruit_month', 'location', 'market', 'monthly_history_price']
    con = sqlite3.connect('database.sqlite')
    cur = con.cursor()

    cmds = []
    for t in tables:
        cur.execute('delete from '+t+"s;")
        cmds.append(".import norm_csv/"+t+".csv "+t+"s")
        #print(".import "+t+".csv "+t+"s")
    con.commit()
    subprocess.call(["sqlite3", "database.sqlite", "-cmd",".mode csv",cmds[0], cmds[1], cmds[2], cmds[3],cmds[4], cmds[5], cmds[6]])
    '''subprocess.call(".mode csv")'''
    '''for t in tables:
        cmd = ".import "+t+".csv "+t+"s"
        subprocess.call(cmd)'''

    #subprocess.call(["sqlite3 database_testpy.sqlite", ".mode csv"])
