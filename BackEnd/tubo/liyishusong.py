#回溯时使用所有数据
#与t-1,t-2价格区间比较
#价格区间外0BP
import pandas as pd
import numpy as np

#读取数据
#alldf = pd.read_excel("C:\\Users\\sys\\Downloads\\190210新.xlsx",encoding="GBK")
tdfs=[]
for i in range(1,3):
    tdfs.append(pd.read_csv(str(i)+".csv"))
alldf=pd.concat(tdfs)
tdfs=[]
alldf.drop("Unnamed: 0",axis=1,inplace=True)
alldf=alldf.reset_index()
alldf.drop("index",axis=1,inplace=True)
alldf.columns=["成交编号","成交日期","成交时间","交易方式","债券类型","名称","买入方","买入方交易员","卖出方","卖出方交易员","净价（元）","到期收益率（%）","券面总额（万元）","交易金额（元）","结算日","结算金额（元）"]


#参数设置
tradenostr='成交编号'
txntimestr="当天成交时间"
datestr="结算日"
bondtpstr="债券类型"
trddatestr="成交日"
amtstr='券面总额（万元）'
amtfield='券面总额（万元）'
fromstr="卖出方"
tostr="买入方"
fromacntstr="卖出方交易员"
toacntstr="买入方交易员"
pricestr="净价（元）"
pricet='结算金额（元）'
ratestr='到期收益率（%）'
dlmthdstr="交易方式"
odateformat="%Y-%m-%d"
dateformat1="%Y%m%d"
dateformat="%Y/%m/%d"
dateformat2="%Y-%m-%d hh:mm:ss"
matchingmthdstr="X-Bond"
bondstr="名称"


findthres_lilv=0.01   #利率债价差
findthres_other=0.2   #非利率债价差
amtthres=5000    #盈利亏损阈值
remove_maker=True #去掉做市商
save_folder="chain_result2" #结果存储路径


marketpricethres=0.05
price_ratio_min=0.015
single_price_boundary_min=2
traget_price_ratio_min=0.05
pathlenth=3







alldf[trddatestr]=alldf["成交时间"].str[0:4]+alldf["成交时间"].str[5:7]+alldf["成交时间"].str[8:10]
alldf[txntimestr]=pd.to_datetime(alldf["成交时间"].str[0:19],format="%Y-%m-%d %H:%M:%S")
alldf=alldf[alldf[dlmthdstr].isin(['RFQ','Negotiate'])]


def getdict(inindex,a):
    indict={}
    inde=len(inindex)
    inva=a.loc[inindex,amtfield].values
    for i in range(pow(2,inde)):
        t=0
        indexi=i
        for j in range(inde-1,-1,-1):
            if indexi&1>0:
                t=t+inva[j]
            indexi=indexi>>1
        if t in indict.keys():
            indict[t].add(i)
        else:
            indict[t]=set([i])
    return indict





def chooseedge(index,amt,a,direction):
    if direction=="f":
        dirstr=fromstr
        diracntstr=fromacntstr
        oristr=tostr
        oriacntstr=toacntstr
    elif direction=="b":
        dirstr=tostr
        diracntstr=toacntstr
        oristr=fromstr
        oriacntstr=fromacntstr
    else:
        return []
    node=a.loc[index,oristr]
    price=a.loc[index,pricestr]
    acnt=a.loc[index,oriacntstr]
    #print(dirstr)
    #print(node)
    dirdf=(a[a[dirstr]==node]).copy()
    dirindex=dirdf.index
    if(len(dirindex)==0):
        return []
    pd=np.array(dirdf[pricestr].values)-price
    if direction=="b":
        pd=-pd
    #pd[pd<=0.005]=0
    dirdf["pd"]=pd
    dirdf=dirdf[(dirdf["pd"]<=findthres) & (dirdf["pd"]>=0)]
    dirdf=dirdf[(dirdf[amtstr]>0)]

    dirdf["pd"]=dirdf["pd"]/findthres*0.2+0.8
    if(len(dirdf.index)==0):
        return []
    
    
    ad=np.array(dirdf[amtfield].values)-amt
    #maxad=max(ad)
    #dirdf["ao"]=ad
    dirdf["ad"]=np.abs(ad)/amt
    dirdf["acntd"]=1
    eindex=dirdf[dirdf[diracntstr]==acnt].index
    dirdf.loc[eindex,"acntd"]=0
    dirdf["sim"]=dirdf["ad"]*dirdf["pd"]
    #indf.loc[indf[indf["ao"]<0].index,"ad"]=indf.loc[indf[indf["ao"]<0].index,"ad"]+maxad #绝对值差距越小越好，优先可以传递的量包含当前交易量的边
    dirdf=dirdf.sort_values(by=["acntd","sim"])
    return list(dirdf.index)



def trace_trade_chains1(a,inst,direction):
    paths=[]
    pathids=[]
    pathid=0
    truetargetnum=0
    pathend=[]
    pathget=[]
    pathendamt=[]
    #loop2
    #a=b.copy()    
    #nmts=np.array(nods)
    #point=nmts[nmts[:,1]==str(nmts[:,1].astype(float).max()),0][0]
    point=inst
    #print(point)
    if direction=="f":
        dirstr=fromstr
        oristr=tostr
    elif direction=="b":
        dirstr=tostr
        oristr=fromstr
    else:
        return a,[]
    
    
    maxlength=0
    visit=list(a[(a[dirstr]==point)].sort_values(by=pricestr).index)#当前访问节点
    oripaths=visit.copy()
    visitmnt=list(a[(a[dirstr]==point)].sort_values(by=pricestr)[amtstr].values) #当前可传递量
    visitmntget=list(np.zeros(len(visit)))   #当前传递量

    depths=list(np.zeros(len(visit)))
    xt=False
    circle=False
    while((len(visit)>0)):
        #print(cur
        cur=visit[-1]
        #print(cur)
        curmnt=visitmnt[-1]
        curdepth=depths[-1]
        
        #print(cur)
        inindex=chooseedge(cur,curmnt,a,direction)
        while (len(inindex)>0):
            if inindex[0] in visit:
                inindex.remove(inindex[0])
                if len(inindex)==0:
                    circle=True
            else:
                break
                
        while (len(inindex)>0) :
            #print(a.loc[cur,"from"],a.loc[cur,"to"])
            visit.append(inindex[0])
            visitmnt.append(min(a.loc[inindex[0],amtfield],curmnt))
            depths.append(curdepth+1)
            inindex.remove(inindex[0])
            #pairs[cur]=inindex
            visitmntget.append(0)
            cur=visit[-1]
            curmnt=visitmnt[-1]
            curdepth=depths[-1]
            #snode=a.loc[cur,oristr]
            #tnode=a.loc[cur,dirstr]
            #cprice=a.loc[cur,pricestr]
            #print("123"+snode)
            inindex=chooseedge(cur,curmnt,a,direction)
            #pairs[cur]=inindex
            #print("1r"+str(cur))
            #print(2)
            #print(inindex)
            while (len(inindex)>0):
                if inindex[0] in visit:
                    inindex.remove(inindex[0])
                    if len(inindex)==0:
                        circle=True
                else:
                    break
            #pairs[cur]=inindex
            #ta=a[(a[pricestr]<=(cprice+findthres))&(a[pricestr]>=(cprice-findthres))]    #判断该节点是否净溶出
            #amt=ta[ta[fromfield]==snode][amtfield].sum()-ta[ta[tostr]==snode][amtfield].sum()
            #if amt>0:
                #break
        #print("amt"+str(amt))
        vol=curmnt
        if circle==False:  #找到一个净融出节点
            #if amt>0:
               # vol=min(curmnt,amt)
            #else:
            #print(vol)
            #print("vol"+str(vol))
            #ramnt=ramnt-vol
            #print("ramnt"+str(ramnt))
            #paths.append([cur,visitmntget[n]+vol])
            n=len(visit)-1
            while (curdepth>0): #递归减去已经用掉的量
                #cur=visit[n]
                a.loc[cur,amtfield]=a.loc[cur,amtfield]-vol

                visitmnt[n]=visitmnt[n]-vol
                visitmntget[n]=visitmntget[n]+vol
                n=n-1
                curdepth=depths[n]
                cur=visit[n]
                if cur in oripaths:
                    curoripath=cur
            a.loc[cur,amtfield]=a.loc[cur,amtfield]-vol
            visitmnt[n]=visitmnt[n]-vol
            visitmntget[n]=visitmntget[n]+vol
            #if visitmntget[-1]>0:
            
        #print("visitmntget")
        #print(visitmntget)
        #print(visitmnt)
        #print(pairs[visit[-1]])
        else:        #找到环节点或者正融出节点
            #print("circle")
            circle=False
            #print(visit[-1])
            #print(visit)
            if(len(visit)>0):
                #print(len(visit))
                #print(len(visitmnt))
            #循环减掉量已经用完的路径
                cur=visit[-1]
                entry=a.loc[cur,oristr]
                cto=a.loc[cur,dirstr]
                vs=[]
                n=len(visit)-1
                while (cto!=entry): #循环添加链条
                    vs.append(a.loc[cur,amtfield])
                    #print("c"+str(cur))
                    n=n-1
                    cur=visit[n]
                    cto=a.loc[cur,dirstr]
                vs.append(a.loc[cur,amtfield])
                #print("c"+str(cur))
                minv=min(vs)
                cur=visit[-1]
                #entry=a.loc[cur,fromfield]
                cto=a.loc[cur,dirstr]
                
                while (cto!=entry): #循环减去已经用掉的量，这里会开始么？
                    #cur=visit[n]
                    a.loc[cur,amtfield]=a.loc[cur,amtfield]-minv
                    if a.loc[cur,amtfield]==0:
                        a.drop(cur,inplace=True)

                    visit.pop()
                    visitmnt.pop()
                    depths.pop()
                    visitmntget.pop()
                    cur=visit[-1]
                    cto=a.loc[cur,dirstr]
                a.loc[cur,amtfield]=a.loc[cur,amtfield]-minv
                visitmnt[-1]=visitmnt[-1]-minv
                #visit.pop()
                #visitmnt.pop()
                #depths.pop()
                #visitmntget.pop()
        
            #print("a",b.loc[cur,"from"],b.loc[cur,"to"],paths[-1][1])
        
            #print("1d"+str(cur))
        #print(visit)
        #print("pop")
        #
        #print(visit)
        #print(visit)
        #print(visitmntget)
        if(len(visit)>0):
            #print(len(visit))
            #print(len(visitmnt))
            #循环减掉量已经用完的路径
            if visitmntget[-1]>0: #添加新的路径
            #cur=visit[-1]
                pathid=pathid+1
               # maxlength=len(visit)
                #paths.append([cur,visitmntget[-1],pathid])
                cur=visit[-1]
                paths.append(cur)
                pathget.append(visitmntget[-1])
                pathendamt.append(vol)
                pathids.append(pathid)
                pathend.append(1)
                visit.pop()
                visitmnt.pop()
                visitmntget.pop()
                depths.pop()
            while ((len(visitmnt)>0)):
                if (visitmnt[-1]>0 ):
                    break
                cur=visit.pop()
                if visitmntget[-1]>0:
                    #paths.append([cur,visitmntget[-1],pathid])
                    paths.append(cur)
                    pathget.append(visitmntget[-1])
                    pathids.append(pathid)
                    pathend.append(0)
                    pathendamt.append(0)
                    #print("b",b.loc[cur,"from"],b.loc[cur,"to"],paths[-1][1])
                if a.loc[cur,amtfield]==0:
                    a.drop(cur,inplace=True)
                    #print("2d"+str(cur))
                visitmnt.pop()
                depths.pop()
                visitmntget.pop()
        #visitmntget.pop()
    #print(len(visit))
    while len(visit)>0:
        cur=visit.pop()
        if visitmntget[-1]>0:
            #paths.append([cur,visitmntget[-1]])
            paths.append(cur)
            pathget.append(visitmntget[-1])
            pathids.append(pathid)
            pathend.append(0)
            pathendamt.append(0)
        visitmnt.pop()
        depths.pop()
        visitmntget.pop()
    return a,paths,pathids,pathend,pathget,pathendamt

#昌图县农村信用合作联社_4
#浦发银行悦盈利系列之6个月定开型H款理财计划_0
#上海东亚期货有限公司-东亚十七号单一资产管理计划_2
#中国国际金融股份有限公司_3
def trace_trade_chains_bidirection(daydf2,inst,pairmax):
    #print(inst)
    b=daydf2.copy()
    #print(len(daydf))
    features=[]
    a=b
    #loop1
    
    pathlist=[]
    titles=[]
    pathindex=[]
    pathvalues=[]
    #print(a[(a[fromstr]==inst) | (a[tostr]==inst)])
    a,paths1,ids1,pe1,pathget1,pathendamt1=trace_trade_chains1(a,inst,"b")
    #print(a[(a[fromstr]==inst) | (a[tostr]==inst)])
    a=daydf2.copy()
    a,paths2,ids2,pe2,pathget2,pathendamt2=trace_trade_chains1(a,inst,"f")
    #print(a[(a[fromstr]==inst) | (a[tostr]==inst)])
    paths2.reverse()
    ids2.reverse()
    pe2.reverse()
    pathget2.reverse()
    pathendamt2.reverse()
    #print(len(paths2))
    #print(len(set(paths2)))
    #print(paths1)
    #print(paths2)
    s1=paths1
    s2=paths2
    #i1=s1.intersection(s2)
    df1=daydf2.loc[s1,namelist].copy().reset_index()
    df1.drop("index",axis=1,inplace=True)
    df1["路径标识"]=ids1
    df1["路径端点"]=pe1
    df1["方向"]="上游"
    df1["母路径"]=-1
    df1["目标交易员"]="SSS"
    df1["传递交易量"]=pathget1
    df1["端点交易量"]=pathendamt1
    df2=daydf2.loc[s2,namelist].copy().reset_index()
    df2.drop("index",axis=1,inplace=True)
    df2["路径标识"]=ids2
    df2["方向"]="下游"
    df2["路径端点"]=pe2
    df2["母路径"]=-1
    df2["目标交易员"]="SSS"
    df2["传递交易量"]=pathget2
    df2["端点交易量"]=pathendamt2
    #df3=daydf.loc[list(i1),[tradenostr,datestr,fromstr,tostr,fromacntstr,toacntstr,amtstr,pricestr,ratestr,pricet]]
    #df3["方向"]="双向"
    #paths=paths1+paths2
    #paths=list(set(paths))
    
    patharea1={}
    patharea2={}
    l1=list(df1[(df1[tostr]==inst)]["路径标识"].unique())
    l1.sort()
    l2=list(df2[(df2[fromstr]==inst)]["路径标识"].unique())
    l2.sort()
    endpahs1=[-1]+l1
    endpahs2=[-1]+l2
    for i in range(1,len(endpahs1)):
        patharea1[endpahs1[i]]=np.arange(endpahs1[i-1]+1,endpahs1[i]+1)
    for i in range(1,len(endpahs2)):
        patharea2[endpahs2[i]]=np.arange(endpahs2[i-1]+1,endpahs2[i]+1)
    
    acnts=set(list(df1[df1[tostr]==inst][toacntstr].unique())+list(df2[df2[fromstr]==inst][fromacntstr].unique()))
    #print(acnts)
    acntdf1=df1[(df1[tostr]==inst)].sort_values(by=pricestr).copy().reset_index()
    acntdf2=df2[(df2[fromstr]==inst)].sort_values(by=pricestr).copy().reset_index()
    acntdf1.drop("index",axis=1,inplace=True)
    acntdf2.drop("index",axis=1,inplace=True)
    acntdf1["xr"]=(acntdf1[pricet])/acntdf1[amtstr]
    acntdf2["xr"]=(acntdf2[pricet])/acntdf2[amtstr]
    #acv1=acntdf1[["方向","路径标识",pricestr]].drop_duplicates()
    #acv2=acntdf2[["方向","路径标识",pricestr]].drop_duplicates()
    #acv=pd.concat([acv1,acv2]).sort_values(by=pricestr)
    acntdfs=[]
    #print(acv)
    if(acntdf1[amtstr].sum()-acntdf2[amtstr].sum())>0:
        print("1111111111111111111111")
        print(inst)
        print(len(acntdf2))
    if(acntdf1[amtstr].sum()-acntdf2[amtstr].sum())<0:
        print("22222222222222222222")
        print(inst)
        print(len(acntdf1))
    stats1=[]
    stats2=[]
    df1n=df1.copy()
    df2n=df2.copy()
    #print(len(acntdf1))
    for row in range(len(acntdf1.index)):
        xrow=acntdf1.iloc[row,:]
        tprice=xrow[pricestr]
        priced=np.array(acntdf2[pricestr].values)-tprice
        acntdf2["pd"]=np.abs(priced)
        acntdf2["acntd"]=1
        eindex=acntdf2[acntdf2[fromacntstr]==xrow[toacntstr]].index
        acntdf2.loc[eindex,"acntd"]=0
        acntdf2["timed"]=np.abs((acntdf2[txntimestr]-xrow[txntimestr])/np.timedelta64(1,'D'))
        ps=xrow["路径标识"]
        ids=patharea1[ps]
        tmpdf=df1[df1["路径标识"].isin(ids)]
        tmpdf["目标交易员"]=xrow[toacntstr]
        tmpdf["母路径"]=ps
        acntdfs.append(tmpdf)
        leftdf=tmpdf[tmpdf["路径端点"]==1][[fromstr,"方向","端点交易量"]]
        leftdf["交易损益"]=0
        while xrow[amtstr]>0:
            ad=np.array(acntdf2[amtstr].values)-xrow[amtstr]
            acntdf2["ad"]=np.abs(ad)
            acntdf2=acntdf2.sort_values(by=["acntd","ad","pd","timed"])
            if len(acntdf2[acntdf2[amtstr]>0])<1:
                break
            t2i=acntdf2[acntdf2[amtstr]>0].index[0]
            tamt1=acntdf2.loc[t2i,amtstr]
            #print(xrow[amtstr])
            #print(2)
            #print(acntdf2.loc[t2i,:])
            #print(tamt)
            tamt=min(xrow[amtstr],tamt1)
            xr=acntdf2.loc[t2i,"xr"]-xrow["xr"]
            leftdf1=leftdf.copy()
            lindex=leftdf1.index
            leftdf1["端点交易量"]=df1n.loc[lindex,"端点交易量"]*tamt/xrow[amtstr]
            df1n.loc[lindex,"端点交易量"]=df1n.loc[lindex,"端点交易量"]-leftdf1["端点交易量"]
            leftdf1["交易损益"]=leftdf1["端点交易量"]*xr
            leftdf1["交易分组"]=pairmax
            stats1.append(leftdf1)
            
            ps=acntdf2.loc[t2i,"路径标识"]
            ids=patharea2[ps]
            tmpdf=df2[df2["路径标识"].isin(ids)]
            tmpdf["母路径"]=ps
            tmpdf["目标交易员"]=acntdf2.loc[t2i,fromacntstr]
            rightdf=tmpdf[tmpdf["路径端点"]==1][[tostr,"方向","端点交易量"]]
            rindex=rightdf.index
            rightdf["端点交易量"]=df2n.loc[rindex,"端点交易量"]*tamt/tamt1
            df2n.loc[rindex,"端点交易量"]=df2n.loc[rindex,"端点交易量"]-rightdf["端点交易量"]
            rightdf["交易损益"]=rightdf["端点交易量"]*xr
            rightdf["交易分组"]=pairmax
            stats2.append(rightdf)
            pairmax=pairmax+1
            
            xrow[amtstr]=xrow[amtstr]-tamt
            acntdf2.loc[t2i,amtstr]=acntdf2.loc[t2i,amtstr]-tamt
            
            if acntdf2.loc[t2i,amtstr]==0:
                
                acntdfs.append(tmpdf)
                

                
                
                
                
                
                
                
    
    #print(len(acntdfs))
    #print(acntdfs)
                
        
        '''
        for row in range(len(acv.index)):
            #print(row)
            dirs=acv.iloc[row,0]
            ps=acv.iloc[row,1]
            if dirs=="上游":
                ids=patharea1[ps]
                tmpdf=df1[df1["路径标识"].isin(ids)]
                tmpdf["母路径"]=ps
                acntdfs.append(tmpdf)
            else:
                ids=patharea2[ps]
                tmpdf=df2[df2["路径标识"].isin(ids)]
                tmpdf["母路径"]=ps
                acntdfs.append(tmpdf)
        tmpdf=pd.concat(acntdfs)
        tmpdf["目标交易员"]=acnt
        allacntdfs.append(tmpdf)
        '''
    #print(len(allacntdfs))
    #print(len(acntdfs))
    #print(len(stats1))
    #print(len(stats2))
    return pd.concat(acntdfs),pairmax,pd.concat(stats1),pd.concat(stats2)
    




if remove_maker==True:
    makerdf= pd.read_csv("maker.csv",encoding="GBK")
    makerset=set(makerdf["机构名称"].values)
else:
    makerset=set([])
    

alldf=alldf.dropna()
alldf=alldf[alldf[dlmthdstr].isin(['RFQ','Negotiate'])]





allr=[]
allstats1=[]
allstats2=[]
newinst=0
newindex=max(alldf.index)
pairmax=0
namelist=[tradenostr,datestr,txntimestr,amtstr,fromstr,tostr,fromacntstr,toacntstr,pricestr,dlmthdstr,trddatestr,pricet,ratestr]
namelist2=[tradenostr,datestr,txntimestr,amtstr,tostr,fromstr,toacntstr,fromacntstr,pricestr,dlmthdstr,pricet,ratestr, '路径标识', '路径端点', '方向','传递交易量','端点交易量',
       '母路径', '目标交易员', '目标机构', '目标债券','目标日期', '目标分组', '交易损益']
   #价格差阈值
dategroup=alldf.groupby(datestr)
    #bonddf["month"]=bonddf[datestr].apply(lambda x: pd.to_datetime(str(x.year)+"/"+str(x.month)+"/01",format=dateformat))
    #months=bonddf["month"].unique()
    #for month in months:
for date in list(dategroup.indices.keys()):
    print("开始处理"+str(date)[0:10]+"数据"+".....")
    allr=[]
    allstats1=[]
    allstats2=[]
    daydf=dategroup.get_group(date)
    daydf[datestr]=pd.to_datetime(daydf[datestr],format="%Y-%m-%d")
    daydf[trddatestr]=pd.to_datetime(daydf[trddatestr],format=dateformat1)
    bondgroup=daydf.groupby(bondstr) 
    print(len(daydf))
    for bondname in list(bondgroup.indices.keys()): #bondgroup.indices.keys()
        bonddf=bondgroup.get_group(bondname).copy()
        bondtp=bonddf.head(1)[bondtpstr].values[0]
        if bondtp in ["国债","政策性金融债"]:
            findthres=findthres_lilv
        else:
            findthres=findthres_other
        bonddf=bonddf[namelist]
    
        inset=set(bonddf[fromstr].unique().tolist()).intersection(set(bonddf[tostr].unique().tolist()))-makerset
        xbuygroup=bonddf.groupby([fromstr])
        xsellgroup=bonddf.groupby([tostr])
        tlist=[]
        netlist=[]
        n1=0
        for i in inset:
            xbuy=xbuygroup.get_group(i)
            xsell=xsellgroup.get_group(i)
            buysum=xbuy[amtstr].sum()
            sellsum=xsell[amtstr].sum()
            netp=0
            if buysum==sellsum:
                netp=xbuy[pricet].sum()-xsell[pricet].sum()
                if (netp<-amtthres) | (netp>amtthres):
                    n1=n1+1
                    tlist.append(i)
                    netlist.append(netp)
        if len(tlist)>0:
            daydf1=bonddf.copy()   #.reset_index()
            #daydf1.drop("index",axis=1,inplace=True)
            day_group=daydf1.groupby([fromstr,tostr,fromacntstr,toacntstr,ratestr])
            more=[]
            dset=[]
            
            for di in day_group.indices:
                tdf=day_group.get_group(di)
                if len(tdf.index)>1:
                    tdf0=tdf.head(1).copy()
                    tdf0[tradenostr]=("-").join(tdf[tradenostr].values)
                    tdf0[amtstr]=tdf[amtstr].sum()
                    tdf0[pricet]=tdf[pricet].sum()
                    dset=dset+list(tdf.index)
                    more.append(np.array(tdf0.values))
            dset=set(dset)
            #oridf=daydf1.loc[dset,:].copy()
            #for li in dset:
            #daydf1.drop(dset,inplace=True)
            if len(more)>0:
                tempdaydf1=pd.DataFrame(np.concatenate(more),columns=namelist)
            #daydf1=daydf1.reset_index()
            #daydf1.drop("index",axis=1,inplace=True)
        for instindex in range(len(tlist)):
            inst=tlist[instindex]
            net=netlist[instindex]
            #print(net)
            instset=set(list(daydf1[(daydf1[fromstr]==inst) |(daydf1[tostr]==inst) ].index)).intersection(dset)
            daydf2=daydf1.copy()
            daydf2.drop(instset,inplace=True)
            if len(more)>0:
                daydf2=pd.concat([daydf2,tempdaydf1])
            daydf2=daydf2.reset_index()
            daydf2.drop("index",axis=1,inplace=True)
            rdf,pairnum,stats1,stats2=trace_trade_chains_bidirection(daydf2,inst,pairmax)
            pairmax=pairnum
            rdf["目标机构"]=inst
            rdf["目标债券"]=bondname
            rdf["目标日期"]=date
            rdf["目标分组"]=newinst
            rdf["交易损益"]=net
            stats1["目标机构"]=inst
            stats1["目标债券"]=bondname
            stats1["目标日期"]=date
            stats1["目标分组"]=newinst
            stats2["目标机构"]=inst
            stats2["目标债券"]=bondname
            stats2["目标日期"]=date
            stats2["目标分组"]=newinst
            newinst=newinst+1
            allr.append(rdf)
            allstats1.append(stats1)
            allstats2.append(stats2)


        
    if len(allr)>0:   
        pd.concat(allr)[namelist2].to_csv(save_folder+"/"+str(date)[0:10]+"_result.csv")
        pd.concat(allstats1).to_csv(save_folder+"/"+str(date)[0:10]+"_s1.csv")
        pd.concat(allstats2).to_csv(save_folder+"/"+str(date)[0:10]+"_s2.csv")
        
        
        
        
        
        
        
        
        
        
        
        
        
'''
        for targetprice in targetlist:
            print("价格区间"+str(targetprice[1])+"_"+str(targetprice[2])+".....")
            pricepath=monthpath+"/"+str(targetprice[1])+"_"+str(targetprice[2])
            minprice=targetprice[1]*0.01
            maxprice=targetprice[2]*0.01
            outthres=0.01
            result,result_in,owndf,trademntpricedf,owntraderatiovalue=getdaichiinfo(dmonthdf,minprice,maxprice,pricepath)#计算某个价格网络的代持信息
            if(len(result)<1):
                continue
            buy_stats(dmonthdf,minprice,maxprice,pricepath,True)
            buy_stats(dmonthdf,minprice,maxprice,pricepath,False)
            #result_in=get_inst_clusters(result_in,pricepath)
            targetinst=get_candidate_inst_1(dmonthdf,pricepath) #获取所有可疑机构
            
            daydict,nodedict,edgedict,linklist,daynodename,savedf,ratioresult,outratioresult=construct_graph(dmonthdf,minprice,maxprice) #构建代持网络
            targetinst=targetinst.intersection(set(list(daynodename.keys())))
            print("开始回溯"+str(len(targetinst))+"家机构.....")
            trace_trade_chains(linklist,daydict,nodedict,edgedict,pricepath,daynodename,targetinst,savedf,ratioresult,outratioresult) #回溯代持网络
'''

