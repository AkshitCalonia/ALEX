import os
from pymongo import MongoClient
from openai import OpenAI

def connect_to_mongodb(uri):
    try:
        client = MongoClient(uri)
        print("Connected to MongoDB Atlas")
        return client
    except Exception as e:
        print("An error occurred while connecting to MongoDB Atlas:", e)
        return None

def insert_into_mongodb(client, database_name, collection_name, data):
    try:
        db = client.get_database(database_name)
        collection = db.get_collection(collection_name)
        collection.insert_one(data)
        print("Data inserted into MongoDB Atlas")
    except Exception as e:
        print("An error occurred while inserting into MongoDB Atlas:", e)

def generate_number(prompt="give me an essay on wrestling"):
    try:
        # Initialize OpenAI client
        client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
        
        # Generate completion from OpenAI
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Specify the model
            messages=[{"role": "user", "content": prompt}],
            max_tokens=40,  # Limiting the tokens to prevent generating lengthy responses
            temperature=0,  # Disabling randomness to ensure consistent results
        )

        # Extract generated text
        generated_text = completion.choices[0].message.content.strip()
        
        # Connect to MongoDB Atlas
        mongodb_uri = "mongodb+srv://jinash_r:<password>@cluster0.eadbiwt.mongodb.net/?retryWrites=true&w=majority"  # Replace with your MongoDB Atlas connection URI
        mongodb_client = connect_to_mongodb(mongodb_uri)
        
        # Insert generated text into MongoDB
        if mongodb_client:
            insert_into_mongodb(mongodb_client, "hacklytics", "trial", {"prompt": prompt, "generated_text": generated_text})
        
        return generated_text
    except Exception as e:
        print("An error occurred:", e)
        return None

if __name__ == "__main__":
    text = generate_number()
    if text is not None:
        print("Generated number:", text)
