function file_exists(name)
   local f=io.open(name,"r")
   if f~=nil then io.close(f) return true else return false end
end
local mattata_ai = require('mattata-ai')
local var
local handle
while 1 do
	while not file_exists("a.tmp") do
		os.execute("sleep 0.1")
	end
	file = io.open("a.tmp","r")
	io.input(file)
	var = io.read()
	io.close(file)
	io.popen("rm a.tmp")
	file=io.open("out.tmp","w")
	io.output(file)
	io.write(mattata_ai.talk(var,"en"))
	io.close(file)
end
