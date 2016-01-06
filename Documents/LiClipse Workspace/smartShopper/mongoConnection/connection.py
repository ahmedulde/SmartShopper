'''
Created on Dec 30, 2015

@author: ugupta
'''

from pymongo import MongoClient

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
    
    x = 
        
        
        