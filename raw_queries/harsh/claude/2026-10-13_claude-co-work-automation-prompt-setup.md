---
conversation_id: d4fdcac2-c41a-41b9-8297-a9f17aee2e82
platform: claude
username: "harsh"
title: "Claude co-work automation prompt setup"
created_at: "2026-10-13 14:23:58 EDT"
updated_at: "2026-10-13 14:26:19 EDT"
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
