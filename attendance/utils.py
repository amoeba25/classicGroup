#Helper functions 

#List of utility functions used in views
from django.contrib.auth.models import User
from .models import Present, Time


import os
import dlib
from imutils.face_utils import FaceAligner
from imutils.video import VideoStream
import cv2
import imutils
from imutils import face_utils
import face_recognition
from sklearn.svm import SVC
import matplotlib as mpl
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from django_pandas.io import read_frame
import seaborn as sns
import pandas as pd
from pandas.plotting import register_matplotlib_converters
from matplotlib import rcParams

import numpy as np
import datetime
import math




from django.db.models import Count


def username_present(username):
    '''
    param-username : input a username
    returns if username present or not
    '''
    if User.objects.filter(username = username).exists():
        return True
    return False


def create_dataset(username):
    '''
    param-username : creates the dataset of the username
    
    returns a created database of different images
    '''
    id = username
    path = f'D:/Soham/Genuis vision/classicGroup/attendance/face_recognition_data/training_dataset/{id}'
    
    
    #checking if training data for user exists
    if os.path.exists(path) == False:
        os.makedirs(path)
    directory = path
    
	# Detect face
	#Loading the HOG face detector and the shape predictpr for allignment
    print("[INFO] Loading the facial detector")
    detector = dlib.get_frontal_face_detector() #HOG + SVM modificaation
    # data_path = os.path.join(os.getcwd(), "attendance\face_recognition_data\shape_predictor_68_face_landmarks.dat")
    # print(data_path)
    
    predictor = dlib.shape_predictor("D:/Soham/Genuis vision/classicGroup/attendance/face_recognition_data/shape_predictor_68_face_landmarks.dat")   #Add path to the shape predictor ######CHANGE TO RELATIVE PATH LATER
    fa = FaceAligner(predictor , desiredFaceWidth = 96)
    
    #capture images from the webcam and process and detect the face
    # Initialize the video stream
    print("[INFO] Initializing Video stream")
    vs = VideoStream(src=0).start()
	#time.sleep(2.0) ####CHECK######
	
	# Our dataset naming counter
    sampleNum = 0
    
    # Capturing the faces one by one and detect the faces and showing it on the window
    while(True):
        # Capturing the image
        #vs.read each frame
        frame = vs.read()
        #Resize each image
        frame = imutils.resize(frame ,width = 800)
        #the returned img is a colored image but for the classifier to work we need a greyscale image
        #to convert
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #To store the faces
        #This will detect all the images in the current frame, and it will return the coordinates of the faces
        #Takes in image and some other parameter for accurate result
        faces = detector(gray_frame,0)
        #In above 'faces' variable there can be multiple faces so we have to get each and every face and draw a rectangle around it.
        for face in faces:
            print("inside for loop")
            (x,y,w,h) = face_utils.rect_to_bb(face)
            face_aligned = fa.align(frame,gray_frame,face)
            # Whenever the program captures the face, we will write that is a folder
            # Before capturing the face, we need to tell the script whose face it is
            # For that we will need an identifier, here we call it id
            # So now we captured a face, we need to write it in a file
            sampleNum = sampleNum+1
            # Saving the image dataset, but only the face part, cropping the rest
            
            if face is None:
                print("face is none")
                continue
            cv2.imwrite(directory+'/'+str(sampleNum)+'.jpg'	, face_aligned)
            face_aligned = imutils.resize(face_aligned ,width = 400)
            #cv2.imshow("Image Captured",face_aligned)
            # @params the initial point of the rectangle will be x,y and
            # @params end point will be x+width and y+height
            # @params along with color of the rectangle
            # @params thickness of the rectangle
            
            #draws a bounding box
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),1)
            # Before continuing to the next loop, I want to give it a little pause
            # waitKey of 100 millisecond
            cv2.waitKey(50)

        #Showing the image in another window
        #Creates a window with window name "Face" and with the image img
        cv2.imshow("Add Images",frame)
        #Before closing it we need to give a wait command, otherwise the open cv wont work
        # @params with the millisecond of delay 1
        cv2.waitKey(1)
        #To get out of the loop
        if(sampleNum>300):
            break

    #Stoping the videostream
    vs.stop()
    # destroying all the windows
    cv2.destroyAllWindows()

#predicting whose face
def predict(face_aligned,svc,threshold=0.7):
    '''
    param - face_aligned : 
    param - svc : the SVC classifier
    param - threshold : theshold amount for prediction
    
    returns the predicted prob if more than threshold
    '''
    face_encodings=np.zeros((1,128))
    try:
        x_face_locations=face_recognition.face_locations(face_aligned)
        faces_encodings=face_recognition.face_encodings(face_aligned,known_face_locations=x_face_locations)
        if(len(faces_encodings)==0):
            return ([-1],[0])
    except:
        return ([-1],[0])
    prob=svc.predict_proba(faces_encodings)
    result=np.where(prob[0]==np.amax(prob[0]))
    if(prob[0][result[0]]<=threshold):
        return ([-1],prob[0][result[0]])

    return (result[0],prob[0][result[0]])

#visualising the data
def vizualize_Data(embedded, targets,):
    '''
    
    returns a plot
    '''
    X_embedded = TSNE(n_components=2).fit_transform(embedded)
    for i, t in enumerate(set(targets)):
        idx = targets == t
        plt.scatter(X_embedded[idx, 0], X_embedded[idx, 1], label=t)
    plt.legend(bbox_to_anchor=(1, 1));
    rcParams.update({'figure.autolayout': True})
    plt.tight_layout()	
    plt.savefig('./recognition/static/recognition/img/training_visualisation.png')
    plt.close()


#updates the punch in the db
def update_attendance_in_db_in(present):
    
    #gets current date and time
	today=datetime.date.today()
	time=datetime.datetime.now()
    
	for person in present:
            user = User.objects.get(username=person)
            try:
                qs=Present.objects.get(user=user,date=today)
            except :
                qs= None
            
            if qs is None:
                if present[person]==True:
                            a=Present(user=user,date=today,present=True)
                            a.save()
                else:
                    a=Present(user=user,date=today,present=False)
                    a.save()
            else:
                if present[person]==True:
                    qs.present=True
                    qs.save(update_fields=['present'])
            if present[person]==True:
                a=Time(user=user,date=today,time=time, out=False)
                a.save()

#updates the punch out in the db
def update_attendance_in_db_out(present):
	today=datetime.date.today()
	time=datetime.datetime.now()
	for person in present:
		user=User.objects.get(username=person)
		if present[person]==True:
			a=Time(user=user,date=today,time=time, out=True)
			a.save()
		



def check_validity_times(times_all):

	if(len(times_all)>0):
		sign=times_all.first().out
	else:
		sign=True
	times_in=times_all.filter(out=False)
	times_out=times_all.filter(out=True)
	if(len(times_in)!=len(times_out)):
		sign=True
	break_hourss=0
	if(sign==True):
			check=False
			break_hourss=0
			return (check,break_hourss)
	prev=True
	prev_time=times_all.first().time

	for obj in times_all:
		curr=obj.out
		if(curr==prev):
			check=False
			break_hourss=0
			return (check,break_hourss)
		if(curr==False):
			curr_time=obj.time
			to=curr_time
			ti=prev_time
			break_time=((to-ti).total_seconds())/3600
			break_hourss+=break_time


		else:
			prev_time=obj.time

		prev=curr

	return (True,break_hourss)


def convert_hours_to_hours_mins(hours):
	h=int(hours)
	hours-=h
	m=hours*60
	m=math.ceil(m)
	return str(str(h)+ " hrs " + str(m) + "  mins")


#used
def hours_vs_date_given_employee(present_qs,time_qs,admin=True):
	register_matplotlib_converters()
	df_hours=[]
	df_break_hours=[]
	qs=present_qs

	for obj in qs:
		date=obj.date
		times_in=time_qs.filter(date=date).filter(out=False).order_by('time')
		times_out=time_qs.filter(date=date).filter(out=True).order_by('time')
		times_all=time_qs.filter(date=date).order_by('time')
		obj.time_in=None
		obj.time_out=None
		obj.hours=0
		obj.break_hours=0
		if (len(times_in)>0):			
			obj.time_in=times_in.first().time
			
		if (len(times_out)>0):
			obj.time_out=times_out.last().time

		if(obj.time_in is not None and obj.time_out is not None):
			ti=obj.time_in
			to=obj.time_out
			hours=((to-ti).total_seconds())/3600
			obj.hours=hours
		

		else:
			obj.hours=0

		(check,break_hourss)= check_validity_times(times_all)
		if check:
			obj.break_hours=break_hourss


		else:
			obj.break_hours=0


		
		df_hours.append(obj.hours)
		df_break_hours.append(obj.break_hours)
		obj.hours=convert_hours_to_hours_mins(obj.hours)
		obj.break_hours=convert_hours_to_hours_mins(obj.break_hours)
			
	
	
	
	df = read_frame(qs)	
	
	
	df["hours"]=df_hours
	df["break_hours"]=df_break_hours

	print(df)
	
	sns.barplot(data=df,x='date',y='hours')
	plt.xticks(rotation='vertical')
	rcParams.update({'figure.autolayout': True})
	plt.tight_layout()
	if(admin):
		plt.savefig('./recognition/static/recognition/img/attendance_graphs/hours_vs_date/1.png')
		plt.close()
	else:
		plt.savefig('./recognition/static/recognition/img/attendance_graphs/employee_login/1.png')
		plt.close()
	return qs
	

#used
def hours_vs_employee_given_date(present_qs,time_qs):
	register_matplotlib_converters()
	df_hours=[]
	df_break_hours=[]
	df_username=[]
	qs=present_qs

	for obj in qs:
		user=obj.user
		times_in=time_qs.filter(user=user).filter(out=False)
		times_out=time_qs.filter(user=user).filter(out=True)
		times_all=time_qs.filter(user=user)
		obj.time_in=None
		obj.time_out=None
		obj.hours=0
		obj.hours=0
		if (len(times_in)>0):			
			obj.time_in=times_in.first().time
		if (len(times_out)>0):
			obj.time_out=times_out.last().time
		if(obj.time_in is not None and obj.time_out is not None):
			ti=obj.time_in
			to=obj.time_out
			hours=((to-ti).total_seconds())/3600
			obj.hours=hours
		else:
			obj.hours=0
		(check,break_hourss)= check_validity_times(times_all)
		if check:
			obj.break_hours=break_hourss


		else:
			obj.break_hours=0

		
		df_hours.append(obj.hours)
		df_username.append(user.username)
		df_break_hours.append(obj.break_hours)
		obj.hours=convert_hours_to_hours_mins(obj.hours)
		obj.break_hours=convert_hours_to_hours_mins(obj.break_hours)

	



	df = read_frame(qs)	
	df['hours']=df_hours
	df['username']=df_username
	df["break_hours"]=df_break_hours


	sns.barplot(data=df,x='username',y='hours')
	plt.xticks(rotation='vertical')
	rcParams.update({'figure.autolayout': True})
	plt.tight_layout()
	plt.savefig('./recognition/static/recognition/img/attendance_graphs/hours_vs_employee/1.png')
	plt.close()
	return qs


#getting all the empolyees
def total_number_employees():
	qs=User.objects.all()
	return (len(qs) -1)
	# -1 to account for admin 


#getting which employees present
def employees_present_today():
	today=datetime.date.today()
	qs=Present.objects.filter(date=today).filter(present=True)
	return len(qs)


#used	
def this_week_emp_count_vs_date():
	today=datetime.date.today()
	some_day_last_week=today-datetime.timedelta(days=7)
	monday_of_last_week=some_day_last_week-  datetime.timedelta(days=(some_day_last_week.isocalendar()[2] - 1))
	monday_of_this_week = monday_of_last_week + datetime.timedelta(days=7)
	qs=Present.objects.filter(date__gte=monday_of_this_week).filter(date__lte=today)
	str_dates=[]
	emp_count=[]
	str_dates_all=[]
	emp_cnt_all=[]
	cnt=0
	for obj in qs:
		date=obj.date
		str_dates.append(str(date))
		qs=Present.objects.filter(date=date).filter(present=True)
		emp_count.append(len(qs))
	while(cnt<5):
		date=str(monday_of_this_week+datetime.timedelta(days=cnt))
		cnt+=1
		str_dates_all.append(date)
		if(str_dates.count(date))>0:
			idx=str_dates.index(date)

			emp_cnt_all.append(emp_count[idx])
		else:
			emp_cnt_all.append(0)
	df=pd.DataFrame()
	df["date"]=str_dates_all
	df["Number of employees"]=emp_cnt_all
	
	sns.lineplot(data=df,x='date',y='Number of employees')
	plt.savefig('./recognition/static/recognition/img/attendance_graphs/this_week/1.png')
	plt.close()

#used
def last_week_emp_count_vs_date():
	today=datetime.date.today()
	some_day_last_week=today-datetime.timedelta(days=7)
	monday_of_last_week=some_day_last_week-  datetime.timedelta(days=(some_day_last_week.isocalendar()[2] - 1))
	monday_of_this_week = monday_of_last_week + datetime.timedelta(days=7)
	qs=Present.objects.filter(date__gte=monday_of_last_week).filter(date__lt=monday_of_this_week)
	str_dates=[]
	emp_count=[]


	str_dates_all=[]
	emp_cnt_all=[]
	cnt=0

	for obj in qs:
		date=obj.date
		str_dates.append(str(date))
		qs=Present.objects.filter(date=date).filter(present=True)
		emp_count.append(len(qs))

	while(cnt<2):

		date=str(monday_of_last_week+datetime.timedelta(days=cnt))
		cnt+=1
		str_dates_all.append(date)
		if(str_dates.count(date))>0:
			idx=str_dates.index(date)

			emp_cnt_all.append(emp_count[idx])
			
		else:
			emp_cnt_all.append(0)

	df=pd.DataFrame()
	df["date"]=str_dates_all
	df["emp_count"]=emp_cnt_all
	
	sns.lineplot(data=df,x='date',y='emp_count')
	plt.savefig('./recognition/static/recognition/img/attendance_graphs/last_week/1.png')
	plt.close()


