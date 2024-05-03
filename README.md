# PROFE

## Description

PROFE is an interactive teaching assistant powered by Gemini large language models and accessible via WhatsApp. With PROFE, you can seek assistance in understanding any school-related topic. Whether it's a specific subject, concept, or even your own class notes in the form of images or PDFs, PROFE is equipped to provide insightful explanations and answer your questions.

Please note that while PROFE aims for accuracy, occasional inaccuracies may occur; users are encouraged to verify information independently.

** Key features **

- Versatile Assistance: PROFE can provide assistance on a wide range of topics, tailored to your individual learning needs.

- Support for Multimedia Inputs: Share images or PDFs of your class notes with PROFE, allowing for more comprehensive assistance.

- Text and Audio Responses: Receive responses in either text or audio format, enhancing accessibility and convenience.

- Customized Quizzes: PROFE can generate sample quizzes based on the topic you provide or your own class notes, helping reinforce your understanding through practice.

Take a look at a descriptive video of PROFE [here](https://www.youtube.com/watch?v=tzv6KvlM1Kk&ab_channel=Ra%C3%BAlEnriqueP%C3%A9rezRioja).

## Installation

To run a demo of PROFE, follow these steps:

1. **Set Up ngrok:**
   - Create a free ngrok account and obtain your authentication token. You can sign up and download ngrok from [here](https://ngrok.com/download).
   - After setting up ngrok, retrieve your NGROK_DOMAIN and paste it into the .env file.

2. **Configure Twilio:**
   - Create a free Twilio account and obtain your account number and authentication token.
   - Add both your account number and authentication token to the .env file.

3. **Obtain Gemini API Key:**
   - Obtain your Gemini API key from [here](https://aistudio.google.com/app/apikey) and add it to the .env file.

4. **Install Dependencies:**
   - Navigate to the root directory of the project and run the following command to install the necessary dependencies:
     ```
     make install
     ```

5. **Activate Environment:**
   - Run the following command to activate the project environment:
     ```
     make activate
     ```

6. **Set Auth keys**
   - Set the 'GOOGLE_APPLICATION_CREDENTIALS' key to the path of the service account key file in the .env file.
   - To get this key click "ADD KEY" in the Service Account section of the Google Cloud Console and download the JSON file.
   - Make sure that the Google Service Account has access to the [Text-to-Speech API](https://console.cloud.google.com/marketplace/product/google/texttospeech.googleapis.com) and the [Speech-to-Text API](https://console.cloud.google.com/marketplace/product/google/speech.googleapis.com).
   - Specify the folder with credentials for Google Forms in the env variable GOOGLE_CREDENTIAL_PATH. You can follow the instructions [here](https://developers.google.com/forms/api/quickstart/python).

   ![alt text](https://github.com/feradauto/PROFE/blob/main/resources/google_service_account_key.png?raw=true)

7. **Run PROFE API:**
   - Start the PROFE API by running the following command:
     ```
     make run-with-clean-db
     ```

8. **Start ngrok:**
   - Open a new terminal window and start ngrok by running the following command:
     ```
     make start-ngrok
     ```

9. **Set Up Twilio Configuration:**
   - Copy the ngrok URL and append `/api/v1/whats/message` to it.
   - Navigate to the Twilio console and set the URL for the WhatsApp sandbox to the ngrok URL. You can find this configuration under Messaging > Try it out > WhatsApp > Sandbox Settings.