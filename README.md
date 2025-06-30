# Blog Generation with Amazon Bedrock and AWS Lambda

This project demonstrates an automated blog generation pipeline that leverages **Amazon Bedrock** for Large Language Model (LLM) inference and **AWS Lambda** for serverless orchestration. The generated blog content is stored in **Amazon S3**, making the entire pipeline scalable, event-driven, and cloud-native.

---

## Overview

The system takes a blog topic as input, generates a ~200-word blog using a foundation model hosted on Amazon Bedrock (e.g., Meta Llama), and saves the resulting blog post to an S3 bucket. It’s triggered via AWS Lambda, making it suitable for integration with API Gateway or event-driven architectures.

---

## Key Features

- End-to-end automated blog generation
- Uses LLM from Amazon Bedrock (e.g., Llama model)
- Serverless architecture using AWS Lambda
- Blog output stored directly to Amazon S3
- Configurable using environment variables
- Logging and exception handling included

---

## Tech Stack

| Component        | Technology                   |
| ---------------- | ---------------------------- |
| LLM Inference    | Amazon Bedrock (Llama model) |
| Cloud Functions  | AWS Lambda                   |
| Object Storage   | Amazon S3                    |
| Environment Mgmt | Python-dotenv                |
| Runtime          | Python 3.x                   |
| SDK              | Boto3 (AWS SDK for Python)   |

---

## Key Components

### 1. `blog_generate_using_bedrock(blogtopic: str) -> str`

- Constructs a prompt using the topic.
- Sends it to Amazon Bedrock to generate a blog.
- Returns the generated blog string.

### 2. `save_blog_details_s3(s3_key, s3_bucket, generate_blog)`

- Uploads the generated blog to an S3 bucket.

### 3. `lambda_handler(event, context)`

- Entry point for the AWS Lambda function.
- Parses the input event (expects JSON with `blog_topic` key).
- Calls the blog generator and saves the result to S3.

---

## Example Input Payload

```json
{
  "blog_topic": "The Impact of AI in Healthcare"
}
```

---

## Sample Output

- An S3 object in the folder `blog-output/` with the filename as a timestamp (e.g. `143225.txt`) containing the generated blog content.

---

## Deployment & Usage

1. Deploy the code to AWS Lambda.
2. Set up IAM permissions for Lambda to invoke Bedrock and write to S3.
3. Trigger the Lambda via API Gateway or direct invocation.
4. View the result in the S3 bucket under `blog-output/`.

---

## Future Improvements

- Add support for other model providers on Bedrock.
- Include metadata or tags in the generated blog.
- Store logs and analytics in a structured database (e.g., DynamoDB).
- Frontend UI using Streamlit or a web dashboard.

---

## License

This project is licensed under the MIT License.
