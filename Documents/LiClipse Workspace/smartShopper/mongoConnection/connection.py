from pymongo import MongoClient
import datetime

client = MongoClient()

client =  MongoClient('mongodb://admin:abcd1234@ds043002.mongolab.com:43002/sgm_demo')


def linear_regression(x, y):
    length = len(x)
    sum_x = sum(x)
    sum_y = sum(y)
    
    
    sum_x_squared = sum(map(lambda a: a * a, x))
    sum_of_products = sum([x[i] * y[i] for i in range(length)])
    
    a = (sum_of_products - (sum_x * sum_y) / length) / (sum_x_squared - ((sum_x ** 2) / length))
    b = (sum_y - a * sum_x) / length
    return a, b

def datetime2daysindifference(x):
    no_days = len(x)
    #print("num of days: "+ str(no_days))
    diff_dates = []
    diff_dates.append(0)
    for i in range(0, no_days-1):
        date1 = x[i]
        date2 = x[i+1]
        diff = date2 - date1
        second_diff = diff.total_seconds()
        day_diff =  int(second_diff/(24*60*60))
        diff_dates.append(int(day_diff))
    #print(diff_dates)
    return diff_dates
 
if __name__ == '__main__':
    db = client.sgm_demo
    
    all_user =  db.user.find({},{"_id":1})
    
    all_item = db.item_details.find({},{"_id":1})

    items = []
    
    '''
    for item in all_item:
            for user in all_user:
            #printing  users
            print(user)
            #'listbought':True, 'user':user['_id'], 'listitems.itemref':item['_id']
            all_purchsed_grocery = db.grocery_list.find({'listbought':True, 'user':user['_id']})
                
            for g in all_purchsed_grocery:
                
                print(g['listitems.itemref'])
                
    '''  
    itemid = []  
    userItems = {}     

    for item in all_item:
        itemid.append(item["_id"])
          
    for user in all_user:
        items_purchased = []
        #printing  users
        #print(user)
        itemref = []
        all_purchsed_grocery = db.grocery_list.find({'listbought':True, 'user':user['_id']})    
        item_bought = []
        days_bought = []
        quantity = []
        for grocery_list in all_purchsed_grocery:
            for items in grocery_list["listitems"]:
                item_bought.append(items["itemref"])
                days_bought.append(items["bought_at"])
                quantity.append(items["quantity"])
        #print(item_bought)
        #print(days_bought)
        #print(quantity)
        
        for j in itemid:
            date_bought = []
            quant = []
            for k in range(0, len(item_bought)):
                if j == item_bought[k]:
                    date_bought.append(days_bought[k])
                    quant.append(quantity[k])
            if len(date_bought) != 0:
                diff_days = datetime2daysindifference(date_bought)
                a,b = linear_regression(diff_days, quant)
                print(a,b)
                date = date_bought[len(date_bought)-1] + datetime.timedelta(days=a)
                print(date)
                previous_prediction = db.predictions.find({'userid':user , 'itemref':j})
                if previous_prediction.count() == 0:
                    predict = ({"userid":user, "itemref":j, "next_date":date, "predict_quantity":b , "lastModified": datetime.datetime.now()} )
                    db.predictions.insert(predict)
                else:
                    db.inventory.update({ "userid": user, "itemref":j },{ "$set": {"next_date": date, "predict_quantity":b}, "$currentDate": { "lastModified":True}})
                