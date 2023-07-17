# 429 project

##Report

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
