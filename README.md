
## CS321 - Software Engineering
**Project 1: Automated Eye Tracking Data Correction**<br>
*GitHub Repository: https://github.com/isabella-feng/CS421-project1*

### Abstract
In this project, I conducted a replication of the research project in the paper *Carr, Jon W., et al. "Algorithms for the automated correction of vertical drift in eye-tracking data." Behavior Research Methods 54.1 (2022): 287-310.* by generating simulation of 5 types of errors and run 10 algorithms on them. I compared the result and had a better understanding of vertical drift correction algorithms and their usage. 

### Results
For each of the 5 errors (noise, slope, shift, within-line regression, between-line regression) that were discussed in the essay, I run each of 10 correction algorithms with on them error magnitude / probability from 1 to 10 for 100 times. The results are as below.

For noise errors, the performance of *split*, *warp*, *compare*, and *segment* are very consistent across different probabilities of errors, while the accuracy for other algorithms declines as the errors become more frequent. Among the 10 algorithms, *split* performs the best with the highest mean accuracy and consistency. *segment* has the lowest mean accuracy.
![Fig 1. Noise error](/graphs/noise_comparison.png "Fig 1. Noise error")

For slope errors, we test with different magnitude of sloping from extremely downward to extremely upward. The performance of *merge*, *warp*, *compare*, and *segment* are very consistent across different probabilities of errors. The *regress* method performs fairly consistently but with dips when the slope was 0.4 and -0.4. The accuracy for other algorithms declines as the slop becomes more extreme. Among the 10 algorithms, *merge* performs the best with the highest mean accuracy and consistency. *split* has the lowest mean accuracy and is very inconsistent across different extent of sloping.
![Fig 2. Slope error](/graphs/slope_comparison.png "Fig 2. Slope error")

For shift errors, we test with different magnitude of shifting from extremely downward to extremely upward. The performance of *cluster*, *warp*, *compare*, and *segment* are very consistent across different probabilities of errors. Interestingly, merge is not very accurate when it's upward shifting but fairly accurate when it's downward shifting. The accuracy for other algorithms declines as the shift becomes more extreme. The *stretch* method in general performs poorly as the shift becomes more extreme, but with two dips when the shift was 0.4 and -0.4.  Among the 10 algorithms, *cluster* performs the best with the highest mean accuracy and consistency. *split* has the lowest mean accuracy and is very inconsistent across different extent of sloping.
![Fig 3. Shift error](/graphs/shift_comparison.png "Fig 3. Shift error")

For within-line regression errors, the performance of all algorithms delinces as the regression becomes more frequent. Among the 10 algorithms, *attach*, *cluster*, *regress*, and *stretch* perform the best with the highest mean accuracy. *compare* has the lowest mean accuracy.
![Fig 4. Within-line regression error](/graphs/within_line_reg_comparison.png "Fig 4. Within-line regression error")

For between-line regression errors, the performance of all algorithms declines dramatically as soon as between-line regression appears, and declines more as the regression becomes more frequent. The accuracy becomes fairly low and consistent when probability is above 4. Among the 10 algorithms, *warp* and *segment* perform slightly better than others. *compare* has the lowest mean accuracy.
![Fig 5. Between-line regression error](/graphs/between_line_reg_comparison.png "Fig 5. Between-line regression error")



### Discussions

Generally, my results are essentially similar to the ones presented in the original paper. Note that the *regress*' performance dip in slope error, which was brought to attention in the paper, is seen in my results. 

It is worth noting that the performance of *compare* is fair and is certainly not as bad as it was described in the paper. I deem that it is because we are using the simulated data instead of a real data, especially data from children. Therefore, since *compare* is bad with behaviors such as regression, it doesn't perform quite bad on simulated data with controlled variables. 

For two regression errors, the accuracy of all algorithms declines as opposed to some algorithms being invariant as shown in the paper. I suppose it may be due to the extent of regression error created, or the way that accuracy was calculated. 

### Extensions
- Create a version of the Warp algorithm that detects regressions and adapts to them.
Since my results for between-line regression errors do not show much variance among algorithms, I am creating this adapted version of Warp towards within-line regression. 
I use an algorithm to detect whether the collection of fixations has significant amount of within-line regression errors. If it has, *attach* is used instead of *warp*. 
The algorithm goes like this: 1) randomly select a fixation 2) check its next 10 fixations, and check whether there are more than 2 backward in x value, which means that there are regressions instead of return sweeps. Lastly, repeat these two steps for 10 times, and if 3 or more of them exhibit such regression behavior, use *attach*. Else use *warp*.
The result of *adapted_warp*, comparing to other algorithms after running on within-line regression errors for 100 times, is shown below. 
![Fig 6. adapted_warp on within-line regression error](/graphs/adatped_warp_comparison.png "Fig 6. adapted_warp on within-line regression error")
My *adapted_warp* algorithm has a mean accuracy of  0.80, whereas *warp* has only 0.76. *adapted_warp* is superior than *warp* because it takes the best of *attach* method when encountering regressions. 

### Reference
The code for 10 algorithms is acquired from J# on W. Carr's GitHub https://github.com/jwcarr/drift.







