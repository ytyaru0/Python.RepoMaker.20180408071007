#!python3
#encoding:utf-8
import os.path
import argparse

class Main:
    def Run(self):
        parser = argparse.ArgumentParser(
            description='Repository Maker.',
        )
        sub_parser = parser.add_subparsers()
        
        parser_update = sub_parser.add_parser('update', help='see `update -h`')
        parser_update.set_defaults(handler=self.__Update)
        
        parser_change = sub_parser.add_parser('change', help='see `change -h`')
        parser_change.add_argument('-d', '--description')
        parser_change.add_argument('-home', '--homepage')
        parser_change.add_argument('-l', '--license')
        parser_change.set_defaults(handler=self.__Change)
        
        parser.add_argument('-o', '--output-dir')
        parser.add_argument('-u', '--username')
        parser.add_argument('-d', '--description')
        parser.add_argument('-hp', '--homepage')
        parser.add_argument('-m', '--messages', action='append')
        parser.add_argument('-l', '--license')
        parser.add_argument('-e', '--exception', action='append')
        parser.add_argument('-s', '--ssh-host')
        parser.set_defaults(handler=self.__Make)

        args = parser.parse_args()
        if hasattr(args, 'handler'): args.handler(args)
        else: parser.print_help()

    def __Make(self, args):
        print('ReadMe.mdなどを作成する予定。args={}'.format(args))
        
    def __Update(self, args):
        print('ライセンスの年号更新を実装する予定。args={}'.format(args))
        
    def __Change(self, args):
        print('リポジトリの説明、URL、ライセンスの変更を実装する予定。args={}'.format(args))
        

if __name__ == '__main__':
    main = Main()
    main.Run()
