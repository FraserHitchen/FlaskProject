## LO4.1
One area where the testing lacked was in system testing, since it was limited to manual UI testing and some performance testing. 

Starting with the UI testing, it was quite limited since the only tester was myself and the tests were performed manually rather than automatically. Having additional testers would likely reveal more test cases than I could think of personally, and performing black-box testing with those who don’t know the inner workings of the program could reveal faults that I might overlook as someone more familiar with the program.

The performance testing provided interesting results but was limited since I only have one machine to run it on, making it difficult to gauge how well it would hold up on a variety of hardware. In addition the performance testing was limited to load/stress testing on a short time frame, whereas with more time I could have also performed soak and endurance testing to see how the system fares with a sustained amount of traffic over a long period.

Other elements of software testing were missing mostly due to practicality, such as security and error testing. Since the project deals with personal information stored on databases, security would be important in a real production environment to ensure that user data is safe and not vulnerable to things such as SQL injection. Unfortunately I don’t know enough about these attacks to perform one on my own system. Error testing for situations such as network connectivity issues or server crashes would also be relevant in a real environment but are difficult to test with my resources and knowledge.

## LO4.2
Setting an exact target for test coverage is difficult since there are so many factors that go into it. For this project I feel that the most important aspects to consider for the testing coverage are the code coverage (the overall percentage of code being tested), the requirement coverage (the percentage of requirements begin tested) and the risk coverage (what risks have been checked for).

Due to the small size of the project, it should be possible to cover the majority of code and requirements so I would set the target levels for these metrics at around 80%.

The potential risks are harder to identify and test for considering the resources available to me so I would set a target level around 50%.

## LO4.3

Looking at the test coverage from my testing I believe the results are positive. Using the Coverage tool I calculated that the testing covers 91% of the code in  main.py. 

I believe that I have covered all of the requirements with at least one test case, so the requirements coverage is 100%.

The risk coverage is hard to quantify, while I have tested most of the internal risks such as bad requests I have performed limited testing of external risks such as malicious attacks, heavy stress testing or endurance testing. Since these would be very important issues if taken to production I would say that I have failed to meet the target for risk coverage.

## LO4.4
To achieve the target level I would need to perform additional testing focused on the risks of the program. In order to do this effectively and efficiently more resources and time would be needed, as well as additional testers to help with more white and black-box testing of the system.
