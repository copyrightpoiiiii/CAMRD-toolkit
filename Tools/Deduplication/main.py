#coding=utf-8

import argparse
import os

import database as db
from analysis import Load, Redundancy
import plot

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--use-db', help="use database or not, default 'false'", action='store_true')
    parser.add_argument('--plot-result', help="plot result or not, default 'false'", action='store_true')
    parser.add_argument('-mysql-user', help="mysql username, default 'root'", type=str, default='root')
    parser.add_argument('-mysql-psw', help="mysql password, default '12345'", type=str, default='12345')
    parser.add_argument('-mysql-database', help="mysql database, default 'db'", type=str, default='db')
    parser.add_argument('--load-info', help="whether image info needed to load into database, default 'false'", action='store_true')
    args = parser.parse_args()

    __FIGURE_PATH = 'Figure/'
    __DATA_PATH = 'DataSet/'

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
        red.images_to_filecount_by_path('%s%s' %(__DATA_PATH, 'Image_file_count.csv'))
    
    if args.plot_result:
        if not os.path.isdir(__FIGURE_PATH):
            os.mkdir(__FIGURE_PATH)

        print('--- plotting result ---')
        plt = plot.Plot()

        print('[figure] fig.9(a) in paper, the proportion of accessed files')
        plt.accessed_file_proportion('%s%s' %(__DATA_PATH, 'Accessed_file.csv'), '%s%s' %(__DATA_PATH, 'Image_file_count.csv'), '%s%s' %(__FIGURE_PATH, 'Fig9a_Accessed_file_proportion.png'))
        print('[figure] fig.9(b) in paper, the type of accessed files')
        plt.accessed_file_type('%s%s' %(__DATA_PATH, 'Accessed_file.csv'), '%s%s' %(__FIGURE_PATH, 'Fig9b_Accessed_file_proportion.png'))
        print('[figure] fig.9(c) in paper, the layer where files access')
        plt.accessed_file_in_layer('%s%s' %(__DATA_PATH, 'Accessed_file.csv'), '%s%s' %(__FIGURE_PATH, 'Fig9c_Accessed_file_in_layer.png'))
        print('[figure] fig.9(d) in paper, CDF of the number of same accessed files')
        plt.accessed_file_shared('%s%s' %(__DATA_PATH, 'Accessed_file.csv'), '%s%s' %(__FIGURE_PATH, 'Fig9d_Accessed_file_shared.png'))
        print('[figure] fig.9(e) in paper, the redundancy between different versions of images in accessed-file level')
        plt.accessed_file_redundancy('%s%s' %(__DATA_PATH, 'Accessed_file.csv'), '%s%s' %(__FIGURE_PATH, 'Fig9e_Accessed_file_redundancy.png'))

        print('[figure] fig.14 in paper, file-level redundancy in repo and registry')
        plt.file_redundancy('%s%s' %(__DATA_PATH, 'Redundancy_file_level.csv'), '%s%s' %(__FIGURE_PATH, 'Fig14_Redundancy_file_level.png'))
        
        '''
        print('[figure] fig.16 in paper, the latency of the proportion of accessed image data in container-running phase')
        plt.container_running('%s%s' %(__DATA_PATH, 'IO_latency_nginx.csv'), '%s%s' %(__FIGURE_PATH, 'Fig16_Container_running.png'))

        print('[figure] fig.17(a) in paper, time cost comparison between traditional and on-demand images in four phases')
        plt.four_phase('%s%s' %(__DATA_PATH, 'Conv_and_Running.csv'), '%s%s' %(__FIGURE_PATH, 'Fig17a_Four_phase.png'))
        '''
        print('[figure] fig.17(b) in paper, conversion size')
        plt.conversion_size('%s%s' %(__DATA_PATH, 'Conv_size.txt'), '%s%s' %(__FIGURE_PATH, 'Fig17b_Conversion_size.png'))

if __name__ == '__main__':
    main()