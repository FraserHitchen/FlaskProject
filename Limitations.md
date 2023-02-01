While I believe that my approach in testing the program was generally good and the results were positive, there are still several limitations to my method.

One area where the testing lacked was in system testing, since it was limited to manual UI testing and some performance testing. 

Starting with the UI testing, it was quite limited since the only tester was myself and the tests were performed manually rather than automatically. Having additional testers would likely reveal more test cases than I could think of personally, and performing black-box testing with those who don’t know the inner workings of the program could reveal faults that I might overlook as someone more familiar with the program.

The performance testing provided interesting results but was limited since I only have one machine to run it on, making it difficult to gauge how well it would hold up on a variety of hardware. In addition the performance testing was limited to load/stress testing on a short time frame, whereas with more time I could have also performed soak and endurance testing to see how the system fares with a sustained amount of traffic over a long period.

Other elements of software testing were missing mostly due to practicality, such as security and error testing. Since the project deals with personal information stored on databases, security would be important in a real production environment to ensure that user data is safe and not vulnerable to things such as SQL injection. Unfortunately I don’t know enough about these attacks to perform one on my own system. Error testing for situations such as network connectivity issues or server crashes would also be relevant in a real environment but are difficult to test with my resources and knowledge.

Looking at the test coverage I believe the results are very positive. Setting an exact target for coverage is practically impossible since there are so many factors that go into it, but I believe that the 88% obtained from my testing indicates that the tests are covering the vast majority of important test cases.

However this number could also be quite easily improved, since the convergence tool I used shows which lines of code are not used. I could use that to go back and create additional unit tests, though this would take extra time which could be used for more important testing.

For my testing I had a test yield of 100%, indicating that all of the tests that I wrote passed. This is good since it indicates that all of the test cases worked as expected, but it doesn’t tell the whole story since with a coverage of 88% there are some pieces of code not being tested and there may be additional cases which I haven’t thought of and so have no code or tests.
