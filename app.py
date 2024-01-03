
#----------------------------------- Import Libraries---------------------------------------------------
from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np 
import pandas as pd 

app = Flask(__name__)

#-----------------------------------Load DataFrame and File---------------------------------------------

with open("popular_df.pkl","rb") as file:
    popular_df = pickle.load(file)

with open('pt.pkl','rb') as file:
    pt = pickle.load(file)
    
with open('books.pkl','rb') as file:
    books = pickle.load(file)

with open('similarity_scores.pkl','rb') as file:
    similarity_scores = pickle.load(file)


#--------------------------------Home Page-------------------------------------------------------------
@app.route("/")
def Home_App():
    return render_template("index.html",
                           book_name = list(popular_df['Book-Title'].values),
                           author = list(popular_df['Book-Author'].values),
                           image = list(popular_df['Image-URL-M'].values),
                           votes = list(popular_df['num_rating'].values),
                           rating = list(popular_df['avg_rating'].values))


#-------------------------------Recommended------------------------------------------------------------
@app.route("/recommend")
def recommend():
    return render_template("recommend.html")

#------------------------------Recommended
@app.route("/recommended_books" , methods=['POST'])
def recommend_books():
    user_input = request.form.get('user_input')
    
    # index fectch
    index = np.where(pt.index==user_input)[0][0]
    # similarity score of this index >> book
    similar_items = sorted(list(enumerate(similarity_scores[index])),key=lambda x: x[1], reverse=True)[1:9] # 1 to 6 books
    data = []
    for i in similar_items:
        item = []
        #print(pt.index[i[0]])   # Book Index  
        temp_df = books[books['Book-Title']==pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        
        data.append(item)
    print(data)
    return render_template('recommend.html',data=data)



if __name__=="__main__":
    app.run(debug=True, port=8080, host="0.0.0.0")




