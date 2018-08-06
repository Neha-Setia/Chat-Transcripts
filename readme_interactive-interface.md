## End to End Interactive Interface powered by Machine learning using Rest APIs by mining Unstructured Content.

With the advent of AI, Automation of Services has picked up much faster pace than ever before. And hence, technology has also changed  the way customer service solutions are designed. One industry which has gained momentum due to this disruption of Artificial Intelligence is - Customer service industry. Artificial Intelligence has transformed the customer interactions considerably. Machine Learning and Natural Language Processing(NLP) together are the technology behind these interactions. Natural language processing supports your daily interactions with AI software using its ability to process and interpret spoken/written messages. 

Let's say we have a mobile phone and some things are working we don't have enough Internet on our phone or the internet provider has sent us a excessively high bill or we want to find out some promotion about roaming overseas because we are about to travel as what we normally do is we call them up and we talk to the customer support Representative. Hence, it was representative who used their mind to assess our problem and come up with a solution and more often than not they can solve our problem. Because it's a human being a human being over the phone there's no natural language processing there. With an immense improvements in the cognitive technology, chatbots are gaining momentum. It's very close to giving the user the experience of texting to another human. It allows you to text things, using it to pass your result into the decision tree and learn.

This composite code pattern brings you the end-to-end solution which will show case on how one can construct interactive interface powered by machine learning for any decision-support service using rest apis. The composite code pattern makes use of the Code Pattern [`Automating the process of extracting Features for ml model from Unstructured Data`](https://github.com/IBM/extract-features-for-ml-model-from-unstructured-data/blob/master/README.md) and [Automate the Decision-Making process using Machine learning with Minimal Manual Intervention](https://github.com/IBM/automate-business-decisions-with-machine-learning).

It's an end-to-end solution as it will :

1. Take the Documents in unstructured formats like PDFs or Word Documents and process them. 

2. [Automate the process of Extracting features](https://github.com/IBM/extract-features-for-ml-model-from-unstructured-data) for building the machine learning model for that domain. For more details, go through the [readme.md](https://github.com/IBM/extract-features-for-ml-model-from-unstructured-data/blob/master/README.md).

3.  Prepare Machine learning Model from the data extracted in the step 2 and automate the process of the decision support  using the Code Pattern [`Automate the Decision-Making process using Machine learning with Minimal Manual Intervention`](https://github.com/IBM/automate-business-decisions-with-machine-learning).

4. Interactive Interface will ask you the question then on the basis of your answer, it passes your result into the decision tree and get you the most approriate recommendation. It will analyse further whether to ask next question or the current information received from the user is good enough to take the decision. If yes, which questions to ask. The section `Exposing the Jupyter Notebook Code as Rest API` of the readme.md explains how the python code in the notebook from the Step 3 can be exposed as Rest API  and a python Flask application can be built on top of it. Finally, 

5. Deploy the application on IBM Cloud.

 
# Architecture Diagram.


## Exposing the Notebook Code as Rest API




