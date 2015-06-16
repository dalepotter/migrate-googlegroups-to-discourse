Pseudocode for script to import data into Discuss

# Set-up parameters
	Set API key for the forum
	Get category_id of the ‘Archived Google Groups’ category from the API (or set this manually)

# Load Google Group data into the memory
	Open file of Google group JSON data in read mode
	Convert the JSON into a python dictionary variable

# Loop over each of the threads and messages to add them to Discuss
# Loop over each thread and create a topic
	For each thread:
		Send API call (POST) to create a topic
		Store topic ID of the response received
		Send API call (PUT) to modify the topic and add the correct category_id
		Add topic_id variable to this dictionary iteration
		
# Loop over each message within the thread and create a topic
		For each message contained within the thread:
			Prepare the post body to prepend ‘Posted by [name] on [date]:’
Send API call (POST) to create a post
Add returned post_id variable to this dictionary iteration

# Log data back to the file
Convert to JSON
Write the new dictionary variable (i.e. including topic and post IDs) to a new file
