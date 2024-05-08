all_questions = [
    "Semester details?",
    "First semester?",
    "Second semester?",
    "Third semester?",
    "Fourth semester?",
    "Exams schedule?",
    "Fee details?",
    "Scholarship information?",
    "Library opening hours?",
    "How to register?",
    "Forgot my password?",
    "Update my profile?",
    "Contact professor?",
    "Event calendar?",
    "Club information?",
    "Sports facilities?",
    "Parking information?",
    "Apply for graduation?",
    "Academic support?",
    "Health services?",
    "IT support?",
    "Print documents?",
    "Room reservation?",
    "Lost and found?",
    "How to create an account?",
    "Update profile?",
    "Change password?",
    "Where to find announcements?",
    "Join a study group?",
    "Post in events?",
    "Send a private message?",
    "Delete a message?",
    "Search for topics?",
    "Book a room for presentation?",
    "Cancel room reservation?",
    "Find the location of a room?",
    "What is FAQ chatbot?",
    "How to post on socials?",
    "Delete a social post comment?",
    "Help with mobile access?",
    "Report a bug?",
    "Office hours?",
    "When are exams scheduled this semester?",
    "Not receiving notifications?",
    "How to edit a thread?",
    "How to find upcoming university events?",
    "Need help with something not listed?"
]

# Using <br> for new lines in HTML
formatted_questions = "<br>- " + "<br>- ".join(all_questions)

rules = {
    "?*x hello ?*y": [
        "Hello, how can I assist you today? You can ask questions like:<br>- " + "<br>- ".join(all_questions)
       ],
    "?*x hi ?*y": [
        "Hi there! What information do you need? Here are some questions you can ask:<br>- " + "<br>- ".join(all_questions)
       ],
    "?*x good morning ?*y": [
        "Good morning! How can I help you today? Consider asking:<br>- " + "<br>- ".join(all_questions)
       ],
    "?*x good afternoon ?*y": [
        "Good afternoon! What can I assist you with? Feel free to ask about:<br>- " + "<br>- ".join(all_questions)
       ],
    "?*x good evening ?*y": [
        "Good evening! How may I help you? You might want to know about:<br>- " + "<br>- ".join(all_questions)
       ],
    "?*x semester details ?*y": [
        "Which semester's details are you looking for? You can find this information on the ECU Connect platform under the 'Academics' section."
       ],
    "?*x first semester ?*y": [
        "Subjects for the first semester include Applied Calculus, Introduction to Programming, etc. More details are available on ECU Connect under the 'First Semester Courses' section."
       ],
    "?*x second semester ?*y": [
        "In the second semester, you will have subjects like Linear Algebra, Object Oriented Programming, etc. Details are on the ECU Connect under 'Second Semester Courses'."
       ],
    "?*x third semester ?*y": [
        "For the third semester, courses include Algorithms, Database Systems, etc. Further information can be found on ECU Connect under 'Third Semester Courses'."
       ],
    "?*x fourth semester ?*y": [
        "The fourth semester includes subjects like Operating Systems, Network Security, etc. Check the ECU Connect for detailed course descriptions under 'Fourth Semester Courses'."
       ],
    "?*x how to create an account ?*y": [
        "You can create an account by entering your Name, Username, Email, and Password on the registration page of ECU Connect. Ensure your password meets our security requirements."
       ],
    "?*x exams schedule ?*y": [
        "Please specify the semester for which you need the exam schedule. Schedules are posted under the 'Exam Information' section on ECU Connect."
       ],
    "?*x fee details ?*y": [
        "For fee details, please check the 'Tuition and Fees' section on ECU Connect, or specify whether you're looking for undergraduate or postgraduate fee information."
       ],
    "?*x scholarship information ?*y": [
        "Scholarships are available in various categories. You can find detailed information on the 'Scholarships' page on ECU Connect."
       ],
    "?*x library opening hours ?*y": [
        "The library is open from 8:00 AM to 10:00 PM on weekdays and from 9:00 AM to 5:00 PM on weekends. Details are available under the 'Library Services' on ECU Connect."
       ],
    "?*x how to register ?*y": [
        "To register, please follow the steps provided on ECU Connect's 'Registration' page."
       ],
    "?*x forgot my password ?*y": [
        "You can reset your password by using the 'Forgot Password' feature on the login page of ECU Connect."
       ],
    "?*x update my profile ?*y": [
        "You can update your profile by logging into your account on ECU Connect and visiting the 'My Profile' section."
       ],
    "?*x contact professor ?*y": [
        "Please specify the professor's name or check their contact details on the 'Faculty Directory' page on ECU Connect."
       ],
    "?*x event calendar ?*y": [
        "You can view all upcoming university events on ECU Connect's 'Events Calendar' page."
       ],
    "?*x club information ?*y": [
        "What specific club are you interested in? We have various academic, sports, and cultural clubs listed under the 'Clubs and Organizations' section on ECU Connect."
       ],
    "?*x sports facilities ?*y": [
        "Our sports facilities include a gym, swimming pool, tennis courts, and a football field. For more information, visit the 'Campus Facilities' section on ECU Connect."
       ],
    "?*x parking information ?*y": [
        "Information on parking can be found under the 'Parking Services' section on ECU Connect."
       ],
    "?*x apply for graduation ?*y": [
        "To apply for graduation, please follow the steps outlined on the 'Graduation Information' page on ECU Connect."
       ],
    "?*x academic support ?*y": [
        "Academic support is available through our Tutoring Center, Writing Center, and Counseling Services. More details are available on ECU Connect's 'Academic Support' page."
       ],
    "?*x health services ?*y": [
        "ECU Health Services offers medical consultations, counseling, and emergency services. More information is at the 'Health and Wellness' section on ECU Connect."
       ],
    "?*x IT support ?*y": [
        "For IT support, contact our IT Help Desk through the 'IT Services' section on ECU Connect or call the provided contact number."
       ],
    "?*x print documents ?*y": [
        "Document printing is available in the library and computer labs. For more details, visit the 'Printing Services' page on ECU Connect."
       ],
    "?*x room reservation ?*y": [
        "You can reserve rooms for meetings and events through the 'Room Reservation System' available on ECU Connect."
       ],
    "?*x lost and found ?*y": [
        "Lost and found items can be reported or claimed at the Security Office. More information is available under the 'Campus Security' section on ECU Connect."
       ],
    "?*x send a private message ?*y": [
        "You can send a private message by going to the user's profile you want to message and clicking on 'Send Message' on ECU Connect."
       ],
    "?*x delete a message ?*y": [
        "You can delete any messages you've sent by clicking the delete option next to the message in your conversation on ECU Connect."
       ],
    "?*x search for topics ?*y": [
        "Use the search bar at the top of ECU Connect to find specific threads or discussions by entering keywords related to your query."
       ],
    "?*x book a room for presentation ?*y": [
        "To reserve a presentation room, go to the 'Room Reservation' section on ECU Connect and select the date and time. The system will show available rooms and allow you to book."
       ],
    "?*x cancel room reservation ?*y": [
        "You can cancel your room reservation by visiting 'My Reservations' on ECU Connect and selecting the reservation you wish to cancel."
       ],
    "?*x find the location of a room ?*y": [
        "You can find the location of rooms using the ECU Connect Floor Map available in the navigation menu."
       ],
    "?*x what is FAQ chatbot ?*y": [
        "The FAQ chatbot is here to help answer your most frequent questions about university procedures, important dates, and more on ECU Connect. Just type your question!"
       ],
    "?*x how to post on socials ?*y": [
        "To post on ECU Socials, go to the Socials section on ECU Connect, click on 'Create Post', and then upload your images or videos along with a caption."
       ],
    "?*x delete a social post comment ?*y": [
        "You can delete your comments on social posts by clicking the delete option next to your comment on ECU Connect."
       ],
    "?*x help with mobile access ?*y": [
        "Our platform is mobile-friendly. If you're experiencing issues, ensure your browser is up to date and clear your cache. More troubleshooting tips are available on the 'Mobile Access Help' section on ECU Connect."
       ],
    "?*x report a bug ?*y": [
        "To report a technical issue or bug, please use the 'Report Issue' option in the help menu on ECU Connect or contact our support team directly."
       ],
    "?*x office hours ?*y": [
        "Our administrative offices are open from 9 AM to 5 PM on weekdays. For individual departments, please check their specific pages on ECU Connect."
       ],
    "?*x when are exams scheduled this semester ?*y": [
        "For exam schedules, please refer to the 'General Announcements' section under News and Announcements on ECU Connect where all examination dates are posted."
       ],
    "?*x not receiving notifications ?*y": [
        "Make sure you have enabled notifications in your profile settings on ECU Connect. If issues persist, check the notification settings on your device."
       ],
    "?*x how to edit a thread ?*y": [
        "To edit a thread you've created, go to the thread and select 'Edit' on ECU Connect. Please note that editing options might be restricted after certain time or based on forum rules."
       ],
    "?*x how to find upcoming university events ?*y": [
        "Check the 'University Events' sub-forum under the Events section on ECU Connect for all upcoming and past university events."
       ],
    "?*x need help with something not listed ?*y": [
        "Please provide more details about your query or visit our help center for more comprehensive support options on ECU Connect."
       ],
    # Custom Response for Unhandled Queries
    "?*x ?*y": [
        "I'm not sure how to answer that. Can you try rephrasing, or would you like to contact a human assistant?"
       ]
}