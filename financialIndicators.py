"""
Input:
	stockPrices : array of floats
	period : integer
	volume : array of floats
	shortPeriod: integer
	longPeriod: integer
	StockPricesHigh: array of floats
	StockPricesLow: array of floats
	MACDArray: array of floats
	array: array of floats
"""
import math

class FinancialService(object):

	"""
	-pre: len(stockPrices)!= 0 ^ 0<period<(len(StockPrices))
	-post: list with exponential moving average calculated 
	"""

	def ExponencialAverage(self,stockPrices,period):
		EMAList = []
		media = 0.0
		for i in range(period):
			media += stockPrices[i]
		media /= (period)
		listaMod = stockPrices[(period):]
		EMAList.append(media)
		div = (2.0/(period+1))
		for i in range(len(listaMod)):
			EMAList.append((listaMod[i]*div)+(EMAList[i]*(1-(div))))
		return EMAList

	"""
	-pre: len(stockPrices)!= 0 ^ 0<period<(len(stockPrices))
	-post: list with SMA calculated 
	"""

	def SMA(self,stockPrices,period):
		lf=[]
		media = 0.0
		p = period
		a = 0
		while (period <= len(stockPrices)):
			i = a
			while (i < period):
				media += (stockPrices[i])
				i = i+1
			lf.append(media/float(p))
			period = (period + 1)
			a = a +1 
			media = 0.0
		return(lf)

	"""
	-pre: len(StockHigh)==len(StockLow)==len(stockPrices) ^ len(stockPrices)!=0 ^ 0<period<(len(stockPrices))
	-post: list with ADX calculated 
	"""

	def ADX(self,StockPrices,StockPricesHigh,StockPricesLow,period):

		def calculoPeriodico(l):
			l_aux = []
			l_aux.append(sum(l[0:(period-1)]))
			i = 0
			j = (period-1)
			while j < len(l):
				l_aux.append(l_aux[i]-(l_aux[i]/period)+l[j])
				i += 1
				j += 1
			return l_aux

		def DIPeriodico(list1,list2):
			l_aux = []
			i = 0
			while i<len(list1):
				l_aux.append((list1[i]/list2[i])*100)
				i +=1
			return l_aux

		#CALCULO DE TR (True Range)
		tr = []
		i = 1
		while (i<len(StockPrices)):
			tr.append(max((StockPricesHigh[i]-StockPricesLow[i]),abs(StockPricesHigh[i]-StockPrices[i-1]),abs(StockPricesLow[i]-StockPrices[i-1])))
			i += 1

		#CALCULO DE ATR 
		atr = calculoPeriodico(tr)

		#CALCULO PARA +DM
		dm_pos = []

		i = 1
		while i < len(StockPrices):
			if ((StockPricesHigh[i]-StockPricesHigh[i-1])>(StockPricesLow[i-1]-StockPricesLow[i])):
				dm_pos.append(max((StockPricesHigh[i]-StockPricesHigh[i-1]),(0)))
			else:
				dm_pos.append(0)
			i += 1

		#CALCULO PARA -DM
		dm_neg = []
		i = 1
		while i < len(StockPrices):
			if ((StockPricesLow[i-1]-StockPricesLow[i])>(StockPricesHigh[i]-StockPricesHigh[i-1])):
				dm_neg.append(max((StockPricesLow[i-1]-StockPricesLow[i]),(0)))
			else:
				dm_neg.append(0)
			i += 1

		#CALCULO PARA +Dm 
		dm_p = (calculoPeriodico(dm_pos))

		#CALCULO PARA -Dm 
		dm_n = (calculoPeriodico(dm_neg))

		# CALCULO PARA +DI
		di_p = DIPeriodico(dm_p,atr);

		# CALCULO PARA -DI 
		di_n = DIPeriodico(dm_n,atr);

		# CALCULO PARA DX 
		dx = []
		for i in range(len(di_p)):
			dx.append(((abs(di_p[i]-di_n[i]))/(di_p[i]+di_n[i]))*100)

		#CALCULO PARA ADX
		adxList = []
		i = 0
		suma = 0.0
		while i < len(di_p):
			suma += (dx[i])
			i += 1
		adxList.append(suma/len(di_p))
		i = 0
		j = period
		while i < len(dx[period:]):
			adxList.append((adxList[i]*(period-i)+dx[j])/(period))
			j += 1
			i += 1

		return adxList

	"""
	-pre: len(array) != 0
	-post: standard deviation of "array"
	"""

	def StandardDeviation(self,array):
		media=0.0
		desviacion=0.0
		for i in range(len(array)):
			media+=array[i]
		media/=len(array)
		for i in range(len(array)):
			desviacion+=(array[i]-media)**2		
		desviacion/=media
		return math.sqrt(desviacion)

	"""
	-pre: len(array) != 0
	-post: coefficient of variation of "array"
	"""

	def CoefficientOfVariation(self,array):
		media = 0.0
		for i in range(len(array)):
			media+=array[i]
		media /= len(array)
		desviacion=self.StandardDeviation(array)
		return desviacion/abs(media)

	"""
	-pre: len(StockPrice) != 0 ^ shortPeriod<=longPeriod ^ shortPeriod>0
	-post: list with MACD calculated 
	"""
		
	def MACD(self,stockPrices,shortPeriod,longPeriod):
		macdList = []
		list1 = (self.ExponencialAverage(stockPrices,shortPeriod)[(longPeriod-shortPeriod):])
		list2 = (self.ExponencialAverage(stockPrices,longPeriod))

		for i in range(len(list2)):
			macdList.append(list1[i]-list2[i])

		return macdList

	"""
	-pre: len(MACDArray) != 0 ^ period>0
	-post: list with Signal calculated 
	"""

	def Signal(self,MACDArray,period):
		return self.ExponencialAverage(MACDArray,period)

	"""
	-pre: len(StockPrice) != 0
	-post: list with OBV calculated 
	"""

	def OBV (self,StockPrice,volume):
		obvList = []
		obvList.append(volume[0])
		i = 2
		while i < (len(StockPrice)):
			if (StockPrice[i]>StockPrice[i-1]):
				obvList.append(obvList[i-2]+volume[i-1])
			if (StockPrice[i]<StockPrice[i-1]):
				obvList.append(obvList[i-2]-volume[i-1])
			elif (StockPrice[i]==StockPrice[i-1]):
				obvList.append(obvList[i-2]+0)
			i +=1
		return obvList

	"""
	-pre: len(StockHigh)==len(StockLow)==len(stockPrices) ^ len(stockPrices)!=0 ^ 0<period<(len(stockPrices))
	-post: list with CCI calculated 
	"""

	def CCI(self,StockPrices,StockPricesHigh,StockPricesLow,period):

		def obtener_periodo(array,periodo,num):
			a = ((len(array))-(periodo-1))
			i = 0
			lista = []
			while (i < a):
				lista.append(array[i:periodo+i])
				i = i+1
			return lista[num]

		stockTP = []
		stockTPD = []
		deviation = []
		stockCCI = []
		for i in range(len(StockPrices)):
			stockTP.append((StockPricesHigh[i]+StockPricesLow[i]+StockPrices[i])/3)
		stockTPD = self.SMA(stockTP,period)
		j = 0
		while (j < (len(stockTPD))):
			listaAuxiliar = []
			des = 0.0
			i = 0
			while (i<period):
				listaAuxiliar = obtener_periodo(stockTP,period,j)
				des += abs(stockTPD[j]-listaAuxiliar[i])
				i +=1
			des/=(period)
			deviation.append(des)
			j += 1
		l = (len(stockTP))-(len(stockTPD))
		listaMod = (stockTP[l:])
		for i in range(len(listaMod)):
			stockCCI.append((listaMod[i]-stockTPD[i])/(0.015*deviation[i]))
		return stockCCI

	"""
	-pre: len(StockHigh)==len(StockLow)==len(stockPrices) ^ len(stockPrices)!=0
	-post: list with stochastic K calculated 
	"""

	def K(self,StockPrices,StockPricesHigh,StockPricesLow):
		valMin = min(StockPricesLow)
		valMax = max(StockPricesHigh)
		estocasticoK = []
		for i in range(len(StockPrices)):
			estocasticoK.append(100*((StockPrices[i]-valMin)/(valMax-valMin)))
		return estocasticoK

	"""
	-pre: len(StockHigh)==len(StockLow)==len(stockPrices) ^ len(stockPrices)!=0 ^ 0<period<(len(stockPrices))
	-post: list with stochastic D calculated 
	"""

	def D(self,StockPrices,StockPricesHigh,StockPricesLow,period):
		return self.SMA(self.K(StockPrices,StockPricesHigh,StockPricesLow),period)