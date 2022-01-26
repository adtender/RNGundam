from doctest import OutputChecker
import config
import sys
import sqlite3
import subprocess

def main(arg):
    if len(arg) > 1:
        arg = str(arg[1])
    else:
        arg = input("Enter index of file you want to regenerate (Column A on xlsx): ")

    print(arg)

    conn = sqlite3.connect(config.Text_Location + 'history.db')
    cursor = conn.cursor()
    regen = """SELECT RUNCOMMAND FROM HISTORY"""
    cursor.execute(regen)
    oldCommand = cursor.fetchall()[int(arg)][0]
    new = "regenerate"
    newCommand = new.join(oldCommand.rsplit("output", 2))
    print(newCommand)
    conn.commit()
    conn.close()
    subprocess.check_output(newCommand, shell=True)


if __name__ == "__main__":
    main(sys.argv)