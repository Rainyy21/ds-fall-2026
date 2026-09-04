## Homework Submission
- All homework is due at 12:01 PM (noon) the day before the next class.
- All completed homework task links must be pasted into your HW Submission Sheet Google Sheet. (link to that is in bookmarked in slack). 
- Submit GitHub links to your PR completed exercise.

## Homework Instructions: How to hand in your HWs.
__HW assignments can be found in your syllabus under that week file__

__All HWs are due at 12:01 PM (noon) the day before the next class__

- Wednesday's class: HW due 12:01 PM on Tuesday
- Thursday's class: HW due 12:01 PM on Wednesday
- Friday's (both 12:30 PM and 06:30 PM): HW due 12:01 PM on Thursday

## There are usually 3 sections of HW every week.

### #1 Pre-Class HW [~1hr]
This covers the topic we are about to teach.  This is HW that will help you come to class better prepared to learn the material that week.
* Watch / read / do the tutorial listed above.
* Go to your class slack channel.  
* Find the usually most recent message from your TA instructor that says "Week X: Pre-Class learnings".
* Respond in-thread to that message with least one thing you learned from the videos/reading/or tutorial.
	* Your response can be It can be as short as one sentence, or as long as a book.
* Still in Slack, copy the link to your response.
* Pasted that to your response in HW Submission sheets Pre-Class column for that week.

__Submit by pasting the link to your message under the "Pre-Class Slack Link" column.__

### #2 Exercise HW [~1hr]

This is a coding assignment that you usually start in class. It is located in the `Exercise-DONT-EDIT-MAKE-COPY.ipynb` file.

#### Instructions

A bot reviews every homework PR automatically. It only merges your PR if the
filename and the folder are both exactly right, so read steps 2 and 4 carefully
— that's where almost every rejection comes from.

1. **Make a copy** of `Exercise-DONT-EDIT-MAKE-COPY.ipynb`.
   - Do **not** edit or submit the original template. Work only on your copy.
2. **Rename your copy.** The filename has to follow this exact pattern:

   ```
   {your_unique_id}_week_{NN}_exercise.ipynb
   ```

   - It **must end in `_exercise.ipynb`.** Not `_hw`, not `_homework`, not just your name.
   - `{NN}` is the week number. `week_01` and `week01` both work; it has to match the week folder you put it in.
   - `{your_unique_id}` must be either **`Firstname_Lastname`** or an identifier **containing at least one digit** (e.g. a student number). **Initials alone will be rejected** — we share this repo across all sections and initials collide.
   - ✅ Good:
     - `faizan_khan_week_03_exercise.ipynb`
     - `student_12345678_week_03_exercise.ipynb`
     - `Ada_Lovelace_week3_exercise.ipynb`
   - ❌ Rejected:
     - `faizan_khan_week_3_hw.ipynb` — doesn't end in `_exercise`
     - `Faizan_Khan_week1.ipynb` — missing `_exercise`
     - `fk_week_03_exercise.ipynb` — bare initials
     - `faizan_khan_week_03_excercise.ipynb` — typo in "exercise"
3. **Complete all questions** in your copy of the exercise notebook.
   - A copy that still matches the blank template gets flagged, not merged.
4. **Move it into the `exercise/` folder** for that week — e.g. `Week-01-Pandas/exercise/`.
   - Leaving it at the week's root (next to `Lecture.ipynb`) will be rejected.
   - The week number in your filename must match the week folder it's in.
5. **Delete any earlier copies.** If you renamed or moved the file, make sure the old one isn't still committed — one submission file per PR.
6. **One week per PR.** Don't bundle Week 1 and Week 2 into the same pull request.
7. **Push your completed notebook to your fork.**
   ```bash
   # NEVER DO:
   git add .

   # Instead, add only your exercise file:
   git add YOUR-EXERCISE-FILE.ipynb
   git commit -m "YOUR COMMIT MESSAGE"
   git push
   ```

### #3 LinkedIn Post [~10min]
Every week you have to post on LinkedIn. It can be anthing data science related unless instructed otherwise.

Publish the post (make sure its a public post.)

If no specific post topic is given that week, here are some topic ideas you can use.
* It can be about starting your CTP journey.
* Asking for advice on most important things to learn for entry level roles.
* Something you leanred in the pre-class videos.
* Why you love or hate pandas.
* Your favorite part about the class.
* A tip or trick that your learned in class.
* Anything related to data science or your journey.

Submit by putting the link to your LI post under the "LinkedIn Post" column.
