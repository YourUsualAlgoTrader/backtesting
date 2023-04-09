



import pandas as pd
import numpy as np
import plotly.graph_objects as go
from tqdm import tqdm

import json
from typing import Any, Dict, List
from numpy import mean, std, nan, log10
from pandas import DataFrame,concat
from json import JSONEncoder

Time = int
Symbol = str
Product = str
Position = int
Dollar = int
UserId = str
Observation = int
round=4
day=1

df=pd.read_csv(f'C:/Users/CYTech Student/IMC/Data/island-data-bottle-round-{round}/prices_round_{round}_day_{day}.csv',sep=";")

class Listing:
    def __init__(self, symbol: Symbol, product: Product, denomination: Product):
        self.symbol = symbol
        self.product = product
        self.denomination = denomination


class Order:
    def __init__(self, symbol: Symbol, price: int, quantity: int) -> None:
        self.symbol = symbol
        self.price = price
        self.quantity = quantity

    def __str__(self) -> str:
        return "(" + self.symbol + ", " + str(self.price) + ", " + str(self.quantity) + ")"

    def __repr__(self) -> str:
        return "(" + self.symbol + ", " + str(self.price) + ", " + str(self.quantity) + ")"


class OrderDepth:
    def __init__(self):
        self.buy_orders: Dict[int, int] = {}
        self.sell_orders: Dict[int, int] = {}


class Trade:
    def __init__(self, symbol: Symbol, price: int, quantity: int, buyer: UserId = None, seller: UserId = None, timestamp: int = 0) -> None:
        self.symbol = symbol
        self.price: int = price
        self.quantity: int = quantity
        self.buyer = buyer
        self.seller = seller
        self.timestamp = timestamp

class TradingState(object):
    def __init__(self,
                 timestamp: Time=0,
                 listings: List=[],
                 order_depths: Dict[Symbol, OrderDepth]={},
                 own_trades: Dict[Symbol, List[Trade]]={},
                 market_trades: Dict[Symbol, List[Trade]]={},
                 position: Dict[Product, Position]={},
                 PNL: Dict[Product,Dollar]={},
                 observations: Dict[Product, Observation]={}):
        self.timestamp = timestamp
        self.listings = listings
        self.order_depths = order_depths
        self.own_trades = own_trades
        self.market_trades = market_trades
        self.position = position
        self.PNL = PNL
        self.observations = observations

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)

class ProsperityEncoder(JSONEncoder):
        def default(self, o):
            return o.__dict__



# class Trader:
#     col=["timestamp","bid_price_1","bid_volume_1","bid_price_2","bid_volume_2","bid_price_3","bid_volume_3","ask_price_1","ask_volume_1","ask_price_2","ask_volume_2","ask_price_3","ask_volume_3","mid_price"]
#     dfBANANAS=DataFrame(columns=col)
#     dfCOCONUTS=DataFrame(columns=col)
#     dfPINA=DataFrame(columns=col)
#     dfPEARLS=DataFrame(columns=col)
#     dfBERRIES=DataFrame(columns=col)
#     dfGEAR=DataFrame(columns=col+["DOLPHIN_SIGHTINGS"])
#     PNL_GEAR=0
#     clotureGear=0
#     longShortGear=0
#     last_price_gear=0
#     # positionDict={"PEARLS":[0,0],"PINA_COLADAS":[0,0],"BANANAS":[0,0],"COCONUTS":[0,0]}
#     linedf=[]
#     PNL_banana=0
#     best_ask_before=0
#     best_bid_before=0
#     takeprofit=0
#     dfUKULELE=DataFrame(columns=col)
#     dfBASKET=DataFrame(columns=col)
#     dfBAGUETTE=DataFrame(columns=col)
#     dfDIP=DataFrame(columns=col)
#
#     #0 hold/take position, 1 close position
#     close_banane=0
#     def run(self, state: TradingState) -> Dict[str, List[Order]]:
#         """
#         Only method required. It takes all buy and sell orders for all symbols as an input,
#         and outputs a list of orders to be sent
#         """
#         # for product in state.order_depths.keys():
#         #
#         #
#         result = {}
#         carnet_ordre=state.order_depths
#
#
#
#         self.linedf=[]
#         self.linedf.append(state.timestamp)
#         orders: list[Order] = []
#         compteur=0
#         for price,qty in carnet_ordre["DIVING_GEAR"].buy_orders.items():
#             if compteur<3:
#                 self.linedf.append(float(price))
#                 self.linedf.append(float(qty))
#
#                 if compteur>=1 and self.linedf[-2]>self.linedf[-4]:
#                     self.linedf[-4:-2],self.linedf[-2:]=self.linedf[-2:],self.linedf[-4:-2]
#
#                 compteur+=1
#
#
#         while compteur<3:
#             self.linedf.append(nan)
#             self.linedf.append(nan)
#             compteur+=1
#         compteur=0
#         for price,qty in carnet_ordre["DIVING_GEAR"].sell_orders.items():
#             if compteur<3:
#                 self.linedf.append(float(price))
#                 self.linedf.append(float(qty))
#
#                 if compteur>=1 and self.linedf[-2]<self.linedf[-4]:
#                     self.linedf[-4:-2],self.linedf[-2:]=self.linedf[-2:],self.linedf[-4:-2]
#
#                 compteur+=1
#
#         while compteur<3:
#             self.linedf.append(nan)
#             self.linedf.append(nan)
#             compteur+=1
#         self.linedf.append((self.linedf[7]+self.linedf[1])/2)
#         self.linedf.append(state.observations["DOLPHIN_SIGHTINGS"])
#
#         self.dfGEAR=concat([self.dfGEAR, (DataFrame([self.linedf],columns=self.col+["DOLPHIN_SIGHTINGS"]))],axis=0)
#
#         pos=0
#
#         if len(self.dfGEAR)>2:
#
#
#             if "DIVING_GEAR" in state.position.keys():
#                 pos=state.position["DIVING_GEAR"]
#
#             #PNL update,if no position PNL reset
#             if pos>0:
#                 self.PNL_GEAR=self.dfGEAR.bid_price_1.iloc[-1]-self.last_price_gear
#             elif pos<0:
#                 self.PNL_GEAR=-self.dfGEAR.ask_price_1.iloc[-1]+self.last_price_gear
#             else:
#                 self.PNL_GEAR=0
#                 self.clotureGear=0
#
#             #if cloture signal is up, then cloture (to cloture all quantity during multiple iteration)
#             if self.clotureGear==1:
#                 orders: list[Order] = [Order("DIVING_GEAR", self.dfGEAR.ask_price_1.iloc[-1], -pos)]
#             elif self.clotureGear==-1:
#                 orders: list[Order] = [Order("DIVING_GEAR", self.dfGEAR.bid_price_1.iloc[-1], -pos)]
#
#             #Cloture signal, and update of buy/sell signal
#             if self.takeprofit==0 and self.PNL_GEAR>100:
#                 self.takeprofit=100
#
#             elif self.takeprofit==0 and self.PNL_GEAR<-300:
#                 if pos>0:
#                     self.clotureGear=-1
#                     self.longShortGear=0
#                     orders: list[Order] = [Order("DIVING_GEAR", self.dfGEAR.bid_price_1.iloc[-1], -pos)]
#                 else:
#                     self.clotureGear=1
#                     self.longShortGear=0
#                     orders: list[Order] = [Order("DIVING_GEAR", self.dfGEAR.ask_price_1.iloc[-1], -pos)]
#             elif self.PNL_GEAR>self.takeprofit+100 and self.takeprofit>0:
#                 self.takeprofit+=100
#
#             elif self.takeprofit>0 and self.PNL_GEAR<self.takeprofit-50:
#
#                 if pos>0:
#                     self.clotureGear=-1
#                     self.longShortGear=0
#                     orders: list[Order] = [Order("DIVING_GEAR", self.dfGEAR.bid_price_1.iloc[-1], -pos)]
#                 else:
#                     self.clotureGear=1
#                     self.longShortGear=0
#                     orders: list[Order] = [Order("DIVING_GEAR", self.dfGEAR.ask_price_1.iloc[-1], -pos)]
#
#
#             #if buy/sell signal up and limit not reach, buy or sell. Update of cloture signal
#             if pos==50 or pos==-50:
#                 self.longShortGear=0
#                 self.clotureGear=0
#             elif self.longShortGear==1:
#                 orders: list[Order] = [Order("DIVING_GEAR", self.dfGEAR.ask_price_1.iloc[-1], 50-pos)]
#                 self.clotureGear=0
#             elif self.longShortGear==-1:
#                 orders: list[Order] = [Order("DIVING_GEAR", self.dfGEAR.bid_price_1.iloc[-1], -50-pos)]
#                 self.clotureGear=0
#
#
#             #Open position signal, update of buy/sell signal
#             if self.dfGEAR.DOLPHIN_SIGHTINGS.iloc[-1]-self.dfGEAR.DOLPHIN_SIGHTINGS.iloc[-2]<-5:
#                 orders: list[Order] = [Order("DIVING_GEAR", self.dfGEAR.bid_price_1.iloc[-1], -50-pos)]
#                 self.last_price_gear=self.dfGEAR.bid_price_1.iloc[-1]
#                 self.longShortGear=-1
#
#             elif self.dfGEAR.DOLPHIN_SIGHTINGS.iloc[-1]-self.dfGEAR.DOLPHIN_SIGHTINGS.iloc[-2]>5:
#                 orders: list[Order] = [Order("DIVING_GEAR", self.dfGEAR.ask_price_1.iloc[-1], 50-pos)]
#                 self.last_price_gear=self.dfGEAR.ask_price_1.iloc[-1]
#                 self.longShortGear=1
#             result["DIVING_GEAR"]=orders
#
#
#         return result
class Trader:


    def run(self, state: TradingState) -> Dict[str, List[Order]]:
        """
        Only method required. It takes all buy and sell orders for all symbols as an input,
        and outputs a list of orders to be sent
        """

        # Initialize the method output dict as an empty dict
        result = {}

        for product in state.order_depths.keys():

            if product == 'PEARLS':

                order_depth: OrderDepth = state.order_depths[product]

                orders: list[Order] = []

                haut_range = 10002
                bas_range = 9998


                if len(order_depth.sell_orders) > 0 and (product not in state.position.keys() or state.position[product]<20):


                    best_ask = min(order_depth.sell_orders.keys())
                    best_ask_volume = order_depth.sell_orders[best_ask]

                    if best_ask <= bas_range:
                        best_ask_volume=min(20-state.position[product],best_ask_volume)
                        #print("BUY", str(-best_ask_volume) + "x", best_ask)
                        orders.append(Order(product, best_ask, best_ask_volume))


                if len(order_depth.buy_orders) != 0 and (product not in state.position.keys() or state.position[product]>-20):

                    best_bid = max(order_depth.buy_orders.keys())
                    best_bid_volume = order_depth.buy_orders[best_bid]
                    if best_bid >= haut_range:
                        best_bid_volume=min(best_bid_volume,+20+best_bid_volume)
                        #print("SELL", str(best_bid_volume) + "x", best_bid)
                        orders.append(Order(product, best_bid, -best_bid_volume))


                result[product] = orders



            if product == 'BANANAS':


                order_depth: OrderDepth = state.order_depths[product]

                orders: list[Order] = []



                if len(order_depth.sell_orders) > 0 and (product not in state.position.keys() or state.position[product]<20):

                    best_ask = min(order_depth.sell_orders.keys())
                    best_ask_volume = order_depth.sell_orders[best_ask]

                    #print("BUY", str(-best_ask_volume) + "x", best_ask)
                    orders.append(Order(product, best_ask, -best_ask_volume))

                result[product] = orders



        return result

def marketSimulation(allMarket,strategy):
    tradingState=TradingState()
    bidNumber=0
    askNumber=0
    position=0
    history={}
    mid_price={}
    mid_price_previous={}
    for name in df.columns:
        if "bid_price" in name:
            bidNumber+=1
        elif "ask_price" in name:
            askNumber+=1
    for product in list(allMarket.loc[:,"product"].drop_duplicates()):
        history[product]={}

    for timestamp in tqdm(allMarket.loc[:,"timestamp"].drop_duplicates()):
        tradingState.timestamp=timestamp
        currentMarket=allMarket.loc[allMarket.loc[:,"timestamp"]==timestamp]
        tradingState.listings=list(currentMarket["product"]) #There shouldn't be any duplicate to begin with
        for product in tradingState.listings:
            tradingState.order_depths[product]=OrderDepth()
            productLine=dict(currentMarket.loc[currentMarket.loc[:,"product"]==product,:].iloc[0])
            if not (np.isnan(productLine["bid_volume_1"]) and np.isnan(productLine["ask_volume_1"])):

                for i in range(1,bidNumber+1):
                    bid_price_i=productLine["bid_price_"+str(i)]
                    if not np.isnan(bid_price_i):


                        tradingState.order_depths[product].buy_orders[bid_price_i]=productLine["bid_volume_"+str(i)] if "bid_volume_"+str(i) in currentMarket.columns else 1
                for i in range(1,askNumber+1):
                    ask_price_i=productLine["ask_price_"+str(i)]
                    if not np.isnan(ask_price_i):

                        tradingState.order_depths[product].sell_orders[ask_price_i]=productLine["ask_volume_"+str(i)] if "ask_volume_"+str(i) in currentMarket.columns else 1
            else:
                tradingState.observations={product:productLine["mid_price"]}
        OrdersPerProduct=strategy.run(tradingState)
        future_own_trade={}
        for product in tradingState.listings:

            productLine=dict(currentMarket.loc[currentMarket.loc[:,"product"]==product,:].iloc[0])
            mid_price[product]=(productLine["ask_price_1"]+productLine["bid_price_1"])/2
        for product,position in tradingState.position.items():
            productLine=dict(currentMarket.loc[currentMarket.loc[:,"product"]==product,:].iloc[0])
            tradingState.PNL[product]+=tradingState.position[product]*(mid_price[product]-mid_price_previous[product]) if not np.isnan(tradingState.position[product]*(mid_price[product]-mid_price_previous[product])) else 0




        for product,orders in OrdersPerProduct.items():


            if product in tradingState.listings:
                trades=[]

                for order in orders:
                    if order.symbol==product:

                        if product not in tradingState.position.keys():
                            tradingState.position[product]=0
                        if product not in tradingState.PNL.keys():
                            tradingState.PNL[product]=0
                        currentMarketProduct=dict(currentMarket.loc[currentMarket.loc[:,"product"]==product,:])
                        quantityNotCleared=order.quantity
                        whichBid=1
                        whichAsk=1
                        ask_price_i=currentMarketProduct["ask_price_"+str(whichAsk)].iloc[0]
                        bid_price_i=currentMarketProduct["bid_price_"+str(whichBid)].iloc[0]

                        while quantityNotCleared>0 and order.price>=ask_price_i and whichAsk<=askNumber:
                            ask_volume_i=currentMarketProduct["ask_volume_"+str(whichAsk)].iloc[0]
                            if "Buy" not in history[product].keys():
                                history[product]["Buy"]=pd.DataFrame(columns=["timestamp","ask_price","volume","PNL"])
                            if quantityNotCleared-ask_volume_i>0:
                                tradingState.position[product]=tradingState.position[product]+ask_volume_i
                                tradingState.PNL[product]=tradingState.PNL[product]-(ask_price_i-mid_price[product])*ask_volume_i
                                trades.append(Trade(product,ask_price_i,ask_volume_i,"Yourself","Unknow",tradingState.timestamp))
                                quantityNotCleared=quantityNotCleared-ask_volume_i
                                history[product]["Buy"]=pd.concat([history[product]["Buy"],pd.DataFrame([[timestamp,ask_price_i,ask_volume_i,tradingState.PNL[product]]],index=[len(history[product]["Buy"])],columns=["timestamp","ask_price","volume","PNL"])])
                            else:
                                tradingState.position[product]=tradingState.position[product]+quantityNotCleared
                                tradingState.PNL[product]=tradingState.PNL[product]-(ask_price_i-mid_price[product])*quantityNotCleared
                                trades.append(Trade(product,ask_price_i,quantityNotCleared,"Yourself","Unknow",tradingState.timestamp))

                                history[product]["Buy"]=pd.concat([history[product]["Buy"],pd.DataFrame([[timestamp,ask_price_i,quantityNotCleared,tradingState.PNL[product]]],index=[len(history[product]["Buy"])],columns=["timestamp","ask_price","volume","PNL"])])
                                quantityNotCleared=0
                            whichAsk+=1
                            ask_price_i=currentMarketProduct["ask_price_"+str(whichAsk)].iloc[0]


                        #To bid, the quantity ordered should be negative


                        while quantityNotCleared<0 and order.price<=bid_price_i and whichBid<=bidNumber:
                            bid_volume_i=currentMarketProduct["bid_volume_"+str(whichBid)].iloc[0]
                            if "Sell" not in history[product].keys():
                                history[product]["Sell"]=pd.DataFrame(columns=["timestamp","bid_price","volume","PNL"])
                            if quantityNotCleared+bid_volume_i<0:
                                tradingState.position[product]=tradingState.position[product]-bid_volume_i
                                tradingState.PNL[product]=tradingState.PNL[product]+(bid_price_i-mid_price[product])*bid_volume_i
                                trades.append(Trade(product,bid_price_i,bid_volume_i,"Yourself","Unknow",tradingState.timestamp))
                                quantityNotCleared=quantityNotCleared+bid_volume_i
                                history[product]["Sell"]=pd.concat([history[product]["Sell"],pd.DataFrame([[timestamp,bid_price_i,bid_volume_i,tradingState.PNL[product]]],index=[len(history[product]["Sell"])],columns=["timestamp","bid_price","volume","PNL"])])
                            else:
                                tradingState.position[product]=tradingState.position[product]+quantityNotCleared
                                tradingState.PNL[product]=tradingState.PNL[product]-(bid_price_i-mid_price[product])*quantityNotCleared
                                trades.append(Trade(product,bid_price_i,quantityNotCleared,"Unknow","Yourself",tradingState.timestamp))

                                history[product]["Sell"]=pd.concat([history[product]["Sell"],pd.DataFrame([[timestamp,bid_price_i,-quantityNotCleared,tradingState.PNL[product]]],index=[len(history[product]["Sell"])],columns=["timestamp","bid_price","volume","PNL"])])

                                quantityNotCleared=0
                            whichBid+=1
                            bid_price_i=currentMarketProduct["bid_price_"+str(whichBid)].iloc[0]

                if len(trades)>0:
                    tradingState.own_trades[product]=trades
        for product in tradingState.listings:
            mid_price_previous[product]=(currentMarket.loc[currentMarket.loc[:,"product"]==product,"ask_price_1"].iloc[0]+currentMarket.loc[currentMarket.loc[:,"product"]==product,"bid_price_1"].iloc[0])/2

    return(strategy,tradingState,history)
round=0
day=-1
df=pd.read_csv(f'C:/Users/CYTech Student/IMC/Data/island-data-bottle-round-{round}/prices_round_{round}_day_{day}.csv',sep=";")









def graphStrategy(df,strategy,*args):
    result,state,history=marketSimulation(df,strategy)
    colorMidPrice=["orange","blue","black"]
    colorAsk=["green","lime","darkgreen"]
    colorBid=["red","tomato","brown"]
    for index,product in enumerate(args):
        if product in state.observations.keys():
            # Create traces
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df.loc[df.loc[:,"product"]==product].reset_index().timestamp,y=df.loc[df.loc[:,"product"]==product].reset_index().mid_price,mode='lines',name='Mid price '+str(product),line=dict(color=colorMidPrice[index])))
        else:
            df.loc[df.loc[:,"product"]==product].mid_price

            # Create traces
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df.loc[df.loc[:,"product"]==product].reset_index().timestamp,y=df.loc[df.loc[:,"product"]==product].reset_index().mid_price,mode='lines',name='Mid price '+str(product),line=dict(color=colorMidPrice[index])))
            if "Buy" in history[product].keys():
                fig.add_trace(go.Scatter(x=history[product]["Buy"].timestamp, y=history[product]["Buy"].ask_price,mode='markers',name='Buy',line=dict(color=colorAsk[index])))
            if "Sell" in history[product].keys():
                fig.add_trace(go.Scatter(x=history[product]["Sell"].timestamp, y=history[product]["Sell"].bid_price,mode='markers',name='Sell',line=dict(color=colorBid[index])))

    fig.show()
    return(result,state,history)

strategy=Trader()
result,state,history=graphStrategy(df,strategy,"BANANAS","PEARLS")