from flask import Flask,render_template,request, redirect, url_for,flash
import requests
import boto3
from boto3.session import Session
import cStringIO
import os
import urllib2
import memcache
import pymysql
import hashlib
import time

app=Flask(__name__)

@app.route('/', methods=['GET','POST'])
def login():
    if request.method == "GET":
	return render_template('login.html')
    if request.method == "POST":
        # some test
        pwd=request.form['pwd']
	
	userfile=os.path.dirname(__file__)+'/UserAccessList.txt'
        f=open(userfile)
        for line in iter(f):
            if uname in line:
                if pwd in line:
                    abc=1
                    break
            else:
                abc=0
        if abc==1:
            return render_template('userInput.html')
    return render_template('login.html')

@app.route('/userInput', methods=['GET','POST'])
def connect():
    if request.method == "GET":
	return render_template('userInput.html')
    results=[]
    if request.method == "POST":
        city=request.form['city']
	#country=request.form['country']
        #region=request.form['region']
        #distance=request.form['distance']
        hostname = 'mydbinstance.cmikrvej0mw4.us-west-2.rds.amazonaws.com'
        username = '*****'
        password = '*****'
        database = 'city'
        myConnection = pymysql.connect( host=hostname, user=username, passwd=password, db=database )
        cur = myConnection.cursor()
	##origLat="(SELECT latitude FROM city.CityInfo2 where city='"+city+"'and region='"+region+"'and country='"+country+"')"
        ##origLon= "(SELECT longitude FROM city.CityInfo2 where city='"+city+"'and region='"+region+"'and country='"+country+"')"
        ##query="SELECT city, 3956 * 2 * ASIN(SQRT( POWER(SIN((" +str(origLat)+" - latitude)*pi()/180/2),2)+COS("+str(origLat)+"*pi()/180 )*COS(latitude*pi()/180)*POWER(SIN(("+str(origLon)+"-longitude)*pi()/180/2),2))) as distance FROM city.CityInfo2 WHERE longitude between ("+str(origLon)+"-"+str(distance)+"/cos(radians("+str(origLat)+"))*69) and ("+str(origLon)+"+"+str(distance)+"/cos(radians("+str(origLat)+"))*69) and latitude between ("+str(origLat)+"-("+str(distance)+"/69)) and ("+str(origLat)+"+("+str(distance)+"/69)) having distance < "+str(distance)+" ORDER BY distance"
	#query="SELECT city, 3956 * 2 * ASIN(SQRT( POWER(SIN(((select latitude from city.CityInfo2 where city='"+city+"') - latitude)*pi()/180/2),2)+COS((select longitude from city.CityInfo2 where city='"+city+"')*pi()/180 )*COS(latitude*pi()/180)*POWER(SIN(((select longitude from city.CityInfo2 where city='"+city+"')-longitude)*pi()/180/2),2))) as distance FROM city.CityInfo2 WHERE longitude between ((select longitude from city.CityInfo2 where city='"+city+"')-10/cos(radians((select latitude from city.CityInfo2 where city='"+city+"')))*69) and ((select longitude from city.CityInfo2 where city='"+city+"')+10/cos(radians((select latitude from city.CityInfo2 where city='"+city+"')))*69) and latitude between ((select latitude from city.CityInfo2 where city='"+city+"')-(10/69)) and ((select latitude from city.CityInfo2 where city='"+city+"')+(10/69)) having distance < 10 ORDER BY distance limit 100"
	#query1 = cur.execute("SELECT city, 3956 * 2 * ASIN(SQRT( POWER(SIN(((select latitude from city.CityInfo2 where city='"+city+"') - latitude)*pi()/180/2),2)+COS((select longitude from city.CityInfo2 where city='"+city+"')*pi()/180 )*COS(latitude*pi()/180)*POWER(SIN(((select longitude from city.CityInfo2 where city='"+city+"')-longitude)*pi()/180/2),2))) as distance FROM city.CityInfo2 WHERE longitude between ((select longitude from city.CityInfo2 where city='"+city+"')-10/cos(radians((select latitude from city.CityInfo2 where city='"+city+"')))*69) and ((select longitude from city.CityInfo2 where city='"+city+"')+10/cos(radians((select latitude from city.CityInfo2 where city='"+city+"')))*69) and latitude between ((select latitude from city.CityInfo2 where city='"+city+"')-(10/69)) and ((select latitude from city.CityInfo2 where city='"+city+"')+(10/69)) having distance < 10 ORDER BY distance limit 100")
        #cur.execute( "SELECT Country,Latitude FROM city.CityInfo where City='"+city+"'")
	query="(select population from city.citypop2 where city='"+city+"' )"
	key1 = hashlib.sha256(query).hexdigest()
        #rows=cur.fetchall()
	starttime=time.time()
        memc = memcache.Client(['mycache.2md5ug.cfg.usw2.cache.amazonaws.com:11211'], debug=1)
        memcheck = memc.get(key1)
	rows=memcheck
	
	#return 'abc'
	#queryTime=time.time()
	#return str(queryTime)
        if not memcheck:
	    #return 'abc'
	    starttime=time.time()
	    cur.execute(query)
	    #return 'abc'
	    rows=cur.fetchall()
	    memc.set(key1,rows)
	
	qtime=time.time()
	listingtime=time.time()
        querytime=qtime-starttime
        ttime=listingtime-starttime
        count=0 
	for row in rows:
	    count=count+1
	    results.append(str(row[0]))
	
	cur.close()
        myConnection.close()
	#return str(results)
	
    	return render_template('userInput.html',results=results,queriedtime=querytime,totaltime=ttime)
       
@app.route('/neighbour',methods=['GET','POST'])
def neighbour():
    if request.method == "GET":
	return render_template('neighbour.html')
    results=[]
    if request.method == "POST":
        population1=request.form['population1']
        population2=request.form['population2']
        
        hostname = 'mydbinstance.cmikrvej0mw4.us-west-2.rds.amazonaws.com'
        username = '*****'
        password = '*****'
        database = 'city'
        myConnection = pymysql.connect( host=hostname, user=username, passwd=password, db=database )
        cur = myConnection.cursor()

	##query1="SELECT city, latitude, longitude, 3956 * 2 * ASIN(SQRT( POWER(SIN((" +str(origLat)+" - latitude)*pi()/180/2),2)+COS("+str(origLat)+"*pi()/180 )*COS(latitude*pi()/180)*POWER(SIN(("+str(origLon)+"-longitude)*pi()/180/2),2))) as distance FROM city.CityInfo2 WHERE longitude between ("+str(origLon)+"-"+str(distance)+"/cos(radians("+str(origLat)+"))*69) and ("+str(origLon)+"+"+str(distance)+"/cos(radians("+str(origLat)+"))*69) and latitude between ("+str(origLat)+"-("+str(distance)+"/69)) and ("+str(origLat)+"+("+str(distance)+"/69)) having distance < "+str(distance)+" ORDER BY distance"
	query="(select city, population from city.citypop2 where population between '"+population1+"' and '"+population2+"' limit 10)"
	#return query
	key1 = hashlib.sha256(query).hexdigest()
	starttime=time.time()

	memc = memcache.Client(['mycache.2md5ug.cfg.usw2.cache.amazonaws.com:11211'], debug=1)
        memcheck = memc.get(key1)   
	#return 'abc'
	rows=memcheck
        if not memcheck:
	    starttime=time.time()
	    population1=request.form['population1']
            population2=request.form['population2']

            hostname = 'mydbinstance.cmikrvej0mw4.us-west-2.rds.amazonaws.com'
            username = '*****'
            password = '*****'
            database = 'city'
	    cur.execute(query)
	    rows=cur.fetchall()
	    #return 'abc'
	    memc.set(key1,rows)
	results=[]    
	qtime=time.time()
	listingtime=time.time()
        querytime=qtime-starttime
        ttime=listingtime-starttime
	#rcount=10
	count=0
	#return 'abc'
	#return query
        #for row in rows:
	    #results.append((row[0])+row[1]) 
	#return 'abc'
	for row in rows:
	    count=count+1
	    results.append(str(row[0])+str(row[1]))
	cur.close()
        myConnection.close()
 	#return 'abc'
	return render_template('neighbour.html',results=results,queriedtime=querytime,totaltime=ttime)

if __name__ == '__main__':
   app.run(debug=True)
