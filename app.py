import boto3 # Imports the AWS SDK for Python, used to interact with AWS services like Bedrock and S3.
import botocore.config # Imports the configuration module for botocore, which is the underlying library for boto3.
import json # Imports the JSON library for working with JSON data, which is commonly used for API requests and responses.

from datetime import datetime # Imports the datetime class from the datetime module for working with dates and times.
from dotenv import load_dotenv
import os
load_dotenv()

S3_BUKCET = os.getenv("S3_BUCKET")
MODEL_ID = os.getenv("MODEL_ID")
AWS_REGION = os.getenv("AWS_REGION")

def blog_generate_using_bedrock(blogtopic:str)-> str:
    # Defines a function to generate a blog post using an AWS Bedrock Foundation Model.
    # It takes one argument: blogtopic (string), which is the topic for the blog.
    # It is type-hinted to return a string.

    prompt=f"""<s>[INST]Human: Write a 200 words blog on the topic {blogtopic}
    Assistant:[/INST]
    """
    # Constructs the prompt string to be sent to the LLM.
    # `f"""..."""` is an f-string, allowing embedding of variables like `blogtopic`.
    # `<s>[INST]Human: ... Assistant:[/INST]` is a specific prompt format often used by Llama 2 models.

    body={
        # Defines the request body as a dictionary, which will be converted to JSON.
        "prompt":prompt, # The constructed prompt for the LLM.
        "max_gen_len":512, # Maximum number of tokens the model should generate in the response.
        "temperature":0.5, # Controls the randomness of the output (lower means more deterministic).
        "top_p":0.9 # Controls diversity of output by sampling from the smallest set of most probable tokens.
    }

    try:
        # Starts a try-except block to catch potential errors during API interaction.
        bedrock=boto3.client("bedrock-runtime",region_name=AWS_REGION,
                             # Initializes a boto3 client for the Bedrock Runtime service.
                             # "bedrock-runtime": Specifies the service to interact with.
                             # "region_name='us-east-1'": Specifies the AWS region where the Bedrock service is accessed.
                             config=botocore.config.Config(read_timeout=300,retries={'max_attempts':3}))
                             # Configures the client with a read timeout of 300 seconds (5 minutes)
                             # and sets the number of retries for failed requests to 3.
        response=bedrock.invoke_model(body=json.dumps(body),modelId=MODEL_ID)
        # Invokes the Bedrock model to generate text.
        # `body=json.dumps(body)`: Converts the Python dictionary `body` into a JSON string.
        # `modelId="meta.llama2-13b-chat-v1"`: Specifies the exact Foundation Model to use (Llama 2 13B Chat model).

        response_content=response.get('body').read()
        # Retrieves the 'body' stream from the Bedrock response and reads its content.
        response_data=json.loads(response_content)
        # Parses the JSON content received from the Bedrock model response into a Python dictionary.
        print(response_data)
        # Prints the full response data received from the model (for debugging/inspection).
        blog_details=response_data['generation']
        # Extracts the generated text (the blog content) from the response data.
        return blog_details
        # Returns the generated blog content.
    except Exception as e:
        # Catches any exception that occurs within the try block.
        print(f"Error generating the blog:{e}")
        # Prints an error message indicating what went wrong.
        return ""
        # Returns an empty string if an error occurs.

def save_blog_details_s3(s3_key,s3_bucket,generate_blog):
    # Defines a function to save the generated blog content to an Amazon S3 bucket.
    # It takes three arguments: s3_key (the desired object key/path in S3),
    # s3_bucket (the name of the S3 bucket), and generate_blog (the blog content to save).

    s3=boto3.client('s3')
    # Initializes a boto3 client for the Amazon S3 service.

    try:
        # Starts a try-except block to catch potential errors during S3 interaction.
        s3.put_object(Bucket = s3_bucket, Key = s3_key, Body =generate_blog )
        # Uploads the `generate_blog` content to the specified S3 bucket and key.
        # `Bucket`: The name of the target S3 bucket.
        # `Key`: The path and filename for the object in S3.
        # `Body`: The content (blog text) to be uploaded.
        print("Code saved to s3")
        # Prints a success message if the object is saved to S3.

    except Exception as e:
        # Catches any exception that occurs within the try block.
        print("Error when saving the code to s3")
        # Prints a generic error message if saving to S3 fails.


def lambda_handler(event, context):
    # This is the main entry point for an AWS Lambda function.
    # `event`: A dictionary containing data about the event that triggered the Lambda function.
    # `context`: An object providing runtime information about the invocation, function, and execution environment.

    # TODO implement
    # A placeholder comment, usually indicating where business logic should be added.
    event=json.loads(event['body'])
    # Parses the 'body' of the incoming event (which is expected to be a JSON string) into a Python dictionary.
    # This is typical for Lambda functions triggered by API Gateway with a JSON payload.
    blogtopic=event['blog_topic']
    # Extracts the 'blog_topic' value from the parsed event data.

    generate_blog=blog_generate_using_bedrock(blogtopic=blogtopic)
    # Calls the `blog_generate_using_bedrock` function to generate the blog content.

    if generate_blog:
        # Checks if a blog was successfully generated (i.e., `generate_blog` is not an empty string).
        current_time=datetime.now().strftime('%H%M%S')
        # Gets the current time and formats it as a string (HHMMSS) to be used in the S3 key.
        s3_key=f"blog-output/{current_time}.txt"
        # Constructs the S3 key (path within the bucket) for the saved blog file.
        s3_bucket=S3_BUKCET
        # Specifies the name of the S3 bucket where the blog will be saved.
        save_blog_details_s3(s3_key,s3_bucket,generate_blog)
        # Calls the `save_blog_details_s3` function to upload the blog to S3.

    else:
        # This block executes if no blog content was generated (e.g., due to an error in Bedrock generation).
        print("No blog was generated")
        # Prints a message indicating that no blog was generated.

    return{
        # Returns a dictionary as the response from the Lambda function.
        'statusCode':200,
        # HTTP status code indicating success.
        'body':json.dumps('Blog Generation is completed')
        # The response body, a JSON string indicating completion.
    }