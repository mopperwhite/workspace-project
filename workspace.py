#!/usr/bin/env python
#encoding=UTF-8
#  
#  Copyright 2014 MopperWhite <mopperwhite@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#


# TODO The same day on different zones
import optparse,time,os,json,shutil,re,atexit

global WORKSPACE_PATH,TIME_FORMAT
TIME_FORMAT="%Y-%m-%d@%Z"
TODAY=False
WORKSPACE_PATH=os.path.join(os.path.expandvars('$HOME'),"Workspace")
DATE_DICT={
	"today":time.strftime(TIME_FORMAT),	
}
class WorkspaceException(Exception):
	pass

def new(args,kwargs):
	date=kwargs["date"]
	git=kwargs["git"]
	if not os.path.isdir(date):
		os.mkdir(date)
        if TODAY:
        	if os.path.exists("Today"):
        		os.remove("Today")
        	os.symlink(date,"Today")
        #Creating a "today" link is not necessary nor safe.
	#But convert.
        #But links cannot be put into the label of nautils, so "today" is still removed.
        if git:
		os.system("cd %s && git init"%date)
        return os.path.join(WORKSPACE_PATH,date)
def remove(args,kwargs):
	date=kwargs["date"]
        if os.path.isdir(date):
                try:
                        os.rmdir(date)
                except OSError,e:
                        if raw_input("Directory %s is not empty.\
Still remove it?[y/N]:"%date).lower()=='y':
                                shutil.rmtree(date)
        else:
                print "%s is not a directory."%date
def work(args,kwargs):
        new(args,kwargs)
	wpl=os.listdir(WORKSPACE_PATH)
	wpl.sort(key=lambda d:-os.path.getctime(os.path.join(WORKSPACE_PATH,d)))
        work=args[0]
        wpath=os.path.join(WORKSPACE_PATH,kwargs["date"],work)
        if not os.path.exists(wpath):
                for d in wpl:
                        if d!=kwargs["date"] and re.search(r"^\d{4,4}-\d{2,2}-\d{2,2}@[A-Z]{3,3}$",d) is not None :
                                if work in os.listdir(os.path.join(WORKSPACE_PATH,d)):
                                        path=os.path.join(WORKSPACE_PATH,d,work)
                                        while(os.path.islink(path)):
                                                path=os.readlink(path)
                                        os.symlink(path,wpath)
                                        print(wpath)
                                        return
        elif os.path.isdir(wpath) or os.path.islink(wpath):
                print wpath
                return
        else:
                raise WorkspaceException("%s is not a file or a link."%wpath)
        newwork(args,kwargs)
def newwork(args,kwargs):
        work=args[0]
        wpath=os.path.join(WORKSPACE_PATH,kwargs["date"],work)
        if not os.path.exists(wpath):
                os.mkdir(wpath)
                print wpath
        elif os.path.isdir(wpath) or os.path.islink(wpath):
                print wpath
        else:
                raise WorkspaceException("%s is not a file or a link."%wpath)
FUNCS_DICT={
	"new":new,
        "remove":remove,
	"work":work,
	"newwork":newwork,
}
def main():
	global WORKSPACE_PATH
	parse=optparse.OptionParser()
	parse.add_option("--date","-d",default="today")
	parse.add_option("--git","-g",default=False)
	parse.add_option("--path","-p",default=WORKSPACE_PATH)
	options, arguments = parse.parse_args()
	if options.path!=WORKSPACE_PATH:
		WORKSPACE_PATH=options.path
	os.chdir(WORKSPACE_PATH)
	kwargs={
		"date":DATE_DICT[options.date] if options.date in DATE_DICT else  time.strptime(options.date, TIME_FORMAT) ,
		"git":options.git,
		
	}
	if arguments:
        	if arguments[0] in FUNCS_DICT:
               		try:
                           	FUNCS_DICT[arguments[0]](arguments[1:],kwargs)
                    	except WorkspaceException as e:
                      		print("Workspace Error:",e.message)
                                sys.exit(1)
          	else:
                   	print "Unknown command '%s'."%arguments[0]
	else:
                print new(arguments[1:],kwargs)
if __name__=="__main__":
	main()
