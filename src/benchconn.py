import os

def genprop(addr, user, password, house, worker, term, time):
	tmp = "db=dm\ndriver=dm.jdbc.driver.DmDriver\n"
	tmp += "conn=jdbc:dm://" + addr + "\n"
	tmp += "user=" + user + "\n"
	tmp += "password=" + password + "\n"
	tmp += "warehouses=" + str(house) + "\n"
	tmp += "loadWorkers=" + str(worker) + "\n"
	tmp += "terminals=" + str(term) + "\n"
	tmp += "runTxnsPerTerminal=0\n"
	tmp += "runMins=" + str(time) + "\n"
	tmp += "limitTxnsPerMin=10000000\nterminalWarehouseFixed=false\nuseStoredProcedures=false\nnewOrderWeight=45\npaymentWeight=43\norderStatusWeight=4\ndeliveryWeight=4\nstockLevelWeight=4\n"
	with open("tmp.prop", "w") as f:
		f.write(tmp)

def load():
	os.system("./runDatabaseDestroy.sh tmp.prop")
	os.system("./runDatabaseBuild.sh tmp.prop|tee tmp.res")
	with open("tmp.res") as f:
		s = f.read()
	return s

def run():
	os.system("./runBenchmark.sh tmp.prop|tee tmp.res")
	with open("tmp.res") as f:
		s = f.read()
	return s

