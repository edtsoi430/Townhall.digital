# Objective:
This project aims to develop AI bots that would respond to human posts in a closed Facebook group using sentiment-analysis and Google Cloud NLP. The project is conducted at the University of Michigan, Ann Arbor and is now used for research purposes. Still under development currently.

# Descriptions of the Project:
We have developed a user-interface and hosted a Closed-Facebook-Group automation tool on Flask.
## Supported functionalities (As of 11/14/2019):
- Create a Closed Facebook Group with a graphical user interface, and invite new members to the group by uploading a csv file containing each intended member's email, row by row.
- When using the aumation tool, it will prompt you to sign in to your gmail. When properly signed in, a csv file named in your inputted group name will be created and uploaded to the corresponding Google Drive. The file will contain information such as Master account ID, Master account PW, creation date of the group and invited members etc.
- Retrieve all the posts and comments from a linked group, listed out in an xlsx file about information such as message posters, message content and date posted etc.
- Basic sentiment analysis and classification, with their corresponding confidence level using Google Natural Language API.

# Updates:
Inspired by OpenAI's GPT2, we are currently extending our project to a neural network architecture by developing a model where we can train the bots to generate text based on human inputs (conversations) retrieved from the closed Facebook group.
