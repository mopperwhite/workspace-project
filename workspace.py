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
import optparse,time,os,json

global WORKSPACE_PATH,TIME_FORMAT
TIME_FORMAT="%Y-%m-%d@%Z"
WORKSPACE_PATH=os.path.join(os.path.expandvars('$HOME'),"Workspace")
DATE_DICT={
	"today":time.strftime(TIME_FORMAT),	
}
class WorkspaceException(Exception):
	pass

def new(date,git):
	if not os.path.isdir(date):
		os.mkdir(date)
	if os.path.exists("today"):
		os.remove("today")
	os.symlink(date,"today")
	if git:
		os.system("cd %s && git init"%date)

FUNCS_DICT={
	"new":new,
}
def main():
	global WORKSPACE_PATH
	parse=optparse.OptionParser()
	parse.add_option("--date","-d",default="today")
	parse.add_option("--git","-g",default="true")
	parse.add_option("--path","-p",default=WORKSPACE_PATH)
	options, arguments = parse.parse_args()
	if options.path!=WORKSPACE_PATH:
		WORKSPACE_PATH=options.path
	os.chdir(WORKSPACE_PATH)
	func_args=(
		DATE_DICT[options.date] if options.date in DATE_DICT else  time.strptime(options.date, TIME_FORMAT) ,
		json.loads(options.git),
	)
	if arguments:
		for f in arguments:
			try:
				FUNCS_DICT[f](*func_args)
			except WorkspaceException as e:
				print("Workspace Error:",e.message)
	else:
		new(*func_args)
if __name__=="__main__":
	main()
