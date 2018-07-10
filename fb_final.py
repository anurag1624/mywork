import facebook
import ast
import json
from datetime import datetime

app_id = '123219615201647'
app_secret = '6cc8fbb0757db93359813688a6f15d30'


def face_book(token, id_app='123219615201647',secret_app='6cc8fbb0757db93359813688a6f15d30'):

    fb ={}
    graph = facebook.GraphAPI(access_token=token)
    
    acc_name = ast.literal_eval(json.dumps(graph.get_object(id='me', fields='name')))
    print(acc_name)

    # -----------------------No Of Connections ----------------------
    try:
        friends = ast.literal_eval(json.dumps(graph.get_object(id='me', fields='friends')))
        fb['NoOfConnections'] = friends['friends']['summary']['total_count']
    except:
        fb['NoOfConnections'] = 'Null'

    # --------------------- Marital Status -------------------------
    try:
        relationship_status = ast.literal_eval(json.dumps(graph.get_object(id='me', fields='relationship_status')))
        fb['MaritalStatus'] = relationship_status['relationship_status']
    except:
        fb['MaritalStatus'] = 'Null'

    # -------------------------Education --------------------------------------
    try:
        education = ast.literal_eval(json.dumps(graph.get_object(id='me', fields='education')))
        ed = education['education']
        fb['Qualification'] = zip([li['school']['name'] for li in ed], [li['type'] for li in ed])
    except:
        fb['Qualification'] = 'Null'

    # ---------------------Active Location --------------------------------
    try:
        tagged_places = ast.literal_eval(json.dumps(graph.get_object(id='me', fields='tagged_places')))
        t = tagged_places['tagged_places']['data']
        t1 = [li['place'] for li in t]
        fb['ActiveLocation'] = [li['location']['city'] for li in t1]
    except:
        fb['ActiveLocation'] = 'Null'

    # ------------------- Family ------------------------------------------
    try:
        family = ast.literal_eval(json.dumps(graph.get_object(id='me', fields='family')))
        fa = family['family']['data']
        fb['Family'] = zip([li['name'] for li in fa], [li['relationship'] for li in fa])
    except:
        fb['Family'] = 'Null'

    # ------------------------ Activity rate---------------------
    try:
        updated_time = ast.literal_eval(json.dumps(graph.get_object(id='me', fields='updated_time')))
        updated_time_1 = updated_time['updated_time']
        updated_time_1 = str(updated_time_1)[0:10]
        up_date = datetime.strptime(updated_time_1, '%Y-%m-%d')
        now = datetime.now()
        time_diff_1 = (now-up_date).days/float(30)
        fb['ActivityRate'] = time_diff_1
    except:
        fb['ActivityRate'] = 'Null'

    # -------------------------Present Location-----------------
    try:
        location = ast.literal_eval(json.dumps(graph.get_object(id='me', fields='location')))
        fb['PresentLocation'] = location['location']['name']
    except:
        fb['PresentLocation'] = 'Null'

    # ------------------------Age of account-------------------
    try:
        feeds = ast.literal_eval(json.dumps(graph.get_object(id='me', fields='feed')))
        feed_1 = feeds['feed']['data']        
        time_list = [li['created_time'] for li in feed_1]
        last_creation_time = str(time_list[-1])[0:10]
        date = datetime.strptime(last_creation_time, '%Y-%m-%d')
        now = datetime.now()
        time_diff = (now-date).days/30
        fb['AgeOfAccount'] = time_diff
    except:
        fb['AgeOfAccount'] = 'Null'

    # -----------------------Likes ------------------------------
    try:
        likes = ast.literal_eval(json.dumps(graph.get_object(id='me', fields='likes', limit=100)))
        a = likes['likes']['data']
        fb['Likes'] = list(set([li['name'] for li in a]))
    except:
        fb['Likes'] = 'Null'
    
    try:
        posts = ast.literal_eval(json.dumps(graph.get_object(id='me', fields='posts')))
        p = posts['posts']['data']
        p1 = [{k: v for k, v in d.iteritems() if k == 'message'} for d in p]
        p2 = filter(None, p1)
        keywords = [li['message'] for li in p2]
        words =''
        for word in range(0,len(keywords)):
            words = words + ' ' + keywords[word]
            
        fb['Keywords'] = words.split()
    except:
        fb['Keywords'] = 'Null'    

    # -------------------------Interests--------------------------
    # --------------------------------------------------------------

    # --------------------------Music -------------------------------------
    try:
        music = ast.literal_eval(json.dumps(graph.get_object(id='me', fields='music')))
        m1 = music['music']['data']
        l_music = [li['name'] for li in m1]
    except:
        l_music = 'Null'

    # -----------------Games ------------------------------------
    try:
        games = ast.literal_eval(json.dumps(graph.get_object(id='me', fields='games')))
        m1 = games['games']['data']
        l_games = [li['name'] for li in m1]
    except:
        l_games = 'Null'

    # -----------------Books ------------------------------------
    try:
        books = ast.literal_eval(json.dumps(graph.get_object(id='me', fields='books')))
        bl = books['books']['data']
        l_books = [li['name'] for li in bl]
    except:
        l_books = 'Null'

    # -----------------Sports ------------------------------------
    try:
        sports = ast.literal_eval(json.dumps(graph.get_object(id='me', fields='sports')))
        sl = sports['sports']['data']
        l_sports = [li['name'] for li in sl]
    except:
        l_sports = 'Null'

    # -------------------------Movies------------------------------------
    try:
        movies = ast.literal_eval(json.dumps(graph.get_object(id='me', fields='movies')))
        m = movies['movies']['data']
        l_movies = [li['name'] for li in m]
    except:
        l_movies = 'Null'

    # --------------------television ------------------------
    try:
        television = ast.literal_eval(json.dumps(graph.get_object(id='me', fields='television')))
        te = television['television']['data']
        l_television = [li['name'] for li in te]
    except:
        l_television = 'Null'
    l_interest = []
    interests = {'Books': l_books,'Games': l_games,'Movies': l_movies,
                 'Music': l_music,'Sports': l_sports,
                 'Television': l_television}
    for inter in interests.keys():
        if interests[inter] != 'Null':
            l_interest.append(inter)
    fb["Interests"] = l_interest

    # ---------------- Mobile Number -----------------
    try:
        rmn = ast.literal_eval(json.dumps(graph.get_object(id='me', fields='user_phone_number')))
        mob = rmn['user_phone_number']
        fb['RMN'] = mob
    except:
        fb['RMN'] = 'Null'

    # -------------------------- Birth Day ------------------------------
    ''' try:
        birthday = ast.literal_eval(json.dumps(graph.get_object(id='1755063324552817', fields='birthday')))
    #print(birthday)
        fb['birthday'] = birthday['birthday']
    except:
        fb['birthday'] = 'Null'
    
    #  ------------------------Name -----------------------------------
    name = ast.literal_eval(json.dumps(graph.get_object(id='me', fields='name')))
    fb['Name'] = name['name']

    '''
    # --------------------Device----------------------------------------
    '''try:
        devices = ast.literal_eval(json.dumps(graph.get_object(id='me', fields='devices')))
        fb['devices'] = devices['devices'][0]['os']
    except:
        fb['devices'] = 'Null'


    try:
        gender = ast.literal_eval(json.dumps(graph.get_object(id='me', fields='gender')))
        fb['gender'] = gender['gender']
    except:
        fb['gender'] = 'Null'
    '''
    # --------------------------- E mail ----------------------------------------
    ''' try:
        email = ast.literal_eval(json.dumps(graph.get_object(id='me', fields='email')))
        fb['email'] = email['email']
    except:
        fb['email'] = 'Null'
    '''
    # ----------------------- Home Town ------------------------------------
    ''' try:
        hometown = ast.literal_eval(json.dumps(graph.get_object(id='me', fields='hometown')))
        fb['hometown'] = hometown['hometown']['name']
    except:
        fb['hometown'] = 'Null'
    '''
    # --------------------television ------------------------
    '''try:
        television = ast.literal_eval(json.dumps(graph.get_object(id='me', fields='television')))
        te = television['television']['data']
        fb['television'] = [li['name'] for li in te]
    except:
        fb['television'] = 'Null'
    '''
        
    return fb

# fb = face_book(access_token,app_id,app_secret)

# data = pd.DataFrame({'FB Detail': fb.keys(),'Value':fb.values()})

# data.to_csv("fb_analysis.csv",index = False)


