import functions as fn
import time
import mysql_connection as sqlcon

fn.introduction()
time.sleep(2)
fn.user_login()

sqlcon.show_all()