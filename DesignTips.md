# Exploration Design Tips #

One of Oppia's strengths is its ability to bring interactivity and [guided discovery learning](https://teachingcommons.stanford.edu/resources/learning/learning-activities/guided-discovery-problems) to online, computer-based learning. Thus, a common format for an Oppia exploration is to pose a problem to the reader, and guide them towards solving this problem by posing a series of questions. This way, the reader actively discovers the answer with the exploration's help, as opposed to just being told what the answer is.

## General tips ##

Once you have a clear idea of what concept your exploration is trying to teach, it's usually easiest to start by coming up with a single series of questions and answers that might help a student understand this concept. These will form the "critical path" of your exploration -- the trunk on which all the other branches will depend. It doesn't really matter what this path is, as long as it goes all the way from start to finish.

As you outline this path, you will also want to think about how you'd like to present it. For example, a story format with the reader cast in the main role is very suitable for a discovery-style exploration: stories can help maintain interest in the subject of the exploration by drawing parallels between exploring a fictional world and investigating the concept you want to teach; and between resolving the plot of the story and solving the core problem in the exploration.

Even if you choose not to have an explicit story with characters, you should still think about characterization: if the exploration is a series of leading questions (with hints, examples, etc.), who is asking these questions, and why? Are they an authority figure who already knows everything, or a fellow learner who comes up with ideas when the real student can't quite make the leap? The latter is more consistent with the idea of "discovery learning", and students are likely to be more receptive to it.

## Exploration design patterns ##
Once you've implemented a basic version of the exploration in Oppia, you can add different branches to it as necessary. There are several common design patterns you can use for this:

### Common misconceptions ###
If you know or anticipate that students will get a question wrong in a particular way (like, say, forgetting to multiply an answer by 2 in a math problem), you can catch that with an appropriate answer classifier and redirect those students to a longer, more elaborate explanation of the topic. After that, this longer path would then typically rejoin the critical path.

### Shortcuts ###
Conversely, if your critical path assumes that a topic typically needs a pretty detailed explanation, you might consider putting in a shortcut answer that would allow a student who has already understood the topic to skip the long path. This works especially well with text or other open-ended input - in such cases, there is often the "mostly-correct" answer that sends the student on the typical path, and the "really nailed it" answer that shows that the student already has a handle on the concept and can jump ahead.

### Loopbacks ###
Another way to deal with wrong answers is to simply loop back and ask the question again. But for this to be beneficial and educational, you must tell the student what was wrong with his answer. Therefore, when using loopbacks like this, you should classify the possible wrong answers in as much detail as possible, and provide detailed feedback on why a particular answer was wrong. (It might also be a good idea to mix and match: loop the student back to the question for simple mistakes, but take them on a longer path that addresses their misconception in detail if they make a more fundamental error.)

There are some considerations and issues to watch out for when using loopbacks:
  * **Do** provide specific feedback about why the answer was wrong (or why the student is being redirected back to this state). This feedback should be constructive enough to help the student find the correct answer.
  * **Do** consider restating or rephrasing the original question in the feedback. This way you are reminding the student what the question was, they may get a better insight with a different phrasing of the same question, and you avoid creating ambiguity with a different question.
  * **Don't** ask a different question in your feedback: It is often surprisingly tempting to phrase your feedback in the form of a question: "What if we tried it this way?" or "What about this number?" But this becomes really confusing for the reader because they are now trying to answer this new question, whereas the exploration is expecting an answer to the original question.
  * **Don't** use loopbacks for incorrect text-field answers (or other free-form classifiers). Avoid situations where there's just one "correct" answer that moves you along, but lots of wrong answers that make you loop back and guess again. Having to read the exploration creator's mind can be very frustrating.
    * A good rule of thumb for whether you should use loopbacks is whether you can separate all the possible "wrong" answers into large groups, for which you can provide explicit helpful feedback that gives the reader more information. If not, you may be better off branching into a longer explanatory branch on a wrong answer. Getting the correct answer on the first guess would then become a "shortcut", rather than form an obstacle that gates the reader's progress.

### Coming back to earlier states ###
It's fine for an exploration to contain cycles. Certain paths that a student takes may bring him back to an earlier state in the exploration, even after he's progressed past it once. The primary reason for this is review: if the student seems completely confused about an earlier topic, the best thing to do may be to go through that topic again.

One bad pattern to avoid here is making the student repeat and review many topics because he forgot or messed up one of them. If you bring a student back to an earlier state, make sure there's also an easy way for them to get back to where they were, once the review is done (perhaps by taking shortcuts that you've put in for students who already know the answers).

### Giving the student an explicit choice ###
You don't always have to guess what's best for the student, or what the student would like to do next. Sometimes you can just ask them! Choice will give them a sense of agency, and might make them a bit more involved in what they're doing, since they chose it! For example, you can ask them things like: which sub-topics they would like to cover (or which ones they would like to cover first), how much detail they'd like to go into in the next explanation (short path or long?), how they'd like you to explain something (pictures? text? a game?), or whether they'd like to practice a skill you just taught.

### Implicit choice through a free-form answer ###
You can also make the choice implicit. Ask a somewhat open-ended question, and branch based on that answer. One very general way to do this is to just ask "Do you have any ideas on how to solve that problem?" and if they mention a specific sub-topic, you can branch on that and address that sub-topic first. This is very effective in making the student feel engaged and like he's actively participating in a discussion: it feels great when you type in an answer and Oppia actually responds to exactly what you said!
  * Students can sometimes get confused and lost if the question is too broad or open-ended, because they are unsure of what exactly is expected of them. They may just say "I don't know". In that case, the exploration can simply go on with a detailed guided walkthrough of the topics involved. If you use a broad question like this, try to make it clear that there's no one right (or wrong) answer; you're just looking for ideas. Or, if you have a specific type of answer in mind, be as explicit as possible about what you're looking for - without giving away the answer, of course! Ultimately, it's up to you as the exploration creator to moderate the broadness of the question.
  * These open-ended questions are also a good time to catch possible misconceptions. In addition to branching on interesting sub-topics the reader might mention, you can also branch on responses that indicate some kind of confusion or misunderstanding.
  * When you are classifying a free-form answer, you don't have to commit to saying whether the answer was "right" or "wrong". Even if your classifiers didn't catch any of the keywords you were looking for, the exploration (or the characters) can simply explain your own point of view on the question and then go from there. This feels more conversational, and won't frustrate students who did have the right idea, but didn't use the words you expected.
  * If the student's answer does trigger a keyword-based classifier, try repeating the triggering words in the feedback that you give for that answer (in a complete sentence, of course). This creates an explicit echo to what the student has just said. It also gives you a chance to form a complete, clear thought around whatever concept triggered the classifier - maybe the student had only a vague idea of what he was talking about, but now it is as if both of you discovered and clarified the idea together.

### Practice exercises and testing ###
Interaction and hands-on experiences can help students better understand and retain the material. And testing of course is important for making sure that the student understood things correctly. Tests, exercises, and hands-on activities can either use custom interactions that you (or someone else!) has built, or simply use Oppia's classifiers. You can also branch based on the results of an exercise: did the student do what you expected? are there certain weak areas that the exercise revealed, that need to be addressed more?

In a way, of course, all of an Oppia exploration is an interactive exercise! But it can be helpful to think of the exploration as separated into "learning" sections and more concentrated "exercise" sections that focus more on repetition and testing of what the student has already learned.

### Optional side-topics ###
Some readers may be interested in learning about or exploring additional topics. You can add side diversions that take take them on a completely optional branch (if they select that option), and then bring them back to the main exploration once that branch is over.

### Counterexamples ###
Counterexamples are a great way to provide feedback for a wrong answer. They are very much in line with the idea of discovery learning - exploring potential answers and seeing patterns in why they are wrong helps the student form a correct model of the problem herself, without relying on passive explanations.


## Parameter-based design patterns ##
Oppia's parameter functionality enables a number of interesting design patterns. You can find a more detailed guide to using parameters, including more specific examples, [here](Parameters.md).

### Randomized questions ###
It's easy to create a randomized parameter that takes one of several specified values at random. You can then use this parameter in a question, so that the question is slightly different every time the student sees it.

### The second time around ###
Often, when a student returns to a state he or she already visited, the original phrasing of the question or statement doesn't make much sense anymore. If you use a parameter to keep track of whether the state's been visited before, you can rephrase the text of the state slightly the second time around using an expression that's something like: `{{"'So, how do you think he does it?' asks your friend." if 1==(redux|int) else "Ah, so where were we again?"}}` In this case, if the parameter "redux" is set to 1, the second phrase is used; if it is not, then the first phrase is used. (You will also need to have a parameter change in that state, setting the parameter appropriately.) You can extend this technique to keep track of the number of times the state's been visited, and display slightly different things depending on that number.

The same technique can also work to give slightly different feedback depending on how the student got to the current state, for example: `{{"Did you take the train here?" if 1==(train_taken|int) else "How did you get here?! I didn't see you on the train"}}`

### Parameterized feedback ###
Sometimes it's useful to use parameters in the feedback you give to the students, especially if the question and answer used those same parameters in some way. This works especially well with math-related explorations and numeric answers, because you can easily perform arithmetic on numerical parameters, and tailor your feedback to apply precisely to the student's answer. You can use expressions like {{(answer|int)+1}} or {{(value1|int)/(value2|int)}} to manipulate and process parameters before displaying them in the feedback (or anywhere else).

### Echoing back the answer ###
Even if your exploration is not mathematical, it can be useful to echo back the student's answer either immediately ("Oh, so you think that {{answer}}?") or later on ("I think you said that your favorite color was {{color}}?"). For the latter case, you'd have to remember that answer using a dedicated parameter ("color" in the example).

