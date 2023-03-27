from models.Job import Job
from models.Candidate import Candidate
import telebot
import re

API_TOKEN = '6076749167:AAHRjq7hEtYRxPVf2IzvsS3Yvt6YOoptPjA'
bot = telebot.TeleBot(API_TOKEN)
jobs = []
appliedJobs = []
candidate = Candidate()
questions = ["What's your name?", "What´s your age?", "What´s your work experience?", "From 0 to 10, how do you consider your skills in the field of programming?", "From 0 to 10, how do you consider your english skills?", "From 0 to 10, how do you consider your communication/soft skills?"]
actualQuestion = 0
option = 0
optionPaidOrFree = 0
state = ""

def createJobs():
    job1 = Job('Altar.io', 'Software developer', 'Develop and maintain web and mobile applications', 18, 1, 7, 5, 6)
    job2 = Job("Simform", "Software engineer", "Solve complex software engineering problems ", 18, 5, 8, 9, 8)
    job3 = Job("Fingent", "Software developer", "Custom software development tailored to users, processes and business requirements", 18, 2, 5, 4, 7)
    job4 = Job("10Pearls", "Developer for process automation", "Automate manual business processes and optimize the customer experience for greater efficiency and engagement", 18, 2, 8, 8, 7)
    job5 = Job("ELEKS", "Web and mobile application developer", "Develop and maintain web and mobile applications", 18, 3, 8, 8, 8)
    job6 = Job("Boladare", "Senior in software development", "Master for software testing", 18, 2, 6, 8, 7)
    job7 = Job("The software house", "Web application developer", "Development of services and web applications with Node.js, React and php", 18, 1, 6, 8, 7)
    job8 = Job("Sidebench", "Front-end Developer", "Front-end development to improve UX of web and mobile applications", 18, 2, 6, 8, 7)
    jobs.append(job1), jobs.append(job2), jobs.append(job3), jobs.append(job4), jobs.append(job5), jobs.append(job6)
    jobs.append(job7), jobs.append(job8)

# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    createJobs()
    restart_candidate()
    global actualQuestion
    actualQuestion = 0
    bot.reply_to(message,f"Hello, I am your adviser to find employees in the software area. With just a few questions, we'll offer you jobs that match your skills. If you don't pass the requirements for jobs, don't worry, we'll help you improve your skills by offering you some courses or certifications.\n {questions[actualQuestion]}")

# Function that is activated when a message cames
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    global actualQuestion
    try:
        if actualQuestion == 0 and re.match("^[a-zA-ZñÑáéíóúÁÉÍÓÚüÜ\s]+", message.text):
            candidate.name = message.text
            actualQuestion += 1
            bot.reply_to(message, questions[actualQuestion])
        elif actualQuestion == 1 and int(message.text):
            candidate.age = int(message.text)
            actualQuestion += 1
            bot.reply_to(message, questions[actualQuestion])
        elif actualQuestion == 2 and int(message.text) >= 0:
            candidate.experience = int(message.text)
            actualQuestion += 1
            bot.reply_to(message, questions[actualQuestion])
        elif actualQuestion == 3 and int(message.text) >= 0 and int(message.text) <= 10:
            candidate.programmation_skills = int(message.text)
            actualQuestion += 1
            bot.reply_to(message, questions[actualQuestion])
        elif actualQuestion == 4 and int(message.text) >= 0 and int(message.text) <= 10:
            candidate.english_skills = int(message.text)
            actualQuestion += 1
            bot.reply_to(message, questions[actualQuestion])
        elif actualQuestion == 5 and int(message.text) >= 0 and int(message.text) <= 10:
            candidate.communication_skills = int(message.text)
            actualQuestion += 1
        if actualQuestion == len(questions):
            for i in jobs:
                if candidate.age >= i.minimum_age and candidate.experience >= i.requirement_experience and candidate.programmation_skills >= i.requirement_programmation_skills and candidate.english_skills >= i.requirement_english_skills and candidate.communication_skills >= i.requirement_communication_skills:
                    appliedJobs.append(i)
            if len(appliedJobs) == 0:
                bot.reply_to(message, "According with your provided information, you can´t apply to offered jobs")
                bot.reply_to(message,
                             "---Your Information---\n" + "Name: " + str(candidate.name) + "\n" + "Age:" + str(
                                 candidate.age) + "\nWork experience: " + str(
                                 candidate.experience) + "\nProgrammation skills: " + str(
                                 candidate.programmation_skills) + "\nEnglish skills: " + str(
                                 candidate.english_skills) + "\nCommunication skills: " + str(
                                 candidate.communication_skills))
                bot.reply_to(message,
                             "Would you like to view online certificate-courses to improve your skills?(yes/no)")
                bot.register_next_step_handler(message, certificate_response)

            else:
                bot.reply_to(message, "According with your provided information, you can apply to next jobs")
                bot.reply_to(message, "---Your Information---\n" + "Name: " + str(candidate.name) + "\n" + "Age:" + str(
                    candidate.age) + "\nWork experience: " + str(
                    candidate.experience) + "\nProgrammation skills: " + str(
                    candidate.programmation_skills) + "\nEnglish skills: " + str(
                    candidate.english_skills) + "\nCommunication skills: " + str(candidate.communication_skills))
                for i in appliedJobs:
                    bot.reply_to(message, "Company: " + str(i.name) + "\n" + "Position: " + str(
                        i.job_position) + "\n" + "Description: " + str(i.description) + "\n" + "Minimum Age: " + str(
                        i.minimum_age) + "\n" + "Work experience: " + str(
                        i.requirement_experience) + "\n" + "Programmation skills: " + str(
                        i.requirement_communication_skills) + "\n" + "English skills: " + str(
                        i.requirement_english_skills) + "\n" + "Communication/soft skills" + str(
                        i.requirement_communication_skills) + "\n")
    except:
        bot.reply_to(message, "Error!! Verify your inputs.\n"+ questions[actualQuestion])

def certificate_response(message):
    if 'yes' or 'y' in message.text.lower():
        bot.send_message(message.chat.id, "Do you prefer a paid or free online course (1/2)")
        bot.register_next_step_handler(message, free_pay)
    elif 'no' or 'n' in message.text.lower():
        bot.reply_to(message,
                     "Thanks for using our tool. See u soon!!")
    else:
        bot.reply_to(message, "Error!! Verify your inputs. Try again...")
        bot.reply_to(message,
                     "Would you like to view online certificate-courses to improve your skills?(yes/no)")
        bot.register_next_step_handler(message, certificate_response)

def free_pay(message):
    try:
        if int(message.text) == 1:
            bot.send_message(message.chat.id, "¡Brilliant! We recommend the following free online courses:\n"
                                              "- Introduction to Software Engineering, offered by Coursera\n"
                                              "- Fundamentals of Object Oriented Programming, offered by ed")
            bot.send_message(message.chat.id,
                             "Thanks for using our tool. See u soon!!")
        if int(message.text) == 2:
            bot.send_message(message.chat.id, "¡Brilliant! We recommend the following free online courses:\n"
                                              "- Software Engineering Fundamentals, offered by Udemy\n"
                                              "- Mobile App Development, offered by Coursera\n"
                                              "- Advanced Software Engineering, offered by Udacity\n"
                                              "- Software design and architecture, offered by edX")
            bot.send_message(message.chat.id,
                         "Thanks for using our tool. See u soon!!")
    except:
        bot.reply_to(message, "Error!! Verify your inputs. Try again...")
        bot.send_message(message.chat.id, "Do you prefer a paid or free online course (1/2)")
        bot.register_next_step_handler(message, free_pay)

def restart_candidate():
    candidate.name = ""
    candidate.age = -1
    candidate.experience = -1
    candidate.programmation_skills = -1
    candidate.english_skills = -1
    candidate.communication_skills = -1
    appliedJobs.clear()
# Iniciamos el bot
bot.polling()
