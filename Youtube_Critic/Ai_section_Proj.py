import os
import google.generativeai as genai

genai.configure(api_key="AIzaSyBAR9hesg9R2XvdGqdmmyfvQA4Zp--UK-Q")

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
)

chat_session = model.start_chat(
  history=[
  ]
)

for channel in os.listdir("Reports"):
    with open(f"Reports/{channel}","r",encoding="utf-8") as f:
        report = f.read()

    response = chat_session.send_message(f"""you are a professional Youtube videos critic,
    you are tasked to grade the channel on specific criteria based on its video scripts provided.

    Your criteria are:

    1 - information desnity: which is how much information is packed in the creator's speech,
    for a high grade, the script must contain more information with fewer words, think of it like density,
    more mass per volume

    2 - natural flow: which is a measure of how well written is the video, a high grade would emphasize,
    high quality speech, a low grade would be mean bad and boring way of talking.

    3 - humanness: the script must be written by a human, if the script is heavily suspected to be AI-Generated,
    then it will get a low grade score

                                        
    each criteria is graded by (low,medium,high,very high)
                                        
    Format your response exactly like this format:
    [
    Channel Name: (channel name)

    information desnity: (grade for information desnity)
    natural flow: (grade for natural flow)
    humanness: (grade for humanness)
    ]

    here are all the information you need:


    {report}
    """)

    print(response.text)
    with open(f"Reports/Critic of {channel}","w",encoding="utf-8") as g:
        g.write(response.text)