from top2vec import Top2Vec

# Step 1: Prepare the text as a list of documents
documents = [
    """
    Re Introduction to NurenAI - Your CRM Solution Partner
    
    Thanks for reaching out On Fri, Aug 30, 2024 at 11:03 PM wrote:
    
    Dear Ankur, I hope this email finds you well. I am reaching out to introduce NurenAI, a comprehensive CRM service provider. 
    Our platform, accessible at crm.nuren.ai, offers a robust set of tools designed to help businesses streamline their 
    customer relationship management processes. At NurenAI, we are committed to providing solutions that enhance productivity, 
    drive sales, and improve customer engagement. Whether you are looking for lead management, sales automation, or customer 
    support features, NurenAI has got you covered. We would love the opportunity to discuss how our services can be tailored 
    to meet your specific needs. Please let us know a convenient time for a quick call or demo session. Looking forward to 
    connecting with you!
    
    Best regards, Adarsh Sharma, Founder NurenAI
    """
]

# Step 2: Create a Top2Vec model
model = Top2Vec(documents, speed="learn", workers=4)  # Adjust parameters as needed

# Step 3: Extract topics
topics, topic_scores, topic_nums = model.get_topics()

# Step 4: Print the topics
for topic_num, (topic_words, score) in enumerate(zip(topics, topic_scores)):
    print(f"Topic {topic_num + 1}:")
    print(f"Keywords: {topic_words}")
    print(f"Score: {score}")
    print("\n")
