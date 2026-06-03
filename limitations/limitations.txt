Limitations 

#LIMITATION: No Persistent Memory Across Sessions
The chatbot can remember conversation history only while the current session is active. Once the application is closed or restarted, the previous conversation history is lost .
##SOLUTION:
This can be solved by implementing  a database such as SQLite, MySQL, or PostgreSQL to store conversation history. When the user returns, previous messages can be retrieved and loaded automatically, allowing the chatbot to continue conversations from where they left off.

#LIMITATION: Retrieval Failure
The chatbot can only answer based on the information it retrieves from the uploaded documents. Sometimes, even when the correct answer exists in the PDF, the system may retrieve less relevant sections instead of the most useful ones. As a result, the chatbot may provide an incomplete or inaccurate answer.
##SOLUTION:
Use more advanced embedding models that better capture the semantic meaning of documents and queries.
Increase the retrieval count (Top-K) so that more relevant chunks are provided to the language model.
Implement reranking models to reorder retrieved chunks based on relevance before sending them to the LLM.

#LIMITATION:No Understanding Beyond Retrieved Context
chatbot is limited to the information available in the uploaded documents.If the document does not contain the answer, the chatbot cannot provide a complete response.
##SOLUTION :
Combine RAG with web search
Use external knowledge sources
Implement a hybrid retrieval system that combines semantic search and keyword-based search. By considering both the meaning of the query and important keywords, the system can retrieve more relevant document chunks and improve answer accuracy.

#LIMITATION : Poor Handling of Misspelled or Grammatically Incorrect Queries
The chatbot performs best when users ask clear and correctly written questions. If a query contains multiple spelling mistakes, grammatical errors, or incomplete sentences, the retrieval system may fail to understand the user's actual intent. As a result, it may retrieve irrelevant chunks or fail to find the correct information even when the answer exists in the uploaded documents.
##SOLUTION:
Use query rewriting where an LLM reformulates the user's question into a clearer version.
Use more advanced embedding models that are more tolerant of spelling and grammar variations.
Allow the chatbot to ask clarification questions when the query is unclear.
