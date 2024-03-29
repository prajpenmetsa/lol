def video(): # fetch images from database 

    current_user = get_jwt_identity()

    # Clear the images folder
    images_folder = 'images'
    if os.path.exists(images_folder):
        for file in os.listdir(images_folder):
            file_path = os.path.join(images_folder, file)
            if os.path.isfile(file_path):
                os.unlink(file_path)
        os.rmdir(images_folder)

    # Delete the output video file
    output_video_file = 'static/images/output_video.mp4'
    if os.path.exists(output_video_file):
        os.remove(output_video_file)

    # Connect to the database
    db_connector = psycopg2.connect("postgresql://QES:WoPH1gwM3_JGB4Zkcovy9w@iss-group-41-4102.7s5.aws-ap-south-1.cockroachlabs.cloud:26257/issproject?sslmode=verify-full")
    user_db = db_connector.cursor()    

    # Fetch user images count
    query = "SELECT user_images FROM user_details WHERE username = %s"
    user_db.execute(query, (current_user,))   
    x = user_db.fetchone()  # Since you are fetching a single value

    if x and int(x[0]) > 0:
        # Fetch image data
        query = "SELECT image, image_metadata FROM images WHERE user_id = (SELECT user_id FROM user_details WHERE username = %s)"
        user_db.execute(query, (current_user,))
        image_data = user_db.fetchall()

        # Create a directory if it doesn't exist
        os.makedirs(images_folder, exist_ok=True)
        
        # Clear the existing image_list
        global image_list
        image_list.clear()
        
        # Save each image to the 'images' folder and add to image_list
        for image, image_metadata in image_data:
            image_base64 = base64.b64encode(image).decode('utf-8')
            filename = f"{uuid4()}.png"  # Generate a unique filename
            image_path = os.path.join(images_folder, filename)
            with open(image_path, 'wb') as img_file:
                img_file.write(base64.b64decode(image_base64))
            image_list.append(image_base64)
        user_db.close()
        db_connector.close()
        print("HEllo", len(image_list))
        return render_template('video_Editor.html', image_list=image_list, duration_var=selected_dur, transition_var=selected_transition, resolution_var=selected_resolution)
    else:
        user_db.close()
        db_connector.close()
        return render_template('upload.html', failure_message="You need to upload images.")