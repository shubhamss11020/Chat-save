---
conversation_id: d4fdcac2-c41a-41b9-8297-a9f17aee2e82
platform: claude
username: "harsh"
title: "Claude co-work automation prompt setup"
created_at: "2026-10-13 14:23:58 EDT"
updated_at: "2026-10-13 15:06:23 EDT"
---

# Claude co-work automation prompt setup

## User (2026-10-13 14:23:29 EDT)

I want you to make an claude co-work automation prompt, here is the call transcript that lists down the requirements. 

I want that I tell this AI to go and see in my calendar which calls were received. Right, all those fireflies calls are in OB. He picked up all the calls from OB.
After picking up all those calls, like a creative director, assess what discussion was there in these calls. From this material, now go and make a council of four people who will decide that they can pick up an interesting conversation from this. Right, that what was discussed in today's call, what is the differentiator in askrews, whatever was happening in the discussions.
Right, now you got the need that I have to make content on this thing. Now go and on this conaskrews am giving you a framework. Think that I have to go on Fiverr.
And on Fiverr, I need a top class person, with triple A rating, who will convert this into a video. Think like him and now go and make his video. Do all this work by yourself at 6 in the evening and email me the link of three videos of the day.

Tell me your understanding first and list down the items that we would need to setup on the claude id to make this working

## Claude (2026-10-13 14:23:58 EDT)

> *Thinking:*
>

I'll start by reading the skill files.

Here's my understanding, and what we'd need to set up before I write the final prompt.

## My understanding

Every day at 6 PM, Cowork runs this pipeline on its own:

1. **Find the day's calls.** It checks your Google Calendar for meetings that happened today, then pulls the matching Fireflies transcripts from your Obsidian (OB) vault.
2. **Read them as a creative director.** It identifies what was discussed, what made AskCruz different, and any interesting moments.
3. **Run a council of four.** Four distinct personas debate and pick the three strongest content ideas of the day. I'd suggest a Strategist, a Storyteller, a Skeptical Buyer and a Social-Media Editor, but you can name your own.
4. **Apply your framework.** Each idea is shaped using the content framework you'll give me.
5. **Think like a top Fiverr video creator.** It takes the role of a triple-A-rated freelancer hired to turn each idea into a video, and produces a script, scenes and the final video.
6. **Email you.** You get one email with links to the three videos of the day.

## What we'd need to set up

**Already connected in your account:**
- Google Calendar
- Gmail
- Google Drive
- Canva

**Still needed:**
1. **Obsidian vault access.** Cowork needs the vault folder shared with it, and I need to know where the Fireflies notes land (folder name and file format). Your AskCruz connector can also list Fireflies calls directly, which would be a fallback.
2. **A scheduled task in Cowork.** It runs daily at 6 PM, but only while your computer is awake and the Claude desktop app is open.
3. **Your framework document.** Save it in a folder Cowork can read. It should cover the AskCruz positioning and differentiators, tone, audience, video length and aspect ratio (for example 9:16, 45 to 60 seconds), and hook and CTA rules.
4. **A video-making method.** This is the biggest gap, because Claude can't render video on its own. The options are:
   - **Claude-built animated pages.** Claude builds an animated video page and gives you a share link. It's free and simple, but it's not a true MP4.
   - **Canva.** Claude builds the video in Canva and shares the link.
   - **An external video tool.** An AI video service such as HeyGen or Runway, plus a voiceover tool, connected through their API. It gives the most polished result, but you'd need to supply the accounts and keys.
5. **A place to store the videos.** A Google Drive folder with link sharing, so the email can carry real links.
6. **Email behavior.** The Gmail connector may only create a draft rather than send. We'd confirm that in a test run, and if it can't send, I'd suggest emailing you the drafts or using Slack as the alert.
7. **A "topics already used" log.** A small file the task checks and updates, so you don't get the same idea twice.
8. **Confidentiality rules.** Client calls are sensitive, so the prompt should say: no client names, numbers or private details in any video unless you've approved them.
9. **A fallback for quiet days.** What it should do if there were no calls, or fewer than three usable topics.

Which video method (item 4) do you want to start with? That choice shapes the rest of the prompt, and I'll write the full Cowork prompt once you decide.

One note: this chat should be archived under your team's process, but the transcript-saving tool isn't connected in this session, so I couldn't save it.

## User (2026-10-13 14:26:18 EDT)

1. you can get the call info from Askcruz vault. For the first draft just pick a call with enriched trasncript on which content can be made 
2. Yes 
3. Yes 
4. No, just think like a hiring agent, go to fibberr website to look for applicants and their experience to replicate their expertise. Its ok if the the quality is not avg right now 
5. You will generate a video on the idea and upload that into a google drive 
6. You will send me the google drive link on my email 

Working on the connector, work on making the prompt.

## Claude (2026-10-13 14:26:39 EDT)

> *Thinking:*
>

Here's the Cowork prompt. Fill in the three `[BRACKETED]` placeholders before scheduling it.

```
# DAILY ASKCRUZ CONTENT FACTORY (runs every day at 6:00 PM)

You are the Creative Director of AskCruz's content studio. Your job is to turn
today's real conversations into three short videos and email me the Google
Drive link. Work fully autonomously. Do not ask me questions. If something
fails, use the fallbacks in Step 8.

## SETTINGS
- MY_EMAIL: [YOUR EMAIL]
- FRAMEWORK_FILE: [PATH TO YOUR FRAMEWORK DOC]
- DRIVE_FOLDER: [GOOGLE DRIVE FOLDER NAME OR LINK]
- DRAFT_MODE: ON
  (When ON: make only ONE video from ONE call, to test the pipeline.
   When OFF: run the full daily flow and make three videos.)

## STEP 1: GATHER TODAY'S CALLS
1. Check Google Calendar for today's meetings, to know which calls happened.
2. Use the AskCruz connector (list_calls with source "fireflies", and also
   search_calls if needed) to find the matching call transcripts.
3. Read each transcript in full with get_call.
4. If DRAFT_MODE is ON: skip the calendar match. Pick ONE recent call that has
   an enriched transcript and enough substance to make content from. Prefer
   calls about what makes AskCruz different, client pain points, or insights.
5. If there are no usable calls, email me one line saying so and stop.

## STEP 2: ACT AS CREATIVE DIRECTOR
For each call, write a short assessment:
- What was discussed?
- What was the most interesting, surprising or quotable moment?
- What does it show about how AskCruz is different from alternatives?
- What problem would a viewer instantly recognise?

## STEP 3: HOLD THE COUNCIL OF FOUR
Run a written debate between four personas. Each one proposes and critiques ideas:
1. The Strategist: does this strengthen AskCruz's positioning and differentiator?
2. The Storyteller: does it have a hook, tension and payoff?
3. The Skeptical Buyer: would a real prospect care, or is it fluff?
4. The Social Editor: would it stop the scroll in the first 2 seconds?

Output the top 3 ideas (top 1 if DRAFT_MODE is ON). For each idea give:
a one-line concept, the hook, and why the council picked it.

## STEP 4: APPLY MY FRAMEWORK
Open FRAMEWORK_FILE and shape every chosen idea strictly by it (tone,
audience, structure, length, format, CTA). If the file is missing or
unreadable, say so in the email and use a sensible default: 9:16, 45 to 60
seconds, strong hook, one clear idea, soft CTA.

## STEP 5: HIRE LIKE A FIVERR AGENT
Before producing the video, research who the best people are:
1. Using the browser, go to fiverr.com and search for short-form video editors
   and explainer video creators.
2. Look only at sellers with top ratings (4.9+), many reviews, and Top Rated
   or Pro status.
3. Read their gig descriptions, portfolios and the praise in their reviews.
   Note what they actually do: pacing, hooks, captions, structure, brief
   questions, deliverables.
4. Write a short "Hiring Notes" summary: the 3 best candidates, their
   strengths, and which techniques you will copy.
5. Do not contact, message or pay anyone. This is research only.

## STEP 6: PRODUCE THE VIDEO AS THAT FREELANCER
Take on the role of the best candidate and deliver the way they would:
1. Write the script with timed scenes, on-screen text and a caption file.
2. Build the video using the tools available on this computer (for example
   Python, ffmpeg or Remotion for animated text, scenes and captions).
   Output a real .mp4 file.
3. Quality can be basic for now. Follow the framework and make the hook strong.
4. Save the script and Hiring Notes next to the video.

## STEP 7: UPLOAD AND EMAIL
1. Upload the video, script and Hiring Notes to DRIVE_FOLDER, in a
   subfolder named with today's date (YYYY-MM-DD).
2. Make sure the link is viewable by me.
3. Send an email to MY_EMAIL.
   Subject: "AskCruz content of the day: [date]"
   Body: for each video, the title, the one-line idea, why the council chose
   it, and the Drive link. Keep it short and easy to read on a phone.

## STEP 8: FALLBACKS
- If you cannot create an .mp4: deliver the full script, scene plan and
  caption file as a Google Doc in Drive, and say clearly in the email that
  the video was not rendered and why.
- If you cannot send email: save the email as a Gmail draft and tell me
  in your final message.
- If Fiverr blocks you: say so in the Hiring Notes and rely on best practice.

## RULES
- Never include client names, company names, revenue figures, or private
  details from calls in any video, script or email, unless the framework
  file explicitly allows it. Anonymise everything ("a mid-size manufacturer").
- Never invent facts, numbers or quotes that are not in the transcripts.
- Keep a log file called "topics_used.md" in DRIVE_FOLDER. Check it first to
  avoid repeating an idea, and add each new one after finishing.
- End by giving me a 3-line summary of what you did.
```

Three things to know before you rely on this:
- **Video rendering is the shakiest step.** An .mp4 depends on a tool like ffmpeg being installed on your machine. The fallback in Step 8 makes sure you still get a usable script if rendering fails.
- **Gmail may only create drafts.** Test this once, and if it can't send, the prompt already falls back to a draft.
- **Run it once manually first** with `DRAFT_MODE: ON`. After one good run, switch it to OFF and schedule it for 6 PM.

Your transcript-saving tool still isn't connected in this session, so this chat wasn't archived.

## User (2026-10-13 14:29:25 EDT)

You wont find the calls with my gmail connected, for now make a test prompt that looks for calls from our askcruz vault by date. rest is connected

## Claude (2026-10-13 14:29:37 EDT)

> *Thinking:*
>

Here's the test prompt. It skips the calendar and finds calls in the AskCruz vault by date. It makes one video and is meant to be run manually.

```
# ASKCRUZ CONTENT FACTORY: TEST RUN (one call, one video)

You are the Creative Director of AskCruz's content studio. Turn one real call
into one short video and email me the Google Drive link. Work autonomously.
Do not ask me questions. If something fails, use the fallbacks in Step 8.

## SETTINGS
- MY_EMAIL: [YOUR EMAIL]
- FRAMEWORK_FILE: [PATH TO YOUR FRAMEWORK DOC]
- DRIVE_FOLDER: [GOOGLE DRIVE FOLDER NAME OR LINK]
- TARGET_DATE: [YYYY-MM-DD, or leave blank for today]

## STEP 1: FIND CALLS IN THE ASKCRUZ VAULT (by date)
1. Do NOT use Google Calendar or Gmail to find calls. The AskCruz connector
   is the only source.
2. Use list_calls with source "fireflies" and month set to the month of
   TARGET_DATE (YYYY-MM). From the results, keep only calls dated TARGET_DATE.
   If TARGET_DATE is blank, use today's date.
3. If no calls match that date, widen to the most recent date that has calls
   (check the previous days in the same month, then the previous month).
   Say which date you ended up using.
4. Open each candidate with get_call (use the call's "id") and read the full
   transcript.
5. Pick ONE call that has an enriched transcript and enough substance for
   content: a clear problem, insight, or a moment showing what makes AskCruz
   different. Skip small talk, scheduling calls and very short calls.
6. If no call is usable, email me one line saying so and stop.

## STEP 2: ACT AS CREATIVE DIRECTOR
Write a short assessment of the chosen call:
- What was discussed?
- The most interesting, surprising or quotable moment
- What it shows about how AskCruz is different
- What problem a viewer would instantly recognise

## STEP 3: HOLD THE COUNCIL OF FOUR
Run a written debate between four personas:
1. The Strategist: does it strengthen AskCruz's positioning?
2. The Storyteller: does it have a hook, tension and payoff?
3. The Skeptical Buyer: would a real prospect care, or is it fluff?
4. The Social Editor: would it stop the scroll in the first 2 seconds?
Pick the single best idea. Give the one-line concept, the hook, and why the
council chose it.

## STEP 4: APPLY MY FRAMEWORK
Open FRAMEWORK_FILE and shape the idea strictly by it. If it is missing, say
so in the email and default to 9:16, 45 to 60 seconds, strong hook, one idea,
soft CTA.

## STEP 5: HIRE LIKE A FIVERR AGENT (research only)
1. In the browser, go to fiverr.com and search for short-form video editors and
   explainer video creators.
2. Look at sellers rated 4.9+ with many reviews and Top Rated or Pro status.
3. Read their gigs, portfolios and reviews. Note their pacing, hooks, captions,
   structure and deliverables.
4. Write "Hiring Notes": the 3 best candidates, their strengths, and which
   techniques you will copy.
5. Do not contact, message or pay anyone.

## STEP 6: PRODUCE THE VIDEO AS THAT FREELANCER
1. Write a script with timed scenes, on-screen text and a caption file.
2. Build the video with tools on this computer (Python, ffmpeg or Remotion).
   Output a real .mp4. Basic quality is fine for this test.
3. Save the script and Hiring Notes next to the video.

## STEP 7: UPLOAD AND EMAIL
1. Upload the video, script and Hiring Notes to DRIVE_FOLDER, in a subfolder
   named with the call date used (YYYY-MM-DD).
2. Make sure I can view the link.
3. Email MY_EMAIL. Subject: "AskCruz content test: [date]". Body: the call date
   and title used, the idea, why the council chose it, and the Drive link.
   Keep it short and easy to read on a phone.

## STEP 8: FALLBACKS
- If you cannot create an .mp4: upload the script, scene plan and captions as a
  Google Doc, and say in the email that the video was not rendered and why.
- If you cannot send email: save it as a Gmail draft and tell me.
- If Fiverr blocks you: say so in the Hiring Notes and rely on best practice.
- If the AskCruz connector returns nothing, say exactly which call was
  attempted and stop. Never invent a call.

## RULES
- Never include client names, company names, revenue figures or private details
  from the call in any video, script or email. Anonymise everything
  ("a mid-size manufacturer").
- Never invent facts, numbers or quotes that are not in the transcript.
- End with a 3-line summary: the call used, the idea chosen, the Drive link.
```

Before running it, replace the four placeholders. The AskCruz `list_calls` tool filters by month only, so the date matching happens inside the prompt, as written in Step 1.

When this test works, we can change Step 1 to pull all of the day's calls and run the council for three videos, then schedule it for 6 PM.

Your transcript-saving tool still isn't connected in this session, so this chat wasn't archived.

## User (2026-10-13 14:32:09 EDT)

why is it asking for folder link, just uploading whereever should do. Also what is framework file?? i dont have it. Make the prompt function without it

## Claude (2026-10-13 14:32:22 EDT)

> *Thinking:*
>

Fair on both. I asked for the Drive folder only to keep things tidy, and the framework file came from your call, where you said you'd provide one. Both are now gone. The prompt creates its own "AskCruz Content" folder in your Drive if needed, and it uses a default framework built into the prompt itself.

```
# ASKCRUZ CONTENT FACTORY: TEST RUN (one call, one video)

You are the Creative Director of AskCruz's content studio. Turn one real call
into one short video and email me the Google Drive link. Work autonomously.
Do not ask me questions. If something fails, use the fallbacks in Step 8.

## SETTINGS
- MY_EMAIL: [YOUR EMAIL]
- TARGET_DATE: [YYYY-MM-DD, or leave blank for today]

## DEFAULT CONTENT FRAMEWORK (use this for every video)
- Format: vertical 9:16, 45 to 60 seconds, burned-in captions.
- Hook (0-3s): one bold line that states a problem, a surprising claim or a
  question the viewer instantly recognises. No intros, no logos first.
- Problem (3-15s): the pain, in plain words a business owner would use.
- Insight (15-40s): what was learned or decided, told as a short story with
  one concrete example.
- Differentiator (40-52s): how AskCruz approaches this differently.
- CTA (last 5s): soft and conversational, e.g. "Follow for more" or
  "Want this for your business? Talk to us."
- Tone: confident, simple, human. No jargon, no hype, no filler.
- One idea per video. Fast pacing, a new visual or text beat every 2-3 seconds.

## STEP 1: FIND CALLS IN THE ASKCRUZ VAULT (by date)
1. Do NOT use Google Calendar or Gmail to find calls. The AskCruz connector
   is the only source.
2. Use list_calls with source "fireflies" and month set to the month of
   TARGET_DATE (YYYY-MM). From the results, keep only calls dated TARGET_DATE.
   If TARGET_DATE is blank, use today's date.
3. If no calls match that date, widen to the most recent date that has calls
   (check the previous days in the same month, then the previous month).
   Say which date you ended up using.
4. Open each candidate with get_call (use the call's "id") and read the full
   transcript.
5. Pick ONE call that has an enriched transcript and enough substance for
   content: a clear problem, insight, or a moment showing what makes AskCruz
   different. Skip small talk, scheduling calls and very short calls.
6. If no call is usable, email me one line saying so and stop.

## STEP 2: ACT AS CREATIVE DIRECTOR
Write a short assessment of the chosen call:
- What was discussed?
- The most interesting, surprising or quotable moment
- What it shows about how AskCruz is different
- What problem a viewer would instantly recognise

## STEP 3: HOLD THE COUNCIL OF FOUR
Run a written debate between four personas:
1. The Strategist: does it strengthen AskCruz's positioning?
2. The Storyteller: does it have a hook, tension and payoff?
3. The Skeptical Buyer: would a real prospect care, or is it fluff?
4. The Social Editor: would it stop the scroll in the first 2 seconds?
Pick the single best idea. Give the one-line concept, the hook, and why the
council chose it.

## STEP 4: SHAPE THE IDEA WITH THE DEFAULT FRAMEWORK
Map the chosen idea onto the structure in DEFAULT CONTENT FRAMEWORK above:
hook, problem, insight, differentiator, CTA.

## STEP 5: HIRE LIKE A FIVERR AGENT (research only)
1. In the browser, go to fiverr.com and search for short-form video editors and
   explainer video creators.
2. Look at sellers rated 4.9+ with many reviews and Top Rated or Pro status.
3. Read their gigs, portfolios and reviews. Note their pacing, hooks, captions,
   structure and deliverables.
4. Write "Hiring Notes": the 3 best candidates, their strengths, and which
   techniques you will copy.
5. Do not contact, message or pay anyone.

## STEP 6: PRODUCE THE VIDEO AS THAT FREELANCER
1. Write a script with timed scenes, on-screen text and a caption file.
2. Build the video with tools on this computer (Python, ffmpeg or Remotion).
   Output a real .mp4. Basic quality is fine for this test.
3. Save the script and Hiring Notes next to the video.

## STEP 7: UPLOAD AND EMAIL
1. Upload the video, script and Hiring Notes to Google Drive. Use a folder
   named "AskCruz Content" (create it if it does not exist), with a subfolder
   for the call date used (YYYY-MM-DD).
2. Make sure I can view the link.
3. Email MY_EMAIL. Subject: "AskCruz content test: [date]". Body: the call date
   and title used, the idea, why the council chose it, and the Drive link.
   Keep it short and easy to read on a phone.

## STEP 8: FALLBACKS
- If you cannot create an .mp4: upload the script, scene plan and captions as a
  Google Doc, and say in the email that the video was not rendered and why.
- If you cannot send email: save it as a Gmail draft and tell me.
- If Fiverr blocks you: say so in the Hiring Notes and rely on best practice.
- If the AskCruz connector returns nothing, say exactly which call was
  attempted and stop. Never invent a call.

## RULES
- Never include client names, company names, revenue figures or private details
  from the call in any video, script or email. Anonymise everything
  ("a mid-size manufacturer").
- Never invent facts, numbers or quotes that are not in the transcript.
- End with a 3-line summary: the call used, the idea chosen, the Drive link.
```

Only two placeholders remain: your email, and the date (or leave the date blank to use today). Once you've seen the first video, you can tell me what you'd change about the style and I'll fold it into the framework section.

Your transcript-saving tool still isn't connected in this session, so this chat wasn't archived.

## User (2026-10-13 14:49:19 EDT)

this is giving me this file, not the video. I want it to make the video

**Attachments:**
- 📎 **attachment** *(Attached in Claude conversation)*

## Claude (2026-10-13 14:49:43 EDT)

> *Thinking:*
>

That file is the script package, not the video. The doc describes a finished 59.4-second render, so the video was probably built on your machine but never reached Drive. I can't see the run, so that's an inference. It would also explain why only a text file arrived.

The cause is in my last prompt: Step 8 let the run settle for a script-only result, and nothing forced it to confirm that the .mp4 actually landed in Drive. This version makes the video the deliverable and treats a script-only result as a failure.

The Fiverr research failed for a separate reason: that run had no browser. The prompt now tries the Chrome browser first and skips Fiverr quickly if it's blocked, so it can't hold up the video.

```
# ASKCRUZ CONTENT FACTORY: TEST RUN (one call, one VIDEO)

You are the Creative Director of AskCruz's content studio. Turn one real call
into one finished short VIDEO FILE (.mp4) and email me the Google Drive link
to that video. The video is the deliverable. A script, a doc or notes alone
is NOT a successful run. Work autonomously. Do not ask me questions.

## SETTINGS
- MY_EMAIL: [YOUR EMAIL]
- TARGET_DATE: [YYYY-MM-DD, or leave blank for today]

## DEFAULT CONTENT FRAMEWORK
- Format: vertical 9:16 (1080x1920), 45 to 60 seconds, burned-in captions.
- Hook (0-3s): one bold line that states a problem, a surprising claim or a
  question the viewer instantly recognises. No intros, no logos first.
- Problem (3-15s): the pain, in plain words a business owner would use.
- Insight (15-40s): what was learned or decided, with one concrete example.
- Differentiator (40-52s): how AskCruz approaches this differently.
- CTA (last 5s): soft, e.g. "Want this for your business? Talk to us."
- Tone: confident, simple, human. No jargon, no hype.
- One idea per video. A new visual or text beat every 2-3 seconds.

## STEP 1: FIND THE CALL (AskCruz vault, by date)
1. Do NOT use Google Calendar or Gmail to find calls. Use the AskCruz
   connector only.
2. list_calls with source "fireflies" and month = month of TARGET_DATE. Keep
   calls dated TARGET_DATE (today if blank).
3. If none match, use the most recent date that has calls, and say which.
4. Read candidates in full with get_call (use "id").
5. Pick ONE call with an enriched transcript and real substance: a clear
   problem, insight, or what makes AskCruz different. Skip small talk and
   scheduling calls. If the recording has an internal part and a prospect
   part, use only the business-relevant part.
6. If nothing is usable, email me one line saying so and stop.

## STEP 2: CREATIVE DIRECTOR ASSESSMENT (keep it brief)
What was discussed, the most quotable moment, what it shows about how
AskCruz is different, and the problem a viewer would recognise.

## STEP 3: COUNCIL OF FOUR (keep it brief)
Strategist, Storyteller, Skeptical Buyer, Social Editor each give a short
verdict. Pick the single best idea with a one-line concept and a hook.

## STEP 4: MAP TO THE FRAMEWORK
Hook, problem, insight, differentiator, CTA, with timings.

## STEP 5: FIVERR RESEARCH (time-boxed, never blocks the video)
1. Try the Chrome browser tool on fiverr.com: search short-form video
   editors, look at sellers rated 4.9+ with many reviews and Top Rated or
   Pro status, and note their pacing, hooks and caption style.
2. If the browser is unavailable or Fiverr blocks you, do not retry. Write
   one line in Hiring Notes saying so and continue using short-form best
   practice. Never invent seller names.
3. Do not contact, message or pay anyone.

## STEP 6: BUILD THE VIDEO (THIS IS THE MAIN TASK)
1. Write the timed script and on-screen text.
2. Check the tools: run `ffmpeg -version` and `python3 --version`. If ffmpeg
   is missing, install it (pip install imageio-ffmpeg, or the system
   package). If Pillow is missing, pip install pillow.
3. Render every scene as a 1080x1920 image (large bold text, high contrast,
   branded colours, a progress bar, captions in the safe area), then stitch
   them into an .mp4 with ffmpeg (H.264, yuv420p, 30 fps). Add simple
   transitions or a subtle zoom so it is not static. Silent or with a
   simple background music track is fine for now.
4. Compress so the file is small enough to upload: target under 15 MB
   (for example `-crf 28 -preset slow`, 1080x1920 is still fine).
5. Verify the file with ffprobe: it must be a valid .mp4, about 45 to 60
   seconds, 9:16. If it fails, fix it and re-render. Try at least 3
   different approaches before giving up.
6. Name it: askcruz_content_YYYY-MM-DD.mp4. Also save the script, the SRT
   captions and the Hiring Notes as small text files next to it.

## STEP 7: UPLOAD THE VIDEO AND CONFIRM IT LANDED
1. In Google Drive, use a folder "AskCruz Content" (create it if needed) and
   a subfolder named with the call date (YYYY-MM-DD).
2. Upload the .mp4 FIRST, with the correct video/mp4 MIME type. Then upload
   the script, captions and notes as secondary files.
3. VERIFY the upload: read the file's metadata from Drive and confirm the
   mime type is video/mp4 and the size matches the local file. If it does
   not, re-upload. Try at least 3 times, and try a smaller compressed
   version if size is the problem.
4. Make sure I can view the video link.
5. Email MY_EMAIL. Subject: "AskCruz content test: [date]".
   Body, in this order: (1) the link to the VIDEO file itself, (2) the call
   date and title used, (3) the one-line idea and why the council picked
   it, (4) a link to the script folder. Keep it short, phone-friendly.

## STEP 8: IF THE VIDEO STILL FAILS
- The video is the goal. Do not end the run with only a script or a doc and
  call it done.
- If the video rendered but could not upload: keep it in the Cowork outputs
  folder, tell me the exact file path, and say so in the email and in your
  final message.
- If the video could not be rendered: the email subject must start with
  "FAILED: no video", the first line must explain exactly which step failed
  and the error, and then include the script as a fallback.
- If email sending is unavailable: save a Gmail draft and tell me.
- If the AskCruz connector returns nothing: say which call you tried, and stop.

## RULES
- Never include client names, company names, revenue figures or private
  details from the call anywhere. Anonymise everything.
- Never invent facts, numbers or quotes that are not in the transcript.
- End with a 3-line summary: call used, idea chosen, the video link (or the
  exact reason there is no video).
```

If the next run still doesn't deliver a video, the email will now name the failing step, so we'll know whether it's rendering or the Drive upload. If the Drive connector turns out to reject binary files, the fix is to have the video saved to your Cowork outputs folder instead. In that case tell me what error the run reports.

Your transcript-saving tool still isn't connected in this session, so this chat wasn't archived.

## Claude (2026-10-13 15:06:23 EDT)

Fair on both. I asked for the Drive folder only to keep things tidy, and the framework file came from your call, where you said you’d provide one. Both are now gone. The prompt creates its own “AskCruz Content” folder in your Drive if needed, and it uses a default framework built into the prompt itself.

# ASKCRUZ CONTENT FACTORY: TEST RUN (one call, one video)

You are the Creative Director of AskCruz's content studio. Turn one real call
into one short video and email me the Google Drive link. Work autonomously.
Do not ask me questions. If something fails, use the fallbacks in Step 8.

## SETTINGS
- MY_EMAIL: [YOUR EMAIL]
- TARGET_DATE: [YYYY-MM-DD, or leave blank for today]

## DEFAULT CONTENT FRAMEWORK (use this for every video)
- Format: vertical 9:16, 45 to 60 seconds, burned-in captions.
- Hook (0-3s): one bold line that states a problem, a surprising claim or a
  question the viewer instantly recognises. No intros, no logos first.
- Problem (3-15s): the pain, in plain words a business owner would use.
- Insight (15-40s): what was learned or decided, told as a short story with
  one concrete example.
- Differentiator (40-52s): how AskCruz approaches this differently.
- CTA (last 5s): soft and conversational, e.g. "Follow for more" or
  "Want this for your business? Talk to us."
- Tone: confident, simple, human. No jargon, no hype, no filler.
- One idea per video. Fast pacing, a new visual or text beat every 2-3 seconds.

## STEP 1: FIND CALLS IN THE ASKCRUZ VAULT (by date)
1. Do NOT use Google Calendar or Gmail to find calls. The AskCruz connector
   is the only source.
2. Use list_calls with source "fireflies" and month set to the month of
   TARGET_DATE (YYYY-MM). From the results, keep only calls dated TARGET_DATE.
   If TARGET_DATE is blank, use today's date.
3. If no calls match that date, widen to the most recent date that has calls
   (check the previous days in the same month, then the previous month).
   Say which date you ended up using.
4. Open each candidate with get_call (use the call's "id") and read the full
   transcript.
5. Pick ONE call that has an enriched transcript and enough substance for
   content: a clear problem, insight, or a moment showing what makes AskCruz
   different. Skip small talk, scheduling calls and very short calls.
6. If no call is usable, email me one line saying so and stop.

## STEP 2: ACT AS CREATIVE DIRECTOR
Write a short assessment of the chosen call:
- What was discussed?
- The most interesting, surprising or quotable moment
- What it shows about how AskCruz is different
- What problem a viewer would instantly recognise

## STEP 3: HOLD THE COUNCIL OF FOUR
Run a written debate between four personas:
1. The Strategist: does it strengthen AskCruz's positioning?
2. The Storyteller: does it have a hook, tension and payoff?
3. The Skeptical Buyer: would a real prospect care, or is it fluff?
4. The Social Editor: would it stop the scroll in the first 2 seconds?
Pick the single best idea. Give the one-line concept, the hook, and why the
council chose it.

## STEP 4: SHAPE THE IDEA WITH THE DEFAULT FRAMEWORK
Map the chosen idea onto the structure in DEFAULT CONTENT FRAMEWORK above:
hook, problem, insight, differentiator, CTA.

## STEP 5: HIRE LIKE A FIVERR AGENT (research only)
1. In the browser, go to fiverr.com and search for short-form video editors and
   explainer video creators.
2. Look at sellers rated 4.9+ with many reviews and Top Rated or Pro status.
3. Read their gigs, portfolios and reviews. Note their pacing, hooks, captions,
   structure and deliverables.
4. Write "Hiring Notes": the 3 best candidates, their strengths, and which
   techniques you will copy.
5. Do not contact, message or pay anyone.

## STEP 6: PRODUCE THE VIDEO AS THAT FREELANCER
1. Write a script with timed scenes, on-screen text and a caption file.
2. Build the video with tools on this computer (Python, ffmpeg or Remotion).
   Output a real .mp4. Basic quality is fine for this test.
3. Save the script and Hiring Notes next to the video.

## STEP 7: UPLOAD AND EMAIL
1. Upload the video, script and Hiring Notes to Google Drive. Use a folder
   named "AskCruz Content" (create it if it does not exist), with a subfolder
   for the call date used (YYYY-MM-DD).
2. Make sure I can view the link.
3. Email MY_EMAIL. Subject: "AskCruz content test: [date]". Body: the call date
   and title used, the idea, why the council chose it, and the Drive link.
   Keep it short and easy to read on a phone.

## STEP 8: FALLBACKS
- If you cannot create an .mp4: upload the script, scene plan and captions as a
  Google Doc, and say in the email that the video was not rendered and why.
- If you cannot send email: save it as a Gmail draft and tell me.
- If Fiverr blocks you: say so in the Hiring Notes and rely on best practice.
- If the AskCruz connector returns nothing, say exactly which call was
  attempted and stop. Never invent a call.

## RULES
- Never include client names, company names, revenue figures or private details
  from the call in any video, script or email. Anonymise everything
  ("a mid-size manufacturer").
- Never invent facts, numbers or quotes that are not in the transcript.
- End with a 3-line summary: the call used, the idea chosen, the Drive link.

Only two placeholders remain: your email, and the date (or leave the date blank to use today). Once you’ve seen the first video, you can tell me what you’d change about the style and I’ll fold it into the framework section.

Your transcript-saving tool still isn’t connected in this session, so this chat wasn’t archived.

## User (2026-10-13 15:06:23 EDT)

this is giving me this file, not the video. I want it to make the video

## Claude (2026-10-13 15:06:23 EDT)

That file is the script package, not the video. The doc describes a finished 59.4-second render, so the video was probably built on your machine but never reached Drive. I can’t see the run, so that’s an inference. It would also explain why only a text file arrived.

The cause is in my last prompt: Step 8 let the run settle for a script-only result, and nothing forced it to confirm that the .mp4 actually landed in Drive. This version makes the video the deliverable and treats a script-only result as a failure.

The Fiverr research failed for a separate reason: that run had no browser. The prompt now tries the Chrome browser first and skips Fiverr quickly if it’s blocked, so it can’t hold up the video.

# ASKCRUZ CONTENT FACTORY: TEST RUN (one call, one VIDEO)

You are the Creative Director of AskCruz's content studio. Turn one real call
into one finished short VIDEO FILE (.mp4) and email me the Google Drive link
to that video. The video is the deliverable. A script, a doc or notes alone
is NOT a successful run. Work autonomously. Do not ask me questions.

## SETTINGS
- MY_EMAIL: [YOUR EMAIL]
- TARGET_DATE: [YYYY-MM-DD, or leave blank for today]

## DEFAULT CONTENT FRAMEWORK
- Format: vertical 9:16 (1080x1920), 45 to 60 seconds, burned-in captions.
- Hook (0-3s): one bold line that states a problem, a surprising claim or a
  question the viewer instantly recognises. No intros, no logos first.
- Problem (3-15s): the pain, in plain words a business owner would use.
- Insight (15-40s): what was learned or decided, with one concrete example.
- Differentiator (40-52s): how AskCruz approaches this differently.
- CTA (last 5s): soft, e.g. "Want this for your business? Talk to us."
- Tone: confident, simple, human. No jargon, no hype.
- One idea per video. A new visual or text beat every 2-3 seconds.

## STEP 1: FIND THE CALL (AskCruz vault, by date)
1. Do NOT use Google Calendar or Gmail to find calls. Use the AskCruz
   connector only.
2. list_calls with source "fireflies" and month = month of TARGET_DATE. Keep
   calls dated TARGET_DATE (today if blank).
3. If none match, use the most recent date that has calls, and say which.
4. Read candidates in full with get_call (use "id").
5. Pick ONE call with an enriched transcript and real substance: a clear
   problem, insight, or what makes AskCruz different. Skip small talk and
   scheduling calls. If the recording has an internal part and a prospect
   part, use only the business-relevant part.
6. If nothing is usable, email me one line saying so and stop.

## STEP 2: CREATIVE DIRECTOR ASSESSMENT (keep it brief)
What was discussed, the most quotable moment, what it shows about how
AskCruz is different, and the problem a viewer would recognise.

## STEP 3: COUNCIL OF FOUR (keep it brief)
Strategist, Storyteller, Skeptical Buyer, Social Editor each give a short
verdict. Pick the single best idea with a one-line concept and a hook.

## STEP 4: MAP TO THE FRAMEWORK
Hook, problem, insight, differentiator, CTA, with timings.

## STEP 5: FIVERR RESEARCH (time-boxed, never blocks the video)
1. Try the Chrome browser tool on fiverr.com: search short-form video
   editors, look at sellers rated 4.9+ with many reviews and Top Rated or
   Pro status, and note their pacing, hooks and caption style.
2. If the browser is unavailable or Fiverr blocks you, do not retry. Write
   one line in Hiring Notes saying so and continue using short-form best
   practice. Never invent seller names.
3. Do not contact, message or pay anyone.

## STEP 6: BUILD THE VIDEO (THIS IS THE MAIN TASK)
1. Write the timed script and on-screen text.
2. Check the tools: run `ffmpeg -version` and `python3 --version`. If ffmpeg
   is missing, install it (pip install imageio-ffmpeg, or the system
   package). If Pillow is missing, pip install pillow.
3. Render every scene as a 1080x1920 image (large bold text, high contrast,
   branded colours, a progress bar, captions in the safe area), then stitch
   them into an .mp4 with ffmpeg (H.264, yuv420p, 30 fps). Add simple
   transitions or a subtle zoom so it is not static. Silent or with a
   simple background music track is fine for now.
4. Compress so the file is small enough to upload: target under 15 MB
   (for example `-crf 28 -preset slow`, 1080x1920 is still fine).
5. Verify the file with ffprobe: it must be a valid .mp4, about 45 to 60
   seconds, 9:16. If it fails, fix it and re-render. Try at least 3
   different approaches before giving up.
6. Name it: askcruz_content_YYYY-MM-DD.mp4. Also save the script, the SRT
   captions and the Hiring Notes as small text files next to it.

## STEP 7: UPLOAD THE VIDEO AND CONFIRM IT LANDED
1. In Google Drive, use a folder "AskCruz Content" (create it if needed) and
   a subfolder named with the call date (YYYY-MM-DD).
2. Upload the .mp4 FIRST, with the correct video/mp4 MIME type. Then upload
   the script, captions and notes as secondary files.
3. VERIFY the upload: read the file's metadata from Drive and confirm the
   mime type is video/mp4 and the size matches the local file. If it does
   not, re-upload. Try at least 3 times, and try a smaller compressed
   version if size is the problem.
4. Make sure I can view the video link.
5. Email MY_EMAIL. Subject: "AskCruz content test: [date]".
   Body, in this order: (1) the link to the VIDEO file itself, (2) the call
   date and title used, (3) the one-line idea and why the council picked
   it, (4) a link to the script folder. Keep it short, phone-friendly.

## STEP 8: IF THE VIDEO STILL FAILS
- The video is the goal. Do not end the run with only a script or a doc and
  call it done.
- If the video rendered but could not upload: keep it in the Cowork outputs
  folder, tell me the exact file path, and say so in the email and in your
  final message.
- If the video could not be rendered: the email subject must start with
  "FAILED: no video", the first line must explain exactly which step failed
  and the error, and then include the script as a fallback.
- If email sending is unavailable: save a Gmail draft and tell me.
- If the AskCruz connector returns nothing: say which call you tried, and stop.

## RULES
- Never include client names, company names, revenue figures or private
  details from the call anywhere. Anonymise everything.
- Never invent facts, numbers or quotes that are not in the transcript.
- End with a 3-line summary: call used, idea chosen, the video link (or the
  exact reason there is no video).

If the next run still doesn’t deliver a video, the email will now name the failing step, so we’ll know whether it’s rendering or the Drive upload. If the Drive connector turns out to reject binary files, the fix is to have the video saved to your Cowork outputs folder instead. In that case tell me what error the run reports.

Your transcript-saving tool still isn’t connected in this session, so this chat wasn’t archived.

## User (2026-10-13 15:03:25 EDT)

ok so it made the video but the drive link is not accessible by other id as it is not public, also we have a custom connector that makes videos with higgsfield, named Askcruz studio. Can u update the prompt to utilise that instead??

## Claude (2026-10-13 15:04:03 EDT)

I'll check how the Studio connector works so the prompt matches its tools.

> *Thinking:*
>

Here's the updated prompt. It builds the video entirely through AskCruz Studio, so Drive is no longer involved. The Studio `publish` tool returns a browser-playable link, which replaces the private Drive link.

```
# ASKCRUZ CONTENT FACTORY: TEST RUN (one call, one video, via AskCruz Studio)

You are the Creative Director of AskCruz's content studio. Turn one real call
into one finished short video using the AskCruz Studio connector, publish it,
and email me the link. Work autonomously. Do not ask me questions.
A script or doc alone is NOT a successful run. The deliverable is a
published video link.

## SETTINGS
- MY_EMAIL: [YOUR EMAIL]
- TARGET_DATE: [YYYY-MM-DD, or leave blank for today]
- CREDIT_BUDGET: 100 (maximum Higgsfield credits to spend on this video)

## STEP 1: FIND THE CALL (AskCruz vault, by date)
1. Do NOT use Google Calendar or Gmail to find calls. Use the AskCruz
   connector only.
2. list_calls with source "fireflies" and month = month of TARGET_DATE. Keep
   calls dated TARGET_DATE (today if blank).
3. If none match, use the most recent date that has calls, and say which.
4. Read candidates in full with get_call (use "id").
5. Pick ONE call with an enriched transcript and real substance: a clear
   problem, an insight, or what makes AskCruz different. Skip small talk and
   scheduling calls. If the recording has an internal part and a prospect
   part, use only the business-relevant part.
6. If nothing is usable, email me one line saying so and stop.

## STEP 2: CREATIVE DIRECTOR ASSESSMENT (brief)
What was discussed, the most quotable moment, what it shows about how
AskCruz is different, and the problem a viewer would instantly recognise.

## STEP 3: COUNCIL OF FOUR (brief)
Strategist, Storyteller, Skeptical Buyer and Social Editor each give a short
verdict. Pick the single best idea: a one-line concept and a hook (7 words
or fewer, readable in one second on a phone).

## STEP 4: FIVERR RESEARCH (time-boxed, never blocks the video)
Try the browser on fiverr.com for top-rated (4.9+, many reviews, Top Rated
or Pro) short-form video editors. Note their pacing, hooks and caption style.
If you cannot access it, write one line saying so and move on. Never invent
seller names. Do not contact, message or pay anyone.

## STEP 5: BUILD THE VIDEO IN ASKCRUZ STUDIO
Follow the Studio's own rules exactly. They come from real team rejections.
1. Call studio_guide first and follow it. Then call taste_references to see
   what the team approves and rejects.
2. Call creative_brief with the topic, audience (small businesses in any
   vertical), length 30 to 45 seconds and aspect 9:16. Choose the strongest
   direction for this idea. Pass its concept_id to create_project.
3. create_project with brand "askcruz". Use ONLY claims from the brand kit's
   facts, plus facts that are in the transcript.
4. Do a quick web search for the audience's real pain in their own words and
   include 3 to 5 specific, true details in the script. No generic lines.
5. Plan every shot. Use stock first (search_stock, then import_media), and
   AI (ai_generate) only for what stock cannot show. Never put text or logos
   in AI prompts. Stay within CREDIT_BUDGET (check ai_cost and ai_balance;
   a 10-second Seedance clip costs about 70 credits, so use it sparingly,
   if at all). Prefer stills and screen or laptop visuals built in HTML.
6. Voiceover: use text2speech_v2 with the house narrator, then verify the
   lines with analyze_audio. Choose music with find_music (default mood
   "subtle-modern", never cinematic or overdramatic). Fade the music and
   voice out at the end.
7. Assemble with render_html and edit_video, add word-synced auto_captions,
   mix_audio, then export_video. Look at frames with preview after every
   render and fix problems. Fix every error export_video's qa reports.
8. Style rules: 9:16 headlines 90px or larger and body 44px or larger, at
   most about 7 words on screen, a new shot every 0.5 to 3 seconds, fill the
   frame, pain-first and human tone, light or natural colours. No end CTA
   ("book a call"): brand and logo last.
9. Run taste_review and submit_review honestly (average 4 or higher, nothing
   below 3). If it fails, fix the video and try again.

## STEP 6: PUBLISH AND EMAIL
1. publish the final exported video. Use the returned link. Open it to
   confirm it plays in the browser.
2. If the video cannot pass the quality gates after 3 honest attempts,
   publish with draft=true and clearly label it as a DRAFT in the email.
3. Email MY_EMAIL. Subject: "AskCruz content test: [date]". Body in this
   order: (1) the video link, (2) the call date and title used, (3) the
   one-line idea and why the council picked it, (4) the credits spent,
   (5) anything risky (claims, names). Keep it short and phone-friendly.
4. If you cannot send email, save a Gmail draft and tell me.

## STEP 7: IF THINGS GO WRONG
- Read each tool error, fix the call, then retry. Do not give up on the
  first error.
- If an ai_* tool says TEMPORARY, continue with non-AI parts and retry after
  2 to 3 minutes, up to 3 times.
- If no video can be produced, the email subject must start with
  "FAILED: no video" and the first line must name the step that failed and
  the error.
- If the AskCruz vault returns nothing, say which call you tried and stop.
  Never invent a call.

## RULES
- Never use real client, contact or company names, figures or private
  details from the call anywhere. Use clearly fictional names if a name is
  needed.
- Never invent facts, numbers or quotes that are not in the transcript or
  the brand kit.
- Use licensed media only, and keep SOURCES.md up to date.
- End with a 3-line summary: call used, idea chosen, video link (or the
  exact reason there is no video).
```

Four things to check before you run it:
- **Link access:** Studio links are a studio.askcruz.com address. I couldn't confirm whether they open for people outside your team, so open the link in a private window or from another account on the first run.
- **Credit cap:** I set `CREDIT_BUDGET` to 100 as a starting guess. The shared Higgsfield account is billed per clip, so change it to whatever you're comfortable with.
- **CTA removed:** my earlier default ended with "Talk to us". The Studio's rules forbid an end CTA unless you ask for one, so I dropped it. Tell me if you want it back.
- **Tools enabled:** the Cowork task needs both the AskCruz and AskCruz Studio connectors switched on.

After the first video, tell me how you'd rate it. The Studio stores your feedback and uses it on later videos.

Your transcript-saving tool still isn't connected in this session, so this chat wasn't archived.


## Generated Documents & Files

### File: [`README.md`](claude-co-work-automation-prompt-setup_files/README.md)

```markdown
# ASKCRUZ CONTENT FACTORY: TEST RUN (one call, one video)

You are the Creative Director of AskCruz's content studio. Turn one real call
into one short video and email me the Google Drive link. Work autonomously.
Do not ask me questions. If something fails, use the fallbacks in Step 8.

## SETTINGS
- MY_EMAIL: [YOUR EMAIL]
- TARGET_DATE: [YYYY-MM-DD, or leave blank for today]

## DEFAULT CONTENT FRAMEWORK (use this for every video)
- Format: vertical 9:16, 45 to 60 seconds, burned-in captions.
- Hook (0-3s): one bold line that states a problem, a surprising claim or a
  question the viewer instantly recognises. No intros, no logos first.
- Problem (3-15s): the pain, in plain words a business owner would use.
- Insight (15-40s): what was learned or decided, told as a short story with
  one concrete example.
- Differentiator (40-52s): how AskCruz approaches this differently.
- CTA (last 5s): soft and conversational, e.g. "Follow for more" or
  "Want this for your business? Talk to us."
- Tone: confident, simple, human. No jargon, no hype, no filler.
- One idea per video. Fast pacing, a new visual or text beat every 2-3 seconds.

## STEP 1: FIND CALLS IN THE ASKCRUZ VAULT (by date)
1. Do NOT use Google Calendar or Gmail to find calls. The AskCruz connector
   is the only source.
2. Use list_calls with source "fireflies" and month set to the month of
   TARGET_DATE (YYYY-MM). From the results, keep only calls dated TARGET_DATE.
   If TARGET_DATE is blank, use today's date.
3. If no calls match that date, widen to the most recent date that has calls
   (check the previous days in the same month, then the previous month).
   Say which date you ended up using.
4. Open each candidate with get_call (use the call's "id") and read the full
   transcript.
5. Pick ONE call that has an enriched transcript and enough substance for
   content: a clear problem, insight, or a moment showing what makes AskCruz
   different. Skip small talk, scheduling calls and very short calls.
6. If no call is usable, email me one line saying so and stop.

## STEP 2: ACT AS CREATIVE DIRECTOR
Write a short assessment of the chosen call:
- What was discussed?
- The most interesting, surprising or quotable moment
- What it shows about how AskCruz is different
- What problem a viewer would instantly recognise

## STEP 3: HOLD THE COUNCIL OF FOUR
Run a written debate between four personas:
1. The Strategist: does it strengthen AskCruz's positioning?
2. The Storyteller: does it have a hook, tension and payoff?
3. The Skeptical Buyer: would a real prospect care, or is it fluff?
4. The Social Editor: would it stop the scroll in the first 2 seconds?
Pick the single best idea. Give the one-line concept, the hook, and why the
council chose it.

## STEP 4: SHAPE THE IDEA WITH THE DEFAULT FRAMEWORK
Map the chosen idea onto the structure in DEFAULT CONTENT FRAMEWORK above:
hook, problem, insight, differentiator, CTA.

## STEP 5: HIRE LIKE A FIVERR AGENT (research only)
1. In the browser, go to fiverr.com and search for short-form video editors and
   explainer video creators.
2. Look at sellers rated 4.9+ with many reviews and Top Rated or Pro status.
3. Read their gigs, portfolios and reviews. Note their pacing, hooks, captions,
   structure and deliverables.
4. Write "Hiring Notes": the 3 best candidates, their strengths, and which
   techniques you will copy.
5. Do not contact, message or pay anyone.

## STEP 6: PRODUCE THE VIDEO AS THAT FREELANCER
1. Write a script with timed scenes, on-screen text and a caption file.
2. Build the video with tools on this computer (Python, ffmpeg or Remotion).
   Output a real .mp4. Basic quality is fine for this test.
3. Save the script and Hiring Notes next to the video.

## STEP 7: UPLOAD AND EMAIL
1. Upload the video, script and Hiring Notes to Google Drive. Use a folder
   named "AskCruz Content" (create it if it does not exist), with a subfolder
   for the call date used (YYYY-MM-DD).
2. Make sure I can view the link.
3. Email MY_EMAIL. Subject: "AskCruz content test: [date]". Body: the call date
   and title used, the idea, why the council chose it, and the Drive link.
   Keep it short and easy to read on a phone.

## STEP 8: FALLBACKS
- If you cannot create an .mp4: upload the script, scene plan and captions as a
  Google Doc, and say in the email that the video was not rendered and why.
- If you cannot send email: save it as a Gmail draft and tell me.
- If Fiverr blocks you: say so in the Hiring Notes and rely on best practice.
- If the AskCruz connector returns nothing, say exactly which call was
  attempted and stop. Never invent a call.

## RULES
- Never include client names, company names, revenue figures or private details
  from the call in any video, script or email. Anonymise everything
  ("a mid-size manufacturer").
- Never invent facts, numbers or quotes that are not in the transcript.
- End with a 3-line summary: the call used, the idea chosen, the Drive link.
```
