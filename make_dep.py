#!/usr/bin/env python3

import os
import argparse

SUPPORTED_EXTENSIONS = ['.f90']
IGNORE = ['iso_c_binding']

class DepBuilder:

    def __init__(self, path=None, dep_path=None, obj_path=None, ignore=IGNORE):
        
        if path is not None:
            assert isinstance(path, str), 'String expected as a path'
            self.path = path + '/'
        else:
            self.path = os.getcwd() + '/'
        if dep_path is not None:
            assert isinstance(dep_path, str), 'String expected as a dep_path'
            self.dep_path = dep_path + '/'
        else:
            self.dep_path = ''
        if obj_path is not None:
            assert isinstance(obj_path, str), 'String expected as a obj_path'
            self.obj_path = obj_path + '/'
        else:
            self.obj_path = ''
        self.ignore = ignore
        
        self.src = self.get_src()
        self.deps = self.get_deps()
        
        self.create_dep_files()
        
    def get_src(self):
        
        src = [i for i in os.listdir(self.path) if any([i.endswith(j)\
               for j in SUPPORTED_EXTENSIONS])]
        
        return src
    
    def get_deps(self):
        
        deps = [[i] for i in self.src]
        
        for i, src_file in enumerate(self.src):
            with open(self.path + src_file) as file:
                
                if file.name.endswith('.f90'):
                
                    for line in file:
                        if line.count('use') > 0:
                            ignore = False
                            if self.ignore:
                                for j in self.ignore:
                                    if line.count(j) > 0: ignore = True
                            if not ignore:
                                mods = [i.replace(';', '').replace(' ', '').\
                                        replace('\n', '').replace(',','').partition('only')[0]\
                                        for i in line.split('use ')\
                                        if i.replace(';', '').replace(' ', '')]
                        
                                deps[i].extend(mods)
                
                else:
                    pass
        
        return deps
    
    def create_dep_files(self):
        
        for i, src_file in enumerate(self.src):
            my_dep_file = self.dep_path + '.' + src_file.replace('.f90', '.d').replace('.cxx', '.d')
            my_rule = self.obj_path + src_file.replace('.f90', '.o').replace('.cxx', '.o') + ':'
            
            for dep in self.deps[i]:
                if dep == src_file:
                    my_rule += ' ' + self.path + dep
                else:
                    my_rule += ' ' + self.obj_path + dep + '.o'
            
            with open(my_dep_file, 'w') as file:
                file.write(my_rule + '\n')


parser = argparse.ArgumentParser(prog='gendep')

parser.add_argument('-p', '--path', nargs='?', default=None)
parser.add_argument('-d', '--dep_path', nargs='?', default=None)
parser.add_argument('-o', '--obj_path', nargs='?', default=None)

args = parser.parse_args()

test = DepBuilder(path=args.path, dep_path=args.dep_path, obj_path=args.obj_path)