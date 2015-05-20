#!/usr/bin/env ruby
$workspace=File.join Dir.home,'Workspace'
def work name
        puts File.join $workspace,name
end
if __FILE__==$0
        send(ARGV[0],ARGV[1])
end
