from django.shortcuts import render,redirect
from .forms import usernameForm
from django.contrib import messages
from django.contrib.auth.models import User
from .utils import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

#import mpld3
import time
import pickle

from face_recognition.face_recognition_cli import image_files_in_folder
from imutils.face_utils import rect_to_bb
from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import KNeighborsClassifier

# from attendance_system_facial_recognition.settings import BASE_DIR

from django.http import HttpResponse

mpl.use('Agg')

# Create your views here.
# def home(request):
#     return render(request, 'attendance/recognition/home.html')

@login_required
def dashboard(request):
	if(request.user.username=='admin'):
		print("admin")
		return render(request, 'attendance/recognition/admin_dashboard.html')
	else:
		print("not admin")
		return render(request,'attendance/recognition/employee_dashboard.html')


@login_required
def user_register(request):
	if request.user.username!='admin':
		return redirect('not-authorised')
	if request.method=='POST':
		form=UserCreationForm(request.POST)
		if form.is_valid():
			form.save() ###add user to database
			messages.success(request, f'Employee registered successfully!')
			return redirect('dashboard')
	else:
		form=UserCreationForm()
	return render(request,'attendance/users/register.html', {'form' : form})


@login_required
def add_photos(request):
    if request.user.username!='admin':
        return redirect('not-authorised')
    if request.method=='POST':
        form=usernameForm(request.POST)
        data = request.POST.copy()
        username=data.get('username')
        if username_present(username):
            create_dataset(username)
            messages.success(request, f'Dataset Created')
            return redirect('add-photos')
        else:
            messages.warning(request, f'No such username found. Please register employee first.')
            return redirect('dashboard')
    else:
        form=usernameForm()
        return render(request,'attendance/recognition/add_photos.html', {'form' : form})

#training the model
@login_required
def train(request):
    main_dir = "D:/Soham/Genuis vision/classicGroup/attendance/face_recognition_data"
    if request.user.username!='admin':
        return redirect('not-authorised')

    training_dir=f'{main_dir}/training_dataset'
    count=0
    for person_name in os.listdir(training_dir):
        curr_directory=os.path.join(training_dir,person_name)
        if not os.path.isdir(curr_directory):
            continue
        for imagefile in image_files_in_folder(curr_directory):
            count+=1

    X=[]
    y=[]
    i=0


    for person_name in os.listdir(training_dir):
        print(str(person_name))
        curr_directory=os.path.join(training_dir,person_name)
        if not os.path.isdir(curr_directory):
            continue
        for imagefile in image_files_in_folder(curr_directory):
            print(str(imagefile))
            image=cv2.imread(imagefile)
            try:
                X.append((face_recognition.face_encodings(image)[0]).tolist())
                y.append(person_name)
                i+=1
            except:
                print("removed")
                os.remove(imagefile)

    targets=np.array(y)
    encoder = LabelEncoder()
    encoder.fit(y)
    y=encoder.transform(y)
    X1=np.array(X)
    print("shape: "+ str(X1.shape))
    np.save(f'{main_dir}/classes.npy', encoder.classes_)
    svc = SVC(kernel='linear',probability=True)
    svc.fit(X1,y)
    svc_save_path=f"{main_dir}/svc.sav"
    with open(svc_save_path, 'wb') as f:
        pickle.dump(svc,f)
	
    # vizualize_Data(X1,targets)
    messages.success(request, f'Training Complete.')
    return render(request,"recognition/train.html")

#marking punch-in view
def mark_your_attendance(request):
    
    main_dir = "D:/Soham/Genuis vision/classicGroup/attendance/face_recognition_data"
    
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(f"{main_dir}/shape_predictor_68_face_landmarks.dat")   #Add path to the shape predictor ######CHANGE TO RELATIVE PATH LATER
    svc_save_path=f"{main_dir}/svc.sav"	
			
    with open(svc_save_path, 'rb') as f:
            svc = pickle.load(f)
    fa = FaceAligner(predictor , desiredFaceWidth = 96)
    encoder=LabelEncoder()
    encoder.classes_ = np.load(f'{main_dir}/classes.npy')


    faces_encodings = np.zeros((1,128))
    no_of_faces = len(svc.predict_proba(faces_encodings)[0])
    count = dict()
    present = dict()
    log_time = dict()
    start = dict()
    for i in range(no_of_faces):
        count[encoder.inverse_transform([i])[0]] = 0
        present[encoder.inverse_transform([i])[0]] = False

    vs = VideoStream(src=0).start()
    sampleNum = 0
    while(True):
        
        frame = vs.read()
        
        frame = imutils.resize(frame ,width = 800)
        
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        faces = detector(gray_frame,0)
        
        


        for face in faces:
            print("INFO : inside for loop")
            (x,y,w,h) = face_utils.rect_to_bb(face)

            face_aligned = fa.align(frame,gray_frame,face)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),1)
                    
            
            (pred,prob)=predict(face_aligned,svc)
            

            
            if(pred!=[-1]):
                
                person_name=encoder.inverse_transform(np.ravel([pred]))[0]
                pred=person_name
                if count[pred] == 0:
                    start[pred] = time.time()
                    count[pred] = count.get(pred,0) + 1

                if count[pred] == 2 and (time.time()-start[pred]) > 1.2:
                    count[pred] = 0
                else:
                #if count[pred] == 4 and (time.time()-start) <= 1.5:
                    present[pred] = True
                    log_time[pred] = datetime.datetime.now()
                    count[pred] = count.get(pred,0) + 1
                    print(pred, present[pred], count[pred])
                cv2.putText(frame, str(person_name)+ str(prob), (x+6,y+h-6), cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,0),1)

            else:
                person_name="unknown"
                cv2.putText(frame, str(person_name), (x+6,y+h-6), cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,0),1)
            
            
            #cv2.putText()
            # Before continuing to the next loop, I want to give it a little pause
            # waitKey of 100 millisecond
            #cv2.waitKey(50)

        #Showing the image in another window
        #Creates a window with window name "Face" and with the image img
        cv2.imshow("Mark Attendance - In - Press q to exit",frame)
        #Before closing it we need to give a wait command, otherwise the open cv wont work
        # @params with the millisecond of delay 1
        #cv2.waitKey(1)
        #To get out of the loop
        key=cv2.waitKey(50) & 0xFF
        if(key==ord("q")):
            break

    #Stoping the videostream
    vs.stop()

    # destroying all the windows
    cv2.destroyAllWindows()
    update_attendance_in_db_in(present)
    return redirect('home')


#marking punch-out view
def mark_your_attendance_out(request):
	
    main_dir = "D:/Soham/Genuis vision/classicGroup/attendance/face_recognition_data"
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(f"{main_dir}/shape_predictor_68_face_landmarks.dat")   #Add path to the shape predictor ######CHANGE TO RELATIVE PATH LATER
    svc_save_path=f"{main_dir}/svc.sav"	
			
    with open(svc_save_path, 'rb') as f:
            svc = pickle.load(f)
    fa = FaceAligner(predictor , desiredFaceWidth = 96)
    encoder=LabelEncoder()
    encoder.classes_ = np.load(f'{main_dir}/classes.npy')

    faces_encodings = np.zeros((1,128))
    no_of_faces = len(svc.predict_proba(faces_encodings)[0])
    count = dict()
    present = dict()
    log_time = dict()
    start = dict()
    for i in range(no_of_faces):
        count[encoder.inverse_transform([i])[0]] = 0
        present[encoder.inverse_transform([i])[0]] = False

    vs = VideoStream(src=0).start()

    sampleNum = 0
	
    while(True):
        
        frame = vs.read()
        
        frame = imutils.resize(frame ,width = 800)
        
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        faces = detector(gray_frame,0)
        
        for face in faces:
            print("INFO : inside for loop")
            (x,y,w,h) = face_utils.rect_to_bb(face)

            face_aligned = fa.align(frame,gray_frame,face)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),1)
                    
            
            (pred,prob)=predict(face_aligned,svc)
            

            
            if(pred!=[-1]):
                
                person_name=encoder.inverse_transform(np.ravel([pred]))[0]
                pred=person_name
                if count[pred] == 0:
                    start[pred] = time.time()
                    count[pred] = count.get(pred,0) + 1

                if count[pred] == 4 and (time.time()-start[pred]) > 1.5:
                    count[pred] = 0
                else:
                #if count[pred] == 4 and (time.time()-start) <= 1.5:
                    present[pred] = True
                    log_time[pred] = datetime.datetime.now()
                    count[pred] = count.get(pred,0) + 1
                    print(pred, present[pred], count[pred])
                cv2.putText(frame, str(person_name)+ str(prob), (x+6,y+h-6), cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,0),1)

            else:
                person_name="unknown"
                cv2.putText(frame, str(person_name), (x+6,y+h-6), cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,0),1)
            
            #cv2.putText()
            # Before continuing to the next loop, I want to give it a little pause
            # waitKey of 100 millisecond
            #cv2.waitKey(50)

        #Showing the image in another window
        #Creates a window with window name "Face" and with the image img
        cv2.imshow("Mark Attendance- Out - Press q to exit",frame)
        #Before closing it we need to give a wait command, otherwise the open cv wont work
        # @params with the millisecond of delay 1
        #cv2.waitKey(1)
        #To get out of the loop
        key=cv2.waitKey(50) & 0xFF
        if(key==ord("q")):
            break

    #Stoping the videostream
    vs.stop()

    # destroying all the windows
    cv2.destroyAllWindows()
    update_attendance_in_db_out(present)
    return redirect('home')


#attendance report views
def view_attendance_home(request):
    return HttpResponse('Attendance home!')

def view_attendance_date(request):
    return HttpResponse('Attendance date!')

def view_attendance_employee(request):
    return HttpResponse('Attendance employee')

def view_my_attendance_employee_login(request):
    return HttpResponse('Attendance employee')
    
@login_required
def not_authorised(request):
	return render(request,'attendance/recognition/not_authorised.html')