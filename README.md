# 429 project

## Week 1
### Auto-ML helper for marketing specialists
(project name is in progress)

### Value Proposition
Marketers often need to use machine learning models to evaluate sales, conversions, and business development. However, for these generally simple tasks, it is necessary to have a machine learning specialist. We offer a website that automatically processes incoming data in the most efficient way and allows you to use previously prepared bundles of model + preprocessing to process new data. The difference from the existing Auto ML solutions is that the existing ones are used for too wide a range of tasks and are too general to work effectively or require specialized knowledge.

### Lean Startup Questionnaire

Marketers sometimes need data research in their work and either a separate employee or knowledge is needed for this. Our solution will allow us to conduct such research without attracting additional resources, since our solution will be understandable and automated. To determine the needs and tasks, we have scheduled interviews with SEZ marketers. Depending on their experience, we will adapt the product.

### Leveraging AI, Open-Source, and Experts

Our project will be based on machine learning models to automate the user's task. The AI will select the necessary hyperparameters depending on the data entered by the user. For the validity of our solution, we will consider the functionality of existing projects and identify their weaknesses. And we will also use ready-made libraries for basic machine learning. To consult with the implementation of our project, we contacted a person working in the industry. We received advice, criticism and recommendations from him. And we will continue to cooperate with him to improve the project.

### Defining the Vision for Your Project

Marketers often need to use machine learning models to evaluate sales, conversions, and business development. However, for these generally simple tasks, it is necessary to have a machine learning specialist. We offer a website that automatically processes incoming data in the most efficient way and allows you to use previously prepared bundles of model + preprocessing to process new data. The difference from the existing Auto ML solutions is that the existing ones are used for too wide a range of tasks and are too general to work effectively or require specialized knowledge.

As the project grows, we will have to switch to a fundamentally different architecture, since the current one assumes a search of hyperparameters optimized using the optima library (where hyperparameters are all stages of preprocessing, and the machine learning model, and its hyperparameters).  This is enough for now, but after the completion of the work within the capstone project, one of the more complex schemes will be used.

### Technology Stack

##### Frontend:
HTML, CSS, JS, Figma
##### Backend:
Python, Django (can be changed), SQLite
##### ML part:
SciKit-Learn, Pandas, Optima, PyTorch

## Week 2

### Technical stack
1) Breakdown of components:
Our solution is represented by two server applications: the first is responsible for the site itself, the personal account and data loading, the second has large computing power and is responsible for working with data uploaded to users. They will exchange information about the work done and the work that needs to be done. We chose this configuration because of the need for large computing capacities and the need to scale them over time.
2) Data management:
General data about the user and his projects will be stored on the server with the site (presumably using SQL), and machine learning models will be stored on another server (the storage format has not yet been selected and will be based on the data required for saving). They will exchange requests and data among themselves.
3) User interface design:
Our designer is responsible for developing the design of the entire project. The interface is built taking into account ready-made solutions as references. At the moment, experiments are underway in Figma and the final layout is not ready.
4) Integration and API:
At this stage, we do not need an additional API. But our application architecture just implies using the API in the form of a special program on a computing cluster.
5) Scalability and performance: No
load test has been conducted yet, but scalability is at the heart of the architecture. In any case, the application can be installed on an additional server to increase performance.
6) Security and privacy:
It is planned to use asymmetric encryption to transfer all information and requests. It is also planned to store all user data in encrypted form so that data leakage does not have destructive consequences.
7) Error handling and fault tolerance:
Any non-critical errors will be logged for further processing. And a registry of unsolvable errors will be created and exceptions for them will be worked out. Moreover, this registry will be located on both applications since they perform different tasks.

### Team roles

Arina Zavelevich - UI/UX Designer
Aksinya Kochunova - Front-end
Ernest Mackewitch - Front-end
Rostislav Kulik - Back-end, team lead
Evgeny Sorokin - ML
Maxim Baranov - ML


### Questionnaire week 2:
Tech Stack Resources: we do not use specialized literature, first of all we work with Habr and other Internet resources. Probably, books will be needed on specific narrower areas, such as security, for example.

Mentorship Support: Danil Arapov, a 4th-year student, acts as a mentor for us, providing very significant information support as he has more knowledge on the topic of ML than ours.

Exploring Alternative Resources: Three main resources - Youtube, Habr, Kaggle


Learning Objectives: the main task of the project is to develop in the areas selected by the team members. So, for example, the part of the room engaged in ML will expand their knowledge, and the Front-end part will get a lot of useful experience. For better assimilation of new knowledge, the team regularly exchanges observations and experiences.


Sharing Knowledge with Peers: Yes, we organize the exchange of information found, although not always centralized (that is, not always in full). Most often, information is transmitted along the way.

AI: No, but the idea sounds promising. We'll try to use it.

### Week 3 report

At this stage of development, the main focus is on the development of an ML model, currently working with some manual edits for classification and regression tasks. We transmit the dataset, get the result in the form of a machine learning model and preprocessing parameters. A good accuracy of using this data on the test part of the dataset is demonstrated. In the near future, this part will be translated into the OOP version.

In addition, the scheme of the files and the interaction of the servers and the user for the exchange of this data has been thought out.

The design and user interface is also under development.

At this moment the project consists of several self-working prototypes. During the upcoming week we are going to unite them in MVP. Also, we have virtual server and domain name "click-ml.ru" for our project. This virtual server is responsive for site hosting. ML calculations that require GPU server on this stage will be executed on our local machines (laptops). This decision was made because of high prices of GPU servers.


## Weeks 4-6 report

[![Presentation](https://i.ibb.co/fDkmqm6/presi.jpg)](https://shorturl.at/pKX36)

In this report, we provide information about the work done during this time, testing, results, tasks and further prospects for the development of the project.

### Description of the project
[![Logo_link](https://i.ibb.co/C0JFLDK/link.png)](http://click-ml.ru/)

Many areas of human economic activity can be improved by the mass usage of machine learning and other artificial intelligence technologies. For most of the projects an AI-specialist is needed to insert the AI into decision making process. However, there exist areas where machine learning can be inserted without such specialists. For example, marketing, sociology, political technologies, economic planning and consulting. In these areas, there are already exist classical methods of analytics that can be improved by the usage of an AI. However, many companies refuse to improve the quality of their services as a result of the high work payments for Data Science specialists. And even if a DS specialist is involved in such work, its essence is limited to fairly simple tasks of classification and regression of available data.
Our project provides an opportunity to apply machine learning technologies without involving data science specialists. To do this, we use an approach of AI training, which is commonly called Auto-ML. Obviously, the set of tasks that can be solved using this approach is quite limited at the current stage of technology development. However, the amount of these tasks motivates us to create a tool in which Auto-ML can be accessible for anyone, even for those people who are not professionally connected with data analysis.
Our project, click-ml, provides an opportunity for any user to create their own machine learning model and get the results of its work "in two clicks". You do not need specialized knowledge to interact with our service. The end user shuld provide to the service only a CSV table with data for training, and a CSV table of an identical format for obtaining predictions from the model.
Interaction with the user is implemented through the website, where user can work with machine learning model without delving into the principles of its work.

### Accomplished work
[![Sceme](https://i.ibb.co/mJXFhkb/git2.png)](https://github.com/r-kulik/clickml)

* #### Machine Learning Tasks
   In order to perform the assigned classification or regression task, we use the `Optuna` library. With the help of this library, we start the process of researching and investigation for the best combination of hyperparameters of preprocessing and model training. The hyperparameter iteration space is a choice between the following options:
    * Method of inserting missing elements:
        * Mean
        * MostFrequent
    * Data scaling method:
        * Standart
        * Robust
        * MinMax
    * Type of machine learning model:
        * For regression:
            * LinearRegression
            * PolynomialRegression
            * XGboostRegression
        * For classification:
            * LogisticRegression
            * DecisionTree
            * RandomForest
            * XGboost Classifier

    Optuna uses Bayesian optimization for search, so it does not sort through unpromising options, which significantly increases the speed of convergence.
    In addition, obviously unnecessary columns are removed and automatic encoding occurs using one-hot encoder.

* #### Backend Part

    The backend part of our application is implemented using the Django framework (Python). During this time, we have accomplished work on creating and debugging Django views and models. At the moment, a user system has been implemented (registration, authorization of users in our application), a system for creating an ML-model training task, system for sending models for training, using ready-made ML-models, obtaining results. To implement these tasks, both databases and the server's file storage are used.

* #### Integration of system parts
    > For correct understanding of the next paragraph, we need to introduce the following notation:
        **VPS server** is the machine on which Django code is executed. It is engaged in receiving tasks and sending the results of the system to the current user. It is present in the system in a single instance.
        **GPU server** is the machine on which the models are trained and the calculations that are necessary to obtain the results are performed. The number of such machines in the system is unlimited.
        **GPU pool** is the set of currently working GPU-machines that are ready to complete the computational tasks

    We decided to implement a distributed computing system to save money. At the moment, the architecture of our service looks like this:

    [![Sceme](https://i.ibb.co/pyTQwXy/scheme.png)]()

    Theoretically, any computer can join the GPU pool if it runs `WebProcessing.py `. The script will start requesting calculation tasks, but if the task is not completeby the executor, it will become available for execution by other GPU servers again.
    The GPU machine requests tasks using an HTTP GET request, and sends interim progress reports to the VPS server, which makes them available to the user.

* #### Frontend part
    Using the standard HTML, CSS, JavaScript development stack, the appearance of click-ml.ru was completely created during these weeks. The design is based on layouts created by our design team.
    Also, to visualize the interim reports on the training of the model, we have mastered and integrated the WebSocket technology, which allows the user to track the results of training "online".

* #### Designs
     All designs were created using Figma and were approved by all members of the team.

### Testing

* #### Quality testing of ML-models

    Datasets from Kaggle were used for testing:
    * Binomial classification
        * https://www.kaggle.com/competitions/playground-series-s3e17 (Accuracy: ~0.915)
        * https://www.kaggle.com/c/titanic (Accuracy: ~0.82)
    * Polynomial classification:
        * https://www.kaggle.com/datasets/shivam2503/diamonds (Accuracy: ~0.85)
    * Regression
        * https://www.kaggle.com/competitions/house-prices-advanced-regression-techniques (RMSE: ~0.199, R2: 0.82)

    On average, according to the test results, accuracy that was demonstrated by our models was not inferior to the accuracy of a beginer DataScience specialist.

    Metrics used for internal testing:
    * For regression: **R2-score**
    * For binomial classification: **F1-score**
    * For multinomial classification: **ROC AUC** (One-vs-rest strategy)

* #### User's unwanted behaviour and stress testing
    We tried to run our ML-code on three different GPU machines with simultaneous upload of several correct and corrupted .csv files. On this stage we discovered several problems:
    * GPU-server must report errors that had been occured during the runtime to the server
    * For 5 simultaneous users with 25 models to train each even with 3 GPU machines waiting time is sugnificant. If we want to make this project public, we need much more faster GPU machines and aasynchronous task delivery and execution architecture
* #### User test
    We asked our friends try to use our website.
    Positive moments from their feedback:
    * Interface is simple, so it is easy to use it
    * Сolor scheme suits the purpose of our project
    * Hometasks from Introduction to Machine Learning course are completed ;-)

    Problems that they mentioned:
    * User should be able to see the results of learning during the process of model train
    * User should be able to see the reasons of exceptions that were caused by his unwanted behaviour. For this moment user can only see the exception traceback and unprepared user will have no idea how to interpreter it.


### Results
You can visit our website to see the results of our work. (But GPU machines can be turned off :-) )
[![Logo_link](https://i.ibb.co/C0JFLDK/link.png)](http://click-ml.ru/)
click-ml.ru

### Further tasks
* #### Error handling
    We assume that there can be problems, errors and bubg in our project. So, fixing them is out first priority.
* #### Safety improvements
    Intefaces for VPS-GPU communications are open and accessible for any user. We are going to implement secure system of task handling, encryption of source data and protect our server from attacs.
* #### Extension of user scenarios
    We want to suggest our user to choose from templated of datasets. For example, marketing specialist who are using our website ырщuld be able to predict the depth of the average check by using our template of dataset of purcases.
* #### Optuna improvements:
    For ML-part of our project we want to implement these improvements:
    * Correct processing of date and time. Now they practically do not give information to the model due to the fact that they are not recognized as date and time
    * Adding feature selection to increase the speed and efficiency of both training and prediction
    * Adding automatic feature creation using the `featuretools` framework.

### Project development prospects
* #### Apply Large Language Processing for interaction with the user
    In the future, it is planned to implement an LLP interface for closer and more accurate communication between the user and the trained model. So, the user will be able to describe more precisely what he wants to get, and the model will describe the processing steps, which will also help in interpretation. In addition, users who have some DS skills will be able to specify the necessary and unnecessary functions

* #### Extended system of visualization
    For exmaple we can add some graphs for user's better understanding of model training process. For example he will be able to see "online" the increasing the prediction accuracy during the work of `Optuna`
* #### Commercialization of the project
    For the full-fledged work of our project, GPU servers, data science specialists and the desire develop it are necessary. To do this, it is necessary to consider ways to commercialize the project. In the future, we would like to implement a subscription system for our project for regular users, and display ads for users without a subscription.
