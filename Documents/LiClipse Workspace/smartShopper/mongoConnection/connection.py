'''
Created on Dec 30, 2015

@author: ugupta
'''
import json
from pymongo import MongoClient
from collections import Counter
client = MongoClient()

client =  MongoClient('mongodb://admin:abcd1234@ds043002.mongolab.com:43002/sgm_demo')

def linear_regression(x, y):
    #x --> number days between two purchase date. An array
    #y --> number of items purchased. An array
    length = len(x)
    sum_x = sum(x)
    sum_y = sum(y)

 
    sum_x_squared = sum(map(lambda a: a * a, x))
    sum_of_products = sum([x[i] * y[i] for i in range(length)])

    a = (sum_of_products - (sum_x * sum_y) / length) / (sum_x_squared - ((sum_x ** 2) / length))
    b = (sum_y - a * sum_x) / length
    return a, b



if __name__ == '__main__':
    db = client.sgm_demo
    
    all_user =  db.user.find({},{"_id":1})
    
    all_item = db.item_details.find({},{"_id":1})
    
    purchase_dates = []
    quantity = []
    items = []
    itemid = []  
    userItems = {}	 

    for item in all_item:
        itemid.append(item["_id"])
        
    for user in all_user:
	items_purchased = []
	itemref = []
	all_purchsed_grocery = db.grocery_list.find({'listbought':True, 'user':user['_id']})    
        for grocery_list in all_purchsed_grocery:
        	items_purchased.append(grocery_list['listitems'])           
        	for items in items_purchased:
			for i in items:
                	        if i["itemref"] in itemid:
				    itemref.append(i["itemref"])	
        userItems[user['_id']]=Counter(itemref)
    print(userItems)	
        
        
        
    
    
