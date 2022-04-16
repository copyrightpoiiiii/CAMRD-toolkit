#coding=utf-8

import argparse
import os

import database as db
from analysis import Load, Redundancy

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--use-db', help="use database or not, default 'false'", action='store_true')
    parser.add_argument('--plot-result', help="plot result or not, default 'false'", action='store_true')
    parser.add_argument('-mysql-user', help="mysql username, default 'root'", type=str, default='root')
    parser.add_argument('-mysql-psw', help="mysql password, default '12345'", type=str, default='12345')
    parser.add_argument('-mysql-database', help="mysql database, default 'db'", type=str, default='db')
    parser.add_argument('--load-info', help="whether image info needed to load into database, default 'false'", action='store_true')
    args = parser.parse_args()

    __FIGURE_PATH = 'Deduplication/Figure/'
    __DATA_PATH = 'Deduplication/DataSet/'

    if args.use_db:
        if not os.path.isdir(__DATA_PATH):
            os.mkdir(__DATA_PATH)
            
        print('--- connect database ---')
        print('[mysql] user: %s, password: %s, database: %s' %(args.mysql_user, args.mysql_psw, args.mysql_database))
        db.init(args.mysql_user, args.mysql_psw, args.mysql_database)

        if args.load_info:
            print('--- load docker information into database ---')
            db.drop_all_and_create_all_tables()
            Load(db.Session()).into_database()

        print('--- analysis procedure ---')
        red = Redundancy(db.Session())
        red.redundancy_file_level('%s%s' %(__DATA_PATH, 'Redundancy_file_level.csv'))
        red.images_to_filecount_by_path('%s%s' %(__DATA_PATH, 'image_file_count.csv'))

if __name__ == '__main__':
    main()