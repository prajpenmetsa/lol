import psycopg2
from flask import Flask, render_template, jsonify, request, redirect, url_for, make_response
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, set_access_cookies, unset_jwt_cookies
from flask_bcrypt import Bcrypt
from io import BytesIO
from psycopg2 import Binary
import cv2
import base64
import numpy as np
import os
import uuid
import base64
from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip
from moviepy.video.fx.all import fadein, fadeout

app = Flask(__name__)
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_ACCESS_COOKIE_PATH'] = '/api/'
app.config['JWT_REFRESH_COOKIE_PATH'] = '/token/refresh'
app.config['JWT_COOKIE_CSRF_PROTECT'] = False
app.config['JWT_SECRET_KEY'] = 'super-secret'
jwt = JWTManager(app)

def get_db_connection():
    cert_decoded = base64.b64decode(os.environ['R00T_CERT_BASE64'])
    cert_path = '/opt/render/.postgresql/root.crt'
    os.makedirs(os.path.dirname(cert_path), exist_ok=True)
    with open(cert_path, 'wb') as cert_file: 
        cert_file.write(cert_decoded)

get_db_connection()

db = psycopg2.connect("postgresql://lakshmi:-wsuF7g_tKtqKXTFAm4huw@iss-group-3-4110.7s5.aws-ap-south-1.cockroachlabs.cloud:26257/defaultdb?sslmode=verify-full")
cursor = db.cursor()

# Initialize Bcrypt for password hashing
bcrypt = Bcrypt()

# Mock database of users (you can replace this with your actual user fetching method)
def fetch_user(username):
    print(username)
    query = "SELECT * FROM user_info WHERE username = %s;"
    cursor.execute(query, (username,))
    x = cursor.fetchone()
    return x

# Routes
@app.route('/')
def index():
    return render_template('landing.html')

@app.route('/landing')
def landing():
    return render_template('landing.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        name = request.form.get('name')
        
        # Hash the password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Insert the new user into the database
        query = "INSERT INTO user_info (username, password, email, name) VALUES (%s, %s, %s, %s);"
        cursor.execute(query, (username, hashed_password, email, name))
        db.commit()

        return render_template('signupsuccess.html')
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('name')
        password = request.form.get('password')
        if username == "admin" and password == "admin":
            return render_template("admin.html")

        user = fetch_user(username)
        if user and bcrypt.check_password_hash(user[2], password):
            access_token = create_access_token(identity=user[0])  # Assuming user[0] is user_id
            resp = jsonify({'login': True})
            set_access_cookies(resp, access_token)
            response= make_response(redirect('/api/auth'))
            response.set_cookie('access_token_cookie', value=access_token, max_age=3600, httponly=True)
            return response


            return jsonify(access_token=access_token), 200
        else:
            return jsonify({"msg": "Invalid username or password"}), 401
    return render_template("login.html")

@app.route('/api/auth', methods=['POST', 'GET'])
@jwt_required()
def createtoken():
    return render_template("index.html")
#     if request.method == 'POST':
#         username = request.form.get('name')
#         password = request.form.get('password')
#         if username == "" or password == "":
#             return jsonify({"msg": "Missing username or password"}), 400
#         query = "SELECT * FROM user_info WHERE username = %s;"
#         cursor.execute(query, (username,))
#         result = cursor.fetchall()
#         if result is None:
#             return render_template("signup.html")
#         print(result)
#         if (bcrypt.check_password_hash(result[0][2], password) == False):
#             return jsonify({"msg": "Missing username or password"}), 400
#         access_token = create_access_token(identity=username)
#         print(access_token)

        # session['jwt_token'] = access_token

@app.route('/videopage')
def videopage():
    return render_template('videopage.html')

@app.route('/api/uploadimg', methods=['POST'])
@jwt_required()
def upload_images():
    return render_template('display.html')
    # user = get_jwt_identity()
    # db = psycopg2.connect("postgresql://lakshmi:-wsuF7g_tKtqKXTFAm4huw@iss-group-3-4110.7s5.aws-ap-south-1.cockroachlabs.cloud:26257/defaultdb?sslmode=verify-full")
    # cursor = db.cursor()
    # query = "SELECT user_id FROM user_images WHERE user_id = %s"
    # cursor.execute(query, (str(user),))
    # user_id_exists = cursor.fetchone()
    # if 'images' not in request.files and user_id_exists is None:
    #     return 'No image file', 400
    # files = request.files.getlist('images')
    # for file in files:
    #     if file.filename == '':
    #         return render_template('display.html')
    #     # Check if the user_id exists in the user_images table
    #     query = "SELECT user_id FROM user_images WHERE user_id = %s"
    #     cursor.execute(query, (str(user),))
    #     user_id_exists = cursor.fetchone()

    #     if user_id_exists:
    #         print("Hi")
    #         # If user_id exists, increment num_images
    #         update_query = "UPDATE user_images SET num_images = num_images + 1 WHERE user_id = %s"
    #         cursor.execute(update_query, (user_id_exists[0],))
    #         db.commit()
    #         update_query = "SELECT num_images FROM user_images"
    #         cursor.execute(update_query)
    #         number_images = cursor.fetchone()
    #         columnname = "image"+str(number_images[0])
    #         namecname = columnname + "_name"
    #         filename = file.filename
    #         query = "UPDATE user_images SET " + namecname + " = %s WHERE user_id = %s"
    #         cursor.execute(query, (filename, str(user_id_exists[0])))
    #         db.commit()
    #         update_query = "UPDATE user_images SET " + columnname + " = %s WHERE user_id = %s"
    #         file_contents = file.read()
    #         binary_data = BytesIO(file_contents).read()
    #         cursor.execute(update_query, (Binary(binary_data), str(user_id_exists[0])))
    #         db.commit()
            
    #     else:
    #         file_contents = file.read()
    #         binary_data = BytesIO(file_contents).read()
    #         filename = file.filename
    #         insert_query = "INSERT INTO user_images (user_id, num_images, image1, image1_name) VALUES (%s, 1, %s, %s)"
    #         cursor.execute(insert_query, (str(user), Binary(binary_data), filename))
    #         db.commit()

        # Insert the image into the database
        # file_contents = file.read()
        # binary_data = BytesIO(file_contents).read()
        # insert_query = "INSERT INTO images (user_id, image_metadata, image) VALUES ((SELECT user_id FROM user_info WHERE username = %s), %s, %s)"
        # image_metadata = file.filename  # Provide the image metadata here
        # image_values = (user, image_metadata, Binary(binary_data))
        # cursor.execute(insert_query, image_values)
        # db.commit()



# def resize_with_black_fill(frame, output_width, output_height):
#     h, w = frame.shape[:2]
#     aspect_ratio = w / h
    
#     if aspect_ratio > output_width / output_height:
#         new_w = output_width
#         new_h = int(new_w / aspect_ratio)
#     else:
#         new_h = output_height
#         new_w = int(new_h * aspect_ratio)
    
#     resized_frame = cv2.resize(frame, (new_w, new_h))
#     black_filled_frame = np.zeros((output_height, output_width, 3), dtype=np.uint8)
#     y_offset = (output_height - new_h) // 2
#     x_offset = (output_width - new_w) // 2
#     black_filled_frame[y_offset:y_offset+new_h, x_offset:x_offset+new_w] = resized_frame
    
#     return black_filled_frame


# # Route to handle video creation and delivery

# @app.route('/display', methods=['POST'])
# def display():
#     user_id = get_jwt_identity()
#     images_folder = 'images'
#     if os.path.exists(images_folder):
#         for file in os.listdir(images_folder):
#             file_path = os.path.join(images_folder, file)
#             if os.path.isfile(file_path):
#                 os.unlink(file_path)
#         os.rmdir(images_folder)
#     output_video_file = 'static/images/output_video.mp4'
#     if os.path.exists(output_video_file):
#         os.remove(output_video_file)    
#     query = "SELECT username FROM user_info WHERE user_id = %s"
#     cursor.execute(query, (str(user_id),))
#     username = cursor.fetchone()[0]

#     db = psycopg2.connect("postgresql://lakshmi:-wsuF7g_tKtqKXTFAm4huw@iss-group-3-4110.7s5.aws-ap-south-1.cockroachlabs.cloud:26257/defaultdb?sslmode=verify-full")
#     cursor = db.cursor()
#     image_list = []
#     query = "SELECT num_images FROM user_images WHERE user_id = %s"
#     cursor.execute(query, (str(user_id),))
#     imgcount = int(cursor.fetchone()[0])
#     for i in range(imgcount):
#         columnname = "image"+str(i+1)
#         query = "SELECT " + columnname + " FROM user_images WHERE user_id = %s"
#         cursor.execute(query, (str(user_id),))
#         image = cursor.fetchone()[0]
#         image_base64 = base64.b64encode(image).decode('utf-8')
#         filename = f"{uuid4()}.png"  # Generate a unique filename
#         image_path = os.path.join(images_folder, filename)
#         with open(image_path, 'wb') as img_file:
#             img_file.write(base64.b64decode(image_base64))
#         imagelist.append(image_path)

#     # Query user_images table to get image paths for the user
#     # Build function to fetch image paths from user_images table and store in user_images list 


#     # Define output video parameters
#     output_width = 1920
#     output_height = 1080
#     fps = 24

#     # Create a list to hold video clips
#     clips = []

#     # Loop through each image path
#     for image_path in image_list:
#         img = cv2.imread(image_path)
#         img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

#         img_resized = resize_with_black_fill(img, output_width, output_height)

#         clip = ImageClip(img_resized, duration=1/fps)

#         clips.append(clip)

#     # Concatenate all clips into a single video
#     final_clip = concatenate_videoclips(clips)

#     # Define temporary directory to store video
#     # Define temporary file path for the video
#     # Write video to temporary file
#     # Send video file to user 

#     return render_template('display.html')




# @app.route('/get_images', methods=['POST'])
# def get_images():
#     user_id = request.json['user_id']
#     try:
#         db_connection = psycopg2.connect("postgresql://lakshmi:-wsuF7g_tKtqKXTFAm4huw@iss-group-3-4110.7s5.aws-ap-south-1.cockroachlabs.cloud:26257/defaultdb?sslmode=verify-full")
#         cursor = db_connection.cursor()

#         # Retrieve image paths and names from the database for the given user_id
#         cursor.execute(f"SELECT * FROM user_images WHERE user_id={user_id}")
#         images_data = cursor.fetchone()

#         # Construct a list of image paths and names
#         image_paths = []
#         image_names = []
#         for i in range(2, len(images_data), 2):
#             if images_data[i] is not None:
#                 image_paths.append(images_data[i])
#                 image_names.append(images_data[i+1])

#         # Load the first image to get its dimensions
#         first_image = cv2.imread(image_paths[0])

#         # Return image paths, names, and dimensions as JSON response
#         return jsonify({'image_paths': image_paths[:12], 'image_names': image_names[:12], 
#                         'first_image_height': first_image.shape[0], 
#                         'first_image_width': first_image.shape[1]})

#     except Exception as e:
#         return jsonify({'error': str(e)})
#     finally:
#         if db_connection:
#             cursor.close()
#             db_connection.close()


@app.route('/display')
def display():

    # List of image paths and transition names
    image_transitions = ['img:pics/a.jpg', 'trn:fadeout', 'img:pics/b.jpg', 'trn:fadeout', 'img:pics/c.jpg', 'trn:fadeout', 'img:pics/d.jpg', 'trn:fadeout', 'img:pics/e.jpg', 'trn:fadeout', 'img:pics/f.jpg', 'trn:fadeout','img:pics/g.jpg', 'trn:fadeout', 'img:pics/h.jpg', 'trn:fadeout']

    # Create a list to hold the clips
    clips = []

    def resize_with_black_fill(frame, output_width, output_height):
        h, w = frame.shape[:2]
        aspect_ratio = w / h
        
        if aspect_ratio > output_width / output_height:
            new_w = output_width
            new_h = int(new_w / aspect_ratio)
        else:
            new_h = output_height
            new_w = int(new_h * aspect_ratio)
        
        resized_frame = cv2.resize(frame, (new_w, new_h))
        black_filled_frame = np.zeros((output_height, output_width, 3), dtype=np.uint8)
        y_offset = (output_height - new_h) // 2
        x_offset = (output_width - new_w) // 2
        black_filled_frame[y_offset:y_offset+new_h, x_offset:x_offset+new_w] = resized_frame
        
        return black_filled_frame

    # Loop through each item in the list
    for i, item in enumerate(image_transitions):
        # Split the item into type and value
        item_type, item_path = item.split(':', 1)

        # If the item is an image, create an ImageClip
        if item_type == 'img':
            fps = 25
            img = cv2.imread(item_path)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 
            img_resized = resize_with_black_fill(img, 1920, 1080)  # output video dimensions are set to 1920x1080
            clip = ImageClip(img_resized, duration=1/fps)
            if i > 0 and image_transitions[i-1] == 'trn:fadein': # If the previous item was a 'fadein' transition, apply it to this clip
                clip = fadein(clip, 0.5)  # 0.5 second fade-in
            clips.append(clip)

        # If the item is a transition, apply it to the last clip
        elif item_type == 'trn' and clips:
            if item_path == 'fadeout':
                clips[-1] = fadeout(clips[-1], 0.5)  # 0.5 second fade-out

    # Concatenate all clips into a single video
    final_clip = concatenate_videoclips(clips)
    return render_template('display.html')

if __name__ == '__main__':
    app.run(debug=True)