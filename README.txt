BANKING RAG PROJECT - START HERE

1. Open this folder in VS Code.
2. Create and activate a virtual environment:
   Windows PowerShell:
       py -m venv .venv
       .\.venv\Scripts\Activate.ps1

3. Install dependencies:
       python -m pip install --upgrade pip
       pip install -r requirements.txt

4. Copy .env.example to a new file named .env.
   Add your Pinecone API key and confirm AWS_REGION and BEDROCK_MODEL_ID.
   Never share or commit your .env file.

5. Configure AWS credentials using an IAM identity with Bedrock permissions:
       aws configure
   Enter your own access key, secret key and region when prompted.
   Alternatively use an existing AWS profile/role. Do not paste credentials into Python files.

6. In AWS Bedrock, make sure the chosen Claude model and Titan Text Embeddings V2
   are available/enabled for your AWS account and region.

7. In Pinecone, create an API key. The application creates the index automatically
   with dimension 1024. Ensure PINECONE_REGION is a valid serverless region.

8. Copy your PDF files into the documents folder.
   A fictional sample PDF is supplied separately as Banking_Policy_Sample.pdf.
   Rename/copy it into documents, e.g. documents/banking_policy_sample.pdf.

9. Run:
       python main.py

10. Example questions:
       What are the basic eligibility requirements?
       Which documents are required for a personal loan?
       What happens if a customer misses a payment?
       Does submitting an application guarantee approval?

MODULES
- loader.py: PDF loading
- chunking.py: text splitting
- embeddings.py: Titan embeddings
- vectordb.py: Pinecone index and vector storage
- llm.py: Claude on Bedrock
- main.py: retrieval + prompt + answer loop
- config.py: environment configuration

NOTE
This starter re-indexes the PDFs each time it starts. For a production system,
add document IDs, duplicate prevention, update/delete workflows, access control,
logging, evaluation, and monitoring. This sample is for learning, not real banking decisions.
