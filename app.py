from flask import Flask
from flask import render_template
from flask import request
import csv
from matplotlib import pyplot as plt
import matplotlib
matplotlib.use('Agg')

with open('data.csv') as f:
    l = []
    reader = csv.DictReader(f)
    for row in reader:
        l.append(row)
f.close()

app = Flask(__name__)

@app.route("/",methods = ["GET","POST"])

def index_page():
	if request.method == "GET":
		return render_template("index.html")



	if request.method == "POST":
		#Value of radio button
		radio_selected = request.form["ID"]
		#typed input value
		value_typed = request.form["id_value"]

		#READ THE FILE
		x = csv.DictReader(open('data.csv'))
		data_old,data = [],[]
		for i in x:
			data_old.append(i)
		#CLEANING THE KEYS OF THE FILE
		for i in data_old:
			d1 = {'Student id':'Student id', ' Course id':'Course id', ' Marks':'Marks'}
			data.append(dict((d1[key], value) for (key, value) in i.items()))
		#CLEANING THE VALUES OF THE FILE
		for i in data:
			i['Student id']=i['Student id'].strip()
			i['Course id']=i['Course id'].strip()
			i['Marks']=i['Marks'].strip()

		#NOW WE DIVIDE BETWEEN COURSE ID OR STUDENT ID 
		if radio_selected == 'student_id':
			student_data = []
			for i in data:
				if i["Student id"]==str(value_typed):
					student_data.append(i)



			if student_data ==[]:
				return render_template('error.html')
			else:
				count = 0
				for i in student_data:
					count+=int(i["Marks"])
				return render_template("students.html",data = student_data,radio = radio_selected,value = value_typed, total = count)
		#COURSE ID CHOSEN
		if radio_selected == 'course_id':
			course_data = []
			for i in data:
				if i["Course id"]==str(value_typed):
					course_data.append(i)
			if course_data ==[]:
				return render_template('error.html')

			else:
				marks = []
				for i in course_data:
					marks.append(int(i["Marks"]))
				av_marks = sum(marks)/len(marks)
				max_marks = max(marks)

				marks = []
				for i in course_data:
					marks.append(int(i["Marks"]))
				
				x = marks
				plt.clf()
				plt.xlabel("Marks")
				plt.ylabel("Frequency")
				plt.hist(x, bins = 10)
				plt.savefig('static/histogram.png')
				return render_template("courses.html",data = course_data,radio = radio_selected,value = value_typed, average_marks = av_marks,maximum_marks = max_marks)

if __name__  == "__main__":
	app.debug = True#checks for errors before running the app
	#THis should be false in production else it may leak some sensitive info
	app.run()